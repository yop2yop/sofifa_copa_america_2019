# Import Iniciales
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
%matplotlib inline

import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

# Equipos internacionales participes de Copa America 2019
Copa_America={"Argentina":["https://sofifa.com/team/1369/argentina/"],"Bolivia":["https://sofifa.com/team/111451/bolivia/"],"Brazil":["https://sofifa.com/team/1370/brazil/"],"Chile":["https://sofifa.com/team/111459/chile/"],"Colombia":["https://sofifa.com/team/111109/colombia/"],"Ecuador":["https://sofifa.com/team/111465/ecuador/"],"Paraguay":["https://sofifa.com/team/1375/paraguay/"],"Peru":["https://sofifa.com/team/111108/peru/"],"Uruguay":["https://sofifa.com/team/1377/uruguay/"],"Venezuela":["https://sofifa.com/team/111487/venezuela/"]}
# Se agrega el tiempo de contrato y posición en que juegan.
# Pero el resto son las mismas variables de la información básica
columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'posicion',
           'contrato', 'Value', 'Wage', 'Special']
data = DataFrame(columns=columns)

for i in Copa_America:
    url=Copa_America[i][0]
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    table_body = soup.find('tbody')
    for j,row in enumerate(table_body.findAll('tr')):
        td = row.findAll('td')
        picture = td[0].find('img').get('data-src')
        pid = td[0].find('img').get('id')
        nationality = td[1].find('a').get('title')
        flag_img = td[1].find('img').get('data-src')
        name = td[1].findAll('a')[1].text
        age = int(td[2].text.strip())
        overall = int(td[3].text.strip())
        potential = int(td[4].text.strip())
        posicion = td[5].find("span").text.strip()
        contrato = td[5].find("div").text[-11:]
        value = td[7].text.strip()
        wage = td[7].text.strip()
        special = int(td[10].text.strip())
        player_data = DataFrame([[pid, name, age, picture, nationality, flag_img, overall,
                                      potential, posicion, contrato, value, wage, special]])
        player_data.columns = columns
        data = data.append(player_data, ignore_index=True)

data = data.drop_duplicates()
data.to_csv('Copa_america.csv', encoding='utf-8')
