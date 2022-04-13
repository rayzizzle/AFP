# A “design document” for your project in the form of a Markdown file called DESIGN.md that discusses, technically, how you implemented your project and why you made the design decisions you did. Your design document should be at least several paragraphs in length. Whereas your documentation is meant to be a user’s manual, consider your design document your opportunity to give the staff a technical tour of your project underneath its hood.

Let's take a look underneath the hood of our CS50 Final Project and explain to you the decisions we made on the backend.

We utilized SQL, HTML, and CSS to create our website. 

# Login/Register Methodology:

Using analogous metholodology from the Finance problem set, we created register and login features that allow someone to create an account and then log in. Before you log in, all you see displayed are the Rules of Play homepage. Only after you log in do you see the different tabs regarding creating and joining assassins games.

# Create a Game Methodology:

For creating a game, we decided that any user (once logged in) can start an assassins game. This means that they can assign a Game Name and a Keyword for a Game, and they will become the admin. These values are all imported into a table. 

# Join a  Game Methodology:

For joining a game, the user has to input the keyword that was (hopefully) given to them by the admin. On this page they can see all of the available games in a table that displays Game Name and Admin Name. If they put in a correct keyword, they successfully join that game. If not, the get an error.

# Your Games Methodology:

Under the Your Games tab, we implemented SQL and Python to display a table of all of the games a player has created and is the admin for. On this tab, the admin has the option to hit the Start Game button. The Start Game button then triggers our algorithm that runs the game. Using SQL, we create 

# Games You've Joined Methodology:

Under the Games You've Joined tab, we display all of the games a player has joined and is playing in. 

# View Target Methodology:

We first check to see if the target column is empty. If it is empty, the webpage displays that the game has not started yet. If the target column has an entry, then using SQL, we pull the target from the table and display "Your target is _______".
