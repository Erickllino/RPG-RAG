


### Pega o contexto do NPC


import random


# Aqui pegaremos o contexto da campanha e local do NPC
import random

races = {
    "human": {"str": 1, "dex": 1, "con": 1, "int": 1, "wis": 1, "cha": 1},
    
    "elf": {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 0},
    "high_elf": {"str": 0, "dex": 2, "con": 0, "int": 1, "wis": 0, "cha": 0},
    "wood_elf": {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 1, "cha": 0},
    "dark_elf": {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 1},

    "dwarf": {"str": 0, "dex": 0, "con": 2, "int": 0, "wis": 0, "cha": 0},
    "hill_dwarf": {"str": 0, "dex": 0, "con": 2, "int": 0, "wis": 1, "cha": 0},
    "mountain_dwarf": {"str": 2, "dex": 0, "con": 2, "int": 0, "wis": 0, "cha": 0},

    "halfling": {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 0},
    "lightfoot_halfling": {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 1},
    "stout_halfling": {"str": 0, "dex": 2, "con": 1, "int": 0, "wis": 0, "cha": 0},

    "dragonborn": {"str": 2, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 1},
    "gnome": {"str": 0, "dex": 0, "con": 0, "int": 2, "wis": 0, "cha": 0},
    "forest_gnome": {"str": 0, "dex": 1, "con": 0, "int": 2, "wis": 0, "cha": 0},
    "rock_gnome": {"str": 0, "dex": 0, "con": 1, "int": 2, "wis": 0, "cha": 0},

    "half_elf": {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 2},
    "half_orc": {"str": 2, "dex": 0, "con": 1, "int": 0, "wis": 0, "cha": 0},

    "tiefling": {"str": 0, "dex": 0, "con": 0, "int": 1, "wis": 0, "cha": 2}
}

class Race:
    def __init__(self, name, base_bonus, subraces=None):
        self.name = name
        self.base_bonus = base_bonus
        self.subraces = subraces or {}

    def get_bonus(self, subrace=None):
        bonus = self.base_bonus.copy()
        if subrace and subrace in self.subraces:
            for stat, value in self.subraces[subrace].items():
                bonus[stat] = bonus.get(stat, 0) + value
        return bonus

class NPC():
    def __init__(self):
        self.str
        self.dex
        self.con
        self.int
        self.wis
        self.char

        self.race
        self.stats = self.roll_stats
    
    def roll_stats(self):
        stats = []
        for _ in range(6):
            rolls = []
            for _ in range(4):
                rolls.append(random.randint(1, 6))
            stat = max(sum(rolls) - min(rolls), 8)
            print(stat)
            stats.append(stat)


        stats.sort(reverse=True)
        
        return stats

    def roll_race(self, context):
        
        # TODO: adicioanr porcentagem pra cada local
        if "Ferramar" in context:
            return random.choice(["human", "draconato", "aasimar"])
        elif "Ressamar" in context:
            return random.choice(["human", "tritão", "tabaxi"])
        elif "Andarilhos" in context:
            return random.choice(["human", "tabaxi", "tiefling"])
        elif "Gluckslott" in context:
            return random.choice(["anão", "gnomo", "draconato"])
        elif "Fortunasue" in context:
            return random.choice(["human", "tiefling", "halfling"])
        elif "Maraven" in context:
            return random.choice(["human", "halfling", "tiefling"])
        elif "MataReal" in context:
            return random.choice(["human", "orc", "meio-orc", "tabaxi"])
        elif "SilvanVale" in context:
            return random.choice(["human", "aasimar", "gnomo"])
        elif "Steinberg" in context:
            return random.choice(["anão", "gnomo", "draconato"])
        else:            
            return random.choice(list(races.keys()))
        
        """
        Ferramar
        - Humanos
        - Draconatos
        - Aasimar (militares)
        Ressamar
        - Humanos
        - Tritões (minorias costeiras)
        - Tabaxi
        Andarilhos
        - Humanos
        - Tabaxi
        - Tieflings
        Gluckslott
        - Anões
        - Gnomos
        - Draconatos
        Fortunasue
        - Humanos
        - Tieflings
        - Halflings
        Maraven
        - Humanos (majoritários)
        - Halflings (fortes no comércio)
        - Tieflings (minoria urbana)
        MataReal
        - Humanos
        - Orcs e Meio-orcs
        - Tabaxi (rotas nômades)
        SilvanVale
        - Humanos
        - Aasimar (raros, ligados a ordens naturais)
        - Gnomos (engenharia leve e hidráulica)]
        Steinberg
        - Anões (majoritários)
        - Gnomos
        - Alguns Draconatos (minorias técnicas/militares)
        
        
        
        """        
        pass


class Combative_NPC(NPC):
    def __init__(self):

        self.classe

    def roll_class(self):
        pass            

    def background():
        NotImplemented

    def define_stats(self):
        
        # TODO: aqui usa a classe para determinar quais stats são mais importantes e distribuir os stats rolados de acordo com a classe

        pass

class Non_Combative_NPC(NPC):
    def __init__(self):
        pass




def get_npc_context(npc_name):
    # aqui tem que pegar o contexto do npc, usando o nome do npc
    # e retornar o contexto do npc
    return "Contexto do NPC: " + npc_name


def generate_npc(npc_name):
    context = get_npc_context(npc_name)
    npc = Combative_NPC()
    stats = npc.roll_stats(1)  # Nível 1 por padrão
    # aqui tem que usar o contexto do npc para gerar o npc
    npc_description = "Descrição do NPC: " + npc_name + " - " + context
    return npc_description


def main():
    npc_name = "Gandalf"
    npc = generate_npc(npc_name)
    print(npc)
    
if __name__ == "__main__":
    main()