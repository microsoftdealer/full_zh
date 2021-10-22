import aiohttp
from bs4 import BeautifulSoup
from typing import List, Union, Tuple
from datetime import datetime
from dateutil import parser
import re


async def get(url, headers=None, image=None, params=None):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url, headers=headers, params=params, timeout=60.0) as response:
            headers = response.headers
            if image:
                img = await response.read()
                return headers, img
            text = await response.text()
            return text, headers


async def get_golden_keys():
    url = 'https://owwya.com/borderlands-3-shift-codes/'
    text, _ = await get(url)
    bs = BeautifulSoup(text, 'html.parser')
    inner_content = bs.find('div', {'class': 'content-inner'})
    codes_list = inner_content.find_all('li')
    return codes_parser([code.text for code in codes_list])


def codes_parser(codes_list: List[str]) -> List[str]:
    pattern = r'((\w{5}-){4}\w{5}).+(\d+).+\(\w+\s\w+\s(.+,.*?\d+).+[)]'
    pattern_permanent = r'((\w{5}-){4}\w{5}).+(\d+).+\((Permanent)'
    parsed_code_list = []
    for code in codes_list:
        look = re.search(pattern, code)
        look_permanent = re.search(pattern_permanent, code)
        if look:
            groups = look.groups()
            if len(groups) > 2 and date_validator(groups[3])[1]:
                parsed_code_list.append(f'Актуальный Shift код: {groups[0]}\n'
                                        f'Валиден до {date_validator(groups[3])[0]}\n'
                                        f'Кол-во золотых ключей: {groups[2]}')
        elif look_permanent:
            groups = look_permanent.groups()
            if len(groups) > 2:
                parsed_code_list.append(f'Постоянный Shift код: {groups[0]}\n'
                                        f'Кол-во золотых ключей: {groups[2]}')
    return parsed_code_list


def date_validator(eng_date: str) -> Tuple[str, bool]:
    month_dict = {
        1: 'Января',
        2: 'Февраля',
        3: 'Марта',
        4: 'Апреля',
        5: 'Мая',
        6: 'Июня',
        7: 'Июля',
        8: 'Августа',
        9: 'Сентября',
        10: 'Октбяря',
        11: 'Ноября',
        12: 'Декабря',
    }
    code_time = parser.parse(eng_date)
    today_time = datetime.now()
    if today_time <= code_time:
        return f'{code_time.day} {month_dict[code_time.month]} {code_time.year}', True
    else:
        return 'Код неактивен', False


def test_sum():
    isinstance()