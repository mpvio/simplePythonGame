from elements import Elements
from interactions import Interactions
from character import Character
from actions import Actions
from states import States

from random import choice, randrange

class GameMaster:
    team1: list[Character]
    team2: list[Character]
    allCharacters: list[Character]

    def __init__(self):
        self.team1, self.team2 = [], []
        self.createTeams()
        self.allCharacters = []
        self.allCharacters.extend(self.team1)
        self.allCharacters.extend(self.team2)
        #good interactions for offense and support
        self.keyInteractions = [Interactions.Neutral, Interactions.OtherIsGenerative, Interactions.OtherIsDestructive]
        #good to support an ally with this interaction
        #self.supportiveInteractions = [Interactions.SelfIsGenerative, Interactions.Neutral, Interactions.OtherIsGenerative, Interactions.OtherIsDestructive]
        #good to attack a foe with this interaction
        #self.offensiveInteractions = [Interactions.SelfIsDestructive, Interactions.Neutral, Interactions.OtherIsGenerative, Interactions.OtherIsDestructive]
    
    #run game
    def gameLoop(self):
        while self.gameOver() == False:
            self.setPlayerActions()
            self.setAIActions()
            self.executeTeamActions()
            self.displayTeams()
            self.resetTeams()

    #create/ display/ reset teams
    def createTeams(self):
        for team in range(1,3):
            for player in range (1,4):
                n = choice(list(Elements))
                x = Character(team, player, n)
                if team == 1: self.team1.append(x)
                else: self.team2.append(x)

    def displayTeams(self):
        for ch in self.allCharacters:
            print(ch.getAll())

    def resetTeams(self):
        for c in self.allCharacters: 
            c.changeState(States.Default)
            c.setTarget(0, 0)

    #compute characters' support/ attack/ target abilities
    def performAction(self, actor: Character, target: Character, action: Actions) -> Interactions:
        interaction = self.compareElements(actor.element, target.element)
        if action == Actions.Attack:
            self.combat(actor, target, interaction)
        else:
            self.support(actor, target, interaction)
        return interaction

    def support(self, actor: Character, target: Character, interaction: Interactions):
        match interaction:
            case Interactions.SelfIsGenerative: 
                target.changeState(States.SuperBuffed)
            case Interactions.SelfIsDestructive:
                target.changeState(States.SuperDebuffed)
            case _:
                targetStateValue = min(target.state.value+2, 4)
                newState = States(targetStateValue)
                target.changeState(newState)
                #player is hurt by supporting someone who is dangerous to them
                if interaction == Interactions.OtherIsDestructive:
                    actorStateValue = max(actor.state.value-2, -4)
                    newState = States(actorStateValue)
                    actor.changeState(newState)
                #player is also buffed by supporting someone who is beneficial to them
                if interaction == Interactions.OtherIsGenerative:
                    actorStateValue = min(actor.state.value+2, 4)
                    newState = States(actorStateValue)
                    actor.changeState(newState)
    
    def combat(self, actor: Character, target: Character, interaction: Interactions):
        atkModifier = (int) (actor.state.value/2) if actor.action == Actions.Guard else (int) (actor.state.value)
        effectiveAtk = actor.atk + atkModifier
        match interaction:
            case Interactions.SelfIsGenerative: 
                target.reduceHp(-effectiveAtk)
            case Interactions.SelfIsDestructive:
                target.reduceHp(effectiveAtk*2)
            case _:
                target.reduceHp(effectiveAtk)
                #take recoil damage when attacking one who is dangerous to self
                if interaction == Interactions.OtherIsDestructive:
                    actor.reduceHp(effectiveAtk/2)
                #heal when attacking one who is beneficial to self
                if interaction == Interactions.OtherIsGenerative:
                    actor.reduceHp(-effectiveAtk/2)

    def findTarget(self, target: tuple[int, int]):
        (teamNo, id) = target
        if teamNo == 1: team = self.team1
        else: team = self.team2
        try:
            return team[id-1]
        except:
            return None
    
    def teamIsWiped(self, team : list[Character]):
        for c in team: 
            if c.isAlive() == True: return False
        return True
        
    def gameOver(self):
        gameOver = self.teamIsWiped(self.team1) or self.teamIsWiped(self.team2)
        return gameOver
    
    def isPlayerAlive(self, team: int, id: int):
        player = self.findTarget((team, id))
        if player == None: return False
        else: return player.IsAlive()

    #calculate type of interaction between characters
    def compareElements(self, element1: Elements, element2: Elements):
        #water
        if element1 == Elements.Water:
            if element2 == Elements.Wood:  return Interactions.SelfIsGenerative
            elif element2 == Elements.Fire: return Interactions.SelfIsDestructive
            elif element2 == Elements.Metal: return Interactions.OtherIsGenerative
            elif element2 == Elements.Earth: return Interactions.OtherIsDestructive
            else: return Interactions.Neutral
        #wood
        if element1 == Elements.Wood:
            if element2 == Elements.Fire:  return Interactions.SelfIsGenerative
            elif element2 == Elements.Earth: return Interactions.SelfIsDestructive
            elif element2 == Elements.Water: return Interactions.OtherIsGenerative
            elif element2 == Elements.Metal: return Interactions.OtherIsDestructive
            else: return Interactions.Neutral
        #fire
        if element1 == Elements.Fire:
            if element2 == Elements.Earth:  return Interactions.SelfIsGenerative
            elif element2 == Elements.Metal: return Interactions.SelfIsDestructive
            elif element2 == Elements.Wood: return Interactions.OtherIsGenerative
            elif element2 == Elements.Water: return Interactions.OtherIsDestructive
            else: return Interactions.Neutral
        #earth
        if element1 == Elements.Earth:
            if element2 == Elements.Metal:  return Interactions.SelfIsGenerative
            elif element2 == Elements.Water: return Interactions.SelfIsDestructive
            elif element2 == Elements.Fire: return Interactions.OtherIsGenerative
            elif element2 == Elements.Wood: return Interactions.OtherIsDestructive
            else: return Interactions.Neutral
        #metal
        if element1 == Elements.Metal:
            if element2 == Elements.Water:  return Interactions.SelfIsGenerative
            elif element2 == Elements.Wood: return Interactions.SelfIsDestructive
            elif element2 == Elements.Earth: return Interactions.OtherIsGenerative
            elif element2 == Elements.Fire: return Interactions.OtherIsDestructive
            else: return Interactions.Neutral
        return Interactions.Neutral
    
    #player team actions
    def setPlayerActions(self):
        #text version
        for c in self.team1:
            if c.isAlive():
                action = int(input("Guard: 1, Support: 2, Attack: 3. Choose: "))
                if action > 3 or action < 1: 
                    c.setAction(Actions.Idle)
                elif action == 1:
                    c.setAction(Actions.Guard)
                else:
                    team = int(input("1: Your Team, 2: Enemy Team. Choose: "))
                    id = int(input("Enter ID of character (1,2,3): "))
                    c.setTarget(team, id)
                    if action == 2: c.setAction(Actions.Support)
                    else: c.setAction(Actions.Attack)

    def setAIActions(self):
        for c in self.team2: 
            if c.isAlive(): 
                unknownChars : list[Character] = []
                #destructive allies & generative foes are ignored
                genOrNeutAllies : list[Character] = []
                destOrNeutFoes : list[Character] = []

                #valid = unknown OR allies good to support OR foes good to attack
                validTargets : list[Character] = []

                for chara in self.allCharacters:
                    if chara.isAlive() == False or chara == c: 
                        #if chara is dead or chara is self, skip to next character
                        continue
                    interaction = c.getComparison(chara)
                    if interaction == None:
                        unknownChars.append(chara)
                        validTargets.append(chara)
                    else:
                        if chara.team == c.team:
                            #for character on same team, only consider if supporting them is beneficial (not destructive)
                            if interaction in self.keyInteractions or interaction == Interactions.SelfIsGenerative:
                                genOrNeutAllies.append(chara)
                                validTargets.append(chara)
                        #for character on other team, only consider if attacking them is beneficial (not generative)
                        elif interaction in self.keyInteractions or interaction == Interactions.SelfIsDestructive:
                            destOrNeutFoes.append(chara)
                            validTargets.append(chara)

                #select a target or guard
                if len(validTargets) == 0:
                    c.action = Actions.Guard 
                    c.target = None
                    print(c.getName(), "will", c.action.name)
                else:
                    target = self.chooseMove(c, validTargets)
                    if target.team == c.team: 
                        if target.hp < 8 and c.getComparison(target) == Interactions.SelfIsGenerative: 
                            #emergency heal if ally hp is low, else support
                            c.action = Actions.Attack
                        else: c.action = Actions.Support
                    #target is on other team.
                    elif target.state in [States.Buffed, States.SuperBuffed] and c.getComparison(target) == Interactions.SelfIsDestructive: 
                        #if target is buffed or superbuffed, debuff. else attack
                        c.action = Actions.Support
                    else: c.action = Actions.Attack
                    c.target = target
                    print(c.getName(), "will", c.action.name, c.target)

                # #create dictionary of valid actions
                # choicesDict: dict[str, list[Character]] = dict()
                # if len(unknownChars) > 0: choicesDict["unknown"] = unknownChars
                # if len(genOrNeutAllies) > 0: choicesDict["allies"] = genOrNeutAllies
                # if len(destOrNeutFoes) > 0: choicesDict["foes"] = destOrNeutFoes
                # if len(choicesDict) == 0:
                #     #action is Guard
                #     c.action = Actions.Guard 
                #     print(c.getName(), "will", c.action.name)
                # else: 
                #     action, target = self.chooseMove(c, choicesDict)
                #     c.action = action
                #     c.target = (target.team, target.id)
                #     print(c.getName(), "will", c.action.name, c.target)
    
    def chooseMove(self, c: Character, options: list[Character]):
        for o in options:
            if o.team == c.team and o.hp < 8 and c.getComparison(o) == Interactions.SelfIsGenerative: return o
            elif o.team != c.team and o.state in [States.Buffed, States.SuperBuffed] and c.getComparison(o) == Interactions.SelfIsDestructive: return o
        return choice(options)
    #ai team actions
    # if c.isAlive()
    # check if there are any missing interactions:
    # if yes, there's a chance of attacking an unknown enemy/ supporting an unknown ally
    # for each interaction in map:
    # check if other party is alive
    # from those alive:
    # for ALLIES:
    # if generative reaction towards ally:
    # if ally has low HP: "attack"
    # else: support ally
    # for ENEMIES:
    # if destructive reaction towards enemy:
    # either support or attack (some way to coordinate, e.g. game_master list tracking number of buffs/ debuffs on an enemy?)
    # TEST
    # if enemy is buffed/ default -> "support" enemy
    # else -> attack enemy
    # ELSE?
    # attack random enemy
    def setAIActionsOld(self):
        for c in self.team2:
            if c.isAlive():
                targets = self.allCharacters.copy()
                targets.remove(c)
                generativeInteractions: list[Character] = []
                destructiveInteractions: list[Character] = []
                neutralInteractions: list[Character] = []
                noInteractionsYet: list[Character] = []
                for t in targets:
                    #list of valid targets = all alive characters except self
                    if t.isAlive() == False:
                        targets.remove(t)
                    else:
                        charTargetTuple = [item for item in c.comparisons if item[0] == t]
                        #sort other characters based on what interaction (if any) self has with them
                        if len(charTargetTuple) == 0: 
                            noInteractionsYet.append(t)
                        else:
                            interaction = charTargetTuple[0][1]
                            if interaction == Interactions.SelfIsGenerative:
                                generativeInteractions.append(t)
                            elif interaction == Interactions.SelfIsDestructive:
                                destructiveInteractions.append(t)
                            else:
                                neutralInteractions.append(t)
                #possible actions:
                # 1. guard -> do this if any of the others fails?
                # 2. attack generative ally
                # 3. support generative ally
                # 4. attack destructive enemy
                # 5. support destructive enemy
                # 6. attack neutral enemy
                # 7. support neutral ally
                # 8. support random unknown/ ally [don't support unknown enemies?]
                # 9. attack random unknown/ enemy [don't attack unknown allies?]
                randomChoice = randrange(0, 10)
                lists = {
                    "gen": generativeInteractions,
                    "dest": destructiveInteractions,
                    "neut": neutralInteractions,
                    "none": noInteractionsYet
                }
                if randomChoice < 9:
                    action, mark = self.findTargetFromLists(c, lists.copy())
                else:
                    action = Actions.Guard
                    mark = c
                c.action = action
                #temp, switch to saving Character itself after implementing UI
                c.target = mark
                print(c.getName(), c.action.name, c.target)
                
    def findTargetFromLists(self, c: Character, lists: dict[str, list[Character]])-> tuple[Actions, Character]:
        #if all four categories are empty
        if len(lists) == 0: return Actions.Guard, c

        key = choice(list(lists.keys()))
        value = lists.pop(key)
        #if chosen category is empty
        if len(value) == 0: return self.findTargetFromLists(c, lists)
        else:
            if key == "gen": 
                return self.findGenerativeTarget(c, value)
            elif key == "dest": 
                return self.findDestructiveTarget(c, value)
            elif key == "neut": 
                return self.findGenerativeTarget(c, value)
            else: 
                return self.findUnknownTarget(value)
    
    def findGenerativeTarget(self, c: Character, chars: list[Character]):
        mark = choice(chars)
        if mark.team == c.team: action = Actions.Support
        else: action = Actions.Attack
        return action, mark

    def findDestructiveTarget(self, c: Character, chars: list[Character]):
        mark = choice(chars)
        if mark.team == c.team: action = Actions.Attack
        else: action = Actions.Support
        return action, mark

    def findUnknownTarget(self, chars: list[Character]):
        mark = choice(chars)
        if randrange(0,2) == 1: action = Actions.Attack
        else: action = Actions.Support
        return action, mark

    #execute team actions
    def executeTeamActions(self):
        activeCharacters: list[Character] = sorted(self.allCharacters, key=lambda character: character.action.value)
        for ch in activeCharacters:
            if ch.isAlive():
                action = ch.getAction()
                if action in [Actions.Attack, Actions.Support]:
                    chTarget : Character = ch.getTarget()
                    if chTarget == None: 
                        ch.setAction(Actions.Idle)
                        continue
                    if chTarget.team not in [1, 2]:
                        ch.setAction(Actions.Idle)
                        continue
                    if chTarget.id not in [1, 2, 3]:
                        ch.setAction(Actions.Idle)
                        continue
                    interaction = self.performAction(ch, chTarget, action)
                    #add this reaction to character's table AND the reverse (e.g. selfIsGenerative -> otherIsGenerative) to the target's table
                    ch.addComparison(chTarget, interaction)
                    reverseInteraction = Interactions(interaction.value*-1)
                    chTarget.addComparison(ch, reverseInteraction)
                    print(f"{ch.getName()} performed {ch.action.name} on {chTarget.getName()}. Interaction was {interaction.name}.")
                else:
                    print(f"{ch.getName()} will {ch.action.name}.")
                    

    
