# AMI (Arcane Message interference)

import random
import math
e = math.e
k = 0.05


def calculate_p(m):
    d = float(input("Input the distance in km: "))
    d0 = 100

    I = float(input("Input the magic interference index: "))
    I = min(1, max(I,0))

    C = len(m.split(" "))/len(m)
    C = min(1, max(C, 0))
    d_critico = d0*((1-I)*(1-C))
    p_erro = 1/(1 + e**(-k*(d - d_critico)))
    print(f"O erro é: {p_erro}")
    return p_erro

import string

def word_error(word):
    if len(word) == 0:
        return word

    tipo = random.choice(["swap", "remove", "insert", "reverse"])

    # 🔤 Trocar uma letra
    if tipo == "swap":
        i = random.randint(0, len(word)-1)
        nova_letra = random.choice(string.ascii_lowercase)
        return word[:i] + nova_letra + word[i+1:]

    # ➖ Remover uma letra
    elif tipo == "remove" and len(word) > 1:
        i = random.randint(0, len(word)-1)
        return word[:i] + word[i+1:]

    # ➕ Inserir uma letra
    elif tipo == "insert":
        i = random.randint(0, len(word))
        nova_letra = random.choice(string.ascii_lowercase)
        return word[:i] + nova_letra + word[i:]

    # 🔁 Inverter palavra (erro arcano forte)
    elif tipo == "reverse":
        return word[::-1]

    return word


def process_message():

    msg = input("Input the mensage: ")
    p_erro = calculate_p(msg)
    palavras = msg.split(' ')

    l = len(palavras)
    for i in range(l):
        p = random.random()
        if p < p_erro:
            palavras[i] = word_error(palavras[i])
            print(f"a palavra: '{palavras[i]}' enviou com erro ---- p:{p}")

    msg_final = " ".join(palavras)
    print(msg_final)
    return msg_final


process_message()