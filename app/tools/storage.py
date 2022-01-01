import json
import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))
from constant import APP_DEBUG

data = {}
data["history"] = []
data["users"] = []
data["r_d"] = ""
data["main_port"] = ""

BASE_DIR = f"c:/users/{os.getlogin()}/.zeta"

if not os.path.exists(BASE_DIR):
	os.mkdir(BASE_DIR)
STORAGE_PATH = f"{BASE_DIR}/storage.json"

if APP_DEBUG:
	from  random import randrange
	STORAGE_PATH = f"c:/users/{os.getlogin()}/documents/storage{randrange(10, 90)}.json"

def dumpStorage(data):
	with open(STORAGE_PATH, "w") as storage:
		json.dump(data, storage, indent=4)

def loadStorage():
	if not os.path.exists(STORAGE_PATH): create_database()
	with open(STORAGE_PATH, "r") as storage:
		return json.load(storage)

def create_database():
	dumpStorage(data)

def save_history(h_data):
	if not os.path.exists(STORAGE_PATH): create_database()
	base = loadStorage()
	base['history'].append(h_data)
	dumpStorage(base)

def save_r_d(dir):
	if not os.path.exists(STORAGE_PATH): create_database()
	base = loadStorage()
	base['r_d'] = dir
	dumpStorage(base)

def load_r_d():
	return loadStorage()["r_d"]

def load(key):
	return loadStorage()[key]

def loadById(key,id) -> dict:
	tmp : int = 0
	for i in load(key):
		if tmp == id:
			return i
		tmp	+= 1
	return {}
def set_(key, value):
	if not os.path.exists(STORAGE_PATH): create_database()
	base = loadStorage()
	base[key] = value
	dumpStorage(base)
def load_history():
	return loadStorage()["history"]

def format_file_name(filename, max_s=15):
	if len(filename) > max_s:
		name, extention = filename.split(".")[-2:]
		return f"{name[:max_s]}...{extention}"
	return filename


def destination_path():
    if load_r_d() == "":
        return f"c:/users/{os.getlogin()}/desktop"
    return load_r_d()


def units_conv(size):
	units = {
		"b": "Bytes",
		"m" : "Mo",
		"k" : "Ko",
		"g" : "Go"
	}

	s, unit = size.split(" ")
	s = int(s)

	while unit.lower() != units["g"].lower():

		if unit.lower() == units["b"].lower() and s < 1000:
			break
		if unit.lower() == units["m"].lower() and s < 1000:
			break
		if unit.lower() == units["k"].lower() and s < 1000:
			break


		if unit.lower() == units["b"].lower():
			s /= 1024
			unit = units["k"]

		if unit.lower() == units["k"].lower() and s > 1000:
			s /= 1024
			unit = units["m"]

		if unit.lower() == units["m"].lower() and s > 1000:
			s  /= 1024
			unit = units["g"]

	return f"{round(s, 1)} {unit}"

fileType = {
	"image":"jpg png jpeg",
	"video":"mp4 avi",
	"audio":"mp3",
	"compressed":"zip iso rar",
	"document":"doc pdf docx txt",
	"Application":"exe smi",
	"Photoshop":"psd",
	"Figma":"fig",
}

def titled(func):
	def wrapper(*args,**kwargs):
		return func(*args,**kwargs).title()
	return wrapper

def cutFileName(filename):
	# print()
	if "(" in filename: filename = filename.replace("(",'')
	if ")" in filename: filename = filename.replace(")",'')
	print(len("".join(filename.split(".")[:-1])))

	if "/" in filename:
		filename = filename.split("/")[-1]
	if len("".join(filename.split(".")[:-1])) <= 40: return filename
	loop = len(filename) // 40
	name = list(filename)
	for i in range(1,loop):
		a = 40*i
		name[40*i] = "-\n"
	return "".join(name)

@titled
def getFileType(filename):
	extension = filename.split(".")[-1]
	for k,v in fileType.items():
		if extension in v:
			return k
	return "Unknown"

			









