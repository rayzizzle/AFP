# This documentation is to be a user’s manual for your project. Though the structure of your documentation is entirely up to you, it should be incredibly clear to the staff how and where, if applicable, to compile, configure, and use your project. Your documentation should be at least several paragraphs in length. It should not be necessary for us to contact you with questions regarding your project after its submission. Hold our hand with this documentation; be sure to answer in your documentation any questions that you think we might have while testing your work.

Welcome to our CS50 Final Project: Assassins.

This fall, a club we are in decided to play the game Assassins, a game that is played across high school campuses and colleges around the country. For those unfamiliar with the game, everyone who wants to play signs up. Then, everyone is randomly assigned a target. The goal is to "kill" your target and avoid being "killed". "Killing" methodology can vary by game, but a typical gameplay method is to "kill" via touching your target with a spoon. Once "killed", you are out of the game and your target becomes the new target of your killer. Everyone in our club wanted to play, but we struggled with how to assign every player a target without someone being in charge of the game and therefore unable to play. There exists no online platform for the game Assassins. We tried using Elfster, a Secret Santa platform, to anonymously assign targets so that everyone could play. However, Elfster created closed loops of several players. This was a problem because once those loops reached their end (aka one player "killed" everyone in their loop), then that player was left with no one else to kill. Thus, came the inspiration for our final project: a website that can facilitate the game Assasins without the need for someone to oversee the entire game and without the issue of closed loops. 

In the folder AFP (whic stands for A Final Project), open app.py. Once you do flask run, the website should appear in separate tab.

On the homepage, you will see an explanation of the game Assassins and the rules for gameplay. There will be a section to Log In or to Register. You can go ahead and register an account to experiment with the game.

Once logged in, more tabs will appear that include Create a Game, Join a Game, Your Games, Games You've Joined, and View Target. In the Create a Game tab, you have the option to... create a game. By creating a game, you become the admin for the game, but that just means you are in charge of sharing the keyword amongst the group you want to play and you are in charge of clicking the button to start the game. Once you set the keyword, you have to tell other players to use your keyword to sign up for your game. The admin who creates the game ALSO has to join the game.

This brings us to the Join a Game tab. In the Join a Game tab, you will see a display of all available games going on and who the admins are for each game. Then there is a section to input the keyword to join a game. The keyword has to match an existing keyword for you to actually be able to join a game. Once you enter the correct keyword (which you should have gotten from the admin) for the game you want to join, then you will have successfully joined the game.

Under the Your Games tab, you will see a display of all of the games you are the admin for. There is a Start Game button next to each game, which you will click once you want to start a game.

Under the Games You've Joined tab, you will see a display of the games you have joined. 

Under the View Target tab, it will be blank until the game has been started by the admin. Upon the start of the game, the View Target tab will display your target. Thus, the game begins and you can start spooning! Once you are killed, you tell your killer who their new target is, and there should never be closed loop problems because our algorithm ensures the randomized order is one enormous, continuous loop.

https://youtu.be/Qa7DCcc5wRI
Hope you enjoy!

Sincerely,
Aurelia Balkanski, Benjamin Jachim-Gallagher, and Ilija Wan-Simm# AFP
