# ai-mafia-party-game
LLM integrated mafia party game where you can play against AI
Use your api key to integrate with your own AI. 

Roles currently supported: Mafia, Town, Detective and Doctor

# Features
* Chat relay between multiple AI
* Player interaction with the chat
* Voting system
* Private chat rooms for mafia members

# Features planned
* muting players or AI that are breaking the chat system

# How it works
Randomly, a player is selected to speak. The conversation history is sent to the player/AI. They can add to the discussion.
There are commands that players can use to interact with the game mechanics

# Commands
!speak <name> tries to force the player or AI to speak by forcing the game to choose that player to speak next
!vote <name> allows players to vote on who they don't trust or who they want to kill

# Architecture

