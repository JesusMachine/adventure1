--- TODO ---

- player.inspect()
	- for env and for objects
- Change order of player/battle_opponent attack depending on who initiates battle (in player.attack())
	- could create new flag for attack_first

--- BUGS ---

- entering unknown action for world.get_input() throws error
- 


--- UPDATES ---

Update 19.12.15.0
- Added timecounter to player
- Added object.print_out and env.print_out
- Added miss actions for player.attack()
- moved kill mechanics to player.attack() from world.get_input()
- created world.loop()
	- main loop for get_input and update()
- resolved attacking object.is_alive=False

