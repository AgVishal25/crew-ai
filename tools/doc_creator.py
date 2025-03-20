from langchain.tools import tool
import os
from docx import Document




class DocCreator:
    def __init__(self):
        pass
    
    @tool("Create a document")
    def create_doc(self,input_data):
        """
        Creates a word document with the given text and saves in the local working directory

        Parameter:
        input_data(str) : This is the input data for the document
        """
        file = "word_file.docx"
        document = Document()
        document.add_paragraph(input_data)
        document.save(file)
        return True


from langchain.tools import BaseTool

class DocTool(BaseTool):
    name: str = "Create a document"
    description: str = "Creates a Word document with the given text and saves it in the local directory."

    def _run(self, tool_input: str) -> bool:
        # Instantiate DocCreator and run the create_doc method
        doc_creator = DocCreator()
        return doc_creator.create_doc(tool_input)

    async def _arun(self, tool_input: str) -> bool:
        # Async version is not implemented
        raise NotImplementedError("Async mode not implemented for DocTool.")