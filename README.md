# DeepStar Documentation

# Current State:

https://youtu.be/ie4C534y8_4

# Overview

I made DeepStar with a friend/colleague/designer (a super cool dude named [Matt Fultz](http://www.herowithacomputer.com/)) of mine during our company's bi-annual "hack days" - a two day long event where employees could work on and produce whatever they wanted. Because I have an interest in game development and my everyday job involves using a lot of python, I decided to check out [Pygame](http://www.pygame.org/hifi.html), a python wrapper for SDL, and see what I could produce in two days with assets generously provided by Matt.

For 16 hours of work I think we did alright.

There are some (IMO) less than desirable OO design decisions that I have plans to fix. The first is the lack of a virtual controller - the player object solely relies on a class that requires the use of a ps3 controller. In addition I wish that I had taken a more compositional approach to the game objects, since I think the way I used inheritance in this case just obfuscates the reader as to how everything is actually working together.

Currently, Matt and I are working to expand upon this initial code project. While Pygame was a lot of fun I wouldn't recommend it for a more serious endeavor. It isn't the most optimized of frameworks and even with this simple game I think I observed some frames being dropped, although I guess that was to be expected, since my chief concern was getting the darn thing working.
