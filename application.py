#!/usr/bin/env python 

import os
import sys
import time
import random
import math
import re
from copy import copy

start_game = False
class World(): # Global Container
	size = (20,20)
	def __init__(self):
		self.map = self.create_world(World.size)
		self.writer = Writer()
		self.env = None # Instant access to current environment (so you dont have to type a huge thing for actions)
		self.player = Player('Billy Bob Thornton') #TODO this must be changed eventually
		self.new_game()
	def create_world(self,world_size): # Populates world dict with mxn locations, each containing an environment
		world_map = {}
		for i in range(world_size[0]):
			for j in range(world_size[1]):
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
			base = random.choice(list(Monster.base.keys()))
			modifier = random.choice(list(Monster.modifier.keys()))
			attr = modifier, base
			# TODO - base and modifier should be based on location/environment type, not random
			pass
		elif thing_type == Item:
			base = random.choice(list(Item.base_type.keys()))
			modifier = random.choice(list(Item.modifier_type.keys()))
			attr = modifier, base
			pass
		elif thing_type == Equipment:
			# TODO - create equipment type
			pass
		self.map[location].contents.append(thing_type(attr))
		pass
	def new_game(self):
		self.place_gen((0,0),'forest') # Change this to world_gen later (Populates ALL of map with items and monsters - uses place_gen, then thing_gen)
		self.env = self.map[(0,0)]

		# self.env.contents.append(Item(('Regular','Potion')))
		# self.env.contents.append(Item(('Regular','Potion')))
		# self.env.contents.append(Item(('Regular','Potion')))

		# self.thing_gen((0,0),Villager) # TODO Remove later
		self.thing_gen((0,0),Monster) # TODO remove later
		# self.thing_gen((0,0),Item)

		# TODO add static characters and environments here
		# TODO add randomized characters and environments here
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
		if not start_game:
			player = Player('Jim')
		self.update()
		self.loop()
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
			self.writer.msg_slow('You died a horrible, agonizing death... GAME OVER')
	def get_input(self): # Basic Input System (Reader). # TODO Test ALL Features
		action_dict = {
		"inspect":self.player.inspect, # no noun req if in battle
		"attack":self.player.attack, # no noun req if in battle
		"talk":self.player.talk, # noun req
		"inventory":self.player.inventory_print, # no noun req
		"move":self.player.move, # no noun req if in battle
		"use":self.player.use, # noun req
		"grab":self.player.grab, # noun req
		"help": self.help_menu # no noun req
		}
		action_flag = True
		noun_flag = True
		noun = None
		if self.player.is_inbattle: # Remove certain choices (and change help menu) if in battle
			del action_dict['talk']
			del action_dict['grab']
			name_list = [self.player.battle_opponent.name.lower()]
			noun_flag = False
		else:
			name_list = [''.join(x.name.lower().split()) for x in self.env.contents]
		while action_flag:
			self.writer.msg_slow('What do you do?')
			cmd = input(": ").lower().split()
			if cmd == ['eat','shit','and','die']: # Easter egg
				self.writer.msg_slow('You ate some rancid feces.')
				self.player.hp = 0
				break
			if not cmd:
				self.writer.msg_slow('You must enter an action. For help, type "help".')
				return
			if (cmd[0] in action_dict): # Known action
				action_word = cmd[0]
				if action_word == "use":
					name_list = [''.join(x.lower().split()) for x in list(self.player.inventory_dict.keys())]
					noun_flag = True
				if len(cmd)>=2 and noun_flag:
					if cmd[1] == "to":
						del cmd[1]
					noun = ''.join(cmd[1::])
				elif action_word=="help" or action_word=="inventory":
					noun_flag = False
				action_flag = False
			else: # unknown action
				self.writer.msg_slow("{} is an unknown action.".format(cmd[0]))
				self.writer.msg_slow("Please enter a valid action.")
				return
			while noun_flag:
				if action_word == "move":
					dir_list =["north","south","east","west"]
					if noun in dir_list:
						noun_flag = False
						noun_object = noun
					else:
						self.writer.msg_slow(noun+" is not a direction. Which direction do you want to move?")
						noun = ''.join(input(": ").lower().split())
						if noun == "cancel":
							action_flag = True
							break
				elif noun: # if noun has been defined
					if noun in name_list: # TODO add player inventory to search (for use)
						noun_object = [x for x in self.env.contents if ''.join(x.name.lower().split())==noun][0] # TODO this could be used for multiple of same name
						noun_flag = False
					elif action_word=="inspect" and noun=="environment":
						noun_object = self.env
						noun_flag = False
					elif action_word=="use":
						self.writer.msg_slow('You don\'t have any ' + noun +'s in your inventory.' )
						noun = None
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
		elif cmd == ['eat','shit','and','die']: # Easteregg
			pass
		else:
			action_dict[action_word]()
	def update(self): # Updates player and all environments, which then update all objects
		self.env = self.map[(self.player.location[0],self.player.location[1])] # Change environment based on players current location
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
		self.location = [0,0]

		self.print_out =''
		self.inventory_dict={}
		self.equipment_dict={
		'head':None,
		'chest':None,
		'hands':None,
		'legs':None,
		'feet':None,
		'weapon':None
		}

		# State Flags
		self.is_alive = True
		self.is_inbattle = False

		# Stats
		self.level = 1
		self.xp = 0.0
		self.hp = 10
		self.strength = 1
		self.speed = 1
		self.defense = 1
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
		pass
	def inspect(self,*args): # TODO needs to provide who you're at battle with and what their condition is
		if not args: # In battle
			for character in [self, self.battle_opponent]:
				self.print_add(character.name)
				for stat in ['hp','strength','speed','defense']:
					self.print_add('    '+stat+': '+str(getattr(character,stat)))
			# TODO provide qualitative information regarding current stats
		else: # Not in battle
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
				hploss_give = math.ceil(random.uniform(0.5,1)*self.strength / self.battle_opponent.defense)
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
				hploss_take = math.ceil(random.uniform(0.5,1)*self.battle_opponent.strength / self.defense)
				get_hit = random.choices([True,False],weights=[p_gethit,1.0-p_gethit])[0]
				if get_hit:
					self.print_add('You were hit by '+self.battle_opponent.name+'.')
					self.print_add("You've lost "+str(hploss_take)+' hp.')
					self.hp-=hploss_take
				else:
					self.print_add(self.battle_opponent.name+' missed you.')
				if self.hp<=0:
					return
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
		pass
	def inventory_print(self): # Prints items in player.inventory_dict
		if bool(self.inventory_dict):
			self.print_add('Your inventory contains:')
			for x in list(self.inventory_dict.keys()):
				if self.inventory_dict[x]>1:
					modifier = 's'
				else:
					modifier = ''
				self.print_add(str(self.inventory_dict[x]) + " " + x + modifier)
		else:
			self.print_add('Your inventory is empty.')
		pass
	def move(self, *args): #TODO
		#TODO moves player to new location if it exists and if not in battle. If not, states there are mountains there. If in battle, calculates chances to run based on speed. ALSO adds 1 to time if successful.
		if args:
			loc = copy(self.location)
			if args[0]=='north':
				loc[1] += 1
			elif args[0]=='south':
				loc[1] -= 1
			elif args[0]=='east':
				loc[0] += 1
			elif args[0]=='west':
				loc[0] -= 1
			if loc[0]<0 or loc[1]<0 or loc[0]>World.size[0] or loc[1]>World.size[1]:
				self.print_add('Your path is blocked by mountains to the '+args[0]+'.')
			else:
				self.location = loc
				self.print_add('You move '+args[0]+' and find yourself in a new environment.')
		else: # TODO attempt to run from battle
			p_run = 0.5*self.speed / (self.battle_opponent.speed + self.speed) # Chance to run
			run = random.choices(population=[True,False],weights=[p_run,1.0-p_run])[0]
			if run:
				self.print_add('You successfully ran away from ' + self.battle_opponent.name + '.')
				self.is_inbattle = True
				self.battle_opponent.is_inbattle = True
				self.battle_opponent = None
			else:
				self.print_add('You couldn\'t outrun ' + self.battle_opponent.name + '.')
				self.get_attacked()
	def use(self,item): #TODO
		base = item.name.split()[1]
		modifier = item.name.split()[0]
		attr_increase = Item.base_type[base]*Item.modifier_type[modifier]
		attr_val = getattr(self,Item.use_type[base]) + attr_increase # Gets value of item modifying attr
		setattr(self,Item.use_type[base],attr_val)
		self.print_add("You ingest the " + item.name + " and increase your " + Item.use_type[base] + " by " + str(attr_increase) + "!")
		if self.inventory_dict[item.name]>1:
			self.inventory_dict[item.name] -= 1 # reduce number of items by 1
		else:
			del self.inventory_dict[item.name]
		if self.is_inbattle:
			self.get_attacked()

		# Activate item (applies item stats to player) if it exists in players inventory
		# deletes item after use
		pass
	def equip(self,equipment):
		# Replaces current equipment type in player.equipment_dict with chosen
		pass
	def grab(self,item):
		if isinstance(item,Item):
			item.in_inventory = True
			if item.name in list(self.inventory_dict.keys()):
				self.inventory_dict[item.name] += 1
			else:
				self.inventory_dict[item.name] = 1
			self.print_add("You place the " + item.name + " in your inventory.")
		else:
			self.print_add("You can't pick up " + item + ".")
		pass
	def get_attacked(self):
		p_gethit = 0.8*self.battle_opponent.speed / (self.battle_opponent.speed + self.speed)
		hploss_take = math.ceil(random.uniform(0.5,1)*self.battle_opponent.strength / self.defense)
		get_hit = random.choices([True,False],weights=[p_gethit,1.0-p_gethit])[0]
		if get_hit:
			self.print_add('You were hit by '+self.battle_opponent.name+'.')
			self.print_add("You've lost "+str(hploss_take)+' hp.')
			self.hp-=hploss_take
		else:
			self.print_add(self.battle_opponent.name+' missed you.')
		if self.hp<=0:
			return
	def update(self):
		self.create_description()
		if self.hp <= 0:
			self.is_alive = False
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
			if isinstance(x,Monster):
				description += 'a ' + x.name + ', '
			if isinstance(x,Item):
				description += 'a ' + x.name + '.'
			description += x.get_description()
		return description
	def update(self): # Updates all objects in environment
		for x in self.contents:
			x.update()
			if x.print_out.strip(): # Check if there is a printout from object
				self.print_out += x.print_out
			if isinstance(x,Item) or isinstance(x,Equipment): # Check if item or equipment has been picked up
				if x.in_inventory:
					self.contents.remove(x)
		pass
class Monster():
	base = {
	'Rat': [1,1,1,1],
	'Elf': [10,3,5,3],
	'Goblin':[5,3,3,3],
	'Orc': [20,5,3,4]
	}
	modifier = {
	'Regular':[0,0,0,0],
	'Dark': [-2,2,1,-1],
	'High': [1,-2,0,1],
	'Wood': [-2,-1,3,0],
	'Berserker': [0,0,2,-2],
	'Armored': [0,0,-2,2]
	}
	def __init__(self,args):
		# State Flags
		self.is_alive = True
		self.is_inbattle = True
		self.base = args[1]
		self.modifier = args[0]
		self.name = self.modifier + ' ' + self.base
		self.print_out = '' 
		self.create_stats()
		self.create_description()
	def create_stats(self):
		# TODO - Monster stats are based on 1.) arg[0] (base stats) 2.) arg[1] (modifiers - add or subtract) 3.) player.level (multipliers)
		# TODO - Add xp_give
		stats = [math.ceil(x) for x in (Monster.base[self.base] + Monster.modifier[self.modifier])]
		self.hp = stats[0]
		self.strength = stats[1]
		self.speed = stats[2]
		self.defense = stats[3]
		pass
	def create_description(self):
		# TODO
		pass
	def get_description(self):
		return "a big scary monster."# TODO - Change this
		pass
	def create_dialogue(self):
		# TODO
		pass
	def get_dialogue(self):
		# TODO
		pass
	def update(self):
		if self.hp <= 0:
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
			noun_list = ['devil','skank','inbred', 'tool','beggar']
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
			if self.name_known:
				return "it's " + self.adj1 + ", " + self.adj2 + " " + self.name
			else:
				return self.init_description
		else:
			return "While they once looked " + self.adj1 + " and " + self.adj2 + ", now you see a pile of organs, blood and meat. Perhaps some teeth."
	def create_dialogue(self): # If positive, also add probability for a tip (tells you what is to the north/east/west/south)
		if self.desc_type == 'good':
			start_list = ["\"Hi! ","\"Why, hello! ","\"Good Day! "]
			intro_list = ['My name is ', 'You can call me ']
			end_list1 = ["\"It's nice to meet you!\"", "\"Splended to make your aquaintance!\"", "\"Fantastic to meet you.\""]
			end_list2 = ["\"It's nice to see you again!\"", "\"Splended to see you again\"", "\"Fantastic to see you again.\""]
		elif self.desc_type == 'bad':
			start_list = ["\"wudaya want?\" *Spit* ","\"You keep staring and Imma hit ya.\" "]
			intro_list = ['\"You can call me ', "\"The name's "]
			end_list1 = ['\"Hope the back looks better than the front!\"',"\"Don't talk to me no more!\""]
			end_list2 = ['\"What!? Do you want some loose teeth?\"',"\"Thought I made myself clear, get the hell out of here!\""]
		start_dialogue = random.choice(start_list)
		intro_dialogue = random.choice(intro_list) +  self.true_name+'"'  +'. '
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
			self.name_known = True
			return self.create_dialogue()
		else:
			return '"..." The bloody corpse says nothing back.'
	def update(self):
		if self.hp == 0:
			self.is_alive = False
class Equipment():
	def __init__(self):
		pass
class Item(): # Food / Potions
	use_type = {
	'Potion':'hp',
	'Stimulant': 'speed',
	'Steroid': 'strength',
	'Painkiller': 'defense'
	}  # Fraction of amount to provide
	base_type = {
	'Potion': 1,
	'Stimulant': 0.5,
	'Steroid': 0.5,
	'Painkiller': 0.5
	}  # Fraction of amount to provide
	modifier_type = {
	'Regular': 1,
	'Potent': 2,
	'Mighty': 3
	}
	# potion (Temp Health), stimulant (Temp speed), steroid(Temp strength),
	def __init__(self,args):
		self.name_known = True
		self.is_alive = True
		self.in_inventory = False
		self.print_out = ''

		self.base = args[1]
		self.modifier = args[0]
		self.name = self.modifier + ' ' + self.base
		self.points = Item.base_type[self.base]*Item.modifier_type[self.modifier]
	def get_dialogue(self):
		return self.name + " says nothing back."
	def get_description(self):
		if self.base == 'Potion':
			adj = "permanently"
		else:
			adj = "temporarily"
		return " It " + adj + " gives you " + str(self.points) + ' ' + Item.use_type[self.base] + "." 
	def update(self):
		pass


	# All method will be taken care of with player.use() method

def main():
	world = World()
	# print(world.env.name)
	# print(world.env.contents[0].name) # Name of villager to attack
	# world.loop()



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
