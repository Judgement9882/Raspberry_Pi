import cv2
import os

# Video
video_capture = cv2.VideoCapture(0)

# Checking connection
if video_capture.isOpened():
  print('OK')
else:
  print('Video Not Connect')
  exit(0)

# 640 x 480
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Codec
Cod = cv2.VideoWriter_fourcc(*'XVID')

# Save file
out = cv2.VideoWriter("/home/pi/picam/picam_video.mp4", Cod, 20.0, frame_size)

while True:
  ret, frame = video_capture.read()

  # Show video live
  cv2.imshow('Live',frame)

  # Save
  out.write(frame)

  # Escape by key press
  if cv2.waitKey(1) & 0xFF ==ord('q'):
    break
