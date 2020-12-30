import requests
import json
import time
from PIL import Image

game_varsion = "10.25.1"
item_info_url = 'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json'.format(game_varsion)

def item_icon_url(itemID):
	return 'http://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(game_varsion, itemID)

def saveItemIcon(item_info):
	itemIDs = item_info["data"].keys()
	for i,itemID in enumerate(itemIDs):		
		info = requests.get(item_icon_url(itemID))
		img = info.content
		with open("img/item/{}.png".format(itemID), "wb") as a:
			a.write(img)
		print("\r{}/{} saved".format(i, len(itemIDs)), end="")
		time.sleep(0.2)



def main():
	item_info = requests.get(item_info_url)
	item_info = item_info.json()

	#saveItemIcon(item_info)

	print(item_info["data"]["6662"]["image"])


if __name__ == '__main__':
	main()