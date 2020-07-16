#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot

TOKEN = ""

bot = telebot.TeleBot(TOKEN) # инициализация бота
[["*", ["Привет! Как дела у тебя?"], [[["Нормально", "хорошо", "отлично"], ["это круто, да"], []]]]]

dictt = {
"*":[["Привет! Как дела у тебя?"], [], {
	"нормально":[["Это очень хорошо!"], ["*"], {}],
	"плохо":[["хреново...", "а у нее?"], ["*"], {
		"хорошо":[["понятно..."], ["*", "плохо"], {
			"ага":[["конец..."], "end", {}],
		}],
		"плохо":[["хреново...", "а у нее?"], ["*", "плохо"], {
			"агась":[["конец..."], "end", {}],
		}]
	}]
}]
}

#["плохо"][2]

database = {}

@bot.message_handler(func=lambda message: True)
def on_message(message):
	text = message.text
	user_id = message.from_user.id

	if not(user_id) in database:
		database.update({user_id:[[], "Мистер X"]})

	user_name = database[user_id][1]
	user_queue = database[user_id][0]

	pos = dictt
	for i in user_queue:
		pos = pos[i]

	keys = pos.keys()
	