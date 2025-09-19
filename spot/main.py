import os
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openpyxl
from docx import Document
import PyPDF2

# Directory to read files from
DATA_DIR = "./data"  # You can change this to the directory you want

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Tool for reading PDF files
@tool
def read_pdf(file_path: str) -> str:
    """Read the content of a PDF file."""
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])
        return content
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Tool for reading Word documents
@tool
def read_word(file_path: str) -> str:
    """Read the content of a Word document."""
    try:
        loader = UnstructuredWordDocumentLoader(file_path)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])
        return content
    except Exception as e:
        return f"Error reading Word document: {str(e)}"

# Tool for reading Excel files
@tool
def read_excel(file_path: str) -> str:
    """Read the content of an Excel file."""
    try:
        loader = UnstructuredExcelLoader(file_path)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])
        return content
    except Exception as e:
        return f"Error reading Excel: {str(e)}"

# Tool for reading text files
@tool
def read_text_file(file_path: str) -> str:
    """Read the content of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading text file: {str(e)}"

# Tool to list files in the directory
@tool
def list_files(directory: str = DATA_DIR) -> str:
    """List files in the specified directory."""
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"

# Initialize Ollama LLM
llm = Ollama(model="llama2")  # Change to your preferred model

# List of tools
tools = [read_pdf, read_word, read_excel, read_text_file, list_files]

# Initialize the agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    print("Welcome to Spot! I can read local files to answer your questions.")
    print(f"I'm set to read files from: {DATA_DIR}")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = agent.run(user_input)
        print(f"Spot: {response}")