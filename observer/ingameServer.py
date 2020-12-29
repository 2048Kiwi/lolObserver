import json
import time
import threading


def loadJSON(name):
	global data
	data = open(name, 'r')
	data = json.load(data)

response = []


#サーバー用の関数------------------------------------------------------------
from wsgiref.simple_server import make_server
def app(environ, start_response):
	status = '200 OK'
	headers = [
    	('Content-type', 'application/json; charset=utf-8'),
    	('Access-Control-Allow-Origin', '*'),
	]
	start_response(status, headers)
	return response
	#return [json.dumps({'blue_level':[1,1,1,1,1]}).encode("utf-8")]

def startServer():
	with make_server('', 3000, app) as httpd:
		print("Serving on port 3000...")
		httpd.serve_forever()
#--------------------------------------------------------------------------

#ゲーム監視用の諸々----------------------------------------------------------
import pytesseract
import pyocr
import pyocr.builders
from PIL import Image
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
from levelChecker import initLevelImgBuff, levelBoxes, levelCheck
pytesseract.pytesseract.tesseract_cmd = r'G:\Program Files\Tesseract-OCR\tesseract.exe'
pyocr.tesseract.TESSERACT_CMD = r'G:\Program Files\Tesseract-OCR\tesseract.exe'

def screenShot():
	return ImageGrab.grab()

def getTime():
	return time.time()

def timeInit(num):
	timers = []
	for i in range(num):
		timers.append(getTime())
	return timers

def show(img):
	plt.imshow(img)
	plt.show()

def initState(level_boxes):
	champion_state = [{} for i in range(10)]
	for i in range(10):
		champion_state[i]["level"] = 3
		champion_state[i]["dead"] = False
	return champion_state

def printState(champion_state):
	print("------------------------------")
	for i in range(5):
		blueState = champion_state[i]
		blueOut = "{}: level={}, dead={}".format(i, blueState["level"], blueState["dead"])

		redState = champion_state[i+5]
		redOut = "{}: level={}, dead={}".format(i+5, redState["level"], redState["dead"])

		out = blueOut.ljust(30) + redOut
		print(out)

def lolObserver():
	global response
	#ゲームクライアントの原点座標（通常[0,0]）
	game_pos_offset = [0, 60]
	#レベル周りの座標設定
	level_pos_offset = [33, 188]
	level_box_size = [15, 8]
	level_X_interval = 1837
	level_Y_interval = 103
	level_boxes = levelBoxes( game_pos_offset, level_pos_offset, level_X_interval, level_Y_interval, level_box_size )

	champion_state = initState(level_boxes)
	levelImgBuff = initLevelImgBuff(screenShot(), level_boxes)

	auto_notice_levels = [6, 11, 16]
	auto_notice_frags = initFrags(auto_notice_levels)

	tools = pyocr.get_available_tools()
	if len(tools) == 0:
  		print('pyocrが見付かりません。pyocrをインストールして下さい。')

	timers = timeInit(1)
	dt = [1]
	state_update = False
	while True:

		if getTime() - timers[0] > dt[0]:
			img = screenShot()
			levelCheck(img, champion_state, level_boxes, levelImgBuff)
			state_update = True
			timers[0] = getTime()
			
		if state_update:
			printData(champion_state, auto_notice_levels, auto_notice_frags)

			#printState()
			#printJSON()
			print(data)
			response = [json.dumps(data).encode("utf-8")]
			state_update = False
		
#描画情報管理------------------------------------------------------------
def initFrags(levels):
	frags = []
	for i in range(len(levels)):
		buf = [True] * 10
		frags.append(buf)
	return frags

def upDownBanner(conf):
	smID, mode = conf
	data["banner"][smID] = mode
	time.sleep(3)
	data["banner"][smID] = "none"

def bannerManeger(smID, mode):
	t = threading.Thread(target=upDownBanner, args=([smID, mode],)) 
	t.setDaemon(True)
	t.start()

	
def printData(champion_state, levels, frags):
	for i,state in enumerate(champion_state):
		data["level"][i] = champion_state[i]["level"]
		for j,level in enumerate(levels):
			if frags[j][i] and state["level"] == level:
				frags[j][i] = False
				bannerManeger(i, "level")
		
#-------------------------------------------------------------------------
def main():
	loadJSON("data.json")

	t1 = threading.Thread(target=startServer)
	t2 = threading.Thread(target=lolObserver)

	t1.setDaemon(True)
	t2.setDaemon(True)

	t1.start()
	t2.start()

	while True:
		pass

if __name__ == '__main__':
	main()