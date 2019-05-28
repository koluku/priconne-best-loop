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

def getTableInfo(soup):
    table_selector = '#article-body > div.w-instant-database-list > div > table > tr'
    table = soup.select(table_selector)
    return table

def getAreaStageInfo(soup, i):
    area_stage_selctor = '#article-body > div.w-instant-database-list > div > table > tr:nth-child({}) > td:nth-child(1)'.format(i)
    area_stage = soup.select(area_stage_selctor)
    if len(area_stage) == 0:
        return [0, 0]
    origin_text = area_stage[0].text.replace('‐', '-')
    if origin_text[0] == 'H':
        return [0, 0]
    area_stage = origin_text.split('-')
    area = int(area_stage[0])
    stage = int(area_stage[1])
    return [area, stage]

def getRequireItemsInfo(soup, i, items):
    require_items_selctor = '#article-body > div.w-instant-database-list > div > table > tr:nth-child({}) > td:nth-child(2) > a'.format(i)
    origin_require_items = soup.select(require_items_selctor)

    ids = []
    for i in range(3):
        item_url = origin_require_items[i].get('href')
        if item_url not in ITEMURLID:
            a_soup = getSoupObject(item_url)
            item_name_selector = 'title'
            origin_item_name = a_soup.select(item_name_selector)

            title = origin_item_name[0].text
            pattern = '(?<=「).+(?=」.*)'
            result = re.search(pattern, title)
            item_name = result.group()

            for item in items['items']:
                if item['name'] != item_name:
                    continue
                ITEMURLID[item_url] = item['requirements'][0]['id']
            time.sleep(1)
        ids.append(ITEMURLID[item_url])
    return ids

def main():
    with open('cache.json', 'r') as f:
        ITEMURLID.update(json.load(f))
    with open('../src/components/items.json', 'r') as f:
        items = json.load(f)
    with open('../src/components/areas.json', 'r') as f:
        areas = json.load(f)

    soup = getSoupObject('https://gamewith.jp/pricone-re/article/show/130587')
    table = getTableInfo(soup)

    for i in tqdm(range(len(table))):
        area_number, stage_number = getAreaStageInfo(soup, i)
        if area_number == 0:
            continue

        for area in areas['areas']:
            if not (area['area'] == area_number and area['stage'] == stage_number):
                continue

            item_ids = getRequireItemsInfo(soup, i, items)

            for j in range(3):
                area['drops'][j]['id'] = item_ids[j]

        if i % 10 == 0:
            with open('../src/components/areas.json', 'w') as f:
                jd = json.dumps(areas, ensure_ascii=False)
                f.write(jd)
            with open('cache.json', 'w') as f:
                jd = json.dumps(ITEMURLID, ensure_ascii=False)
                f.write(jd)

    with open('../src/components/areas.json', 'w') as f:
        jd = json.dumps(areas, ensure_ascii=False)
        f.write(jd)
    with open('cache.json', 'w') as f:
        jd = json.dumps(ITEMURLID, ensure_ascii=False)
        f.write(jd)

if __name__ == '__main__':
    main()
