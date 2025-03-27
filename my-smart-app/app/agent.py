from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_openai.chat_models.base import BaseChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph  # type: ignore
from langgraph.prebuilt import ToolNode  # type: ignore


class MockAgent:

    def __init__(self, llm: BaseChatOpenAI, tools: list, agent_prompt: str):
        self.tools = tools
        self.agent_prompt = agent_prompt

        tool_node = ToolNode(tools)
        self.llm = llm.bind_tools(tools) 

        graph = StateGraph(MessagesState)
        graph.add_node("agent", self.call_model)
        graph.add_node("tools", tool_node)
        graph.add_edge(START, "agent")

        graph.add_conditional_edges(
            "agent",
            self.should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )
        graph.add_edge("tools", "agent")
        self.graph = graph.compile()

    def should_continue(self, state: MessagesState) -> Literal["tools", END]: 
        messages = state["messages"]
        last_message = messages[-1]
        if not last_message.tool_calls:
            return "end"
        else:
            return "continue"

    def call_model(self, state: MessagesState):
        messages = state["messages"]
        system = SystemMessage(content=self.agent_prompt)
        response = self.llm.invoke([system] + messages)
        return {"messages": messages + [response]}
        #return {"messages": [response]}
