#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot, gdata
from compare_strings import getSimAlt as getSim
from random import randint as rint
from Plot import _plot
from telebot import types

import time

TOKEN = "1352428807:AAEWMRagiUzg9cMiygyjHsixGZyPWwR4gzk"

bot = telebot.TeleBot(TOKEN) # инициализация бота


plot = _plot
plot = plot["passages"]


#["плохо"][2]

def find_passage(passage_name):
	for passage in plot:
		if passage["name"] == passage_name:
			return passage

def find_answer(text, links):
	max_value = 0
	max_pname = None
	for link in links:
		link_text, passage_name = map(str, link["linkText"].split("|"))
		strc = string_compare(link_text, text)
		if link_text in ["*", "/start"]:
			max_value = 1.1
			max_text = link_text
			max_pname = passage_name
		elif strc > max_value:
			max_value = strc
			max_text = link_text
			max_pname = passage_name
			if max_value == 1:
				break
	if links:
		if link_text == "~" and not(max_pname):
			max_pname = passage_name

	return max_pname

def string_compare(first_string, second_string):
	return getSim(first_string, second_string)

def send_message(chat_id, message_text, robot=False):
	if "reconnect" in message_text:
		bot.send_chat_action(chat_id, "upload_video")
		time.sleep(rint(1,4))
		message = None
	elif message_text.startswith("time"):
		time.sleep(rint(2,5))
		message = None
	elif message_text.startswith("$file="):
		if not(robot):
			time.sleep(rint(2,6))
			bot.send_chat_action(chat_id, "upload_document")
			time.sleep(rint(1,3))
		file_id = message_text[6:]
		message = bot.send_document(chat_id, file_id)
	elif message_text.startswith("$photo="):
		if not(robot):
			time.sleep(rint(2,6))
			bot.send_chat_action(chat_id, "upload_photo")
			time.sleep(rint(1,3)) 
		file_id = message_text[7:]
		message = bot.send_photo(chat_id, file_id)
	elif message_text.startswith("$video="):
		if not(robot):
			time.sleep(rint(2,6))
			bot.send_chat_action(chat_id, "upload_video")
			time.sleep(rint(1,3))
		file_id = message_text[7:]
		message = bot.send_photo(chat_id, file_id)
	else:
		if not(robot):
			# time.sleep(rint(2,6))
			bot.send_chat_action(chat_id, "typing")
			time.sleep(7*len(message_text)/100)
		db = gdata.load()
		message = bot.send_message(chat_id, message_text.format(name=db[chat_id][1]), parse_mode="Markdown")
	return message

def on_text_error(chat_id):
	bot.send_message(chat_id, "***Связь прервалась***\n\n`Возможно, линия связи не поддерживает введенный вами смысловой контекст`", parse_mode="Markdown")
	time.sleep(1)
	bot.send_message(chat_id, "***Пытаемся подсоединиться к объекту***", parse_mode="Markdown")
	bot.send_chat_action(chat_id, "upload_video_note")
	time.sleep(rint(2,5))
	bot.send_message(chat_id, "***Соединение установлено***", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def on_message(message):
	if message.chat.id in busylist:
		pass
	else:
		busylist.append(message.chat.id)
		database = gdata.load()
		text = message.text
		user_id = str(message.from_user.id)

		if not(user_id) in database:
			database.update({user_id:["Начало", "Мистер X", 3000, 0]})
			gdata.update(database)
			database = gdata.load()

		user_name = database[user_id][1]
		user_queue = database[user_id][0]

		passage = find_passage(user_queue)
		links = passage["links"]

		txt = message.text
		bot.send_chat_action(user_id, "upload_video")
		if "выбор" in passage["tags"]:
			db = gdata.load()
			res = db[user_id][3]
			if res > 0:
				txt = "справедливость"
			else:
				txt = "рациональность"
		link_name = find_answer(txt, links)
		if link_name:
			passage = find_passage(link_name)
			output = list(map(str, str(passage["cleanText"]).split("\n")))
			tags = passage["tags"]
			links = passage["links"]
			if "подключение" in tags:
				send_message(user_id, "Идёт подключение...", robot=True)
				send_message(user_id, "reconnect")
				send_message(user_id, "Подключено.\n_Код сессии:_ `{code}`".format(code=rint(1000000, 10000000)), robot=True)
			if "справедливость" in tags:
				db = gdata.load()
				db[user_id][3] = db[user_id][3] + 1
				print(db)
				gdata.update(db)
			if "рациональность" in tags:
				db = gdata.load()
				db[user_id][3] = db[user_id][3] - 1
				print(db)
				gdata.update(db)
			if "удача" in tags:
				db = gdata.load()
				db[user_id][2] = db[user_id][2] + 1000
				print(db)
				gdata.update(db)
			if "неудача" in tags:
				db = gdata.load()
				db[user_id][2] = db[user_id][2] - 1000
				gdata.update(db)
			database = gdata.load()
			if "конецобъекта" in tags:
				send_message(user_id, "*На вашем счету:* `{0}` _E-Coin_".format(database[user_id][2]), robot=True)
			while "" in output:
				output.remove("")
			for text in output:
				if text.startswith("robo:"):
					text = text[5:]
					send_message(user_id, text, robot=True)
				else:
					send_message(user_id, text)
			if "полиция" in tags:
				send_message(user_id, "*Система автоматического определения контекста зафиксировала просьбу о вызове службы спасения*\n\n_Подтведите вызов(Вызвать/Это ошибка)..._", robot=True)
			if "клавиатура" in tags:
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
				for link in links:
					link_text, passage_name = map(str, link["linkText"].split("|"))
					markup.row(types.KeyboardButton(link_text))

				bot.send_message(user_id, "$%#@%^&", reply_markup=markup)
			if "концовка" in tags:
				database.pop(user_id)
			else:
				database[user_id][0] = link_name
			gdata.update(database)
		else:
			on_text_error(user_id)
		busylist.remove(message.chat.id)

if __name__ == "__main__":
	global busylist
	busylist = []
	while True:
		try:
			bot.polling()
		except Exception as e:
			print(e)
			bot.send_message(316490607, e)
			time.sleep(15)








