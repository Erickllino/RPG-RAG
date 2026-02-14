import random




mensagem = input()
palavras = mensagem.split(' ')

p_erro = 0.5

for palavra in palavras:
    p = random.random()
    if p < p_erro:

        print(f"a palavra: '{palavra}' enviou com erro ---- p:{p}")