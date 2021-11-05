import cv2
import mediapipe as mp
import time
import numpy as np

def posScreen(roh_meceX,roh_meceY):
	#Todo:
	#width = obrazek.get(cv2.CAP_PROP_FRAME_WIDTH )
	#height = obrazek.get(cv2.CAP_PROP_FRAME_HEIGHT )
	width=640
	height=480
	roh_meceX = round(width*roh_meceX)
	roh_meceY = round(height*roh_meceY)
	return roh_meceX,roh_meceY

#------LIGHTSABER HERE------ 
def nakreslymec(ruka,obrazek,i):


	if i == 0:
		color=(0,255,0)
	else:
		color=(255,0,0)
	
	
	#height,width,dimensons= obrazek.shape
	#print (height,width)#480 640

	#roh_meceX = (ruka[5].x+(ruka[5].x-ruka[17].x)/2)
	AbodX=(ruka[6].x+ruka[10].x+ruka[14].x+ruka[18].x)/4
	AbodY=(ruka[6].y+ruka[10].y+ruka[14].y+ruka[18].y)/4
	
	#AbodX,AbodY=posScreen(AbodX,AbodY)
	
	BbodX=(AbodX*3+ruka[0].x)/4
	BbodY=(AbodY*3+ruka[0].y)/4

	mecPulDelkaX=(AbodX-ruka[18].x)*2.5
	mecPulDelkaY=(AbodY-ruka[18].y)*2.5

	mecSirkaX=BbodX-AbodX
	mecSirkaY=BbodY-AbodY

	CBodX=(BbodX+mecPulDelkaX)
	CBodY=(BbodY+mecPulDelkaY)

	DBodX=(CBodX+mecSirkaX)
	DBodY=(CBodY+mecSirkaY)
	
	EBodX=(DBodX-mecPulDelkaX*2)
	EBodY=(DBodY-mecPulDelkaY*2)

	FBodX=(EBodX-mecSirkaX)
	FBodY=(EBodY-mecSirkaY)

	BodC=posScreen(CBodX, CBodY)
	BodD=posScreen(DBodX, DBodY)
	BodE=posScreen(EBodX, EBodY)
	BodF=posScreen(FBodX, FBodY)

	C2X=(CBodX+mecPulDelkaX*9)
	C2Y=(CBodY+mecPulDelkaY*9)

	D2X=(C2X+mecSirkaX*1.2)
	D2Y=(C2Y+mecSirkaY*1.2)


	pts = [BodC,BodD,BodE,BodF]

	cv2.fillPoly(obrazek, np.array([pts]),(20,0,0))

	C2=posScreen(C2X, C2Y)
	D2=posScreen(D2X, D2Y)

	pts = [BodC,BodD,D2,C2]

	cv2.fillPoly(obrazek, np.array([pts]),(color))
	return obrazek

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
#print("haha")
with mp_hands.Hands(
	model_complexity=0,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5) as hands:
		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				continue
			# To improve performance, optionally mark the image as not writeable to
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = hands.process(image)

			# Draw the hand annotations on the image.
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


			if results.multi_hand_landmarks:
				#print (results)
				i=0
				for hand_landmarks in results.multi_hand_landmarks:
					
					
		
					#------LIGHTSABER HERE------ 
					
					image = nakreslymec(hand_landmarks.landmark,image,i)
					i=i+1
					#------LIGHTSABER HERE------ 


					#print(
					#	f'Midle finger tip coordinates: (',
					#	f'{hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x}, '
					#	f'{hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y})'
					#)	

					mp_drawing.draw_landmarks(
						image,
						hand_landmarks,
						mp_hands.HAND_CONNECTIONS,
						mp_drawing_styles.get_default_hand_landmarks_style(),
						mp_drawing_styles.get_default_hand_connections_style())

			# Flip the image horizontally for a selfie-view display.
			cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
			if cv2.waitKey(5) & 0xFF == 27:
				break
		cap.release()