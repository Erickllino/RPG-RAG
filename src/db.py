from utils.get_data import get_data
from utils.api_key import API_KEY


from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS


import faiss


data = get_data(verbose=False)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    separators=["\n\n", "\n", ".", " "]
)


docs_split = text_splitter.split_documents(data)


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=API_KEY
)


vectorstore = FAISS.from_documents(
    documents=docs_split,
    embedding=embeddings
)


vectorstore.save_local("Data/db/ekalia_vector_db")