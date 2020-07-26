#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot, gdata
from compare_strings import getSim

TOKEN = "1352428807:AAEWMRagiUzg9cMiygyjHsixGZyPWwR4gzk"

bot = telebot.TeleBot(TOKEN) # инициализация бота

plot = []


#["плохо"][2]

def find_passage(passage_name):
	for passage in plot:
		if passage["name"] == passage_name:
			return passage

def find_answer(text, keys):
	max_value = 0
	for i in keys:
		if i == "*":
			max_value = 1.1
			max_object = i
		elif string_compare(i, text) > max_value:
			max_value = string_compare(i, text)
			max_object = i
	return max_object

def string_compare(first_string, second_string):
	return getSim(first_string, second_string)

def send_message(chat_id, message_text):
	if message_text.startswith("$file="):
		file_id = message_text[6:]
		message = bot.send_document(chat_id, file_id)
	elif message_text.startswith("$photo="):
		file_id = message_text[7:]
		message = bot.send_photo(chat_id, file_id)
	elif message_text.startswith("$video="):
		file_id = message_text[7:]
		message = bot.send_photo(chat_id, file_id)
	else:
		message = bot.send_message(chat_id, message_text)
	return message


@bot.message_handler(commands=["start"])
def on_start(message):
	pass

@bot.message_handler(func=lambda message: True)
def on_message(message):
	database = gdata.load()
	text = message.text
	user_id = str(message.from_user.id)

	if not(user_id) in database:
		database.update({user_id:["Начало", "Мистер X"]})

	user_name = database[user_id][1]
	user_queue = database[user_id][0]

	passage = find_passage(user_queue)

	output = list(map(str, str(passage["text"]).split("\n")))

	for text in output:
		send_message(user_id, text)

	




bot.polling()








