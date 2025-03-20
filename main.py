import sys
from crewai import Agent, Task
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from langchain_openai import AzureChatOpenAI
from Final.agents import CustomAgents

load_dotenv()
agents =  CustomAgents()
# default_llm = AzureChatOpenAI(
#     openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
#     azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
#     azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
#     api_key=os.environ.get("AZURE_OPENAI_KEY")
# )


# # Create a researcher agent
# researcher = Agent(
#   role='Senior Researcher',
#   goal='Discover groundbreaking technologies',
#   verbose=True,
#   llm=default_llm,
#   backstory='A curious mind fascinated by cutting-edge innovation and the potential to change the world, you know everything about tech.'
# )

query = input("What is your query:")

# Task for the researcher
document_task = Task(
  description='Saves the data in a word document',
  expected_output=f'Write in description about the given topic by the user and save it in word document. User query :{query} ',
  agent=agents.doc_saver() 
)

# powerpoint_task = Task(
#   description='Saves the data in a powerpoint file',
#   expected_output=f'Generates a json response for the ppt generation tool and saves the ppt.User query :{query}',
#   agent=agents.ppt_saver()
# )

# Instantiate your crew
# tech_crew = Crew(
#   agents=[researcher],
#   tasks=[research_task],
#   process=Process.sequential  # Tasks will be executed one after the other
# )

# tech_crew = Crew (
#     agents=[agents.doc_saver(), agents.ppt_saver()],
#     tasks=[document_task, powerpoint_task],
#     process=Process.sequential,  # Tasks will be executed one after the other
#     verbose = True
# )

tech_crew = Crew (
    agents=[agents.doc_saver()],
    tasks=[document_task],
    process=Process.sequential,  # Tasks will be executed one after the other
    verbose = True
)

# Begin the task execution
result = tech_crew.kickoff()
print(result)
