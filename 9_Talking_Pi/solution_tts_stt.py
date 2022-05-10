import asyncio
# This example uses the sounddevice library to get an audio stream from the
# microphone. It's not a dependency of the project but can be installed with
# `python -m pip install amazon-transcribe aiofile`
# `pip install sounddevice`.
import sounddevice
from boto3 import Session
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from time import sleep
from gpiozero import LEDBoard
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent


session = Session(profile_name="default")
polly = session.client("polly")

def awstts(string_input):
	response = polly.synthesize_speech(Text=string_input, OutputFormat="mp3",VoiceId="Seoyeon")

	# Access the audio stream from the response
	if "AudioStream" in response:
	        with closing(response["AudioStream"]) as stream:
	           output = os.path.join(gettempdir(), "speech.mp3")

	           try:
	            # Open a file for writing the output as a binary stream
	                with open(output, "wb") as file:
	                   file.write(stream.read())
	           except IOError as error:
	              # Could not write to file, exit gracefully
	              print(error)
	              sys.exit(-1)

	else:
	    # The response didn't contain audio data, exit gracefully
	    print("Could not stream audio")
	    sys.exit(-1)

	# Play the audio using the platform's default player
	if sys.platform == "win32":
	    os.startfile(output)
	else:
	    subprocess.call(["mpg321", output])


"""
Here's an example of a custom event handler you can extend to
process the returned transcription results as needed. This
handler will simply print the text out to your interpreter.
"""

class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        # This handler can be implemented to handle transcriptions as needed.
        # Here's an example to get started.
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
#                print(alt.transcript)
#                print(type(alt.transcript))
                print(alt.transcript)
                if (alt.transcript).find("On")>=0 and (str(led.value)[-2]) == '0' :
                    led.on()
                    awstts("LED를 켭니다.")
                    sleep(1)
                elif (alt.transcript).find("Kill")>=0 and (str(led.value)[-2]) == '1':
                    led.off()
                    awstts("LED를 끕니다.")
                    sleep(1)


async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    # Be sure to use the correct parameters for the audio stream that matches
    # the audio formats described for the source language you'll be using:
    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=44100,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region="us-east-1")

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=44100,
        media_encoding="pcm"
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())


led = LEDBoard(18)

awstts("LED제어를 시작합니다. 명령을 내려주세요.")

loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()
