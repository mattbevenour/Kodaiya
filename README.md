# Kodaiya
Welcome to my pet project!

These notebooks attempt to simulate a series of pick-up games of ice hockey from a consistent pool of players of varying skills. We do this by randomly assigning teams each game and randomly determining how many goals individual players contribute to their team's score (or more accurately, how each player's performance contributes to a score delta each game). In this simplified approach, players are stratified into 4 categories (which can be customized in the config.yaml file) with each player signified by their skill category and an index.

Score ranges per player rating-

A Players (3 players- a1, a2, a3): contribute [1,2] goals a game

B Players (3 players- b1, b2, b3): contribute [0,1] goals a game

C Players (2 players- c1, c2): contribute [-1,1] goals a game

D Players (2 players- d1, d2): contribute [-2,0] goals a game


The features of the model will be which players are present on which team each game, and then the label will be a boolean 'Did team 1 win this game?'. Ties will be labeled as a non-win for team 1 and 

For this proof of concept, we make a few assumptions and simplifications:
1) Each player is either on team 1 or team 0. That is to say a player is never absent and the rosters for any given game are mutually exclusive and collectively exhaustive for the player base. In reality, players have varying records of attendance. Further improvements would take a larger player list and construct features indicating which team and whom is present that game, but our imagined approach to that expansion greatly increases the number of features necessary and introduces nulls into the attendance dataset. While perfectly possible to implement, our first pass at the data will avoid answering those questions
2) Player performances are somewhat consistent and encoded in possible score ranges. This is so we already 'know' that A players should be good predictors of their team winning and D players indicative of their team losing. In reality, players of great differences of skill are segregated by line such that A+B players are rarely on the ice the same time as C+D players so that the games are fair and everyone has a chance to perform positively. We won't worry about attempting to match lines and instead proceed as if the possible goal range is sufficent to encode such. A small change would be to estimate a players impact against others of their skill tier by adjusting the possible score range that player provides
3) Only 10 players total in the player base. This could easily be expanded without violating simplification assumption 1 of 'everyone is always in attendance', but a smaller player base should allow individual players to impact the outcome of the game more visibily for the proof of concept
4) Goaltenders effectively do not exist. In our pickup games, we play 4 periods and the goaltenders swap sides each period to account for potential differences in goalie skill. Each players' goal range is intended to be agnostic of goaltenders and to be taken as a typical performance in aggregate.
5) Player position is handwaved to be incorporated into score ranges. In actuality, players excel at many different things, some offensively and some defensively. Changes could be made to have more defensively impactful players contribute negatively to the opposing team's score, but that effectively is identical to increasing your own team's score by a similar amount. Thus a score range for each player is effectively a score delta
6) Players play 100 games. This is a much larger set of games than you would see over the course of a typical 'season' for pickup leagues like this, although my rink's league has enjoyed a very consistent set of players from year to year for the past decade as it is a collection of friends and friends of friends. A larger sample of games could be considered but with only 10 players in the player base, I did not want too many repeat rosters affecting the model. A typical seasonal pickup league has 1 game a week for half the year, we are essentially quadrupuling the number of games a real world dataset would have access to without spanning multiple years. 100 rows is extremely small for Machine Learning datasets but large for the use case.
7) Due to difference in player score range performance, identical rosters playing multiple games -may- result in a different team winning, particularly if the team split is well balanced. This is very reflective of real life and our model will have to accept that.

Future applications of the model would be expanding it to a real roster and real team lineups for a full 24 week season and seeing if the reduced dataset size, increased player count per team, increased player base, and inconsistant attendance would so greatly reduce model performance as to make it a non-viable exercise.
