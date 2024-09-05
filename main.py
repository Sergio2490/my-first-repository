import telebot
import datetime
import time
import threading
import random

first_rem = ''
second_rem = ''
end_rem = ''

bot = telebot.TeleBot('введите токен')

@bot.message_handler(commands=['start'])  # декоратор
def start_message(message):  # сейчас мы б. обрабат. команду /start
    bot.reply_to(message,
                 'Привет! Я чат-бот, который будет напоминать тебе изучать английский. Используй команду /help для просмотра доступных команд.')
    # - рандомный факт об изучении Английского')
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, '/fact - рандомный факт об изучении Английского; \n/settime - для ввода времени напоминания')

@bot.message_handler(commands=['settime'])
def settime_message(message):
    bot.reply_to(message,'Введите через запятую три времени напоминания в формате ЧЧ:ММ,ЧЧ:ММ,ЧЧ:ММ(например,08:00,14:00,20:00):')
    bot.register_next_step_handler(message, func_settime)  # регистрируем следующую ф-цию, к-я б. вызвана после ввода пользователя

def func_settime(message):
    global first_rem, second_rem, end_rem
    try:
        times = message.text.split(',')  # split - метод строки, который разбивает строку на СПИСОК подстрок.
                                         # ЗПТ - это разделитель, по к-му строка б. разбита. times = ['08:00', '14:00', '20:00']
        if len(times) == 3:  # если в списке 3 эл-та, то ОК
            first_rem, second_rem, end_rem = times
            first_rem = first_rem.strip()
            second_rem = second_rem.strip()
            end_rem = end_rem.strip()
            bot.reply_to(message, f'Времена напоминаний установлены: {first_rem}, {second_rem}, {end_rem}')
        else:
            bot.reply_to(message, 'Ошибка: Пожалуйста, снова запустите /settime и введите три времени через запятую в формате ЧЧ:ММ,ЧЧ:ММ,ЧЧ:ММ')
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка при обработке времени. Пожалуйста, попробуйте снова')


@bot.message_handler(commands=['fact'])  # декоратор
def fact_message(message):  # сейчас мы б. обрабат. команду /start
    list = [
        ' **Расширение карьерных возможностей**: Владея английским языком, вы открываете для себя больше карьерных перспектив. Многие международные компании и организации используют английский как основной рабочий язык. Это может повысить вашу конкурентоспособность на рынке труда и открыть двери к новым профессиональным возможностям.',
        '**Доступ к информации и ресурсам**: Английский язык является основным языком в интернете, а также в научных и академических публикациях. Изучение английского позволяет вам получать доступ к обширному количеству информации, включая книги, статьи, исследования и обучающие материалы, которые могут быть недоступны на вашем родном языке.',
        '**Улучшение когнитивных способностей**: Изучение нового языка, такого как английский, способствует улучшению когнитивных функций. Это включает в себя повышение памяти, развитие способности к многозадачности и улучшение навыков решения проблем. Изучение языков также связано с замедлением когнитивного старения и снижением риска развития деменции.'
    ]
    random_fact = random.choice(list)
    bot.reply_to(message, f'Лови факт об Английском {random_fact}')


def send_reminders(chat_id):  # ф-я напоминалка, chat_id - идентификатор чата
    global first_rem, second_rem, end_rem
    while True:  # бесконечный цикл, к-й отслеживает время
        now = datetime.datetime.now().strftime('%H:%M')  # из даты-время берем только текущее время
        if now == first_rem:
            bot.send_message(chat_id, 'Напоминание - время учить Английский утром (или первый раз)!')  # уже send_massage, а не reply_to
            # time.sleep(61)  #время в перем-й now б. держаться в течение минуты. И целую минуту мы б. получать напоминания. Поэт, делаем задержку, ф-ция time.sleep() из модуля time
        elif now == second_rem:
            bot.send_message(chat_id, 'Напоминание - время учить Английский днем (или второй раз)!')

        elif now == end_rem:
            bot.send_message(chat_id, 'Напоминание - время учить Английский вечером (или третий раз)!')

        time.sleep(55)


bot.polling(none_stop=True)  # запукс бота, эта команда всегда дб в конце!
