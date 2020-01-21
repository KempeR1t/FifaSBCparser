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
from telebot import apihelper
from discord_webhook import DiscordWebhook
import threading
from threading import Thread
import itertools

webhook = DiscordWebhook(url='https://xx',
                         username="СВЕЖАЯ ВЫГРУЗКА ТОП ИГРОКОВ В СБЧ", content='@everyone')


TOKEN = 'x'

apihelper.proxy = {'xx'}

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

challenge_list = ['/squad-building-challenges/ALL/155/Beware the Lion',
                  '/squad-building-challenges/ALL/46/Bundesliga',
                  '/squad-building-challenges/ALL/47/Germany',
                  '/squad-building-challenges/ALL/48/85-Rated Squad',
                  '/squad-building-challenges/ALL/42/Germany',
                  '/squad-building-challenges/ALL/43/Spain',
                  '/squad-building-challenges/ALL/44/Italy',
                  '/squad-building-challenges/ALL/45/England',
                  '/squad-building-challenges/ALL/208/Marquee Moments',
                  '/squad-building-challenges/ALL/202/Swansea City vs. Cardiff City',
                  '/squad-building-challenges/ALL/203/Roma vs. Milan',
                  '/squad-building-challenges/ALL/204/Liverpool vs. Spurs',
                  '/squad-building-challenges/ALL/205/Paris vs. OM',
                  '/squad-building-challenges/ALL/184/1. FSV Mainz 05',
                  '/squad-building-challenges/ALL/185/Borussia Dortmund',
                  '/squad-building-challenges/ALL/186/Fortuna Düsseldorf',
                  '/squad-building-challenges/ALL/187/FC Augsburg',
                  '/squad-building-challenges/ALL/188/Bayern München',
                  '/squad-building-challenges/ALL/189/Eintracht Frankfurt',
                  '/squad-building-challenges/ALL/190/Hertha BSC',
                  '/squad-building-challenges/ALL/191/1. FC Köln',
                  '/squad-building-challenges/ALL/192/Bayer 04 Leverkusen',
                  "/squad-building-challenges/ALL/193/Borussia M'gladbach",
                  '/squad-building-challenges/ALL/194/SC Paderborn 07',
                  '/squad-building-challenges/ALL/195/RB Leipzig',
                  '/squad-building-challenges/ALL/196/SC Freiburg',
                  '/squad-building-challenges/ALL/197/FC Schalke 04',
                  '/squad-building-challenges/ALL/198/TSG 1899 Hoffenheim',
                  '/squad-building-challenges/ALL/199/1. FC Union Berlin',
                  '/squad-building-challenges/ALL/200/VfL Wolfsburg',
                  '/squad-building-challenges/ALL/201/Werder Bremen',
                  '/squad-building-challenges/ALL/181/Brazil',
                  '/squad-building-challenges/ALL/182/CSL',
                  '/squad-building-challenges/ALL/183/Smash',
                  '/squad-building-challenges/ALL/26/The Challenger',
                  '/squad-building-challenges/ALL/27/Advanced',
                  '/squad-building-challenges/ALL/28/Fiendish',
                  '/squad-building-challenges/ALL/29/Puzzle Master',
                  '/squad-building-challenges/ALL/168/Amine Harit',
                  '/squad-building-challenges/ALL/22/The Final Four',
                  '/squad-building-challenges/ALL/23/Six Of The Best',
                  '/squad-building-challenges/ALL/24/Elite Eight',
                  '/squad-building-challenges/ALL/25/Around The World',
                  '/squad-building-challenges/ALL/163/Victor Osimhen',
                  '/squad-building-challenges/ALL/18/Give Me Five',
                  '/squad-building-challenges/ALL/19/Seven-League Boots',
                  '/squad-building-challenges/ALL/20/The Whole Nine Yards',
                  '/squad-building-challenges/ALL/21/First XI',
                  '/squad-building-challenges/ALL/149/Carlos Vela',
                  '/squad-building-challenges/ALL/144/Premier League',
                  '/squad-building-challenges/ALL/146/Gunners',
                  '/squad-building-challenges/ALL/147/85-Rated Squad',
                  '/squad-building-challenges/ALL/148/87-Rated Squad']


def get_html(url):
    user_agent = random.choice(user_agent_list)
    # Set the headers
    headers = {'User-Agent': user_agent}
    r = requests.get(url, headers=headers, timeout=5)
    if r.status_code == 200:
        return r

    if r.status_code == 404:
        print(f'Страница не существует! {url}')

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
    #print(groups)
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
        print(f'{link}, {threading.current_thread().name} осталось {length}')
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
            print(f'повтор get_player_list - {link}')
            continue
        else:
            break
    cards = []
    card_info = []
    for div in divs:
        try:
            try:
                card_info_ =  str(div)
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
                    'price_ps': int(div.find('div', class_='ps-price-hover').text.replace(',','').replace('\n','')),
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
            while True:
                try:
                    # soup = BeautifulSoup(get_html(html).text, 'lxml')
                    # if player_att_dict[key]['type'] == 'Unknown':
                    #     info = soup.find('div', id='Player-card')
                    #     type = info.get('data-level')
                    #     rarity = info.get('data-rare-type')
                    #     player_att_dict[key]['type'] = type
                    #     player_att_dict[key]['rarity'] = ('rare' if rarity == 1 else 'non-rare')
                    # else:
                    #     pass
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
    dt_now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+'.csv'
    with open(dt_now, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file,delimiter = ';')
        writer.writerow(['url', 'sbc_count', 'rating', 'position', 'type', 'rarity', 'PS price', 'PS price Update' ,'PC price',
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
    with open('F:\Cloud\Programming\pycharm\Tasks\\' + dt_now, "rb") as f:
        webhook.add_file(file=f.read(), filename=dt_now)
    #webhook.execute()
    bot = telebot.TeleBot(TOKEN)
    bot.send_document(5020676, open('F:\Cloud\Programming\pycharm\Tasks\\' + dt_now, 'rb'))
    #bot.send_document(432775186, open('/home/kemper1t/' + dt_now, 'rb'))
    os.remove('F:\Cloud\Programming\pycharm\Tasks\\' + dt_now)


start_time = time.time()
print(f'запуск скрипта в {time.time()}')
#collect_players(challenge_list[:2])
#collect_players(collect_challenge_list(collect_sbc_id(get_all_sbc(get_html('https://www.futbin.com/squad-building-challenges').text))))

#list_sbc_id = collect_sbc_id(get_all_sbc(get_html('https://www.futbin.com/squad-building-challenges').text))
list_sbc_id = ['76', '98', '96', '95', '94', '84', '81', '72', '71', '17', '16', '4', '5', '3', '11', '10', '9']


# sbc_id_thread_index = (len(list_sbc_id) // 2) + (1 if len(list_sbc_id) % 2 == 1 else 0)
# thread1 = Thread(target=collect_challenge_list, args=(list_sbc_id[:sbc_id_thread_index],))
# thread2 = Thread(target=collect_challenge_list, args=(list_sbc_id[sbc_id_thread_index:],))
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()


#вернуть
# groups = challenge_list
#
# challenge_list_index = (len(groups) // 2) + (1 if len(groups) % 2 == 1 else 0)
#
# thread1 = Thread(target=collect_finish_sbc_list, args=(groups[:challenge_list_index],))
# thread2 = Thread(target=collect_finish_sbc_list, args=(groups[challenge_list_index:],))
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print("--- %s seconds ---" % (time.time() - start_time))
# groups = []

links = ['/20/squad/100355989/sbc', '/20/squad/100355353/sbc', '/20/squad/100355351/sbc', '/20/squad/100355610/sbc', '/20/squad/100355940/sbc', '/20/squad/100355615/sbc', '/20/squad/100355616/sbc', '/20/squad/100355620/sbc', '/20/squad/100355533/sbc', '/20/squad/100355107/sbc', '/20/squad/100355247/sbc', '/20/squad/100355063/sbc', '/20/squad/100355547/sbc', '/20/squad/100355503/sbc', '/20/squad/100355147/sbc', '/20/squad/100355181/sbc', '/20/squad/100355159/sbc', '/20/squad/100355929/sbc', '/20/squad/100355201/sbc', '/20/squad/100355169/sbc', '/20/squad/100355958/sbc', '/20/squad/100354999/sbc', '/20/squad/100355933/sbc', '/20/squad/100355048/sbc', '/20/squad/100355549/sbc', '/20/squad/100355138/sbc', '/20/squad/100355086/sbc', '/20/squad/100355873/sbc', '/20/squad/100355346/sbc', '/20/squad/100355354/sbc', '/20/squad/100353945/sbc', '/20/squad/100353865/sbc', '/20/squad/100353941/sbc', '/20/squad/100355772/sbc', '/20/squad/100338713/sbc', '/20/squad/100337029/sbc', '/20/squad/100340039/sbc', '/20/squad/100338984/sbc', '/20/squad/100341324/sbc', '/20/squad/100329887/sbc', '/20/squad/100330830/sbc', '/20/squad/100312738/sbc', '/20/squad/100307976/sbc', '/20/squad/100316809/sbc', '/20/squad/100342540/sbc', '/20/squad/100314332/sbc', '/20/squad/100310674/sbc', '/20/squad/100332908/sbc', '/20/squad/100319502/sbc', '/20/squad/100339071/sbc', '/20/squad/100352031/sbc', '/20/squad/100308892/sbc', '/20/squad/100323536/sbc', '/20/squad/100309365/sbc', '/20/squad/100309549/sbc', '/20/squad/100308227/sbc', '/20/squad/100311074/sbc', '/20/squad/100309253/sbc', '/20/squad/100309339/sbc', '/20/squad/100341357/sbc', '/20/squad/100309463/sbc', '/20/squad/100308010/sbc', '/20/squad/100308908/sbc', '/20/squad/100309462/sbc', '/20/squad/100354781/sbc', '/20/squad/100355637/sbc', '/20/squad/100354758/sbc', '/20/squad/100354744/sbc', '/20/squad/100354573/sbc', '/20/squad/100355380/sbc', '/20/squad/100354629/sbc', '/20/squad/100354608/sbc', '/20/squad/100353795/sbc', '/20/squad/100354570/sbc', '/20/squad/100354526/sbc', '/20/squad/100355172/sbc', '/20/squad/100354596/sbc', '/20/squad/100354548/sbc', '/20/squad/100353787/sbc', '/20/squad/100309258/sbc', '/20/squad/100317839/sbc', '/20/squad/100350532/sbc', '/20/squad/100317836/sbc', '/20/squad/100324663/sbc', '/20/squad/100308994/sbc', '/20/squad/100316608/sbc', '/20/squad/100313619/sbc', '/20/squad/100339017/sbc', '/20/squad/100330554/sbc', '/20/squad/100350872/sbc', '/20/squad/100307963/sbc', '/20/squad/100308082/sbc', '/20/squad/100340046/sbc', '/20/squad/100312356/sbc', '/20/squad/100314371/sbc', '/20/squad/100308494/sbc', '/20/squad/100309377/sbc', '/20/squad/100319889/sbc', '/20/squad/100318871/sbc', '/20/squad/100312963/sbc', '/20/squad/100342847/sbc', '/20/squad/100330531/sbc', '/20/squad/100309282/sbc', '/20/squad/100316799/sbc', '/20/squad/100312888/sbc', '/20/squad/100307951/sbc', '/20/squad/100308215/sbc', '/20/squad/100340068/sbc', '/20/squad/100335997/sbc', '/20/squad/100354498/sbc', '/20/squad/100354052/sbc', '/20/squad/100355818/sbc', '/20/squad/100355478/sbc', '/20/squad/100354048/sbc', '/20/squad/100354681/sbc', '/20/squad/100355482/sbc', '/20/squad/100353798/sbc', '/20/squad/100355325/sbc', '/20/squad/100354470/sbc', '/20/squad/100355398/sbc', '/20/squad/100355663/sbc', '/20/squad/100354517/sbc', '/20/squad/100354715/sbc', '/20/squad/100354527/sbc', '/20/squad/100355484/sbc', '/20/squad/100353834/sbc', '/20/squad/100354078/sbc', '/20/squad/100353815/sbc', '/20/squad/100318412/sbc', '/20/squad/100318528/sbc', '/20/squad/100318415/sbc', '/20/squad/100323454/sbc', '/20/squad/100332829/sbc', '/20/squad/100319614/sbc', '/20/squad/100318396/sbc', '/20/squad/100320051/sbc', '/20/squad/100332934/sbc', '/20/squad/100335740/sbc', '/20/squad/100319306/sbc', '/20/squad/100312158/sbc', '/20/squad/100308178/sbc', '/20/squad/100352036/sbc', '/20/squad/100345501/sbc', '/20/squad/100308957/sbc', '/20/squad/100324666/sbc', '/20/squad/100333588/sbc', '/20/squad/100339045/sbc', '/20/squad/100352205/sbc', '/20/squad/100312392/sbc', '/20/squad/100311931/sbc', '/20/squad/100311768/sbc', '/20/squad/100308336/sbc', '/20/squad/100349257/sbc', '/20/squad/100307908/sbc', '/20/squad/100338234/sbc', '/20/squad/100308180/sbc', '/20/squad/100330817/sbc', '/20/squad/100334932/sbc', '/20/squad/100351799/sbc', '/20/squad/100351376/sbc', '/20/squad/100354213/sbc', '/20/squad/100351363/sbc', '/20/squad/100352051/sbc', '/20/squad/100351479/sbc', '/20/squad/100351763/sbc', '/20/squad/100351563/sbc', '/20/squad/100351652/sbc', '/20/squad/100351636/sbc', '/20/squad/100352108/sbc', '/20/squad/100351765/sbc', '/20/squad/100351492/sbc', '/20/squad/100352356/sbc', '/20/squad/100351306/sbc', '/20/squad/100351718/sbc', '/20/squad/100351893/sbc', '/20/squad/100351649/sbc', '/20/squad/100351528/sbc', '/20/squad/100352499/sbc', '/20/squad/100351451/sbc', '/20/squad/100352385/sbc', '/20/squad/100352243/sbc', '/20/squad/100352480/sbc', '/20/squad/100351609/sbc', '/20/squad/100351366/sbc', '/20/squad/100351548/sbc', '/20/squad/100353147/sbc', '/20/squad/100352279/sbc', '/20/squad/100351901/sbc', '/20/squad/100311813/sbc', '/20/squad/100326900/sbc', '/20/squad/100312074/sbc', '/20/squad/100331014/sbc', '/20/squad/100308995/sbc', '/20/squad/100309016/sbc', '/20/squad/100335646/sbc', '/20/squad/100311360/sbc', '/20/squad/100345492/sbc', '/20/squad/100329442/sbc', '/20/squad/100335121/sbc', '/20/squad/100308418/sbc', '/20/squad/100311560/sbc', '/20/squad/100327232/sbc', '/20/squad/100336875/sbc', '/20/squad/100325435/sbc', '/20/squad/100320430/sbc', '/20/squad/100333128/sbc', '/20/squad/100335618/sbc', '/20/squad/100319423/sbc', '/20/squad/100324327/sbc', '/20/squad/100310760/sbc', '/20/squad/100329007/sbc', '/20/squad/100330767/sbc', '/20/squad/100335835/sbc', '/20/squad/100313100/sbc', '/20/squad/100325395/sbc', '/20/squad/100349457/sbc', '/20/squad/100348390/sbc', '/20/squad/100348394/sbc', '/20/squad/100355778/sbc', '/20/squad/100355790/sbc', '/20/squad/100355773/sbc', '/20/squad/100353666/sbc', '/20/squad/100353399/sbc', '/20/squad/100353312/sbc', '/20/squad/100354329/sbc', '/20/squad/100355331/sbc', '/20/squad/100351802/sbc', '/20/squad/100353156/sbc', '/20/squad/100353308/sbc', '/20/squad/100351875/sbc', '/20/squad/100352418/sbc', '/20/squad/100353227/sbc', '/20/squad/100353291/sbc', '/20/squad/100352185/sbc', '/20/squad/100353924/sbc', '/20/squad/100353391/sbc', '/20/squad/100355155/sbc', '/20/squad/100351657/sbc', '/20/squad/100353326/sbc', '/20/squad/100354240/sbc', '/20/squad/100351529/sbc', '/20/squad/100351351/sbc', '/20/squad/100351503/sbc', '/20/squad/100351781/sbc', '/20/squad/100352161/sbc', '/20/squad/100352358/sbc', '/20/squad/100352077/sbc', '/20/squad/100351993/sbc', '/20/squad/100355760/sbc', '/20/squad/100346431/sbc', '/20/squad/100342419/sbc', '/20/squad/100354184/sbc', '/20/squad/100354130/sbc', '/20/squad/100311474/sbc', '/20/squad/100322107/sbc', '/20/squad/100335458/sbc', '/20/squad/100321465/sbc', '/20/squad/100326495/sbc', '/20/squad/100325045/sbc', '/20/squad/100349505/sbc', '/20/squad/100310195/sbc', '/20/squad/100321822/sbc', '/20/squad/100341871/sbc', '/20/squad/100354812/sbc', '/20/squad/100311711/sbc', '/20/squad/100327111/sbc', '/20/squad/100349494/sbc', '/20/squad/100309320/sbc', '/20/squad/100340692/sbc', '/20/squad/100331001/sbc', '/20/squad/100313732/sbc', '/20/squad/100332765/sbc', '/20/squad/100313606/sbc', '/20/squad/100311702/sbc', '/20/squad/100319366/sbc', '/20/squad/100351054/sbc', '/20/squad/100355400/sbc', '/20/squad/100350900/sbc', '/20/squad/100349872/sbc', '/20/squad/100350259/sbc', '/20/squad/100355571/sbc', '/20/squad/100349862/sbc', '/20/squad/100350275/sbc', '/20/squad/100350274/sbc', '/20/squad/100350281/sbc', '/20/squad/100328778/sbc', '/20/squad/100330927/sbc', '/20/squad/100348550/sbc', '/20/squad/100341043/sbc', '/20/squad/100324139/sbc', '/20/squad/100354259/sbc', '/20/squad/100353385/sbc', '/20/squad/100324025/sbc', '/20/squad/100329911/sbc', '/20/squad/100343467/sbc', '/20/squad/100348125/sbc', '/20/squad/100324155/sbc', '/20/squad/100344417/sbc', '/20/squad/100324148/sbc', '/20/squad/100348121/sbc', '/20/squad/100316117/sbc', '/20/squad/100324131/sbc', '/20/squad/100348739/sbc', '/20/squad/100354618/sbc', '/20/squad/100353440/sbc', '/20/squad/100331617/sbc', '/20/squad/100353926/sbc', '/20/squad/100323961/sbc', '/20/squad/100354684/sbc', '/20/squad/100351683/sbc', '/20/squad/100352828/sbc', '/20/squad/100355767/sbc', '/20/squad/100352838/sbc', '/20/squad/100352203/sbc', '/20/squad/100351462/sbc', '/20/squad/100355535/sbc', '/20/squad/100351712/sbc', '/20/squad/100351620/sbc', '/20/squad/100351668/sbc', '/20/squad/100351703/sbc', '/20/squad/100351539/sbc', '/20/squad/100354481/sbc', '/20/squad/100352038/sbc', '/20/squad/100351588/sbc', '/20/squad/100352255/sbc', '/20/squad/100352119/sbc', '/20/squad/100351697/sbc', '/20/squad/100352213/sbc', '/20/squad/100351673/sbc', '/20/squad/100351692/sbc', '/20/squad/100351549/sbc', '/20/squad/100351564/sbc', '/20/squad/100351789/sbc', '/20/squad/100351684/sbc', '/20/squad/100351605/sbc', '/20/squad/100355475/sbc', '/20/squad/100353407/sbc', '/20/squad/100352080/sbc', '/20/squad/100329996/sbc', '/20/squad/100336837/sbc', '/20/squad/100353668/sbc', '/20/squad/100313216/sbc', '/20/squad/100323402/sbc', '/20/squad/100324645/sbc', '/20/squad/100314305/sbc', '/20/squad/100312915/sbc', '/20/squad/100315013/sbc', '/20/squad/100350479/sbc', '/20/squad/100332679/sbc', '/20/squad/100328732/sbc', '/20/squad/100313182/sbc', '/20/squad/100309878/sbc', '/20/squad/100309555/sbc', '/20/squad/100342433/sbc', '/20/squad/100313492/sbc', '/20/squad/100308900/sbc', '/20/squad/100315110/sbc', '/20/squad/100309957/sbc', '/20/squad/100308270/sbc', '/20/squad/100311477/sbc', '/20/squad/100308885/sbc', '/20/squad/100343057/sbc', '/20/squad/100313573/sbc', '/20/squad/100308555/sbc', '/20/squad/100312183/sbc', '/20/squad/100309388/sbc', '/20/squad/100329988/sbc', '/20/squad/100353972/sbc', '/20/squad/100332684/sbc', '/20/squad/100331779/sbc', '/20/squad/100323746/sbc', '/20/squad/100296485/sbc', '/20/squad/100341007/sbc', '/20/squad/100340495/sbc', '/20/squad/100329293/sbc', '/20/squad/100319349/sbc', '/20/squad/100302416/sbc', '/20/squad/100293342/sbc', '/20/squad/100300316/sbc', '/20/squad/100298103/sbc', '/20/squad/100302557/sbc', '/20/squad/100332639/sbc', '/20/squad/100320488/sbc', '/20/squad/100329114/sbc', '/20/squad/100324265/sbc', '/20/squad/100297160/sbc', '/20/squad/100294522/sbc', '/20/squad/100296443/sbc', '/20/squad/100300590/sbc', '/20/squad/100304765/sbc', '/20/squad/100299922/sbc', '/20/squad/100289509/sbc', '/20/squad/100324337/sbc', '/20/squad/100345106/sbc', '/20/squad/100304130/sbc', '/20/squad/100328541/sbc', '/20/squad/100324292/sbc', '/20/squad/100332663/sbc', '/20/squad/100355596/sbc', '/20/squad/100355903/sbc', '/20/squad/100355927/sbc', '/20/squad/100355259/sbc', '/20/squad/100355711/sbc', '/20/squad/100355922/sbc', '/20/squad/100355710/sbc', '/20/squad/100355795/sbc', '/20/squad/100355863/sbc', '/20/squad/100355675/sbc', '/20/squad/100355504/sbc', '/20/squad/100355946/sbc', '/20/squad/100355707/sbc', '/20/squad/100355759/sbc', '/20/squad/100355821/sbc', '/20/squad/100355597/sbc', '/20/squad/100355900/sbc', '/20/squad/100355925/sbc', '/20/squad/100355724/sbc', '/20/squad/100355021/sbc', '/20/squad/100354867/sbc', '/20/squad/100355391/sbc', '/20/squad/100355942/sbc', '/20/squad/100355119/sbc', '/20/squad/100355496/sbc', '/20/squad/100355267/sbc', '/20/squad/100355681/sbc', '/20/squad/100355077/sbc', '/20/squad/100355022/sbc', '/20/squad/100355288/sbc', '/20/squad/100293807/sbc', '/20/squad/100316123/sbc', '/20/squad/100300147/sbc', '/20/squad/100347360/sbc', '/20/squad/100316105/sbc', '/20/squad/100308703/sbc', '/20/squad/100294548/sbc', '/20/squad/100294550/sbc', '/20/squad/100294559/sbc', '/20/squad/100330017/sbc', '/20/squad/100294533/sbc', '/20/squad/100329997/sbc', '/20/squad/100330801/sbc', '/20/squad/100294521/sbc', '/20/squad/100330187/sbc', '/20/squad/100331476/sbc', '/20/squad/100318706/sbc', '/20/squad/100326613/sbc', '/20/squad/100335025/sbc', '/20/squad/100331517/sbc', '/20/squad/100335030/sbc', '/20/squad/100326698/sbc', '/20/squad/100325373/sbc', '/20/squad/100318875/sbc', '/20/squad/100327274/sbc', '/20/squad/100291411/sbc', '/20/squad/100331484/sbc', '/20/squad/100335034/sbc', '/20/squad/100318869/sbc', '/20/squad/100326544/sbc', '/20/squad/100355971/sbc', '/20/squad/100355967/sbc', '/20/squad/100355987/sbc', '/20/squad/100355973/sbc', '/20/squad/100355969/sbc', '/20/squad/100355966/sbc', '/20/squad/100355990/sbc', '/20/squad/100355627/sbc', '/20/squad/100355986/sbc', '/20/squad/100355975/sbc', '/20/squad/100355978/sbc', '/20/squad/100355751/sbc', '/20/squad/100355810/sbc', '/20/squad/100355668/sbc', '/20/squad/100355830/sbc', '/20/squad/100355665/sbc', '/20/squad/100355658/sbc', '/20/squad/100355801/sbc', '/20/squad/100355251/sbc', '/20/squad/100355953/sbc', '/20/squad/100355963/sbc', '/20/squad/100355670/sbc', '/20/squad/100355954/sbc', '/20/squad/100355702/sbc', '/20/squad/100355764/sbc', '/20/squad/100354945/sbc', '/20/squad/100355045/sbc', '/20/squad/100355777/sbc', '/20/squad/100355278/sbc', '/20/squad/100355598/sbc', '/20/squad/100336868/sbc', '/20/squad/100304054/sbc', '/20/squad/100355826/sbc', '/20/squad/100355634/sbc', '/20/squad/100310650/sbc', '/20/squad/100355591/sbc', '/20/squad/100309446/sbc', '/20/squad/100304415/sbc', '/20/squad/100301840/sbc', '/20/squad/100288717/sbc', '/20/squad/100347059/sbc', '/20/squad/100307828/sbc', '/20/squad/100333236/sbc', '/20/squad/100334881/sbc', '/20/squad/100298871/sbc', '/20/squad/100329470/sbc', '/20/squad/100354482/sbc', '/20/squad/100327112/sbc', '/20/squad/100303053/sbc', '/20/squad/100349047/sbc', '/20/squad/100330264/sbc', '/20/squad/100347073/sbc', '/20/squad/100318445/sbc', '/20/squad/100322896/sbc', '/20/squad/100346983/sbc', '/20/squad/100355595/sbc', '/20/squad/100323611/sbc', '/20/squad/100294912/sbc', '/20/squad/100300366/sbc', '/20/squad/100347065/sbc', '/20/squad/100338812/sbc', '/20/squad/100332060/sbc', '/20/squad/100319434/sbc', '/20/squad/100330092/sbc', '/20/squad/100332082/sbc', '/20/squad/100308756/sbc', '/20/squad/100338201/sbc', '/20/squad/100349483/sbc', '/20/squad/100307122/sbc', '/20/squad/100330384/sbc', '/20/squad/100327044/sbc', '/20/squad/100330274/sbc', '/20/squad/100326514/sbc', '/20/squad/100307131/sbc', '/20/squad/100337783/sbc', '/20/squad/100337110/sbc', '/20/squad/100335789/sbc', '/20/squad/100340840/sbc', '/20/squad/100295095/sbc', '/20/squad/100310016/sbc', '/20/squad/100331332/sbc', '/20/squad/100329929/sbc', '/20/squad/100331539/sbc', '/20/squad/100333336/sbc', '/20/squad/100295690/sbc', '/20/squad/100335256/sbc', '/20/squad/100297694/sbc', '/20/squad/100328608/sbc', '/20/squad/100342675/sbc', '/20/squad/100331330/sbc', '/20/squad/100355983/sbc', '/20/squad/100355984/sbc', '/20/squad/100355992/sbc', '/20/squad/100355962/sbc', '/20/squad/100355258/sbc', '/20/squad/100355523/sbc', '/20/squad/100355494/sbc', '/20/squad/100355224/sbc', '/20/squad/100355192/sbc', '/20/squad/100355917/sbc', '/20/squad/100355221/sbc', '/20/squad/100355950/sbc', '/20/squad/100355934/sbc', '/20/squad/100355253/sbc', '/20/squad/100355951/sbc', '/20/squad/100355952/sbc', '/20/squad/100355594/sbc', '/20/squad/100354970/sbc', '/20/squad/100355705/sbc', '/20/squad/100355527/sbc', '/20/squad/100355911/sbc', '/20/squad/100354954/sbc', '/20/squad/100355704/sbc', '/20/squad/100354846/sbc', '/20/squad/100355769/sbc', '/20/squad/100355574/sbc', '/20/squad/100354835/sbc', '/20/squad/100355542/sbc', '/20/squad/100355834/sbc', '/20/squad/100355264/sbc', '/20/squad/100347877/sbc', '/20/squad/100347522/sbc', '/20/squad/100354310/sbc', '/20/squad/100350282/sbc', '/20/squad/100347566/sbc', '/20/squad/100347449/sbc', '/20/squad/100347527/sbc', '/20/squad/100352018/sbc', '/20/squad/100347532/sbc', '/20/squad/100347642/sbc', '/20/squad/100348413/sbc', '/20/squad/100347531/sbc', '/20/squad/100347480/sbc', '/20/squad/100347623/sbc', '/20/squad/100352965/sbc', '/20/squad/100347519/sbc', '/20/squad/100347550/sbc', '/20/squad/100354993/sbc', '/20/squad/100347403/sbc', '/20/squad/100347421/sbc', '/20/squad/100347471/sbc', '/20/squad/100347418/sbc', '/20/squad/100347467/sbc', '/20/squad/100354454/sbc', '/20/squad/100347398/sbc', '/20/squad/100347430/sbc', '/20/squad/100347570/sbc', '/20/squad/100347524/sbc', '/20/squad/100347586/sbc', '/20/squad/100347487/sbc', '/20/squad/100355991/sbc', '/20/squad/100355871/sbc', '/20/squad/100355875/sbc', '/20/squad/100355848/sbc', '/20/squad/100355521/sbc', '/20/squad/100355449/sbc', '/20/squad/100355113/sbc', '/20/squad/100355673/sbc', '/20/squad/100355439/sbc', '/20/squad/100355528/sbc', '/20/squad/100355129/sbc', '/20/squad/100355290/sbc', '/20/squad/100355121/sbc', '/20/squad/100355150/sbc', '/20/squad/100355676/sbc', '/20/squad/100355653/sbc', '/20/squad/100355768/sbc', '/20/squad/100355752/sbc', '/20/squad/100355269/sbc', '/20/squad/100355260/sbc', '/20/squad/100355207/sbc', '/20/squad/100355631/sbc', '/20/squad/100355272/sbc', '/20/squad/100355452/sbc', '/20/squad/100355555/sbc', '/20/squad/100355241/sbc', '/20/squad/100355371/sbc', '/20/squad/100355576/sbc', '/20/squad/100355231/sbc', '/20/squad/100355525/sbc', '/20/squad/100355956/sbc', '/20/squad/100355698/sbc', '/20/squad/100355872/sbc', '/20/squad/100333171/sbc', '/20/squad/100355907/sbc', '/20/squad/100290651/sbc', '/20/squad/100335156/sbc', '/20/squad/100354503/sbc', '/20/squad/100318267/sbc', '/20/squad/100323789/sbc', '/20/squad/100328362/sbc', '/20/squad/100334115/sbc', '/20/squad/100334368/sbc', '/20/squad/100334201/sbc', '/20/squad/100302964/sbc', '/20/squad/100303614/sbc', '/20/squad/100333000/sbc', '/20/squad/100303012/sbc', '/20/squad/100296758/sbc', '/20/squad/100335171/sbc', '/20/squad/100338419/sbc', '/20/squad/100342976/sbc', '/20/squad/100332900/sbc', '/20/squad/100297022/sbc', '/20/squad/100318748/sbc', '/20/squad/100293759/sbc', '/20/squad/100293732/sbc', '/20/squad/100293715/sbc', '/20/squad/100315249/sbc', '/20/squad/100341466/sbc', '/20/squad/100355988/sbc', '/20/squad/100355981/sbc', '/20/squad/100355947/sbc', '/20/squad/100355968/sbc', '/20/squad/100355869/sbc', '/20/squad/100355244/sbc', '/20/squad/100355972/sbc', '/20/squad/100355699/sbc', '/20/squad/100355611/sbc', '/20/squad/100354880/sbc', '/20/squad/100355133/sbc', '/20/squad/100354830/sbc', '/20/squad/100355483/sbc', '/20/squad/100355621/sbc', '/20/squad/100355057/sbc', '/20/squad/100354930/sbc', '/20/squad/100355944/sbc', '/20/squad/100355378/sbc', '/20/squad/100355633/sbc', '/20/squad/100355604/sbc', '/20/squad/100355245/sbc', '/20/squad/100354934/sbc', '/20/squad/100355366/sbc', '/20/squad/100354909/sbc', '/20/squad/100355389/sbc', '/20/squad/100355379/sbc', '/20/squad/100355592/sbc', '/20/squad/100355613/sbc', '/20/squad/100354894/sbc', '/20/squad/100354923/sbc', '/20/squad/100355964/sbc', '/20/squad/100354227/sbc', '/20/squad/100304292/sbc', '/20/squad/100348055/sbc', '/20/squad/100342906/sbc', '/20/squad/100355213/sbc', '/20/squad/100323285/sbc', '/20/squad/100295582/sbc', '/20/squad/100295574/sbc', '/20/squad/100303286/sbc', '/20/squad/100323353/sbc', '/20/squad/100324271/sbc', '/20/squad/100321495/sbc', '/20/squad/100332415/sbc', '/20/squad/100304297/sbc', '/20/squad/100355187/sbc', '/20/squad/100296374/sbc', '/20/squad/100304305/sbc', '/20/squad/100304301/sbc', '/20/squad/100332490/sbc', '/20/squad/100330301/sbc', '/20/squad/100329049/sbc', '/20/squad/100324511/sbc', '/20/squad/100324456/sbc', '/20/squad/100333619/sbc', '/20/squad/100320100/sbc', '/20/squad/100333606/sbc', '/20/squad/100326488/sbc', '/20/squad/100332494/sbc', '/20/squad/100350074/sbc', '/20/squad/100354002/sbc', '/20/squad/100353849/sbc', '/20/squad/100353987/sbc', '/20/squad/100354292/sbc', '/20/squad/100353866/sbc', '/20/squad/100353887/sbc', '/20/squad/100353782/sbc', '/20/squad/100354070/sbc', '/20/squad/100353877/sbc', '/20/squad/100355227/sbc', '/20/squad/100354071/sbc', '/20/squad/100354011/sbc', '/20/squad/100353966/sbc', '/20/squad/100354352/sbc', '/20/squad/100354502/sbc', '/20/squad/100354440/sbc', '/20/squad/100353778/sbc', '/20/squad/100354165/sbc', '/20/squad/100353791/sbc', '/20/squad/100354160/sbc', '/20/squad/100353882/sbc', '/20/squad/100354076/sbc', '/20/squad/100354222/sbc', '/20/squad/100353869/sbc', '/20/squad/100355915/sbc', '/20/squad/100354154/sbc', '/20/squad/100354101/sbc', '/20/squad/100354005/sbc', '/20/squad/100345051/sbc', '/20/squad/100353047/sbc', '/20/squad/100300610/sbc', '/20/squad/100311113/sbc', '/20/squad/100336711/sbc', '/20/squad/100314792/sbc', '/20/squad/100330974/sbc', '/20/squad/100300586/sbc', '/20/squad/100330910/sbc', '/20/squad/100339611/sbc', '/20/squad/100296024/sbc', '/20/squad/100306082/sbc', '/20/squad/100309110/sbc', '/20/squad/100345540/sbc', '/20/squad/100302281/sbc', '/20/squad/100350174/sbc', '/20/squad/100289155/sbc', '/20/squad/100292977/sbc', '/20/squad/100335535/sbc', '/20/squad/100299096/sbc', '/20/squad/100303730/sbc', '/20/squad/100307892/sbc', '/20/squad/100335733/sbc', '/20/squad/100312217/sbc', '/20/squad/100335908/sbc', '/20/squad/100322043/sbc', '/20/squad/100316972/sbc', '/20/squad/100335909/sbc', '/20/squad/100341126/sbc', '/20/squad/100311342/sbc', '/20/squad/100355802/sbc', '/20/squad/100355823/sbc', '/20/squad/100355765/sbc', '/20/squad/100355317/sbc', '/20/squad/100355505/sbc', '/20/squad/100355498/sbc', '/20/squad/100353818/sbc', '/20/squad/100353891/sbc', '/20/squad/100353823/sbc', '/20/squad/100299422/sbc', '/20/squad/100299202/sbc', '/20/squad/100331232/sbc', '/20/squad/100305535/sbc', '/20/squad/100342417/sbc', '/20/squad/100307291/sbc', '/20/squad/100354327/sbc', '/20/squad/100355949/sbc', '/20/squad/100355979/sbc', '/20/squad/100355815/sbc', '/20/squad/100328568/sbc', '/20/squad/100328158/sbc', '/20/squad/100327988/sbc', '/20/squad/100328173/sbc', '/20/squad/100328137/sbc', '/20/squad/100337316/sbc', '/20/squad/100294063/sbc', '/20/squad/100318147/sbc', '/20/squad/100316050/sbc', '/20/squad/100327657/sbc', '/20/squad/100294061/sbc', '/20/squad/100316530/sbc', '/20/squad/100351709/sbc', '/20/squad/100327049/sbc', '/20/squad/100354764/sbc', '/20/squad/100326837/sbc', '/20/squad/100332763/sbc', '/20/squad/100337671/sbc', '/20/squad/100299192/sbc', '/20/squad/100307332/sbc', '/20/squad/100354688/sbc', '/20/squad/100337286/sbc', '/20/squad/100324899/sbc', '/20/squad/100318378/sbc', '/20/squad/100306139/sbc', '/20/squad/100327408/sbc', '/20/squad/100320042/sbc', '/20/squad/100354814/sbc', '/20/squad/100353904/sbc', '/20/squad/100354335/sbc', '/20/squad/100355644/sbc', '/20/squad/100354178/sbc', '/20/squad/100354175/sbc', '/20/squad/100353893/sbc', '/20/squad/100353901/sbc', '/20/squad/100354333/sbc', '/20/squad/100353890/sbc', '/20/squad/100354091/sbc', '/20/squad/100310054/sbc', '/20/squad/100354115/sbc', '/20/squad/100338853/sbc', '/20/squad/100292766/sbc', '/20/squad/100294835/sbc', '/20/squad/100349164/sbc', '/20/squad/100312108/sbc', '/20/squad/100352834/sbc', '/20/squad/100311956/sbc', '/20/squad/100340648/sbc', '/20/squad/100323566/sbc', '/20/squad/100328664/sbc', '/20/squad/100301747/sbc', '/20/squad/100354785/sbc', '/20/squad/100337084/sbc', '/20/squad/100304076/sbc', '/20/squad/100317552/sbc', '/20/squad/100305119/sbc', '/20/squad/100342609/sbc', '/20/squad/100303371/sbc', '/20/squad/100341292/sbc', '/20/squad/100311792/sbc', '/20/squad/100327167/sbc', '/20/squad/100312951/sbc', '/20/squad/100335751/sbc', '/20/squad/100303941/sbc', '/20/squad/100306111/sbc', '/20/squad/100323317/sbc', '/20/squad/100320294/sbc', '/20/squad/100355289/sbc', '/20/squad/100353806/sbc', '/20/squad/100353805/sbc', '/20/squad/100354354/sbc', '/20/squad/100316708/sbc', '/20/squad/100324317/sbc', '/20/squad/100323641/sbc', '/20/squad/100332538/sbc', '/20/squad/100327293/sbc', '/20/squad/100337050/sbc', '/20/squad/100337256/sbc', '/20/squad/100331331/sbc', '/20/squad/100343595/sbc', '/20/squad/100327143/sbc', '/20/squad/100329703/sbc', '/20/squad/100300593/sbc', '/20/squad/100300692/sbc', '/20/squad/100328319/sbc', '/20/squad/100309882/sbc', '/20/squad/100323381/sbc', '/20/squad/100320323/sbc', '/20/squad/100297880/sbc', '/20/squad/100328929/sbc', '/20/squad/100349669/sbc', '/20/squad/100347039/sbc', '/20/squad/100326638/sbc', '/20/squad/100303309/sbc', '/20/squad/100343759/sbc', '/20/squad/100303947/sbc', '/20/squad/100303170/sbc', '/20/squad/100325490/sbc', '/20/squad/100326343/sbc', '/20/squad/100343558/sbc', '/20/squad/100322080/sbc', '/20/squad/100305165/sbc', '/20/squad/100298921/sbc', '/20/squad/100350067/sbc', '/20/squad/100302412/sbc', '/20/squad/100341279/sbc', '/20/squad/100302400/sbc', '/20/squad/100340901/sbc', '/20/squad/100311821/sbc', '/20/squad/100305114/sbc', '/20/squad/100337731/sbc', '/20/squad/100303759/sbc', '/20/squad/100299228/sbc', '/20/squad/100323703/sbc', '/20/squad/100315972/sbc', '/20/squad/100330800/sbc', '/20/squad/100341266/sbc', '/20/squad/100329455/sbc', '/20/squad/100329962/sbc', '/20/squad/100347443/sbc', '/20/squad/100309637/sbc', '/20/squad/100309432/sbc', '/20/squad/100352474/sbc', '/20/squad/100320230/sbc', '/20/squad/100345443/sbc', '/20/squad/100333556/sbc', '/20/squad/100327102/sbc', '/20/squad/100319903/sbc', '/20/squad/100301235/sbc', '/20/squad/100312188/sbc', '/20/squad/100315748/sbc', '/20/squad/100354203/sbc', '/20/squad/100354346/sbc', '/20/squad/100354619/sbc', '/20/squad/100354036/sbc', '/20/squad/100354796/sbc', '/20/squad/100353868/sbc', '/20/squad/100354439/sbc', '/20/squad/100354794/sbc', '/20/squad/100355877/sbc', '/20/squad/100346301/sbc', '/20/squad/100355888/sbc', '/20/squad/100342643/sbc', '/20/squad/100341691/sbc', '/20/squad/100355796/sbc', '/20/squad/100341542/sbc', '/20/squad/100341758/sbc', '/20/squad/100341649/sbc', '/20/squad/100342669/sbc', '/20/squad/100342372/sbc', '/20/squad/100341824/sbc', '/20/squad/100342157/sbc', '/20/squad/100342102/sbc', '/20/squad/100341849/sbc', '/20/squad/100342108/sbc', '/20/squad/100342750/sbc', '/20/squad/100355539/sbc', '/20/squad/100341706/sbc', '/20/squad/100341741/sbc', '/20/squad/100341842/sbc', '/20/squad/100342470/sbc', '/20/squad/100342663/sbc', '/20/squad/100341724/sbc', '/20/squad/100342231/sbc', '/20/squad/100342194/sbc', '/20/squad/100341733/sbc', '/20/squad/100342235/sbc', '/20/squad/100344146/sbc', '/20/squad/100341515/sbc', '/20/squad/100353916/sbc', '/20/squad/100354185/sbc', '/20/squad/100354521/sbc', '/20/squad/100353929/sbc', '/20/squad/100353842/sbc', '/20/squad/100355100/sbc', '/20/squad/100353857/sbc', '/20/squad/100344115/sbc', '/20/squad/100337176/sbc', '/20/squad/100354630/sbc', '/20/squad/100336759/sbc', '/20/squad/100336443/sbc', '/20/squad/100340433/sbc', '/20/squad/100350635/sbc', '/20/squad/100336828/sbc', '/20/squad/100337195/sbc', '/20/squad/100336922/sbc', '/20/squad/100336927/sbc', '/20/squad/100337486/sbc', '/20/squad/100336511/sbc', '/20/squad/100336467/sbc', '/20/squad/100337066/sbc', '/20/squad/100336887/sbc', '/20/squad/100336376/sbc', '/20/squad/100344123/sbc', '/20/squad/100336747/sbc', '/20/squad/100353029/sbc', '/20/squad/100336827/sbc', '/20/squad/100336762/sbc', '/20/squad/100336154/sbc', '/20/squad/100344944/sbc', '/20/squad/100336778/sbc', '/20/squad/100337170/sbc', '/20/squad/100342018/sbc', '/20/squad/100346268/sbc', '/20/squad/100336613/sbc', '/20/squad/100336548/sbc', '/20/squad/100354558/sbc', '/20/squad/100354100/sbc', '/20/squad/100353848/sbc', '/20/squad/100353863/sbc', '/20/squad/100355510/sbc', '/20/squad/100353813/sbc', '/20/squad/100344129/sbc', '/20/squad/100348730/sbc', '/20/squad/100337155/sbc', '/20/squad/100337171/sbc', '/20/squad/100355324/sbc', '/20/squad/100354697/sbc', '/20/squad/100336341/sbc', '/20/squad/100336742/sbc', '/20/squad/100337154/sbc', '/20/squad/100336914/sbc', '/20/squad/100339490/sbc', '/20/squad/100337107/sbc', '/20/squad/100336440/sbc', '/20/squad/100344202/sbc', '/20/squad/100339472/sbc', '/20/squad/100336377/sbc', '/20/squad/100340437/sbc', '/20/squad/100336716/sbc', '/20/squad/100336532/sbc', '/20/squad/100336424/sbc', '/20/squad/100352087/sbc', '/20/squad/100337270/sbc', '/20/squad/100339986/sbc', '/20/squad/100336400/sbc', '/20/squad/100344198/sbc', '/20/squad/100336829/sbc', '/20/squad/100336313/sbc', '/20/squad/100336315/sbc', '/20/squad/100336372/sbc', '/20/squad/100336514/sbc', '/20/squad/100355335/sbc', '/20/squad/100354507/sbc', '/20/squad/100355664/sbc', '/20/squad/100354745/sbc', '/20/squad/100354425/sbc', '/20/squad/100354060/sbc', '/20/squad/100354027/sbc', '/20/squad/100353821/sbc', '/20/squad/100336126/sbc', '/20/squad/100336303/sbc', '/20/squad/100336435/sbc', '/20/squad/100336565/sbc', '/20/squad/100336522/sbc', '/20/squad/100346876/sbc', '/20/squad/100337106/sbc', '/20/squad/100337111/sbc', '/20/squad/100336431/sbc', '/20/squad/100337178/sbc', '/20/squad/100336541/sbc', '/20/squad/100336373/sbc', '/20/squad/100340440/sbc', '/20/squad/100336404/sbc', '/20/squad/100346487/sbc', '/20/squad/100336916/sbc', '/20/squad/100337300/sbc', '/20/squad/100336876/sbc', '/20/squad/100336470/sbc', '/20/squad/100336172/sbc', '/20/squad/100336518/sbc', '/20/squad/100336800/sbc', '/20/squad/100336852/sbc', '/20/squad/100336362/sbc', '/20/squad/100341615/sbc', '/20/squad/100339480/sbc', '/20/squad/100342300/sbc', '/20/squad/100336242/sbc', '/20/squad/100336811/sbc', '/20/squad/100337209/sbc', '/20/squad/100354547/sbc', '/20/squad/100354281/sbc', '/20/squad/100354903/sbc', '/20/squad/100354088/sbc', '/20/squad/100354138/sbc', '/20/squad/100353836/sbc', '/20/squad/100353809/sbc', '/20/squad/100354775/sbc', '/20/squad/100354275/sbc', '/20/squad/100353847/sbc', '/20/squad/100354105/sbc', '/20/squad/100354239/sbc', '/20/squad/100353830/sbc', '/20/squad/100354062/sbc', '/20/squad/100353841/sbc', '/20/squad/100336423/sbc', '/20/squad/100337104/sbc', '/20/squad/100354793/sbc', '/20/squad/100355338/sbc', '/20/squad/100336225/sbc', '/20/squad/100336788/sbc', '/20/squad/100341953/sbc', '/20/squad/100336465/sbc', '/20/squad/100337945/sbc', '/20/squad/100337100/sbc', '/20/squad/100336767/sbc', '/20/squad/100339934/sbc', '/20/squad/100336557/sbc', '/20/squad/100336546/sbc', '/20/squad/100336382/sbc', '/20/squad/100340442/sbc', '/20/squad/100339877/sbc', '/20/squad/100336386/sbc', '/20/squad/100336375/sbc', '/20/squad/100336411/sbc', '/20/squad/100352134/sbc', '/20/squad/100336338/sbc', '/20/squad/100352140/sbc', '/20/squad/100336408/sbc', '/20/squad/100336892/sbc', '/20/squad/100336849/sbc', '/20/squad/100336862/sbc', '/20/squad/100341306/sbc', '/20/squad/100337243/sbc', '/20/squad/100339853/sbc', '/20/squad/100353829/sbc', '/20/squad/100354031/sbc', '/20/squad/100353879/sbc', '/20/squad/100354380/sbc', '/20/squad/100353900/sbc', '/20/squad/100355758/sbc', '/20/squad/100354169/sbc', '/20/squad/100353790/sbc', '/20/squad/100353872/sbc']
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
