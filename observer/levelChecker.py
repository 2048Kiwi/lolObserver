import numpy as np

def initLevelImgBuff(game_img, level_boxes):
	imgs = []
	for i in range(10):
		img = game_img.crop(level_boxes[i])
		imgs.append(np.array(img))
	return imgs

def isDead(img):
	for i in img:
		for j in i:
			if not(j[0]==j[1] and j[1]==j[2]):
				return False
	return True

def levelCheck(game_img, champion_state, level_boxes, levelImgBuff):
	for i, state in enumerate(champion_state):
		img = game_img.crop(level_boxes[i])
		img = np.array(img)
		#print(level_boxes[i])
		#show(img)
		state["dead"] = isDead(img)
		if (not state["dead"]) and (not np.array_equal(img, levelImgBuff[i])):
			if (i<5 and (img[0][14]==levelImgBuff[i][0][14]).all()) or (i>=5 and (img[0][0]==levelImgBuff[i][0][0]).all()):
				state["level"] += 1
				levelImgBuff[i] = img

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