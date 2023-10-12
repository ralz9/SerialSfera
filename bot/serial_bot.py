# import telebot
# import requests
# import webbrowser
# from bs4 import BeautifulSoup
# from telebot import types
#
# bot = telebot.TeleBot('6614341358:AAHa0ENRf9T93pVtU75aWAwJZNv4YkZtfkE')
#
#
# def scrape_serial_titles():
#     url = 'http://35.198.162.176/api/v1/series/'
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # Здесь добавьте код для извлечения названий сериалов
#         # Например, если названия находятся в элементах <div> с классом "serial-title":
#         serial_titles = [element.text for element in soup.find_all('div', class_='response-info', span_='')]
#         return serial_titles
#     else:
#         return []
#
#
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton('Сериалы')
#     markup.add(item1)
#     bot.send_message(message.chat.id, 'Привет! Чем могу помочь?', reply_markup=markup)
#
#
# @bot.message_handler(func=lambda message: message.text == 'Сериалы')
# def get_serials(message):
#     serial_titles = scrape_serial_titles()
#     if serial_titles:
#         bot.send_message(message.chat.id, 'Вот список сериалов:\n' + '\n'.join(serial_titles))
#     else:
#         bot.send_message(message.chat.id, 'Не удалось получить список сериалов.')
#
# bot.polling(none_stop=True)
#
#
