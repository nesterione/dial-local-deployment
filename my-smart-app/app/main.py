import uvicorn
from aidial_sdk import DIALApp
from .config import get_settings
from .agent import MockAgent
from .tools import get_weather, get_coordinates
from .app import MySmartApp

app = DIALApp()

settings = get_settings()
agent = MockAgent(settings.llm, [get_weather, get_coordinates], settings.agent_prompt)


app.add_chat_completion("my-smart-app", MySmartApp(agent))

if __name__ == "__main__":
    uvicorn.run(app)
