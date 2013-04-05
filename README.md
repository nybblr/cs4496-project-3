Breakdown
=========

Physics game for CS 4496, project 3 at Georgia Institute of Technology. By Jonathan Martin and Kurtis Eveleigh. [Checkout the homepage](http://nybblr.github.com/cs4496-project-3)

**Breakdown** is a remake of the classic breakout games popular since the advent of PDA mobile games. The game features realtime physics gameplay (thanks to Box2D), various powerups (like inertial warp), and easy level creation from PNG sprites.

The goal of the game is to breakdown the sprite till the screen is empty --- but you'll get more points for doing that in style. Some of the blocks are locked, but banging them a few times will loosen them up. Completely obliterate blocks before they leave the screen, and you'll get a 5 point bonus. Race against the clock and get 20 points in 2 seconds to get an inertial warp, which renders your ball oblivious to bounce interactions with puny pixel blocks.

The game is simple to play: use the left and right arrow keys to move the paddle, and tilt the paddle with "s" and "d". Hitting "c" at the same time activates extreme tilt.

Installation
============
Breakdown needs a few dependencies:
- Python (developed in 2.7.3)
- SWIG (latest)
- PyGame (latest) and dependencies (not limited to):
  - sdl, sdl_mixer, sdl_ttf, sdl_image (all installable through brew)
  - QT for graphics
- PyBox2D 2.02b2

It is recommended that you install in that order. Here's a cheatsheet for quick install:
- Install swig with `pip install swig`
- Install the **latest** pygame with `pip install hg+http://bitbucket.org/pygame/pygame`
- Install the 2.02b2 release of pybox2d with `pip install http://pybox2d.googlecode.com/files/pybox2d-2.0.2b2.zip`

**NOTE:** pip doesn't seem to properly install pybox2d, so you may get an error like "Could not find b2ContactListener" when you try to run the main game.py. In that case, manual install it:

    wget http://pybox2d.googlecode.com/files/pybox2d-2.0.2b2.zip
    unzip pybox2d-2.0.2b2.zip
    cd Box2D # whatever is the name of the unzipped source
    python setup.py build
    python setup.py install

Playing
=======
Clone the source, cd into the directory and run `python game.py`. Have fun!
