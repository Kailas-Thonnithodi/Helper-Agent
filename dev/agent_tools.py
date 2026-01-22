from playwright.async_api import async_playwright

# from langchain
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_classic.agents import Tool
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

# Other
import os
import requests
from dotenv import load_dotenv

# Program Start
load_dotenv(override=True)
serper = GoogleSerperAPIWrapper()

async def playwright_tools():
    '''
    Playwright instance toolkit
    * Runs an instance of the playwright with the tool kit on standby. 
    '''
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright

def get_file_tools():
    '''
    Allows the tools to interact directly with local files. 
    '''
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()

async def other_tools():
    
    file_tools = get_file_tools()
    
    tool_search = Tool(
        name = "search",
        func = serper.run,
        description = "Use this tool when you want to get the results of an online web search."
    )
    
    # allows the llm to run python code
    python_repl = PythonREPLTool

    # wikipedia = WikipediaAPIWrapper()
    # wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    return file_tools + [tool_search, python_repl]
