# **TODO**

<!-- - when player.is_inbattle() -> player.inspect(), player.attack(), player.move() do not require a noun
	-player.inspect(self) only provides details about self and battle_opponent
	-player.move(self) only attempts to run (based on ratio of speed)
	- player.attack(self) means that the player attacked first (thus should try to hit first)
- Change order of player/battle_opponent attack depending on who initiates battle (in player.attack())
	- check if args in player.attack exists or not
	- if exists, player attacks first; if not, battle_opponent attacks first -->
<!-- - player.inspect()
	- for env and for objects -->
<!-- * player.move(args)
  * args if not in battle -->
<!-- * class Items
  * base and modifiers -->
<!-- * world.thing_gen()
  * add items for generation -->
<!-- * make inspect is_inbattle provide:
  * player.hp, or description based on hp
  * battle_opponent.hp, or description based on hp -->
<!-- * player.grab()
  * removes item from environment
  * adds key with item name to -->
<!--  player.inventory_dict
  * adds 1 to value for item key in player.inventory_dict
* player.inventory_dict
  * test self.inventory_print -->
* class equipment
  * weapons and armour
*  world.get_input
<!--   *  add grab -->
  *  add player.equip
<!--   *  other player methods missing? -->
* add self.xp give to
  *  monsters
  *  villagers (small amount still based on relative level)
<!-- * add modifier.types for items -->

# FUTUREDEV
* Make all items besides potions temporary
  * only last x delta_t
* Create method so that player can see where they are in map
  * player.map
* Change equipment to provide multiple stats
  * Swords would provide more speed but maces would provide more strength
* Add equipment and item weights
  * adds to player.weight
  * player.speed is based on player.weight
* Create plot
  * need preset characters, environments
  * Create bosses Class
  * Key items Class which allow progress of storyline
* Rewrite world.get_input
  * Cases are a mess
* Item gen is based on weights
  * both base and mod are weighted
  * regular and potion most prevalent
* stats are dependent on health
  *  if hurt, speed and strength are less
  * defense is static and only depends on level and equipment
* player.equipment_dict 
  * keys = helm, torso, gauntlet, sword, etc
  *  values = items of type
* class item.type()
  * perminent (adds to player stats)
  * temporary (active for # of moves)
* Multiple hits per attack
  * player.attack() structure allows for player or opponent to hit multiple times (or none); make it so that if multiple speed ratio, attack multiple times.
* Split different sections into different modules
  * too confusing and scattered in total

# BUGS
* Certain villager.desc_type = bad do not provide villager name
  * yet name_known = True
* world.get_input()
  * if noun is more than one word and not in name_list, system prints as one word, concatinated
* all cases where .split() results in noun being concatinated without spaces
* Attacking pattern is not consistent (if you initiate, you do not always hit first)
* cannot interact with multiple objects with same name (see line 142 for possible solution)
  * see "TODO this could be used for multiple of same name noun_flag = False"

# UPDATES
* 20.01.19.0
  * Added equipment class
  * Added but did not check player.equip
  * 
* 20.01.12.0
  * Fixed using items in battle bug
  * Deleted action "grab" if is_inbattle
  * Fully implemented player.inspect for battle
    * Displays players stats and enemy stats
    * No noun necessary when in battle
* 20.01.09.0
  * Added and tested player.grab()
  * Finshed implementing use and tested
    * All item properties are administered by player.use
* 20.01.07.0
  * Added player.move() for battle
    * Tested
  * Added Item class
  * Partially implemented player.use()
    * did not check with item. Test noun works.
  * Added player.get_attacked()
  	* If player is in battle and does something besides attack, they will still get attacked
* 19.12.27.2
  * added monster attack mechanism
* 19.12.27.1
  * started item class implementation
  * added but did not implement player.use, player.grab, player.equip
  * added player.location
  * implemented player.move() for on-battle case
* 19.12.27.0
  * stuff
* 19.12.23.0
  * villager dialogue
    * added quotations
* 19.12.21.0
  * world.get_input()
    *  added noun flag and separate while noun_flag
    * reorganized world.get_input() for one word or more input
      * Allows for single word input when in battle
    * added name_lists for move() and use()
  * player.attack()
    * reorganized for if args used (whether continuing attack or starting)
    * removed attack_object
  * player.talk()
    * changed print()'s to self.print_add()
* 19.12.15.1
  * Added player.inventory_dict, player.inventory_print()
  * Provided method for player.attack() to provide no input (args)
*  19.12.15.0
  * Added timecounter to player
  * Added object.print_out and env.print_out
  * Added miss actions for player.attack()
  * moved kill mechanics to player.attack() from world.get_input()
  * created world.loop()
     *  main loop for get_input and update()
  * resolved attacking object.is_alive=False