"""
WorkFlow:

Pre. O usuário insere a campanha ativa, 
(a campanha tem todos os jogadores, posição final deles e oque aconteceu)

1. O usuario insere um input para o Cerebro
2. O input é enviado para o Cerebro (Ollama)
3. O Cerebro entende o input

4. Pega os dados em embedding 
    4.1 Do mundo (Ekalia)
    4.2 Pega os dados da campanha ativa atual
    4.3 Pega os dados das regras

5. O Cerebro cria um output com base no input e nos dados em embedding
6. O output é enviado para o usuário

-Ideias:
Gerador de NPCs
Gerador de missões
Salvar progresso da campanha, junto de logs do jogo, completando com um resumo do que aconteceu


"""

from utils.api_key import API_KEY

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings



class RAG():
    def __init__(self):
        pass

    def transcribe_audio_to_text(audio_path: str) -> str:
        """
        Transcreve um arquivo de áudio para texto usando Whisper.

        Args:
            audio_path: O caminho para o arquivo de áudio.

        Returns:
            A transcrição do áudio como uma string.
        """
        import whisper

        model = whisper.load_model("large")
        result = model.transcribe(audio_path)
        return result["text"]

    def summarize_session_text(session_text: str) -> str:
        """
        Resume o texto da sessão usando um modelo LLM.

        Args:
            session_text: O texto completo da sessão.

        Returns:
            Um resumo do texto da sessão.
        """


        from openai import OpenAI
        client = OpenAI(api_key = )

        response = client.responses.create(
            model="gpt-5.2",
            input="Write a one-sentence bedtime story about a unicorn."
        )

        print(response.output_text)
        return response.output_text



def run_openai():

    # Model
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=1.0,  # Aumenta a criatividade e reduz filtros
        top_p=0.95,  # Aumenta a diversidade de respostas
        max_tokens=2048,
        api_key=API_KEY,
    )

    return llm



def run_local():
    #   WIP: VLLM Local
    ###############################################

    from langchain_openai import ChatOpenAI
    from langchain_openai import OpenAIEmbeddings

    llm = ChatOpenAI(
        model="model/qwen25-7b-awq",
        base_url="http://localhost:8000/v1", #Aqui usa VLLM local
        api_key="none"
    )

    #################################################

    return llm

def choose_method(method):
    if method == 1:
        run_openai()
    elif method == 2:
        run_local()

    return None






def load_db():
# Vector Store Load
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=API_KEY
    )
    from langchain_community.vectorstores import FAISS
    vectorstore = FAISS.load_local(
        "Data/db/ekalia_vector_db",
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )






from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Você é o Cronista Oficial do mundo de Ekalia.
        Use APENAS informações retornadas pelas ferramentas.
        Se algo não existir no lore, diga que não está registrado.
        """
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])




from langchain_core.messages import SystemMessage
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

chat_history = [
    SystemMessage(
        content="Você é um assistente para jogos de RPG de mesa, expert em Dungeons and Dragons 5ª Edição. "
    )
]



###############

def main():
    method = int(input("Escolha o método de execução (1 para OpenAI, 2 para Local): "))
    llm = choose_method(method)
    load_db()

    chat_history = []

    agent = create_tool_calling_agent(
    llm=llm,
    tools=[],
    prompt=prompt
)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[],
        verbose=True
    )


    while True:
        message = input("\nDigite uma mensagem:\n")

        if message.lower() in ["sair", "exit", "quit"]:
            break

        message = [*chat_history, HumanMessage(content=message)]

        result = agent_executor.invoke({"messages": message})
        print(result)


"""start_time = time.time()
word = ""



while word != "quit":
    word = input("Digite uma palavra (ou 'quit' para sair): ")
    if word != "quit":
        resp = llm.invoke(word)
        end_time = time.time()
        elapsed = end_time - start_time
        print(resp)
        print(f"Tempo de resposta: {elapsed:.2f} segundos")
    else:
        print("Quitting")"""