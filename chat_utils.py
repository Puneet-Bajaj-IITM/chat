from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_community.embeddings import OllamaEmbeddings
import os

def load_folder(folder):
    """Load documents from the specified folder.

    Args:
        folder (str): Path to the folder containing documents.

    Returns:
        list: List of loaded documents.
    """
    pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    docx_files = [f for f in os.listdir(folder) if f.endswith('.docx')]
    loaders = [
        PyPDFLoader(os.path.join(folder, f)) for f in pdf_files] + [
        TextLoader(os.path.join(folder, f)) for f in txt_files] + [
        UnstructuredWordDocumentLoader(os.path.join(folder, f)) for f in docx_files
    ]

    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs

def load_db(docs, persist_directory='docs/chroma/'):
    """Load documents into a vector store.

    Args:
        docs (list): List of documents to load.
        persist_directory (str, optional): Directory to persist the vector store. Defaults to 'docs/chroma/'.

    Returns:
        Chroma: Loaded vector store.
    """
    global chunk_size, chunk_overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(docs)
    vectordb = Chroma.from_documents(
        documents=chunks,
        collection_name="ollama_embeds",
        embedding=OllamaEmbeddings(model='nomic-embed-text'),
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def custom_prompt(vectordb, query, k):
    """Generate a custom prompt based on the query.

    Args:
        vectordb (Chroma): Vector store containing documents.
        query (str): Query text.
        k (int): Number of documents to retrieve.

    Returns:
        str: Custom prompt for the query.
    """
    results = vectordb.similarity_search(query, k=k)
    source_knowledge = "\n".join([x.page_content for x in results])
    augment_prompt = f"""Using the contexts below, answer the query:
    Contexts:
    {source_knowledge}

    Query: {query}"""
    
    return augment_prompt, get_retrieved_data(results)

def get_retrieved_data(results):
  l = []
  for result in results:
    a = result.metadata
    a['page_content'] = result.page_content
    l.append(a)
  return l