import threading
import sys
import time

def hoge(num):
	print(num)
	time.sleep(num)
	print(num)

def makeThread(num):
	t = threading.Thread(target=hoge, args=(num,))
	t.setDaemon(True)
	t.start()

for i in range(5):
	makeThread(i)

time.sleep(3)