from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import sqlite3
import sqlite3

""" Baseball Reference Crawler Class Object """

class bbref_register():

    def __init__(self):
        print(" --- baseball-ref-register scraper initialized ---")
        
    def sewp(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.text, features = 'lxml')

    def find_links(self, url):
        html = self.sewp(url)
        href_tags = html.find_all(href = True)
        return [tag['href'] for tag in href_tags]

    def tbl_data(self, url):
        return pd.read_html(url)[0]

    def player_info(self, url):
        soup = self.sewp(url)
        # Get text from tags where player info is
        spans = soup.find_all(['span','strong'])
        ps = soup.find_all('p')
        ps = [tag.text for tag in ps]
        spans = [tag.text for tag in spans]
        data = self.tbl_data(url)
        data['name'] = spans[7]
        data['height'] = ps[2][0:4].replace('-','.')
        data['weight(kg)'] = ps[2][-6:].replace(' ','').replace(')','').replace('kg','')
        data['bats'] = ps[1][6:12].replace('\\', '').replace(' ','')
        data['throws'] = ps[1][-12:].replace(':','').replace('\n','').replace(' ','')
        data['position'] = ps[0][-18:].replace(' ','').replace('\n', '').replace('n:','')
        return data

    def get_links(self, url, identifier):
        soup = self.sewp(url)
        new_def_url = 'https://baseball-reference.com'
        hrefs_tags = soup.find_all('a', href = True)
        return [(new_def_url + tag['href']) for tag in hrefs_tags if identifier in tag['href']]

    def get_plyr_hist(self, br_lg_id):
        new_def_url = 'https://baseball-reference.com'
        tm_links = self.get_links(new_def_url + br_lg_id, 'team.cgi?id=')
        print('Collecting Player links from team pages...')
        plyr_links = [self.get_links(team, '/player.fcgi?id=') for team in tqdm(tm_links)]
        print('Collecting player Data...')
        player_list = list(set([player for team in plyr_links for player in team]))
        return pd.concat([self.player_info(player) for player in tqdm(player_list)])

    def flip_my_data(self, list_of_parsed_league_data):
            mooshed_data_by_year = [pd.concat(year) for year in list_of_parsed_league_data]
            flat_list = []
            for year in mooshed_data_by_year:
                flat_list.append(year)
            self.all_data = pd.concat(flat_list)
            # Make numeric
            self.all_data = self.all_data.apply(pd.to_numeric, errors='coerce').combine_first(self.all_data)
            return self.flip(self.all_data)

        # sqlite function
        def move_to_sql(self, df, data_base_name, table_name):
            print(f" --- Moved Data To Local sqlite3 Database ({data_base_name}, {table_name}) ---")
            self.conn = sqlite3.connect(data_base_name + ".db")
            self.cur = self.conn.cursor()
            return df.to_sql(name = table_name, con = self.conn, if_exists = "replace")
