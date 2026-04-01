


### Pega o contexto do NPC


import random


def get_npc_context(npc_name):
    # aqui tem que pegar o contexto do npc, usando o nome do npc
    # e retornar o contexto do npc
    return "Contexto do NPC: " + npc_name

def roll_stat():
    dices = [+random.randint(1, 6) for _ in range(4)]
    dices.remove(min(dices))
    return sum(dices)


def roll_stats(job, level):
    # aqui tem que rolar os stats do npc com base no level]
    rolls = []
    for stat in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
        rolls.append((stat, roll_stat()))


    # After rolling get level and job to make stats more accurate, for now just return the rolls

    print("Rolagem de stats:")
    print(rolls)

    return {"strength": 10, "dexterity": 10, "constitution": 10, "intelligence": 10, "wisdom": 10, "charisma": 10}

def generate_npc(npc_name):
    context = get_npc_context(npc_name)
    stats = roll_stats(1)  # Nível 1 por padrão
    # aqui tem que usar o contexto do npc para gerar o npc
    npc_description = "Descrição do NPC: " + npc_name + " - " + context
    return npc_description


def main():
    npc_name = "Gandalf"
    npc = generate_npc(npc_name)
    print(npc)
    
if __name__ == "__main__":
    main()