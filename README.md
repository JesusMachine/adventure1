--- TODO ---

- when player.is_inbattle() -> player.inspect(), player.attack(), player.move() do not require a noun
	-player.inspect(self) only provides details about self and battle_opponent
	-player.move(self) only attempts to run (based on ratio of speed)
	- player.attack(self) means that the player attacked first (thus should try to hit first)
- Change order of player/battle_opponent attack depending on who initiates battle (in player.attack())
	- check if args in player.attack exists or not
	- if exists, player attacks first; if not, battle_opponent attacks first
- player.inspect()
	- for env and for objects
- class Items
	- potions to start
- player.inventory()
	- implement player.inventory_add
	- test self.inventory_print




--- FUTUREDEV ---

- stats are dependent on health
	- if hurt, speed and strength are less
	- defense is static and only depends on level and equipment
- player.equipment_dict 
	- keys = helm, torso, gauntlet, sword, etc
	- values = items of type
- class item.type()
	- potions, helms, torso, gauntlet, sword etc 
	- dictates where can be applied (or not if potion)
- Multiple hits per attack
	- player.attack() structure allows for player or opponent to hit multiple times (or none); make it so that if multiple speed ratio, attack multiple times.




--- BUGS ---

- entering unknown action for world.get_input() throws error and exits world.loop()
- world.get_input() isnt right with the action_flag




--- UPDATES ---
19.12.23.0
- villager dialogue
	- added quotations


19.12.21.0
- world.get_input()
	- added noun flag and separate while noun_flag
	- reorganized world.get_input() for one word or more input
		- Allows for single word input when in battle
	- added name_lists for move() and use()
- player.attack()
	- reorganized for if args used (whether continuing attack or starting)
	- removed attack_object
- player.talk()
	- changed print()'s to self.print_add()

Update 19.12.15.1
- Added player.inventory_dict, player.inventory_print()
- Provided method for player.attack() to provide no input (args)

Update 19.12.15.0
- Added timecounter to player
- Added object.print_out and env.print_out
- Added miss actions for player.attack()
- moved kill mechanics to player.attack() from world.get_input()
- created world.loop()
	- main loop for get_input and update()
- resolved attacking object.is_alive=False