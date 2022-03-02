import os

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import openpyxl

url = 'https://store.steampowered.com/search/?term=spiderman'


def get_data(url):
    r = requests.get(url)
    return r.text



def parse(data):
    result = [] # handling data

    soup = BeautifulSoup(data, 'html.parser')

    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    contents = soup.find('div', attrs={'id': 'search_resultsRows'})
    games = contents.find_all('a')

    for game in games:
        link = game['href'] # for redirect

        # parse the data
        title = game.find('span', {'class': 'title'}).text.strip().split('E')[0]
        price = game.find('div', {'class': 'search_price'}).text.strip().split('E')[0]

        released = game.find('div', {'class': 'search_released'}).text.strip().split('E')[0]
        if released == '':
            released = 'No Data'

        # sort
        data_dict = {
            'title' : title,
            'price' : price,
            'link' : link,
            'released' : released,
        }

        # appending
        result.append(data_dict)

    # write json
    with open('json_result.json', 'w') as outfile:
        json.dump(result, outfile)
    return result

def load_data():
    # read json
    with open('json_result.json') as json_file:
        data = json.load(json_file)
    print(data)

# clean data from the parser
def output(datas: list):
    for i in datas:
        print(i)

def generate_data(result, filename):
    df = pd.DataFrame(result)
    df.to_excel(f'{filename}.xlsx', index=False)

if __name__ == '__main__':
    data = get_data(url)
    final = parse(data)

# write to excel
    namefile = input('Input name for the file : ')
    generate_data(final, namefile)

    output(final)
    load_data()