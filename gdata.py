import json

def load():
	with open("data.json", "r") as f:
		return json.load(f)

def update(obj):
	with open("data.json", "w") as f:
		json.dump(obj, f)

def loadCorpus():
	with open("ParaPhraserPlus.json", "r", encoding="utf-8") as f:
		return json.load(f)

def updateCorpus(obj):
	with open("corpus.json", "w", encoding="utf-8") as f:
		json.dump(obj, f)