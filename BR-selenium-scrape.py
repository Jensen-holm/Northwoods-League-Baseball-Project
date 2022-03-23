#%% """ Selenium version of the Baseball Reference Crawler """

""" This scraper takes a much longer time to run get_league_hist than the beautiful soup scraper, you will also have to download a webdriver.
But you will get to watch selenium do it's magic. I would only reccommend running get_league_hist on a small league """

""" Libraries """
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

#%% """" Scrape Baseball Reference class """"

class scrape_br():

    def __init__(self):
        ser = Service("/Users/jense/Downloads/Chromedriver.exe")
        op = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=ser, options=op)

    def get_league_hist(self, lg_href):
        self.lg_home = self.driver.get(lg_href)
        table = self.driver.find_element(By.ID, "div_lg_history")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        tr_list = tbody.find_elements(By.TAG_NAME, 'tr')
        tags = []
        for row in tr_list:
            tags.append(row.find_element(By.TAG_NAME, "a"))
        yr_list = []
        for link in tags:
            yr_list.append(link.get_attribute("href"))
        yr_list = [str(i) for i in yr_list]
        tm_list = []
        for yr in yr_list:
            self.driver.get(yr)
            tm_list.append(self.find_tm_links())
        for i,yr in enumerate(tm_list):
            for j, team in enumerate(yr):
                tm_list[i][j] = team.split(',')
        self.plyr_list = []
        for tm in tqdm(tm_list):
            for player in tqdm(tm):
                for player_link in player:
                    self.driver.get(player_link)
                    self.plyr_list.append(self.find_plyr_links_bat())
                    self.plyr_list.append(self.find_plyr_links_pit())
        print(len(self.plyr_list))
        for i in self.plyr_list:
            print(len(i))

        plyr_data = []
        for team in tqdm(plyr_list):
            for player in tqdm(team):
                self.driver.get(player)
                try:
                   plyr_data.append(self.find_bat_tables())
                except:
                    plyr_data.append(self.find_pitch_tables())
            return plyr_data

    def find_tm_links(self):
        for i in range(1):
            try:
                table = self.driver.find_element(By.ID, "div_standings_pitching")
            except:
                table = self.driver.find_element(By.ID, "regular_season")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        tr_list = tbody.find_elements(By.TAG_NAME, 'tr')
        tags = []
        for row in tr_list:
            try:
                tags.append(row.find_elements(By.TAG_NAME, "a"))
            except:
                print("find_tm_links error, could not get a tags from the tr's")
        tm_list = []
        for link in tags:
            for i in link:
                try:
                    tm_list.append(i.get_attribute("href"))
                except:
                    print("error getting a-ref attribute from find_tm_links")
        return tm_list

    def find_plyr_links_bat(self):
        table = self.driver.find_element(By.ID, "team_batting")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        tr_list = tbody.find_elements(By.TAG_NAME, 'tr')
        a_tags = []
        for row in tr_list:
            try:
             a_tags.append(row.find_elements(By.TAG_NAME, "a"))
            except:
                print("Could not get player links in find_plyr_links_bat")
        player_hrefs = []
        for nested_tag in a_tags:
            for tag in nested_tag:
                try:
                    player_hrefs.append(tag.get_attribute("href"))
                except:
                    print("could not successfully implement find_plyr_links_bat")
        return player_hrefs

    def find_plyr_links_pit(self):
        table = self.driver.find_element(By.ID, "team_pitching")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        tr_list = tbody.find_elements(By.TAG_NAME, 'tr')
        a_tags = []
        for row in tr_list:
            try:
             a_tags.append(row.find_elements(By.TAG_NAME, "a"))
            except:
                print("Could not get player links in find_plyr_links_bat")
        player_hrefs = []
        for nested_tag in a_tags:
            for tag in nested_tag:
                try:
                    player_hrefs.append(tag.get_attribute("href"))
                except:
                    print("could not successfully implement find_plyr_links_bat")
        return player_hrefs

    def find_bat_tables(self):
        x = self.bat_txt = self.driver.find_element(By.ID, "div_standard_batting")
        y = x.get_attribute("innerHTML")
        z = pd.read_html(y)
        return z[0]

    def find_pitch_tables(self):
        x = self.bat_txt = self.driver.find_element(By.ID, "div_standard_pitching")
        y = x.get_attribute("innerHTML")
        z = pd.read_html(y)
        return z[0]

#%% test 
lg = scrape_br()
nwds_hist = lg.get_league_hist("https://www.baseball-reference.com/register/league.cgi?code=NWDS&class=Smr")
