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
# Tool to search files
@tool
def search_files(query: str, directory: str = DATA_DIR) -> str:
    """Search for a query in all readable files in the directory."""
    results = []
    try:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if file.lower().endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            results.append(f"Found in {file}: {content[:200]}...")
                except Exception as e:
                    results.append(f"Error in {file}: {e}")
            elif file.lower().endswith('.pdf'):
                try:
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text()
                        if query.lower() in text.lower():
                            results.append(f"Found in {file}: {text[:200]}...")
                except Exception as e:
                    results.append(f"Error in {file}: {e}")
            elif file.lower().endswith('.docx'):
                try:
                    doc = Document(file_path)
                    text = "\n".join([para.text for para in doc.paragraphs])
                    if query.lower() in text.lower():
                        results.append(f"Found in {file}: {text[:200]}...")
                except Exception as e:
                    results.append(f"Error in {file}: {e}")
            elif file.lower().endswith(('.xlsx', '.xls')):
                try:
                    wb = openpyxl.load_workbook(file_path)
                    text = ""
                    for sheet in wb.worksheets:
                        for row in sheet.iter_rows(values_only=True):
                            text += " ".join([str(cell) if cell else "" for cell in row]) + "\n"
                    if query.lower() in text.lower():
                        results.append(f"Found in {file}: {text[:200]}...")
                except Exception as e:
                    results.append(f"Error in {file}: {e}")
        if results:
            return "\n\n".join(results)
        else:
            return "No matches found."
    except Exception as e:
        return f"Error searching: {str(e)}"

# Tool to get file info
@tool
def get_file_info(file_path: str) -> str:
    """Get metadata about a file."""
    try:
        stat = os.stat(file_path)
        return f"Size: {stat.st_size} bytes, Modified: {stat.st_mtime}"
    except Exception as e:
        return f"Error: {str(e)}"

# Tool to summarize file content
@tool
def summarize_file(file_path: str) -> str:
    """Summarize the content of a file."""
    try:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            content = "\n".join([doc.page_content for doc in documents])
        elif file_path.endswith('.docx'):
            loader = UnstructuredWordDocumentLoader(file_path)
            documents = loader.load()
            content = "\n".join([doc.page_content for doc in documents])
        elif file_path.endswith(('.xlsx', '.xls')):
            loader = UnstructuredExcelLoader(file_path)
            documents = loader.load()
            content = "\n".join([doc.page_content for doc in documents])
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        prompt = PromptTemplate.from_template("Summarize the following text in a few sentences: {text}")
        chain = LLMChain(llm=llm, prompt=prompt)
        summary = chain.run(text=content)
        return summary
    except Exception as e:
        return f"Error summarizing: {str(e)}"

# Tool to list files by type
@tool
def list_files_by_type(extension: str, directory: str = DATA_DIR) -> str:
    """List files of a specific type in the directory."""
    try:
        files = [f for f in os.listdir(directory) if f.lower().endswith(extension.lower())]
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize Ollama LLM
llm = Ollama(model="llama2")  # Change to your preferred model

# List of tools
tools = [read_pdf, read_word, read_excel, read_text_file, list_files, search_files, get_file_info, summarize_file, list_files_by_type]

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