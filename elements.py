from enum import Enum
#from interactions import Interactions

class Elements(Enum):
    Water = 0
    Wood = 1
    Fire = 2
    Earth = 3
    Metal = 4

    # def compare(self, other: self):
    #     #water
    #     if self.value == Elements.Water:
    #         if other.value == Elements.Wood:  return Interactions.SelfIsGenerative
    #         elif other.value == Elements.Fire: return Interactions.SelfIsDestructive
    #         elif other.value == Elements.Metal: return Interactions.OtherIsGenerative
    #         elif other.value == Elements.Earth: return Interactions.OtherIsDestructive
    #         else: return Interactions.Neutral
    #     #wood
    #     if self.value == Elements.Wood:
    #         if other.value == Elements.Fire:  return Interactions.SelfIsGenerative
    #         elif other.value == Elements.Earth: return Interactions.SelfIsDestructive
    #         elif other.value == Elements.Water: return Interactions.OtherIsGenerative
    #         elif other.value == Elements.Metal: return Interactions.OtherIsDestructive
    #         else: return Interactions.Neutral
    #     #fire
    #     if self.value == Elements.Fire:
    #         if other.value == Elements.Earth:  return Interactions.SelfIsGenerative
    #         elif other.value == Elements.Metal: return Interactions.SelfIsDestructive
    #         elif other.value == Elements.Wood: return Interactions.OtherIsGenerative
    #         elif other.value == Elements.Water: return Interactions.OtherIsDestructive
    #         else: return Interactions.Neutral
    #     #earth
    #     if self.value == Elements.Earth:
    #         if other.value == Elements.Metal:  return Interactions.SelfIsGenerative
    #         elif other.value == Elements.Water: return Interactions.SelfIsDestructive
    #         elif other.value == Elements.Fire: return Interactions.OtherIsGenerative
    #         elif other.value == Elements.Wood: return Interactions.OtherIsDestructive
    #         else: return Interactions.Neutral
    #     #metal
    #     if self.value == Elements.Metal:
    #         if other.value == Elements.Water:  return Interactions.SelfIsGenerative
    #         elif other.value == Elements.Wood: return Interactions.SelfIsDestructive
    #         elif other.value == Elements.Earth: return Interactions.OtherIsGenerative
    #         elif other.value == Elements.Fire: return Interactions.OtherIsDestructive
    #         else: return Interactions.Neutral