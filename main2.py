import sys
from crewai import Task, Crew, Process
import os
from dotenv import load_dotenv
from Final.agents import CustomAgents

load_dotenv()
agents = CustomAgents()

# query = input("What is your query:")

document_task = Task(
    description='Saves the data in a word document',
    expected_output=f'Write a description about the given topic by the user and save it in a Word document.',
    agent=agents.doc_saver()
)

tech_crew = Crew(
    agents=[agents.doc_saver()],
    tasks=[document_task],
    process=Process.sequential,
    verbose=True
)

result = tech_crew.kickoff(inputs = {"write a document on mercedes"})
print(result)
