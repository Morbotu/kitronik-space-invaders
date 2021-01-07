# kitronik-space-invaders

This repo contains a project I needed to make for school. I is space invaders for on the [micro:bit](https://microbit.org/) with a [:GAME ZIP 64](https://kitronik.co.uk/products/5626-game-zip-64-for-the-bbc-microbit) attached.

![space invader gif](images/space-invaders.gif)

## Content

The program is in the [kitronik-space-invaders.py](kitronik-space-invaders.py) file. The minified it in [kitronik-space-invaders.min.py](kitronik-space-invaders.min.py). There is also a hex build ready in [kitronik-space-invaders.hex](kitronik-space-invaders.hex).

## How does it work

This project was quite difficult because the [micro:bit](https://microbit.org/) hasn't got much memory. A made the program as small as possible. I was first planning to use classes but those take up a lot of space in memory. This wasn't a problem for the player, since there was only one. The player properties are a x and y position and lives. The y position was constant so I could leave that out. However, the enemies where in larger numbers. I put the enemies in a matrix with the values being the lives of the enemies.
