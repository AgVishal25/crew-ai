import os
from crewai import Agent
from textwrap import dedent
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from Final.tools.doc_creator import DocCreator
from Final.tools.ppt_creator import PptCreator
load_dotenv()

default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

# json_llm = AzureChatOpenAI(
#     openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
#     azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
#     azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
#     api_key=os.environ.get("AZURE_OPENAI_KEY"),
#     response_format={"type": "json_object"}
# )


"""
Agent cheat sheet 
- Think like a boss. Work backwards from the goal and think which employee you need to hire to get the job done.
- Define the Captain of the Crew who orients the other agents towards the goal.
- Define which experts the captain needs to communicate with and delegate tasks to.
    Build a top down structure of the crew.


Goal:
- Understand User queries
- Act according to the user queries
- make sure the user queries have been resolved

Manager/Boss:
- Experty in managing and assigning the tasks to the agents 

Team Members (Agents)
- DB info Retriver
- PPT Generator
- Word Generator
- Web Searcher


Notes 
- Agents should be results driven and have a clear goal in mind
- Agents should be able to communicate with each other and delegate tasks
- Agents should be able to work together to achieve a common goal
- Goals should be actionable
- Backstory should be the resume
- Role is their job title

"""

from Final.tools.doc_creator import DocTool


class CustomAgents:
    def __init__(self):
        self.OpenAIGPT4 = default_llm
        # self.user_input = user_input
        # self.json_llm = json_llm
    def manager(self):
        return Agent(
            role="You are the Mananger in a team ",
            backstory=dedent(f"""You have an experience of 30 years in the field of management. You analyse the team members' potential and according to that you assign task. """),
            goal=dedent(f"""- Understand user queries.
                            - Break the problem into smaller problems and delegate the problems to the other team members  according to their role.
                            """),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )
    
    def doc_saver(self):
        from Final.tools.doc_creator import DocTool  # ensure correct import
        # Create an instance of DocTool
        doc_tool_instance = DocTool()
        # Wrap it in a dictionary with the required keys using instance attributes
        doc_tool = {
            "name": doc_tool_instance.name, 
            "func": doc_tool_instance._run,  # callable that implements the tool functionality
            "description": doc_tool_instance.description
        }
        return Agent(
            role="Document Generator and Saver",
            backstory="Saves documents as per user query",
            goal="Create a document and save it in the local working directory based on the user input.",
            tools=[doc_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def ppt_saver(self):
        return Agent(
            role="Powerpoint PPT generator and saver",
            backstory=dedent(f"""An expert in generating a ppt data in json format. You are a helpful assistant. When asked to make a ppt generate a json output for the tool in a format :
                    {{'slides': 
                        {{'slide_1':
                            {{'title':'<title of the slide>',
                            'content':'<content of the slide>'}}
                    //further slide data
                        }}
                    }}
                    Do NOT provide any other data, apart from JSON.
                    Make sure the data generated is correct format
                            """),
            goal=dedent(f"""Create a ppt and saves in the local working directory. if the user query says so."""),
            tools=[PptCreator.create_ppt],
            allow_delegation=False,
            verbose=True,
            llm=self.json_llm
        )

 