#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot

TOKEN = "1352428807:AAEWMRagiUzg9cMiygyjHsixGZyPWwR4gzk"

bot = telebot.TeleBot(TOKEN) # инициализация бота
[["*", ["Привет! Как дела у тебя?"], [[["Нормально", "хорошо", "отлично"], ["это круто, да"], []]]]]

dictt = [None, None, {
"*":[["Привет! Как дела у тебя?"], ["*"], {
	"нормально":[["Это очень хорошо!"], ["*", "плохо"], {}],
	"плохо":[["хреново...", "а у нее?"], ["*", "плохо"], {
		"хорошо":[["понятно..."], ["*", "плохо", "хорошо"], {
			"ага":[["конец..."], "end", {}],
		}],
		"плохо":[["хреново...", "а у нее?"], ["*", "плохо", "плохо"], {
			"агась":[["конец..."], "end", {}],
		}]
	}]
}]
}]

#["плохо"][2]

def string_compare(first_string, second_string):
	return float(first_string == second_string)

database = {}

@bot.message_handler(func=lambda message: True)
def on_message(message):
	text = message.text
	user_id = message.from_user.id

	if not(user_id) in database:
		database.update({user_id:[[], "Мистер X"]})

	user_name = database[user_id][1]
	user_queue = database[user_id][0]
	print(user_queue)

	pos = dictt[2]
	ch = False
	for i in user_queue:
		print(pos); print("\n\n")
		pos = pos[i]
		ch = True
	if ch:
		pos = pos[2]

	# print(pos)

	keys = pos.keys()

	print(keys)

	for i in keys:
		max_value = 0
		if string_compare(i, text) > max_value:
			max_value = string_compare(i, text)
			max_object = i

	user_queue.append(max_object)
	pos = pos[max_object]

	for i in pos[0]:
		bot.send_message(message.chat.id, i)

	database[user_id][0] = pos[1]





bot.polling()








