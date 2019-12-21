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
			pronoun = random.choice(['He','She'])
			name = random.choice(Villager.names[pronoun])
			attr = name, pronoun
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
		"inspect":self.player.inspect, # no noun req if in battle
		"attack":self.player.attack, # no noun req if in battle
		"talk":self.player.talk, # noun req
		"inventory":self.player.inventory_print, # no noun req
		"move":self.player.move, # no noun req if in battle
		"use":self.player.use, # noun req
		"help": self.help_menu # no noun req
		}
		action_flag = True
		noun_flag = True
		noun = None
		if self.player.is_inbattle: # Remove certain choices (and change help menu) if in battle
			del action_dict['talk']
			name_list = [self.player.battle_opponent.name.lower()]
			noun_flag = False
		else:
			name_list = [x.name.lower() for x in self.env.contents]
		while action_flag:
			self.writer.msg_slow('What do you do?')
			cmd = input(": ").lower().split()
			action_word = cmd[0]
			if (action_word in action_dict):
				if len(cmd)>=2 and noun_flag:
					noun = ''.join(cmd[1::])
				elif action_word=="help" or action_word=="inventory":
					noun_flag = False
				action_flag = False
			else: # unknown verb
				self.writer.msg_slow("{} is an unknown action.".format(action_word))
				self.writer.msg_slow("Please enter a valid action.")
			while noun_flag:
				if action_word == "move":
					name_list =["north","south","east","west"]
				elif action_word == "use":
					name_list = self.player.inventory_dict.keys()
				if noun: # if noun has been defined
					if noun in name_list: # TODO add player inventory to search (for use)
						noun_object = [x for x in self.env.contents if x.name.lower()==noun][0]
						noun_flag = False
					elif action_word=="inspect" and noun=="environment":
						noun_object = self.env
						noun_flag = False
					else: # noun not in name list
						self.writer.msg_slow("There is no " + noun + " here.")
						noun = None
				else: # Noun required, but none provided
					# TODO this needs a prefix/statement dictionary bank based on action type
					self.writer.msg_slow("What do you want to {}?".format(cmd[0]))
					noun = ''.join(input(": ").lower().split())
					if noun == "cancel":
						action_flag = True
						break # exit to action while loop
		if noun:
			action_dict[action_word](noun_object)
		else:
			action_dict[action_word]()

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
	def inspect(self,*args): # TODO needs to provide who you're at battle with and what their condition is
		if not args:
			self.print_add(self.battle_opponent.name)
			for stat in [hp,strength,speed,defense]:
				self.print_add('    '+str(stat)+': '+self.battle_opponent.stat)
			# TODO provide qualitative information regarding current stats
		else:
			inspect_object = args[0]
			self.print_add(inspect_object.get_description())
			# self.print_add()
			# TODO get description of arg - get change obj.get_desc to work with this
			# # # obj.get_desc should provide the necessary prefixes etc for the description.
			pass
		pass
	def attack(self,*args):
		if args: # Player attacks first
			self.battle_opponent = args[0]
			attack_first = True
		else: # NPC attacks first
			attack_first = False


		if not self.battle_opponent.is_alive:
			self.print_add('You attack '+self.battle_opponent.name+"'s dead corpse. You get some blood and guts on yourself but nothing else happens.")
			return

		# Setup Settings
		self.is_inbattle = True
		self.battle_opponent.is_inbattle = True
		p_hit = 0.8*self.speed / (self.battle_opponent.speed + self.speed)
		p_gethit = 0.8*self.battle_opponent.speed / (self.battle_opponent.speed + self.speed)

		#Damage Assignment
		player_flag = True # TODO FUTUREDEV add multiple hits per turn depending on speed ratio
		opponent_flag = True
		while player_flag or opponent_flag:
			if attack_first or not opponent_flag: # if player attacks first or opponent has already attacked
				player_flag = False
				hploss_give = round(random.uniform(0.5,1)*self.strength / self.battle_opponent.defense)
				hit = random.choices(population=[True,False],weights=[p_hit,1.0-p_hit])[0]
				if hit:	
					self.print_add('You hit '+self.battle_opponent.name+'.')
					self.print_add(self.battle_opponent.name+' lost '+str(hploss_give)+" hp.")
					self.battle_opponent.hp-=hploss_give
				else:
					self.print_add('You missed '+self.battle_opponent.name+'.')
				if self.battle_opponent.hp<=0: # Opponent killed -> fight is over
					self.print_add("You've slain "+self.battle_opponent.name+"!")
					self.is_inbattle = False
					self.battle_opponent.is_inbattle = False
					self.battle_opponent = None
					return 
			while opponent_flag: # Opponent attacks
				opponent_flag  = False
				hploss_take = round(random.uniform(0.5,1)*self.battle_opponent.strength / self.defense)
				get_hit = random.choices([True,False],weights=[p_gethit,1.0-p_gethit])[0]
				if get_hit:
					self.print_add('You were hit by '+self.battle_opponent.name+'.')
					self.print_add("You've lost "+str(hploss_take)+' hp.')
					self.hp-=hploss_take
				else:
					self.print_add(self.battle_opponent.name+' missed you.')
				if self.hp <=0: # Player killed
					return
				pass
	def talk(self, talk_object):
		yousay = 'You say hi to '
		if isinstance(talk_object, Villager):
			if talk_object.name_known:
				yousay += talk_object.name +'.'
			else:
				if talk_object.pronoun == 'He':
					yousay += 'the man.'
				else:
					yousay += 'the woman.'
		self.print_add(yousay)
		self.print_add(talk_object.get_dialogue())
		talk_object.name_known = True
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
		self.create_description() # Create environment static description
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
		self.env_description = prefix + ' ' + desc1 + ' ' + desc2 + ' ' + self.name
	def get_description(self): # Get description of environment and contents
		description = 'You find yourself in ' + self.env_description + '.'
		for x in self.contents:
			description +='\n' + 'You see '  # TODO change to more than "you see"
			if isinstance(x,Villager):
				if x.pronoun == 'He':
					description += 'a man... '
				else:
					description += 'a woman... '
			description += x.get_description()
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
	'He':['Jim', 'Ted', 'Bob','Tom'],
	'She':['Jill','Tammy', 'June','Beth']
	}
	def __init__(self,args):
		# Flags
		self.is_alive = True
		self.name_known = False
		self.is_inbattle = False

		#
		self.pronoun = args[1]
		self.name = self.initial_name()
		self.true_name = args[0] # name after name_know
		self.print_out = ''
		self.desc_type = random.choice(['good','bad'])
		self.create_description()

		#Stats
		self.hp = 1
		self.speed = 0 # Cannot hit player
		self.defense = 1
		self.strength = 0 #cannot hurt player
	def initial_name(self):
		if self.pronoun == "He":
			return "man"
		else:
			return "woman"
	def create_description(self):
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
		self.init_description = self.pronoun + ' ' + verb + ' like' + ' ' + prefix + ' ' + self.adj1 + ', ' + self.adj2 + ' ' + noun+'.'
		self.description = "it's "+self.adj1+ ', ' +self.adj2 +' '+self.name+'.'
	def get_description(self):
		if self.is_alive:
			return self.init_description
		else:
			return "While they once looked " + self.adj1 + " and " + self.adj2 + ", now you see a pile of organs, blood and meat. Perhaps some teeth."
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
		intro_dialogue = random.choice(intro_list) +  self.true_name  +'. '
		self.name = self.true_name
		if self.name_known:
			end_dialogue = random.choice(end_list2)
			dialogue = end_dialogue
		else:
			end_dialogue = random.choice(end_list1)
			dialogue = start_dialogue + intro_dialogue + end_dialogue
		return dialogue
	def get_dialogue(self):
		if self.is_alive:
			return self.create_dialogue()
		else:
			return '"..." The bloody corpse says nothing back.'
	def update(self):
		if self.hp == 0:
			self.is_alive = False
class Item():
	pass

def main():
	world = World()
	world.thing_gen((0,0),Villager)
	print(world.env.name)
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