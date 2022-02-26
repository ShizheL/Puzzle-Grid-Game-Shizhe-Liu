# Puzzle-Grid-Game
A really cool game that I programmed using the pygame module.

Initially, the game starts with a 3x3 grid (consisting of 9 small squares). 

You are playing against the program and the program starts first.

You and the program take it in turns to select one of "short" lines on the grid.

The aim of the game is to be the first player to select the line that completes one of the squares on the 3x3 grid (i.e that all the lines around that square have been selected).

This is very similar to the game from the 2019 UKMT Hamilton Olympiad Question 6, but you can select any of the lines, that aren't already selected, you aren't playing against a human and the grid is much larger

However, just like Question 6, it has designed to be incredibly challenging (but not impossible), as my highly intelligent programs knows all the tricks (see generate_values and safe_check functions in the code).

If you do somehow win (unlikely but not impossible), the game starts again, but the grid size increases (4x4, 5x5, 6x6 ...). If not, you get to try again.

I will try to make a two player version in the future.

Have fun!
