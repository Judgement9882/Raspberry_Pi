from gpiozero import LEDBoard, Button
from time import sleep
from datetime import datetime
import random
import os
import argparse
from omxplayer.player import OMXPlayer

button = Button(21)
now = datetime.now()

speechlist = ["지금은 now.year 년 now.month월 now.day일 now.hour시 now.minute분 now.second초야", "현재 시간은 now.hour시 now.minute분 now.second초에요", "오늘은 화요일이고, now.hour시 now.minute분이야", "안녕하세요. now.hour시 now.minute분이에요. 즐거운 하루되세요", "오늘은 now.year년 now.month월 now.day일이고, 지금은 now.hour시 now.minute분이에요. 행복하세요"]

def tts(text):
	"""Synthesizes speech from the input string of text."""
	from google.cloud import texttospeech

	client = texttospeech.TextToSpeechClient()

	input_text = texttospeech.SynthesisInput(text=text)

	# Note: the voice can also be specified by name.
	# Names of voices can be retrieved with client.list_voices().
	voice = texttospeech.VoiceSelectionParams(
		language_code="ko-KR",
		name="ko-KR-Wavenet-C",
		ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
	)

	audio_config = texttospeech.AudioConfig(
		audio_encoding=texttospeech.AudioEncoding.MP3
	)

	response = client.synthesize_speech(
		request={"input": input_text, "voice": voice, "audio_config": audio_config}
	)

	# The response's audio_content is binary.
	with open("output.mp3", "wb") as out:
		out.write(response.audio_content)
		print('Audio content written to file "output.mp3"')


# [END tts_synthesize_text]



while True:
	if button.is_pressed:
		tts(random.choice(speechlist))
		