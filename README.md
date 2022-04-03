# Northwoods League Baseball Project

End goal: Build a model to predict performance in the Northwoods League

Why: Because I want to analyze baseball data outside of the MLB

How: I used a number of python libraries, including beautifulsoup, pandas, sqlite3,
tqdm, matplotlib, seaborn, and sklearn

## Collecting Data:

I built my own webscraper to collect this data mainly using beautifulsoup and pandas. It collects individual player data, returning me a nested list
of dataframes, each nested list being one year scraped, and each item in the list being a player's colligate and Northwoods League stats. 
The scraper starts at https://baseball-reference.com/register/, identifies the league I specify, collects the year links, then collects the
team links from each of those years. From there it gets the player links from each of those team links, and once it has all of the player links,
it then collects the players first table (contains either pitching or hitting statsdepending on what they do more often). This scraper also works for 
any league other than the MLB as listed in the baseball reference league encyclopedia. I also made one with selenium, but it is far 
less efficient and may overheat your computer unless you specify your webdriver to be headless. 

## Cleaning data:

This data alone is not very useful, so what I set out to do is morph the data in a way that is easier to interpret. After doing this 
and merging everything into one giant dataframe, I moved it into a local sqlite3.db file so that I can easily access the data from a relational database.
each row in the data has a players college stats, and a players northwoods stats for that upcoming season. This makes it easier to make data visualizations
and build the model, since that is what I would like to base it off of. 

## Modeling
(Currently working on this part)
During my intial exploration of the scraped data, I was unable to fit a multiple or simple linear regression model that could accuratley predict virtually any summer
league statistic based on colligate statistics. The model that has had the best fit with a 80% - 20% train test split has been a decision tree regressor, which I have
decided to roll with as my final model since it is able to fit the testing data with a considerably lower mean squared error compared to that of the other model types.

The next step in the modeling process is to estimate how many runs a player will score based on their projected total bases. In other words, I calculated the run value of total bases in the Northwoods League from 2014-2019. I did not want to include years earlier than 2014 simply because I feel that 5 years of data was sufficient, and the run environments change a lot year to year so I wanted as much data that I collect to be as recent as possible. 

## Conclusions

