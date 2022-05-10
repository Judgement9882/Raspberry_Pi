import argparse
import os
from gpiozero import LEDBoard, Button

def LEDLight(text):
    if text.find("켜 줘") >= 0:
        if text.find("첫 번째") >= 0:
            leds[0].on()
        elif text.find("두 번째")>=0:
            leds[1].on()
        elif text.find("세 번째")>=0:
            leds[2].on()
        elif text.find("마지막")>=0:
            leds[3].on()
        elif text.find("전부")>=0:
            for i in range(4):
                leds[i].on()

    elif text.find("꺼 줘")>=0:
        if text.find("첫 번째")>=0:
            leds[0].off()
        elif text.find("두 번째")>=0:
            leds[1].off()
        elif text.find("세 번째")>=0:
            leds[2].off()
        elif text.find("마지막")>=0:
            leds[3].off()
        elif text.find("전부")>=0:
            for i in range(4):
                leds[i].off()

# [START speech_transcribe_sync]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="ko-KR",
    )
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config=config, audio=audio)

    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        LEDLight(result.alternatives[0].transcript)
    # [END speech_python_migration_sync_response]


# [END speech_transcribe_sync]

button = Button(21)
leds = LEDBoard(18,23,24,25)

while True:
    if button.is_pressed:
        os.system("record.sh 3")
        transcribe_file("command.wav")
