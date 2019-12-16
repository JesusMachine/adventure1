#!/usr/bin/env python 

import os
import sys
import time
import random
import math
import re

class World(): # Global Container
	def __init__(self):
		self.map = self.create_world(20,20)
		self.writer = Writer()
		self.env = None # Instant access to current environment (so you dont have to type a huge thing for actions)
		self.player = Player('Fake') #TODO this must be changed eventually
		self.new_game()
	def create_world(self,m,n): # Populates world dict with mxn locations, each containing an environment
		world_map = {}
		for i in range(m):
			for j in range(n):
				env_type = 	random.choice(['village','desert','forest'])			
				world_map[(i,j)] = Environment(env_type)
		return world_map
	def place_gen(self,location,env_type): # Creates an environment in a world location
		self.map[location] = Environment(env_type)
		pass
	def thing_gen(self,location,thing_type): # Creates a thing in an environment
		# TODO intantiations things based on 1.) environment at location and 2.) thing_type
		# 
		if thing_type == Villager:
			gender = random.choice(['m','f'])
			name = random.choice(Villager.names[gender])
			attr = name, gender
		elif thing_type == Monster:
			# TODO - init settings for monster
			pass
		elif thing_type == Item:
			#TODO
			pass
		self.map[location].contents.append(thing_type(attr))
		pass
	def new_game(self):
		self.place_gen((0,0),'forest') # Change this to world_gen later (Populates ALL of map with items and monsters - uses place_gen, then thing_gen)
		self.env = self.map[(0,0)]
		start_game = False # TODO Change this when finished debugging!!!
		if start_game:
			self.writer.clear_screen()
			name = input('Please enter your characters name:\n')
			self.player = Player(name)
			# self.tutorial_choice(player.name) # TODO
			self.writer.clear_screen()
			self.writer.msg_slow('You hear a voice in the distance as you slowly regain consciousness.')
			self.writer.msg_slow('"{}"...'.format(self.player.name))
			self.writer.msg_slow('"{}"...'.format(self.player.name))
			self.writer.msg_fastslow('"{}!"'.format(self.player.name),'...')
			self.writer.clear_screen()
			self.writer.msg_slow('"Please help us, {}!"...'.format(self.player.name))
			self.writer.clear_screen()
			self.writer.msg_slow('You awake to find yourself in an unfamiliar forest.')
			self.writer.msg_slow('What do you do?')
			self.loop()
		if not start_game:
			player = Player('Jim')
		pass
	def help_menu(self):
		if not self.player.is_inbattle: # TODO normal help menu
			pass
		if self.player.is_inbattle: # TODO battle help menu
			pass
		pass
	def loop(self):
		while self.player.is_alive:
			self.get_input()
			self.update()
		if not self.player.is_alive:
			self.writer.msg_slow('You died a horrible, agonizing death... GAMEOVER')
	def get_input(self): # Basic Input System (Reader). # TODO Test ALL Features
		action_dict = {
		"inspect":self.player.inspect,
		"attack":self.player.attack,
		"talk":self.player.talk,
		"inventory":self.player.inventory_print,
		"move":self.player.move,
		"use":self.player.use,
		"help": self.help_menu
		}
		if self.player.is_inbattle: # Remove certain choices (and change help menu) if in battle
			del action_dict['talk']
			name_list = [self.player.battle_opponent.name.lower()]
		if not self.player.is_inbattle:
			name_list = [x.name.lower() for x in self.env.contents]
		action_flag = True
		while action_flag:
			self.writer.msg_slow('What do you do?')
			cmd = input(": ").lower().split()
			action_word = cmd[0]
			if (len(cmd)>=2) and (action_word in action_dict):
				noun = ''.join(cmd[1::])
				action_flag = False
			elif action_word == "help":
				self.help_menu()
			elif action_word == "inventory":
				self.player.inventory()
				pass
			# elif self.player.is_inbattle and :
				# action_dict
			elif (len(cmd)<2) and (action_word in action_dict):
				self.writer.msg_slow("What do you want to {}?".format(cmd[0]))
				noun = ''.join(input(": ").lower().split())
				action_flag = False
			else:
				# TODO Change to writer output
				self.writer.msg_slow("{} is an unknown action.".format(action_word))
				self.writer.msg_slow("Please enter a valid action.")
			if noun in name_list: # TODO add player inventory to search (for use)
				noun_object = [x for x in self.env.contents if x.name.lower()==noun][0]
				action_dict[action_word](noun_object)
			else:
				if self.player.is_inbattle:
					self.writer.msg_slow("You can only interact with " + self.player.battle_opponent.name + " while fighting.")
				else:
					self.writer.msg_slow("There is no " + noun + " here.")
	def update(self): # Updates player and all environments, which then update all objects
		for value in self.map.values(): # Update environments
			value.update()
			if value.print_out.strip():
				self.writer.msg_slow(value.print_out) #print messages from environments
				value.print_out=''
		self.player.update() # Update player
		if self.player.print_out.strip():
			self.writer.msg_slow(self.player.print_out) #print messages from player
			self.player.print_out = ''
		pass
class Writer(): # Basic Output System
	def __init__(self):
		self.ostype = os.name
	def msg_slow(self,msg):
		for i in msg:
			sys.stdout.write(i)
			sys.stdout.flush()
			time.sleep(0.05)
		sys.stdout.write('\n')
	def msg_fast(self,msg):
		sys.stdout.write(msg)
		sys.stdout.flush()
		sys.stdout.write('\n')
		input("\r")
	def msg_fastslow(self,msgfast,msgslow):
		sys.stdout.write(msgfast)
		sys.stdout.flush()
		time.sleep(0.3)
		for i in msgslow:
			sys.stdout.write(i)
			sys.stdout.flush()
			time.sleep(0.1)
		sys.stdout.write('\n')
		input("\r")
	def clear_screen(self):
		if self.ostype == 'nt':
			os.system('cls')
		else:
			os.system('clear')
class Player(): # Player resides in world, NOT environment
	def __init__(self,name):
		self.name = name
		self.t = 0
		self.print_out =''
		self.inventory_dict={}
		# State Flags
		self.is_alive = True
		self.is_inbattle = False

		# Stats
		self.level = 1
		self.xp = 0.0
		self.hp = 10
		self.strength = 1
		self.speed = 1
		self. defense = 1
	def level_up(self): # Runs at the end of each action
		lvl_start = self.level
		self.level = int(math.sqrt(xp))
		if self.level>lvl_start:
			self.stats['hp'] += 3
			for key in ['strength','speed','defense']:
				self.stats[key] += random.randint(0,2)
	def create_description(self): # TODO
		# TODO description will be based on current hp out of max hp for level
		self.description = 'None'
		pass
	def print_add(self,msg):
		self.print_out += '\n' + msg
	def inspect(self,object): # TODO needs to provide who you're at battle with and what their condition is
		if self.is_inbattle:
			self.print_add(self.battle_opponent.name)
		pass
	def attack(self, *args):
		#TODO Need to make way such that only player and object can interact until 1.) one dies, or 2.) player moves and escapes (player.speed>object.speed)
		# This should be accomplished in world.get_input()


		## Player attacks first
		for arg in args:
			attack_object = arg # extracting attack_object from tuple
		if not attack_object.is_alive:
			self.print_add('You attack '+attack_object.name+"'s dead corpse. You get some blood and guts on yourself but nothing else happens.")
			return
		self.battle_opponent=attack_object


		# Setup Settings
		self.is_inbattle = True
		self.battle_opponent.is_inbattle = True
		self.battle_opponent = attack_object
		p_hit = self.speed = 0.8*self.speed / (self.battle_opponent.speed + self.speed)
		p_gethit = 0.8*self.battle_opponent.speed / (self.battle_opponent.speed + self.speed)
		hploss_give = self.strength / self.battle_opponent.defense
		hploss_take = self.battle_opponent.strength / self.strength

		#Damage Assignment
			 # Player attacks
		if random.choices(population=[1,0],weights=[p_hit,1-p_hit]):
			self.print_add('You hit '+self.battle_opponent.name+'.')
			self.battle_opponent.hp-=hploss_give
		else:
			self.print_add('You missed '+self.battle_opponent.name+'.')
		if self.battle_opponent.hp<=0: # Opponent killed -> fight is over
			self.print_add("You've slain "+self.battle_opponent.name+"!")
			self.is_inbattle = False
			self.battle_opponent.is_inbattle = False
			self.battle_opponent = None
			return 
			# Opponent attacks
		if random.choices(population=[1,0],weights=[p_gethit,1-p_gethit]):
			self.print_add('You were hit by '+self.battle_opponent.name+'.')
			self.hp-=hploss_take
		else:
			self.print_add(self.battle_opponent.name+' missed you.')
		if self.hp <=0: # Player killed
			return
		pass
	def talk(self, object):
		yousay = 'You say hi to '
		if isinstance(object, Villager):
			if object.name_known:
				yousay += object.name +'.'
			else:
				if object.gender == 'm':
					yousay += 'the man.'
				else:
					yousay += 'the woman.'

		print(yousay)
		print(object.create_dialogue())
		object.name_known = True
		pass
	def inventory_print(self): # Prints items in player.inventory_dict
		for key in self.inventory_dict.keys:
			self.print_add(str(key)+':'+str(self.inventory_dict[key]))
		pass
	def inventory_add(self):# Adds items to self.inventory.dict

		pass
	def move(self, where): #TODO
		#TODO moves player to new location if it exists and if not in battle. If not, states there are mountains there. If in battle, calculates chances to run based on speed. ALSO adds 1 to time if successful.
		pass
	def use(self,item): #TODO
		#TODO activate item if it exists in players inventory
		pass
	def update(self):
		self.create_description()
		if self.hp == 0:
			self.is_alive = False
		pass
		# Always at end of update!
		if not self.is_inbattle:
			self.t += 1

class Environment(): # Local Container -- Contains all Monsters, Villagers, Items except Player (contained in world)
	# env_stuff = {
	# 'forest': {'description':['lush','green'],'things':['Monster','Item','Villager']},
	# 'village':{'description':['small','peaceful'],'things':['Villager','Item']},
	# 'desert':{'description':['dry','hot'],'things':['Monster','Item']}
	# }
	def __init__(self,env_type):
		self.name = env_type
		self.print_out = '' 
		self.contents = list()
		self.create_description()
		self.env_description = self.get_description()
	def create_description(self): # Creates Unique Description
		if self.name == 'forest':
			desc_list1 = ['lush,', 'quiet,', 'peaceful,', 'solumn,', 'eerie,', 'cold,', 'bright,', 'dark,', 'thick,', 'haunted,', 'creepy,']
			desc_list2 = ['green', 'dead', 'burned', 'bare','mountainous']
		elif self.name == 'village': # TODO
			desc_list1 = ['giant']
			desc_list2 = ['dirty']
			pass
		elif self.name == 'desert':
			desc_list1 = ['arid,', 'cold,', 'hot,', 'flat,']
			desc_list2 = ['dusty','bare','lonely','ancient']
		desc1 = random.choice(desc_list1)
		desc2 = random.choice(desc_list2)
		if re.match(r'[aeiou]',desc1[0]):
			prefix = 'an'
		else:
			prefix = 'a'
		self.description = prefix + ' ' + desc1 + ' ' + desc2 + ' ' + self.name
	def get_description(self): # Get description of environment and contents
		description = 'You find yourself in ' + self.description + '.'
		for x in self.contents:
			description +='\n' + 'You see '  # TODO change to more than "you see"
			if isinstance(x,Villager):
				if x.gender == 'm':
					description += 'a man... '
				elif x.gender == 'f':
					description += 'a woman... '
			description += x.description
		return description
	def update(self): # Updates all objects in environment
		for x in self.contents:
			x.update()
			if x.print_out.strip(): # Check if there is a printout from object
				self.print_out += x.print_out
		pass
class Monster(): # TODO cannot have 2 monsters with same name in environment, make a rename method to resolve (can be Elf1 and ELf2 or simply reroll)
	mon_types = { # TODO addmore
	'Elf',
	'Goblin',
	'Orc'
	}
	def __init__(self,args):
		# State Flags
		self.is_alive = True
		self.is_inbattle = True


		self.name = arg[1] + ' ' + arg[0]
		self.print_out = '' 
		self.create_stats()
		self.create_decription()
	def create_stats(self,args):
		# TODO - Monster stats are based on 1.) arg[0] (base stats) 2.) arg[1] (modifiers - add or subtract) 3.) player.level (multipliers)
		# TODO - Add xp_give
		# [hp,strength,speed,defense]
		base = {
		'Elf': [10,3,5,3],
		'Goblin':[5,3,3,3],
		'Orc': [20,5,3,4]
		}
		modifier = {
		'Dark': [-2,2,0,-1],
		'High': [1,-2,0,1],
		'Wood': [-2,-1,3,0],
		'Beserker': [0,0,2,-2],
		'Armored': [0,0,-2,2]
		}
		# TODO
		#  create stats => [round(x) for x in (player.level/4)*(base[arg[0]] + modifier[arg[1]])]
		pass
	def create_description(self):
		# TODO
		pass
	def update(self):
		if self.stats['hp'] ==0:
			self.is_alive == False
class Villager(): # TODO cannot have 2 villagers with same name in environment, make a rename method to resolve (can be Jill1 and Jill2 or simply reroll)
	names = {
	'm':['Jim', 'Ted', 'Bob','Tom'],
	'f':['Jill','Tammy', 'June','Beth']
	}
	def __init__(self,args):
		# Flags
		self.is_alive = True
		self.name_known = False
		self.is_inbattle = False

		#
		self.name = args[0]
		self.print_out = ''
		self.gender = args[1]
		self.desc_type = random.choice(['good','bad'])
		self.description = self.create_description()

		#Stats
		self.hp = 1
		self.speed = 1
		self.defense = 1
		self.strength = 0 #cannot hurt player
	def create_description(self):
		if self.gender == 'm':
			pronoun = 'He'
		else:
			pronoun = 'She'
		if self.is_alive == True:
			# TODO - create self.positive or negative (random)
			# Then, create positive, neutral negative descriptions and dialogue
			# Ex - negative "She smells like a nasty, old whore" - nasty, whore = negative, old = neutral
			# Ex - positive "He looks like a cheery, old friend "
			self.desc_type = random.choice(['bad','good'])
			if self.desc_type == 'bad':
				verb_list = ['looks', 'smells', 'stinks']			
				adj_list1 = ['nasty','angry','scary']
				adj_list2 = ['dirty','filthy','scabbies-ridden','toothless','old','cold']
				noun_list = ['devil','skank','whore', 'tool','beggar']
			elif self.desc_type == 'good':
				verb_list = ['looks','sounds']
				adj_list1 = ['kind','beautiful','friendly','intelligent','young','old']
				adj_list2 = ['warm','observant','upright','modest','vibrant','hard-working']
				noun_list = ['angel','saint','citizen','scholar','professional']
			verb = random.choice(verb_list)
			self.adj1 = random.choice(adj_list1)
			self.adj2 = random.choice(adj_list2)
			noun = random.choice(noun_list)
			if re.match(r'[aeiou]',self.adj1[0]):
				prefix = 'an'
			else:
				prefix = 'a'
			self.description = pronoun + ' ' + verb + ' like' + ' ' + prefix + ' ' + self.adj1 + ', ' + self.adj2 + ' ' + noun
			self.description2 = self.adj1 + ', ' + self.adj2 + ' ' + noun
		else:
			pass # TODO make description of blood or messed up corpse
	def create_dialogue(self): # If positive, also add probability for a tip (tells you what is to the north/east/west/south)
		if self.desc_type == 'good':
			start_list = ["Hi! I'm ","Why, hello! ","Good Day! "]
			intro_list = ['My name is ', 'You can call me ']
			end_list1 = ["It's nice to meet you!", "Splended to make your aquaintance!", "Fantastic to meet you."]
			end_list2 = ["It's nice to see you again!", "Splended to see you again", "Fantastic to see you again."]
		elif self.desc_type == 'bad':
			start_list = ["wudaya want? *Spit* ","You keep staring and Imma hit ya. "]
			intro_list = ['You can call me ', "The name's "]
			end_list1 = ['Hope the back looks better than the front!',"Don't talk to me no more!"]
			end_list2 = ['What!? Do you want some loose teeth?',"Thought I made myself clear, get the hell out of here!"]
		start_dialogue = random.choice(start_list)
		intro_dialogue = random.choice(intro_list) +  self.name  +'. '
		if self.name_known:
			end_dialogue = random.choice(end_list2)
			dialogue = end_dialogue
		else:
			end_dialogue = random.choice(end_list1)
			dialogue = start_dialogue + intro_dialogue + end_dialogue
		return dialogue
	def update(self):
		if self.hp == 0:
			self.is_alive = False
			self.description = "While they once looked " + self.adj1 + " and " + self.adj2 + ", now you see a pile of organs, blood and meat. Perhaps some teeth."
			self.dialogue = "You talk to the bloody corpse, but it says nothing back."
class Item():
	pass

def main():
	world = World()
	world.thing_gen((0,0),Villager)
	# Creating Battle
	world.player.is_inbattle = True
	world.player.battle_opponent = world.env.contents[0]
	world.player.battle_opponent.is_inbattle = True
	# Trying battle
	print(world.env.contents[0].name) # Name of villager to attack
	world.loop()



if __name__ == '__main__':
	main()
	pass



## EXAMPLES LISTS ##

# world.env.contents[0].stats['hp']=0  # Setting object hp to 0



# print(world.env.description)

# print(world.map[(0,0)].description)
# world.place_gen((0,1),'desert')
# print(world.map[(0,1)].description)
# world.thing_gen((0,1),Villager)
# print(world.map[(0,1)].contents[0].dialogue)


# world.thing_gen((0,0),Villager) # Create a villager at (0,0) - must have 
# print(world.map[(0,0)].contents)

# world.place_gen((0,1),'desert') # Create an environment (desert type) at (0,1)
# world.thing_gen((0,1),Villager)
# print(world.map[(0,1)].name) # Print the environment type at (0,1) -- that is, environment.name
# print(world.map[(0,1)].contents[0].name) # Print the name of the first object (villager) at (0,1)


##### Case Tests
# 1 - Changing an object in world.env will also change the world.map[(x,y)] object - they are the same
	# world = World()
	# world.thing_gen((0,0),Villager)
	# print(world.map[(0,0)].contents[0].name)
	# print(world.env.contents[0].name)
	# world.env.contents[0].name = 'Jake'
	# print(world.map[(0,0)].contents[0].name)
	# print(world.env.contents[0].name)
# 2 - Attacking and killing a villager
	# world = World()
	# world.thing_gen((0,0),Villager)
	# # Creating Battle
	# world.player.is_inbattle = True
	# world.player.battle_opponent = world.env.contents[0]
	# world.player.battle_opponent.is_inbattle = True
	# # Trying battle
	# print(world.env.contents[0].name) # Name of villager to attack
	# world.get_input()