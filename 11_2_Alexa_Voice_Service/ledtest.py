#-*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_ask import Ask, statement
from gpiozero import LEDBoard
import time

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT)

led = LEDBoard(18)

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
	return "Raspberry pi LED control"

@ask.launch
def start_skill():
	welcome_message = "Hi, Welcome to Raspberry pi."
	return statement(welcome_message)

@ask.intent("ledonIntent")
def ledonIntent():
	led.on()
	time.sleep(1)
	text = "Ok, LED is turn on"
	return statement(text)

@ask.intent("ledoffIntent")
def ledoffIntent():
	led.off()
	time.sleep(1)
	text = "Ok, LED was turned off"
	return statement(text)

if __name__ == "__main__":
	app.run(port=5000, debug= True)
