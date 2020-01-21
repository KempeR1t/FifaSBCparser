#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import csv
import random
import os
import telebot
from discord_webhook import DiscordWebhook
import threading
from threading import Thread
import itertools



webhook = DiscordWebhook(url='xx',
                         username="СВЕЖАЯ ВЫГРУЗКА ТОП ИГРОКОВ В СБЧ")

TOKEN = 'xx'

'''
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
'''

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

players_dict = {}

player_att_dict = {}

banned_id = ['3','4','5','6','7','8','29','30']

groups = []

links = []


def get_html(url):
    user_agent = random.choice(user_agent_list)
    # Set the headers
    headers = {'User-Agent': user_agent}
    r = requests.get(url, headers=headers, timeout=5)
    if r.status_code == 200:
        return r

    if r.status_code == 404:
        print('Страница не существует!')

def get_all_sbc(html):
    while True:
        try:
            soup = BeautifulSoup(html, 'lxml')
            sbcs = soup.find('div', class_='row col-12 d-flex')
        except Exception:
            print('пытаемся повторить get_all_sbc')
            continue
        else:
            break
    return sbcs


def collect_sbc_id(sbcs):
    sbc_id = []
    while True:
        try:
            sbcs2 = sbcs.findAll('div', class_='col-md-3 col-xs-6 set_col d-none mb-5')
        except Exception:
            print('пытаемся повторить collect_sbc_id')
            continue
        else:
            break
    for sbc in sbcs2:
        text = sbc.find('div', class_='set_desc').text
        if not 'Icon Swaps' in text:
            id = convert_id(sbc.find('a').get('href'))
            if not id in banned_id:
                sbc_id.append(id)
    return sbc_id

def convert_id(text):
    id = re.search(r'\d+',text)
    return id.group(0)

def collect_challenge_list(sbc_id):
    for sbc in sbc_id:
        while True:
            try:
                soup = BeautifulSoup(get_html(f'https://www.futbin.com/squad-building-challenges/ALL/{sbc}').text, 'lxml')
                time.sleep(1)
                challenge_groups = soup.findAll('div', class_='btn_holder')
            except Exception:
                print('пытаемся повторить collect_challenge_list')
                continue
            else:
                break
        for group in challenge_groups:
            groups.append(group.find('a').get('href'))
    return True

def collect_finish_sbc_list(groups):
    length = len(groups)
    for group in groups:
        while True:
            length -= 1
            print(f'{group} осталось {length}')
            try:
                soup = BeautifulSoup(get_html(f'https://www.futbin.com{group}').text, 'lxml')
                tds = soup.findAll('a', class_='squad_url')
            except Exception:
                print('пытаемся повторить collect_finish_sbc_list')
                continue
            else:
                break
        for td in tds:
            links.append(td.get('href'))
    return True

def collect_players(start_links_index, end_links_index):
    length = len(links[start_links_index:end_links_index])
    for link in links[start_links_index:end_links_index]:
        length -= 1
        #print(f'{link}, {threading.current_thread().name} осталось {length}')
        players = get_player_list(link)
        for player in players:
            try:
                if not players_dict.get(player):
                    players_dict[player] = 1
                else:
                    players_dict[player] = players_dict[player] + 1
            except TypeError:
                print(f'пропуск добавления игрока в словарь {player}')
                pass
    #max_player_index = sorted(list(players_dict.values()))[-200]
    #write_to_csv(max_player_index)
    return True


def get_player_list(link):
    while True:
        try:
            soup = BeautifulSoup(get_html(f'https://www.futbin.com{link}').text, 'lxml')
            divs = soup.find('div', id='area').findAll('div', class_='cardetails')
        except Exception:  # Replace Exception with something more specific.
            #print(f'повтор get_player_list - {link}')
            continue
        else:
            break
    cards = []
    card_info = []
    for div in divs:
        try:
            try:
                card_info_ = str(div)
                card_info.append('non-rare' if 'non-rare' in card_info_ else 'rare')
                card_info.append('gold' if 'gold' in card_info_ else 'silver' if 'silver' in card_info_ else 'bronze')
            except Exception:
                card_info = ['Unknown', link]
            if not player_att_dict.get(div.find('a').get('href')):
                player_att_dict[div.find('a').get('href')] = \
                    {'rating': div.find('div', class_='pcdisplay-rat').text,
                     'position': div.find('div', class_='pcdisplay-pos').text,
                     'type': card_info[0],
                     'rarity': card_info[1],
                     'price_ps': int(div.find('div', class_='ps-price-hover').text.replace(',', '').replace('\n', '')),
                     'price_pc': int(div.find('div', class_='pc-price-hover').text.replace(',', '').replace('\n', '')),
                     'price_xbox': int(div.find('div', class_='xbox-price-hover').text.replace(',', '').replace('\n', ''))
                     }
                     # 'price_ps_upd': 'no_data',
                     # 'price_pc_upd': 'no_data',
                     # 'price_xbox_upd': 'no_data'
            cards.append(div.find('a').get('href'))
        except AttributeError:
            print(f'пропуск парсинга игрока {link}')
            pass
    return cards


def get_price_update(key):
    html = 'http://futbin.com' + key
    while True:
        try:
            soup = BeautifulSoup(get_html(html).text, 'lxml')
            player_id = \
                soup.find('div', class_='site-player-page').find('div', class_='container').find('div', id='page-info').get('data-player-resource')
            price_update = [
                get_html(f'https://www.futbin.com/20/playerPrices?player={player_id}').json()[player_id]['prices'][
                    'ps']['updated'],
                get_html(f'https://www.futbin.com/20/playerPrices?player={player_id}').json()[player_id]['prices'][
                    'pc']['updated'],
                get_html(f'https://www.futbin.com/20/playerPrices?player={player_id}').json()[player_id]['prices'][
                    'xbox']['updated']]
        except Exception:
            print('пытаемся повторить get_price_update')
            continue
        else:
            break
    return price_update


def update_top_players_prices(max_player_index, start_players_index, end_player_index):
    i = iter(players_dict.items())
    for key, value in dict(itertools.islice(i, start_players_index, end_player_index)).items():
        if value >= max_player_index:
            html = 'http://futbin.com' + key
            #print(key)
            while True:
                try:
                    soup = BeautifulSoup(get_html(html).text, 'lxml')
                    player_id = \
                        soup.find('div', class_='site-player-page').find('div', class_='container').find('div',
                                                                                                         id='page-info').get(
                            'data-player-resource')
                    price_update = [
                        get_html(f'https://www.futbin.com/20/playerPrices?player={player_id}').json()[player_id]['prices'][
                            'ps']['updated'],
                        get_html(f'https://www.futbin.com/20/playerPrices?player={player_id}').json()[player_id]['prices'][
                            'pc']['updated'],
                        get_html(f'https://www.futbin.com/20/playerPrices?player={player_id}').json()[player_id]['prices'][
                            'xbox']['updated']]
                except Exception:
                    print('пытаемся повторить get_price_update')
                    continue
                else:
                    break
            player_att_dict[key]['price_ps_upd'] = price_update[0]
            player_att_dict[key]['price_pc_upd'] = price_update[1]
            player_att_dict[key]['price_xbox_upd'] = price_update[2]
    return True


def write_to_csv():
    dt_now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + '.csv'
    with open('/home/kemper1t/' + dt_now, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file,delimiter = ';')
        writer.writerow(['url', 'sbc_count', 'rating', 'position', 'type', 'rarity', 'PS price', 'PS price Update', 'PC price',
             'PC price Update', 'XBOX price', 'XBOX price Update'])
        for key, value in players_dict.items():
            if value >= max_player_index:
                #price_update = get_price_update(key)
                writer.writerow([key,value,
                                 player_att_dict[key]['rating'],
                                 player_att_dict[key]['position'],
                                 player_att_dict[key]['type'],
                                 player_att_dict[key]['rarity'],
                                 player_att_dict[key]['price_ps'],
                                 player_att_dict[key]['price_ps_upd'],
                                 player_att_dict[key]['price_pc'],
                                 player_att_dict[key]['price_pc_upd'],
                                 player_att_dict[key]['price_xbox'],
                                 player_att_dict[key]['price_xbox_upd'],
                                 ])
    with open('/home/kemper1t/' + dt_now, "rb") as f:
        webhook.add_file(file=f.read(), filename=dt_now)
    webhook.execute()
    bot = telebot.TeleBot(TOKEN)
    bot.send_document(5020676, open('/home/kemper1t/' + dt_now, 'rb'))
    bot.send_document(432775186, open('/home/kemper1t/' + dt_now, 'rb'))
    os.remove('/home/kemper1t/' + dt_now)

start_time = time.time()
print(f'запуск скрипта в {time.time()}')

list_sbc_id = collect_sbc_id(get_all_sbc(get_html('https://www.futbin.com/squad-building-challenges').text))

sbc_id_thread_index = (len(list_sbc_id) // 2) + (1 if len(list_sbc_id) % 2 == 1 else 0)
thread1 = Thread(target=collect_challenge_list, args=(list_sbc_id[:sbc_id_thread_index],))
thread2 = Thread(target=collect_challenge_list, args=(list_sbc_id[sbc_id_thread_index:],))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

challenge_list_index = (len(groups) // 2) + (1 if len(groups) % 2 == 1 else 0)

thread1 = Thread(target=collect_finish_sbc_list, args=(groups[:challenge_list_index],))
thread2 = Thread(target=collect_finish_sbc_list, args=(groups[challenge_list_index:],))
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("--- %s seconds ---" % (time.time() - start_time))
groups = []

links_index = (len(links) // 2) + (1 if len(links) % 2 == 1 else 0)

thread1 = Thread(target=collect_players, kwargs={'start_links_index':0, 'end_links_index':links_index})
thread2 = Thread(target=collect_players, kwargs={'start_links_index':links_index, 'end_links_index':-1})
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("--- %s seconds ---" % (time.time() - start_time))

max_player_index = sorted(list(players_dict.values()))[-200] if len(list(players_dict.values())) >= 200 else sorted(list(players_dict.values()))[0]

players_index = (len(players_dict) // 2) + (1 if len(players_dict) % 2 == 1 else 0)
print("--- %s seconds ---" % (time.time() - start_time))
thread1 = Thread(target=update_top_players_prices, kwargs={'max_player_index':max_player_index, 'start_players_index':0, 'end_player_index':players_index})
thread2 = Thread(target=update_top_players_prices, kwargs={'max_player_index':max_player_index, 'start_players_index':players_index, 'end_player_index':len(players_dict)})
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("--- %s seconds ---" % (time.time() - start_time))
write_to_csv()

print("--- %s seconds ---" % (time.time() - start_time))
