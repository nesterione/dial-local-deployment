from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from aidial_sdk.chat_completion import Message, Role
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


def dial_to_langchain(messages: list[Message]):
    langchain_messages = []
    for msg in messages:
        match msg.role:
            case Role.SYSTEM:
                langchain_messages.append(SystemMessage(content=msg.content))
            case Role.ASSISTANT:
                langchain_messages.append(AIMessage(content=msg.content))
            case Role.USER:
                langchain_messages.append(HumanMessage(content=msg.content))
            case Role.TOOL:
                langchain_messages.append(ToolMessage(content=msg.content))
    return langchain_messages


class EventProcessor:
    def __init__(self, choice):
        self.choice = choice
        self.stages = {}
        self.handlers = {
            "on_tool_start": self.handle_tool_start,
            "on_tool_end": self.handle_tool_end,
            "on_chat_model_stream": self.handle_chat_model_stream
        }

    async def process_event(self, event):
        event_type = event.get("event")
        handler = self.handlers.get(event_type)
        if handler:
            await handler(event)

    async def handle_tool_start(self, event):
        tool_name = event.get("name")
        run_id = event.get("run_id")
        self.stages[run_id] = self.choice.create_stage(f"Tool Call: {tool_name}")
        self.stages[run_id].__enter__()
        params = event.get("data")
        self.stages[run_id].append_content(f"Calling tool: {tool_name}: {params}\n\n")
        

    async def handle_tool_end(self, event):
        run_id = event.get("run_id")
        output = event["data"].get("output")
        if output and run_id in self.stages:
            content = output.content
            self.stages[run_id].append_content(f"{content}")

            self.stages[run_id].__exit__(None, None, None)
            del self.stages[run_id]

    async def handle_chat_model_stream(self, event):
        chunk = event["data"].get("chunk")
        if not chunk:
            return
        content = chunk.content
        if content:
            self.choice.append_content(content)
    
    async def close(self):
        for stage in self.stages.values():
            stage.__exit__(None, None, None)


class MySmartApp(ChatCompletion):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent.graph

    async def chat_completion(self, request: Request, response: Response) -> None:
        with response.create_single_choice() as choice:
            messages = dial_to_langchain(request.messages)
            event_processor = EventProcessor(choice)
            async for event in self.agent.astream_events(
                {"messages": messages}, version="v1"
            ):
                await event_processor.process_event(event)
            await event_processor.close()
