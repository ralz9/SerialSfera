from telebot import types
from datetime import datetime, timedelta
import telebot
bot = telebot.TeleBot('6551792134:AAEFznOE8COt0AS-swdKyMIegkPHz3DlWWk')
import requests

def conn(message):
    bot.send_message(message.chat.id, "тех поддержка\n "
                                      "+996 507 812 318 - Родион \n "
                                      "+996 709 010 204 - Арлен \n ")


@bot.message_handler(commands=['connection'])
def connection_get(message):
    conn(message)


@bot.message_handler(commands=['chart'])
def send_chart(message):
    try:
        with open('serial_data.txt', 'r') as file:
            chart_data = file.read().split('\n\n')
            for line in chart_data:
                bot.send_message(message.chat.id, line.strip())
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл с данными не найден.")


@bot.message_handler(commands=['site'])
def website(message):
    site_url = "http://35.198.162.176/"

    markup = types.InlineKeyboardMarkup()
    site_button = types.InlineKeyboardButton("Перейти на сайт", url=site_url)
    markup.add(site_button)

    bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы перейти на наш сайт:", reply_markup=markup)





@bot.message_handler(commands=['get_data'])
def handle_start(message):
    response = requests.get('http://34.159.136.83/api/v1/series/recommendations/')
    if response.status_code == 200:
        bot_messages = response.json()
        if bot_messages is not None:
            for message_data in bot_messages:
                title = message_data['title']
                description = message_data['description']
                rating = message_data['rating']
                like = message_data['like_count']
                count_views = message_data['count_views']
                vendor_code = message_data['vendor_code']
                message_text = f"Заголовок: {title}\n" \
                               f"О Сериале: {description}\n" \
                               f"Количество просмотров: {count_views}\n" \
                               f"Артикул: {vendor_code}\n" \
                               f"Рейтинг: {rating}\n" \
                               f"Лайки: {like}"
                bot.send_message(message.chat.id, text=message_text)
        else:
            bot.send_message(message.chat.id, 'Данные отсутствуют.')
    else:
        bot.send_message(message.chat.id, 'Не удалось получить данные.')




@bot.message_handler(commands=['info'])
def send_hello(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Обратная связь", callback_data='privet')
    markup.add(button)
    bot.send_message(message.chat.id, 'Приветствую', reply_markup=markup)


@bot.message_handler(commands=['start', 'restart'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Переход на сайт')
    item2 = types.KeyboardButton('Чарт сериалов')
    item3 = types.KeyboardButton('Рекомендации')
    item4 = types.KeyboardButton('Информация')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Переход на сайт')
def handle_website_button(message):
    site_url = "http://35.198.162.176/api/v1/series"  # Замените на URL вашего сайта
    bot.send_message(message.chat.id, f"Перейдите на наш сайт: {site_url}")
@bot.message_handler(func=lambda message: message.text == 'Чарт сериалов')
def handle_website_button(message):
    send_chart(message)

@bot.message_handler(func=lambda message: message.text == 'Рекомендации')
def handle_website_button(message):
    handle_start(message)

@bot.message_handler(func=lambda message: message.text == 'Информация')
def handle_website_button(message):
    send_hello(message)

if __name__ == "__main__":
    bot.polling(none_stop=True)



if __name__ == '__main__':
    bot.polling(none_stop=True)