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
		self.player = Player('Fake')
		self.new_game()
	def create_world(self,m,n): # Populates world dict with mxn locations, each containing an environment
		world_map = {}
		for i in range(m):
			for j in range(n):
				world_map[(i,j)]=None
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
			self.get_input()
		if not start_game:
			player = Player('Jim')
		pass
	def get_input(self): # Basic Input System (Reader). Will eventually need while loop (which will check if player.alive)
		while self.player.alive:
			if self.player.is_inbattle:
				# TODO Battle options (attack or try to run)
				pass
			else:
				# TODO normal choices
				pass
			pass
	def update(self): # Updates all environments
		for values in self.map:
			values.update()
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
		input("\r")
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
		# State Flags
		self.is_alive = True
		self.is_inbattle = False
		#

		self.name = name
		self.location = [0,0]
		self.xp = 0.0
		self.level = 1
		self.stats = {
		'hp':10,
		'strength':1,
		'speed':1,
		'defense':1,
		}
	def level_up(self): # Runs at the end of each action
		lvl_start = self.level
		self.level = int(math.sqrt(xp))
		if self.level>lvl_start:
			self.stats['hp'] += 3
			for key in ['strength','speed','defense']:
				self.stats[key] += random.randint(0,2)
	def create_description(self):
		# TODO description will be based on current hp out of max hp for level
		self.description = None
	def update(self):
		create_description()
		#TODO
		pass
class Environment(): # Local Container -- Contains all Monsters, Villagers, Items except Player (contained in world)
	# env_stuff = {
	# 'forest': {'description':['lush','green'],'things':['Monster','Item','Villager']},
	# 'village':{'description':['small','peaceful'],'things':['Villager','Item']},
	# 'desert':{'description':['dry','hot'],'things':['Monster','Item']}
	# }
	def __init__(self,env_type):
		self.name = env_type
		self.contents = list()
		self.create_description()
		self.env_description = self.get_description()
	def create_description(self): # Creates Unique Description
		if self.name == 'forest':
			desc_list1 = ['lush,', 'quiet,', 'peaceful,', 'solumn,', 'eerie,', 'cold,', 'bright,', 'dark,', 'thick,', 'haunted,', 'creepy,']
			desc_list2 = ['green', 'dead', 'burned', 'bare','mountainous']
		elif self.name == 'village': # TODO
			desc_list1 = []
			desc_list2 = []
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
		pass
class Monster():
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
		# stat_list = [round(x) for x in (player.level/4)*(base[arg[0]] + modifier[arg[1]])]
		pass
	def create_description(self):
		# TODO
		pass
	def update(self):
		if self.stats['hp'] ==0:
			self.is_alive == False
class Villager():
	names = {
	'm':['Jim', 'Ted', 'Bob','Tom'],
	'f':['Jill','Tammy', 'June','Beth']
	}
	def __init__(self,args):
		self.name = args[0]
		self.gender = args[1]
		self.stats = {'hp':1,'speed':1,'defense':1}
		self.is_alive = True
		self.create_description()
		self.create_dialogue()
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
			desc_type = random.choice([1,2])
			if desc_type == 1:
				verb_list = ['looks', 'smells', 'stinks']			
				adj_list1 = ['nasty','angry','scary']
				adj_list2 = ['dirty','filthy','scabbies-ridden','toothless','old','cold']
				noun_list = ['devil','skank','whore', 'tool','beggar']
			elif desc_type == 2:
				verb_list = ['looks','sounds']
				adj_list1 = ['kind','beautiful','friendly','intelligent','young','old']
				adj_list2 = ['warm','observant','upright','modest','vibrant','hard-working']
				noun_list = ['angel','saint','citizen','scholar','professional']
			verb = random.choice(verb_list)
			adj1 = random.choice(adj_list1)
			adj2 = random.choice(adj_list2)
			noun = random.choice(noun_list)
			if re.match(r'[aeiou]',adj1[0]):
				prefix = 'an'
			else:
				prefix = 'a'
			self.description = pronoun + ' ' + verb + ' like' + ' ' + prefix + ' ' + adj1 + ', ' + adj2 + ' ' + noun
		else:
			pass # TODO make description of blood or messed up corpse
	def create_dialogue(self): # If positive, also add probability for a tip (tells you what is to the north/east/west/south)
		intro_list = ["Hi! I'm "]
		outro_list = ["It's nice to meet you!"]
		introduction = random.choice(intro_list)
		outro = '. ' + random.choice(outro_list)
		self.dialogue = introduction + self.name + outro
		pass
	def update(self):
		if self.stats['hp'] == 0:
			self.is_alive = False
class Item():
	pass

def main():
	world = World()
	for i in range(10):
		world.thing_gen((0,0),Villager)
	# world.update()
	print(world.env.get_description())



if __name__ == '__main__':
	main()
	pass



## EXAMPLES LISTS ##
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