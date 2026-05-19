from pathlib import Path

from .configs import DATA_DIR, INDEX_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP




## get all docs

def get_data():
    data = {
        "File Name": [],
        "Context": [],
        "Content": [],
    }

    for file_path in DATA_DIR.rglob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        data["File Name"].append(file_path.name)
        data["Content"].append(content)

        # Context = relative path inside Ekalia
        context = file_path.parent.relative_to(DATA_DIR)
        data["Context"].append(str(context))

        print(f"Read file: {context}/{file_path.name} ({len(content)})")

    return data


def build_embeddings():
    """Instancia o modelo de embeddings HuggingFace."""
    raise NotImplementedError


import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader

# 1. Configure sua API Key do Groq (pegue em console.groq.com)
#os.environ["GROQ_API_KEY"] = "sua_chave_groq_aqui"

# 2. Embeddings Gratuitos (Roda no seu PC, sem custo de API)
# O modelo 'all-MiniLM-L6-v2' é leve, rápido e muito eficiente.
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. Carregar e Processar Documentos
loader = TextLoader("dados.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 4. Criar o FAISS com os embeddings do HuggingFace
vectorstore = FAISS.from_documents(docs, embeddings)

# 5. Configurar o LLM do Groq
# Modelos populares: "llama-3.3-70b-versatile" ou "mixtral-8x7b-32768"
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# 6. Criar a Chain RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Execução
pergunta = "Resuma os pontos principais do documento."
resposta = qa_chain.invoke(pergunta)
print(f"Resposta do Groq:\n{resposta['result']}")