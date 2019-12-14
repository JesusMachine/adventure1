Major changes to implement:
-- Create dialogue.py module to import dialogue
-- Change all battle system to use is_inbattle flag
	- Use update to update all flags per turn, if is_inbattle
	- Use update to update all flags of player and battle_opponent, if not is_inbattle
		- This will allow for check of alive flag for player and battle_opponent