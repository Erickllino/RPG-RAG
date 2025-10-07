
from langchain_ollama import OllamaLLM
import time

llm = OllamaLLM(model="deepseek-r1:latest")  # ou "llama3"
start_time = time.time()
word = ""


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



while word != "quit":
    word = input("Digite uma palavra (ou 'quit' para sair): ")
    if word != "quit":
        resp = llm.invoke(word)
        end_time = time.time()
        elapsed = end_time - start_time
        print(resp)
        print(f"Tempo de resposta: {elapsed:.2f} segundos")
    else:
        print("Quitting")
