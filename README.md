## Baseball Predictive modeling & Simulation Analysis

Main goal: project a range of numbers for each player in the Northwoods League and simulate
games between teams with said projected ranges. Hopefully will be able to find ideal lineups,
pitching matchups, etc...

## Collecting Data

the file titled BBREF_scraper.py is the code that I wrote to scrape data off of baseball reference.
Once I finished it I would run it in my terminal for ease of use, it allowed me to browse Baseball
Reference, find a league I want to get player data from, run the BBREF_scraper.py file and paste the 
encyclopedia URL for the league as well as what I want the csv file to be called and wallah, it gives 
me the whole Baseball Reference history of each player that has ever played in said league along with 
their name.

## Modeling

Once I had all of that messy data, I filtered out the massive dataframe so that I was left with just the
players colllege statistics, and their summer statistics. 

To start, I modeled hitters based on their college stats from the same year prior using a Tensorflow neural
network. This process was fun to learn, however did not provide me with results I could use in production.
Instead, what worked much better was a random forest regressor. That being said, a 40 R^2 number is not ideal.
But when predicting baseball, I'll take it. To improve the model I instead had the model predict a range of 
numbers for each response variable (I say response variable for now because I may add metrics) instead of one
solid number. Using one standard deviation of the actual values allows for 74% of the players actual numbers
to fall within the small predicted range of values for each category combined. The average miss was off by about
14 units which is likley to the model being somewhat poor at predicting plate appearances in the NWL with a mean
absolute error aroung 20, while the rest of the response variables not topping 8 mean absolute error.

When it comes to modeling pitchers, the Northwoods League is very unpredictable in that pitchers have pitch limits
by their coaches, come and go often and do not stay as long as the hitters per say. The model right now for pitchers is
under construction, as the current r^2 is under 30. I would like to get that number a lot closer to the hitter one
before I go ahead and use this model in production. My other thought is if I cannot get the model where I want it,
it would be useful to scrape the game logs for the NWL live as the season goes on and keep track of probabilites for
each pitcher, which would allow me to incorperate detialed at bat results in the simulator.

## Simulation



## Conclusion

Did I meet the main goal I gave myself at the beginning of this page?
