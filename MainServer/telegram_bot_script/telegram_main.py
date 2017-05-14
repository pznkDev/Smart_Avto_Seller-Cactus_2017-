import telegram_bot_script.telegram_const as const

import telebot

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from AutoApp import parser
from AutoApp.models import Model, Mark, Region

state_dict = {}

bot = telebot.TeleBot(const.token)


def send_msg_greeting(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('yes', 'no')
    bot.send_message(chat_id, const.msg_greeting, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_in_mark(chat_id):
    bot.send_message(chat_id, const.msg_in_mark, parse_mode='Markdown')


def send_msg_wrong_mark(chat_id, wrong_mark, possible_mark):
    markup_possible = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_possible.row(possible_mark)
    bot.send_message(chat_id, const.msg_wrong_mark % (wrong_mark, possible_mark), parse_mode='Markdown',\
                     reply_markup=markup_possible)


def send_msg_in_model(chat_id):
    bot.send_message(chat_id, const.msg_in_model, parse_mode='Markdown')


def send_msg_wrong_model(chat_id, wrong_model, possible_model):
    markup_possible = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_possible.row(possible_model)
    bot.send_message(chat_id, const.msg_wrong_mark % (wrong_model, possible_model), parse_mode='Markdown',
                     reply_markup=markup_possible)


def send_msg_in_region(chat_id):
    bot.send_message(chat_id, const.msg_in_region, parse_mode='Markdown')


def send_msg_wrong_region(chat_id, wrong_region, possible_region):
    markup_possible = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_possible.row(possible_region)
    bot.send_message(chat_id, const.msg_wrong_mark % (wrong_region, possible_region), parse_mode='Markdown',
                     reply_markup=markup_possible)


def send_msg_confirm_search(chat_id):
    markup_confirm = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_confirm.row('yes', 'no')

    request = state_dict[chat_id]

    bot.send_message(chat_id, const.msg_confirm_search
                     % (request['mark'], request['model'], request['region']),
                     parse_mode='Markdown', reply_markup=markup_confirm)


def main():

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        send_msg_greeting(message.chat.id)
        state_dict[message.chat.id] = {'cur_state': const.state_init}

    @bot.message_handler(content_types=['text'])
    def handle_command(message):
        msg_text = str(message.text).strip().lower()

        if msg_text in ['привет', 'hi', 'hello']:
            send_msg_greeting(message.chat.id)
            state_dict[message.chat.id] = {'cur_state': const.state_init}
        else:
            if message.chat.id in state_dict:
                print('Cur state ::: ', state_dict[message.chat.id])

                # get current state
                cur_state = state_dict[message.chat.id]['cur_state']

                if cur_state == const.state_init:
                    if msg_text == 'yes':
                        send_msg_in_mark(message.chat.id)
                        state_dict[message.chat.id]['cur_state'] = const.state_start
                    else:
                        bot.send_message(message.chat.id, const.msg_cancel, parse_mode='Markdown')
                        del state_dict[message.chat.id]

                elif cur_state == const.state_start:
                    marks_list = [mark.name.strip().lower() for mark in Mark.objects.all() if mark]
                    similarity = process.extractOne(msg_text, marks_list, scorer=fuzz.token_sort_ratio)

                    if similarity[1] == 100:
                        state_dict[message.chat.id]['mark'] = msg_text
                        state_dict[message.chat.id]['mark_id'] =\
                            [mark.value_id for mark in Mark.objects.all() if mark.name.strip().lower() == msg_text][0]
                        state_dict[message.chat.id]['cur_state'] = const.state_in_mark
                        send_msg_in_model(message.chat.id)
                        print('Cur state ::: ', state_dict[message.chat.id])
                    else:
                        send_msg_wrong_mark(message.chat.id, msg_text, similarity[0].capitalize())

                elif cur_state == const.state_in_mark:

                    models_list = [model.name.strip().lower() for model in Model.objects.all()
                                   if model.mark_id.strip().lower() == state_dict[message.chat.id]['mark']]
                    similarity = process.extractOne(msg_text, models_list, scorer=fuzz.token_sort_ratio)

                    if similarity[1] == 100:
                        state_dict[message.chat.id]['model'] = msg_text
                        state_dict[message.chat.id]['model_id'] = \
                            [model.value_id for model in Model.objects.all() if model.name.strip().lower() == msg_text][0]
                        state_dict[message.chat.id]['cur_state'] = const.state_in_model
                        send_msg_in_region(message.chat.id)
                        print('Cur state ::: ', state_dict[message.chat.id])
                    else:
                        send_msg_wrong_model(message.chat.id, msg_text, similarity[0].capitalize())

                elif cur_state == const.state_in_model:
                    regions_list = [region.name.strip().lower() for region in Region.objects.all()]
                    similarity = process.extractOne(msg_text, regions_list, scorer=fuzz.token_sort_ratio)

                    if similarity[1] == 100:
                        state_dict[message.chat.id]['region'] = msg_text
                        state_dict[message.chat.id]['region_id'] = \
                            [region.value_id for region in Region.objects.all() if region.name.strip().lower() == msg_text][0]
                        state_dict[message.chat.id]['cur_state'] = const.state_in_region
                        send_msg_confirm_search(message.chat.id)
                        print('Cur state ::: ', state_dict[message.chat.id])
                    else:
                        send_msg_wrong_region(message.chat.id, msg_text, similarity[0].capitalize())

                elif cur_state == const.state_in_region:
                    if msg_text == 'yes':

                        req_search = state_dict[message.chat.id]

                        parser.parse("https://auto.ria.com/search/?" +
                                     "category_id=1&" +
                                     "marka_id=" + str(req_search['mark_id']) +
                                     "&model_id=" + str(req_search['model_id']) +
                                     "&state%5B0%5D=" + str(req_search['region_id']) +
                                     "&s_yers%5B0%5D=0&" +
                                     "po_yers%5B0%5D=0&" +
                                     "price_ot=&" +
                                     "price_do=&" +
                                     "currency=1&" +
                                     "countpage=100")
                    else:
                        bot.send_message(message.chat.id, const.msg_cancel, parse_mode='Markdown')
                        del state_dict[message.chat.id]
            else:
                send_msg_greeting(message.chat.id)
                state_dict[message.chat.id] = {'cur_state': const.state_init}

    bot.polling(none_stop=True, interval=1)


def start_telegram_bot():
    print('Telegram bot: started successfully')
    main()
