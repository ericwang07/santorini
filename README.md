# Santorini
A CLI simulation of the santorini board game. Find the link to the board game instructions [here](http://files.roxley.com/Santorini-Rulebook-Web-2016.08.14.pdf). This will only include the simplest version of the game (only read page 1 of the instruction manual).

## Instructions
Type ```python3 main.py [white_type] [blue_type] [undo/redo] [score_display]``` to run the game. The options for the optional arguments are as follows:

1. ```[white_type]```: The player type of the white player. Options include ```human```, ```random```, or ```heuristic```. Default is ```human```.
2. ```[blue_type]```: The player type of the white player. Options include ```human```, ```random```, or ```heuristic```. Default is ```human```.
3. ```[undo/redo]```: Enable or disable undo/redo functionality for human game mode. Options include ```on``` or ```off```. Default is ```off```.
4. ```[score_display]```:  Enable or disable the displaying of various scores in an ordered list that quantify advantages in the game. Options include ```on``` or ```off```. Default is ```off```. In order, the values in the score tuple represent the ```height_score``` (the sum of heights of the buildings a player's workers stand on), ```center_score``` (for each piece: 2 points for center position, 1 point for a position in the ring surrounding the center, and 0 points for the edge spaces), and ```distance_score``` (sum of the minimum distance to the opponent's workers). All scores are combined in a weighted combination called the ```move_score``` where ```move_score = c1*height_score + c2*center_score + c3*distance_score```. The ```move_score``` is used as a metric to quantify the quality of move and is used for the semi-AI heuristic player to judge and make the next-best move.
