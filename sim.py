#%% """ Northwoods League Baseball Simulator """
import pandas as pd
import sqlite3
from tqdm import tqdm
# from prob import prob_bat rn this is a circular import
# our own modules
#import livr # so we can update the model live during the season

class league():                                                   # the unclean one is all_smr
    def __init__(self, sqlite = True, dbase = "SMR.db", table = "all_smr_clean1", nwds_filter = True, game_log_csv = '', lg_name = ''):

        self.lg_name = lg_name

        conn = sqlite3.connect(dbase)
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

        if sqlite == False:
            df = pd.read_csv("/home/jensen/Documents/Projects/kzoo/" + table)
        elif sqlite != False and sqlite != True:
            print("Error: sqlite must equal true or false in data function.")
        self.data = df
        
        if nwds_filter == True:
            self.data = df[df["Lg_y"] == "NWDS"]

        # # game log data, need to clean this data up first
        # self.gl_bat_data = pd.read_csv()
        # self.gl_pit_data = pd.read_csv()


# only works for players with sidearm college stat pages for now
class Player():

    def __init__(self, name, position, stats, college_url, player_number, rp = False):
        positions = [None, ['RP', 'SP'], 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
        self.name = name
        self.pos = positions[position]
        #self.rc_range = prob_bat(name = self.name, college_url, player_number)

        # branch for pitchers only
        if position == 1 and rp == False:
            self.pos = positions[position][1]
        elif position == 1 and rp == True:
            self.pos = positions[position[0]]

class Team():

    def __init__(self, name):

        df = Data().data
        tm = df[df["Tm_y"] == name]
        hit = df[df["PA_y"] >= 1]
        pit = tm[tm["BF_y"] >= 1]

        cols = ["OPS", "SB", "SO", "BB", "HR"]
        self.stats_cols = []
        for metric in cols:
            for col in tm.columns:
                if metric in col:
                    self.stats_cols.append(metric)

        # idk if the list comprehension version of this loop works yet
        # self.stats_cols = [metric for metric in cols for cols in tm.columns if metric in col]

        self.name = name
        self.hitters = []
        self.pitchers = []

class Game():

    def __init__(self, home, away, home_pitcher, away_pitcher):
        self.home = home
        self.away = away
        self.innings = 9
        self.outs = 3
        self.home_pitcher = self.set_pitchers(self.home.pitchers[home_pitcher])
        self.away_pitcher = self.set_pitchers(self.away.pitchers[away_pitcher])
        self.home_lineup = self.auto_lineup(self.home.hitters)
        self.away_lineup = self.auto_lineup(self.away.hitters)

    def auto_lineup(self, list_of_all_hitters):
        positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
        roster = list_of_all_hitters
        lineup = []
        for pos in positions:
            # this will be lineup of 8 hitters
            lst = [hitter.rating for hitter in list_of_all_hitters if hitter.pos == pos]
            best = max([hitter.rating for hitter in list_of_all_hitters if hitter.pos == pos])
            lineup.append(best)
            roster.remove(best)
        lineup.sort()
        # add the DH as the best hitter that wasnt already added
        lineup += max([hitter.rating for hitter in list_of_all_hitters])
        return lineup

    def set_pitchers(self, pitcher):

        return

    def inning(self):
        outs = 0

        # if there are less than 3 outs...
        while outs > 3:

            # then do another plate appearance
            count = [0, 0]

            while count[0] < 4 and count[1] < 3:

                result = []


        return

    def summary(self):
        print(f'--- {self.home.name} vs. {self.away.name} ---\n')
        print(f"{self.home.name}'s Pitcher: {self.home_pitcher}")
        print(f"{self.away.name}'s Pitcher: {self.away_pitcher}\n")
        print(f"{self.home.name}'s Lineup: {self.home_lineup}")
        print(f"{self.away.name}'s Lineup: {self.away_lineup}\n")

    def play(self):
        self.summary()
        print("Play Ball!")
        return [self.inning() for i in range(self.innings)]
