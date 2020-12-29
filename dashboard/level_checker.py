# -*- coding: utf-8 -*-
import time

import pytesseract
import pyocr
import pyocr.builders
from PIL import Image
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'G:\Program Files\Tesseract-OCR\tesseract.exe'
pyocr.tesseract.TESSERACT_CMD = r'G:\Program Files\Tesseract-OCR\tesseract.exe'


def levelBoxes(pos0, pos1, ix, iy, box_size):
	x0 = pos0[0] + pos1[0]
	y0 = pos0[1] + pos1[1]
	bx, by = box_size
	blue_level_poss = []
	red_level_poss = []
	for i in range(5):
		y = y0 + iy*i
		blue_level_poss.append([x0, y, x0+bx, y+by])
		red_level_poss.append([x0+ix, y, x0+ix+bx, y+by])

	return blue_level_poss + red_level_poss

def img2num(img, tool, bw_threshold, rate, show_img=False):
	#img = np.array(img.convert('L'))
	#img = (img > bw_threshold) * 255
	#img = Image.fromarray(np.uint8(img))
	if rate!=1: img = img.resize((img.width*rate, img.height*rate))

	builder = pyocr.builders.TextBuilder(tesseract_layout=6)
	builder.tesseract_configs.append("digits")
	num = tool.image_to_string(img, lang='eng', builder=builder)

	if show_img:
		plt.imshow(img)
		plt.show()

	return num

def screenShot():
	return ImageGrab.grab()

def getTime():
	return time.time()

def show(img):
	plt.imshow(img)
	plt.show()

def printState(champion_state):
	print("------------------------------")
	for i in range(5):
		blueState = champion_state[i]
		blueOut = "{}: level={}, dead={}".format(i, blueState["level"], blueState["dead"])

		redState = champion_state[i+5]
		redOut = "{}: level={}, dead={}".format(i+5, redState["level"], redState["dead"])

		out = blueOut.ljust(30) + redOut
		print(out)
		

def isDead(img):
	#img = np.array(img)
	for i in img:
		for j in i:
			if not(j[0]==j[1] and j[1]==j[2]):
				return False
	return True

def initState(level_boxes):
	game_img = screenShot()
	state = [{} for i in range(10)]
	for i in range(10):
		state[i]["level"] = 3
		state[i]["dead"] = False
		img = game_img.crop(level_boxes[i])
		state[i]["level_img"] = np.array(img)
	return state

def levelCheck(game_img, champion_state, level_boxes):
	for i, state in enumerate(champion_state):
		img = game_img.crop(level_boxes[i])
		img = np.array(img)
		#print(level_boxes[i])
		#show(img)
		state["dead"] = isDead(img)
		if (not state["dead"]) and (not np.array_equal(img, state["level_img"])):
			if (i<5 and (img[0][14]==state["level_img"][0][14]).all()) or (i>=5 and (img[0][0]==state["level_img"][0][0]).all()):
				state["level"] += 1
				state["level_img"] = img


def main():
	url_img = r'.\img\test.png'

	#ゲームクライアントの原点座標（通常[0,0]）
	game_pos_offset = [0, 60]
	#レベル周りの座標設定
	level_pos_offset = [33, 188]
	level_box_size = [15, 8]
	level_X_interval = 1837
	level_Y_interval = 103
	level_boxes = levelBoxes( game_pos_offset, level_pos_offset, level_X_interval, level_Y_interval, level_box_size )

	champion_state = initState(level_boxes)
	printState(champion_state)

	tools = pyocr.get_available_tools()
	if len(tools) == 0:
  		print('pyocrが見付かりません。pyocrをインストールして下さい。')

	start_time = getTime()
	while(True):
		if getTime()-start_time > 1:
			img = screenShot()
			levelCheck(img, champion_state, level_boxes)

			printState(champion_state)
			process_time = int(1000*(getTime()-start_time-1))
			print("process time = {}[ms]".format(process_time))
			start_time = getTime()
			
	#img = Image.open(url_img)
	#for i in range(10):
	#	num = img2num(img.crop(level_boxes[i]), tool, 150, 1, True)
	#	print([i,num])

if __name__ == '__main__':
	main()