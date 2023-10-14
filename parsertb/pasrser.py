from bs4 import BeautifulSoup
import requests

url = 'https://www.kp.ru/putevoditel/serialy/katalog/2023/'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

teg = bs.find_all('div', class_='large-4 medium-4 small-6 cell')


output_text = ""

for i in teg:
    img_tags = i.find('img')
    zxc = i.text
    zxc_stripped = zxc.strip()
    img_src = img_tags.get('data-lazy-src')


    lines = zxc_stripped.split('\n')
    series = lines[4]
    rating = lines[-1]

    output_text += f"\nСериал: {series}\n"
    output_text += f"Рейтинг: {rating}\n"

    if img_src:
        output_text += f"Изображение:\n{img_src}\n\n"


    print(output_text)



with open('serial_data.txt', 'w', encoding='utf-8') as file:
    file.write(output_text)



