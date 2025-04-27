from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain import hub
import datetime
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

load_dotenv()

# Define a tool
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = GoogleSerperAPIWrapper()
search_tool = Tool(
    name="search_tool",
    func=search_tool.run,
    description="Useful for searching Google to find recent news or information, such as SpaceX launch dates."
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [search_tool, get_system_time]
prompt = hub.pull("hwchase17/react")

# Create ReAct agent
agent = create_react_agent(llm=model, tools=tools, prompt=prompt)
print(f"Agent: {agent}")
# Create AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
print(f"AgentExecutor: {agent_executor}")

# Run the agent
result = agent_executor.invoke({"input": "When was SpaceX's last launch and how many days ago was that from this instant"})
print(result["output"])
# Output: ["http://news1.com", "http://news2.com"]