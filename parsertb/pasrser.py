from bs4 import BeautifulSoup
import requests
import re
url = 'https://www.film.ru/compilation/luchshie-serialy-netflix-za-vse-vremya'

chart_data = ''

response = requests.get(url)

sup = BeautifulSoup(response.text, 'html.parser')

teg = sup.find_all('div', class_='redesign_afisha_movies')

data = []

for i in teg:
    zxc = i.text
    zxc_stripped = zxc.strip()
    zxc_no_spaces = re.sub(r'\s+', '', zxc)

    print(zxc_no_spaces)

# data = []


# for film in teg:
#     zxc = film.text
#     zxc = re.sub(r'\s+', ' ', zxc).strip()
#     match = re.match(r'(.*?) (\d{4}-\.\.\.) (.*?) / (.*?) film\.ru: (\d) зрители: ([\d.]+) IMDb: ([\d.]+)', zxc)
#     if match:
#         title, year, genre, country, rating, viewers, imdb = match.groups()
#         data.append({
#             'Название': title,
#             'Год': year,
#             'Жанр': genre,
#             'Страна': country,
#             'Рейтинг Film.ru': rating,
#             'Зрители': viewers,
#             'IMDb': imdb
#         })

# Выведите каждый элемент данных в удобном формате
# for item in data:
#     print(f"Название: {item['Название']}")
#     print(f"Год: {item['Год']}")
#     print(f"Жанр: {item['Жанр']}")
#     print(f"Страна: {item['Страна']}")
#     print(f"Рейтинг Film.ru: {item['Рейтинг Film.ru']}")
#     print(f"Зрители: {item['Зрители']}")
#     print(f"IMDb: {item['IMDb']}")
#     print()


