import time
import datetime
import Adafruit_SSD1306
from pygame import mixer
import pygame
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os.path

date = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S Dracula service started....')
print(date)

# import evdev
from evdev import InputDevice, categorize, ecodes
keyboard = InputDevice('/dev/input/event0')
keyboard.grab();

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

disp.begin()
disp.clear()
disp.display()

mixer.init()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

font = ImageFont.truetype('/home/dracula/dracula/freecam2.ttf', 32)
font2 = ImageFont.truetype('/home/dracula/dracula/freecam2.ttf', 10)

number = "";
pos = 0;

def playSong(song):
	mixer.music.load(song)
	mixer.music.play()
	while mixer.music.get_busy() == True:
		ev=keyboard.read_one();
		if not ev:
			continue;
		if ev is not None and ev.type == ecodes.EV_KEY:
			evc=categorize(ev)
			key = ecodes.keys[ev.code]
			if key == "KEY_BACKSPACE":
				mixer.music.fadeout(3000); 
				printText("---"); 
				break; 
			else: 
				continue
	printText("xxx");

def clearDisplay():
	draw.rectangle((0,0,width,height), outline=0, fill=0)

def reset():
	global number, pos
	pos =0;
	number="";

def getNumber(keyCode):
	global pos, number;
	value = -1;
	print(keyCode);
	if keyCode == "KEY_KP1":
		value=1;
	if keyCode == "KEY_KP2":
		value=2;
	if keyCode == "KEY_KP3":
		value=3;
	if keyCode == "KEY_KP4":
		value=4;
	if keyCode == "KEY_KP5":
		value=5;
	if keyCode == "KEY_KP6":
		value=6;
	if keyCode == "KEY_KP7":
		value=7;
	if keyCode == "KEY_KP8":
		value=8;
	if keyCode == "KEY_KP9":
		value=9;
	if keyCode == "KEY_KP0":
		value=0;
	if keyCode == "KEY_BACKSPACE":
		value=9999;
		print("RESET BY BACKSPACE")
		printText("---");
		reset();
	if keyCode == "KEY_KPENTER":
		value=1000;
		print("SONG NUMBER", number)
		song="/var/www/" + number + ".mp3"
		if os.path.isfile(song):
			printText("PLAY");
			playSong(song);
			printText("CAJK");
		else:
			printText("NENI")
		reset();

	if(value>-1 and value<10 and pos<3):
		pos=pos+1;
		number=number+str(value);
		printText(number);

def waitForNumber():
	global number, pos
	pos = 0;
	for event in keyboard.read_loop():
		if event.type == ecodes.EV_KEY:
			ev = categorize(event);
			if(ev.keystate == 1):
				getNumber(ev.keycode);

def printText(msg, x=0, y=0):
	clearDisplay();
	draw.text((x,y), msg,  font=font, fill=255)
	disp.image(image)
	disp.display()

printText("RUN!") 
while True: 
	waitForNumber();
