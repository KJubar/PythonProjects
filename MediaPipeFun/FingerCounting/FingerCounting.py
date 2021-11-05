import cv2
import mediapipe as mp
import time


#----Finger Counting HERE-------
def prstZvedly(ruka):
	x0 = ruka[mp_hands.HandLandmark.WRIST].y
	
	x5 = ruka[mp_hands.HandLandmark.INDEX_FINGER_MCP].y	
	x8 = ruka[mp_hands.HandLandmark.INDEX_FINGER_TIP].y	

	x9 = ruka[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
	x12 = ruka[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

	x13 = ruka[mp_hands.HandLandmark.RING_FINGER_MCP].y
	x16 = ruka[mp_hands.HandLandmark.RING_FINGER_TIP].y	

	x17 = ruka[mp_hands.HandLandmark.PINKY_MCP].y
	x20 = ruka[mp_hands.HandLandmark.PINKY_TIP].y

	velikostiPrstu=[x5-x8,x9-x12,x13-x16,(x17-x20)*1.4]
	prsty=[]

	VelZap =x0 - x5


	for velikost in velikostiPrstu:
		if (velikost >= (0.7*VelZap)):
			prsty.append(1)
		else:
			prsty.append(0)

	print (prsty)

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
print("haha")
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
				print (results)
				for hand_landmarks in results.multi_hand_landmarks:
					
					
					#ukazovacek spicka
					#print(
						f'Index finger tip coordinates: (',
						#f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x}, '
					#	f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y})'
					#)


					#----Finger Counting HERE-------
					prstZvedly(hand_landmarks.landmark)


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