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
        """
        Ferramar
        - Humanos
        - Draconatos
        - Aasimar (militares)
        Ressamar
        - Humanos
        - Tritões (minorias costeiras)
        - Tabaxi
        
        
        
        """        
        pass


class Combative_NPC(NPC):
    def __init__(self):

        self.classe

    def roll_class(self):
        pass            

    def background():
        NotImplemented

class Non_Combative_NPC(NPC):
    def __init__(self):
        pass