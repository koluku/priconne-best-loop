from bs4 import BeautifulSoup
import requests
import json
import re
import time
from tqdm import tqdm

ITEMURLID = {}

def getSoupObject(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def getCharatarListInfo(soup):
    charactar_list_selector = '.puri_chara > table > tr'
    charactar_list = soup.select(charactar_list_selector)
    charactar_list_info = []
    for i in range(1, len(charactar_list)):
        charactar_name = charactar_list[i].get('data-col1')
        charactar_rarity = int(charactar_list[i].get('data-col2').replace('★', ''))

        charactar_url_selector = '.puri_chara > table:nth-child(1) > tr:nth-child({}) > td:first-child > a'.format(i+1)
        o_charactar_url = soup.select(charactar_url_selector)
        charactar_url = o_charactar_url[0].get('href')
        charactar_list_info.append({'rarity': charactar_rarity, 'name': charactar_name, 'url': charactar_url, 'equipments': []})
    return charactar_list_info

def getCharactarEquipmentsInfo(charactar_info, items):
    target_url = charactar_info['url']
    soup = getSoupObject(target_url)
    charactar_equipments_selector = '#article-body > div > table'
    charactar_equipments = soup.select(charactar_equipments_selector)
    ur = charactar_equipments[0].find_all('a')

    if len(ur) == 0:
        ur = charactar_equipments[1].find_all('a')
    print('-----------------')
    print('Name: {}, Items: {}'.format(charactar_info['name'], len(ur)))

    if len(ur) != 76:
        return charactar_info

    for i in range(13):
        charactar_a_rank_equipments = {'rank': i+1, 'items': []}

        if i == 12:
            t = 4
        else:
            t = 6
        for j in range(t):
            print('Rank: {}, Item: {}'.format(i+1, j+1))
            charactar_equipment_url = ur[i*6+j].get('href')
            if charactar_equipment_url not in ITEMURLID:
                a_soup = getSoupObject(charactar_equipment_url)
                item_name_selector = 'title'
                origin_item_name = a_soup.select(item_name_selector)

                title = origin_item_name[0].text
                pattern = '(?<=「).+(?=」.*)'
                result = re.search(pattern, title)
                item_name = result.group()

                for item in items['items']:
                    if item['name'] != item_name:
                        continue
                    ITEMURLID[charactar_equipment_url] = item['id']
                time.sleep(1)

            charactar_a_rank_equipments['items'].append({'id': ITEMURLID[charactar_equipment_url],'amount': 1})
        charactar_info['equipments'].append(charactar_a_rank_equipments)
    time.sleep(1)
    return charactar_info

def main():
    with open('cache.json', 'r') as f:
        ITEMURLID.update(json.load(f))
    with open('../src/components/items.json', 'r') as f:
        items = json.load(f)

    target_url = 'https://gamewith.jp/pricone-re/article/show/92923'
    soup = getSoupObject(target_url)
    charactar_list_info = {}
    charactar_list_info['charactars'] = getCharatarListInfo(soup)

    print('list')
    for i, charactar_info in enumerate(charactar_list_info['charactars']):
        charactar_list_info['charactars'][i] = getCharactarEquipmentsInfo(charactar_info, items)
        del(charactar_list_info['charactars'][i]['url'])

        with open('../src/components/charactars.json', 'w') as f:
            jd = json.dumps(charactar_list_info, ensure_ascii=False)
            f.write(jd)
        with open('cache.json', 'w') as f:
            jd = json.dumps(ITEMURLID, ensure_ascii=False)
            f.write(jd)


if __name__ == '__main__':
    main()
