#Importing Libraries
import cv2
import mediapipe as mp
import time
import numpy as np
import serial

#Setting arduino serial
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

#Initialize capturing
cap = cv2.VideoCapture(0)

#use hands class
mpHands = mp.solutions.hands
hands = mpHands.Hands() # using default paramaters of 'Hands()'
mpDraw = mp.solutions.drawing_utils #to draw landmarls

while True:
	#A frame is captured
	success, img = cap.read()
	#converting colorspace to RGB
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	#process the converted results
	results = hands.process(imgRGB)

	#setup horizantal and diagonal lines
	cv2.line(img, (340, 0), (340, 480), (0, 0, 255), 1)
	cv2.line(img, (0, 240), (640, 240), (0, 255, 255), 1)

	#if palm is detected
	if results.multi_hand_landmarks:
		#for each landmarks
		for handLms in results.multi_hand_landmarks:
			for id, lm in enumerate(handLms.landmark):
				h, w, c = img.shape

				#getting x and y cordinates of the palm
				cx, cy = int(lm.x * w), int(lm.y * h)

				#if finger is detected
				if id == 7: # finger 1
					print("x:"+str(cx)+"y:"+str(cy))

					#translate funtion converts cordinates to angle
					def translate(inpval, in_from, in_to, out_from, out_to):
						out_range = out_to - out_from
						in_range = in_to - in_from
						in_val = inpval - in_from
						val = (float(in_val) / in_range) * out_range
						out_val = out_from + val
						return int(out_val)

					#converter funtion encodes X,Y cordinates into 1 string
					def converter(x, y):
						encode = 10000000
						xencode = encode + (x * 10000)
						yencode = encode + y
						return xencode + yencode

					#to convert X,Y to angles
					datax = translate(cx, 640, 0, 20, 160)
					datay = translate(cy, 00, 480, 40, 150)

					#to encode to single string
					cordinates = converter(datax,datay)
					print(cordinates)

					#write_read funtion writes to Serial COM Port
					def write_read(x):
						arduino.write(bytes(x, 'utf-8'))
						time.sleep(0.05)
						data = arduino.readline()
						return data

					# cordinates = 20900090 => To set LED to midpoint

					#to write to serial
					value = write_read(str(cordinates))
					print(value)
			#draw the lines for palm and fingers
			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

	#display the captured frame
	cv2.imshow('Image', np.flip(img,axis=1))
	#for exiting the capture
	cv2.waitKey(1)