import warnings
import pyrebase
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from utils import base64_to_pil_image, pil_image_to_base64
import re
import cv2
import numpy as np
from numpy import mean
from flask import Flask, request
from flask_restful import Resource, Api
import pickle


app = Flask(__name__)
api = Api(app)
 
class testabusive(Resource):
	def get(self, user_index):
		credentials_json = open("credentials.json","rb")
		config = pickle.load(credentials_json)
		credentials_json.close()

		firebase = pyrebase.initialize_app(config)
		db = firebase.database()
		nm = db.child("Appointments").child(user_index).get()
		res= nm.val()
		video_frames = res['hrbase64']
		video_strings = video_frames.split(';')
		#print(video_strings)
		video_strings = video_strings[1:]
		print(len(video_strings))
		video_strings = video_strings*10

		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		def buildGauss(frame, levels):
			pyramid = [frame]
			for level in range(levels):
				frame = cv2.pyrDown(frame)
				pyramid.append(frame)
			return pyramid
		def reconstructFrame(pyramid, index, levels):
			filteredFrame = pyramid[index]
			for level in range(levels):
				filteredFrame = cv2.pyrUp(filteredFrame)
			filteredFrame = filteredFrame[:videoHeight, :videoWidth]
			return filteredFrame


		def applyFFT(frames, fps):
			n = frames.shape[0]
			t = np.linspace(0,float(n)/fps, n)
			disp = frames.mean(axis = 0)
			y = frames - disp

			k = np.arange(n)
			T = n/fps
			frq = k/T # two sides frequency range
			freqs = frq[range(n//2)] # one side frequency range

			Y = np.fft.fft(y, axis=0)/n # fft computing and normalization
			signals = Y[range(n//2), :,:]
			
			return freqs, signals

		def bandPass(freqs, signals, freqRange):

			signals[freqs < freqRange[0]] *= 0
			signals[freqs > freqRange[1]] *= 0

			return signals


		def find(condition):
			res, = np.nonzero(np.ravel(condition))
			return res


		def freq_from_crossings(sig, fs):
			"""Estimate frequency by counting zero crossings
    
			"""
			#print(sig)
			# Find all indices right before a rising-edge zero crossing
			indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
			x = sig[1:]
			x = mean(x)

			
			return x

		def searchFreq(freqs, signals, frames, fs):

			curMax = 0
			freMax = 0
			Mi = 0
			Mj = 0
			for i in range(10, signals.shape[1]):
				for j in range(signals.shape[2]):

					idxMax = abs(signals[:,i,j])
					idxMax = np.argmax(idxMax)
					freqMax = freqs[idxMax]
					ampMax = signals[idxMax,i,j]
					c, a = abs(curMax), abs(ampMax)
					if (c < a).any():
						curMax = ampMax
						freMax = freqMax
						Mi = i
						Mj = j
                # print "(%d,%d) -> Freq:%f Amp:%f"%(i,j,freqMax*60, abs(ampMax))

			y = frames[:,Mi, Mj]
			y = y - y.mean()
			fq = freq_from_crossings(y, fs)
			rate_fft = freMax*60
			
			rate_count = round(20+(fq*10))

			if np.isnan(rate_count):
				rate = rate_fft
			elif abs(rate_fft - rate_count) > 20:
				rate = rate_fft
			else:
				rate = rate_count

			return rate

		def answer(videoStrings):

			sampleLen = 10
			firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
			firstGauss = buildGauss(firstFrame, levels+1)[levels]
			sample = np.zeros((sampleLen, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
		
			idx = 0
			
			respRate = []	

			#pipeline = PipeLine(videoFrameRate)
			face_flag = 0 
			for i in range(len(videoStrings)):
				input_img = base64_to_pil_image(videoStrings[i])

				input_img = input_img.resize((320,240))
				gray = cv2.cvtColor(np.array(input_img), cv2.COLOR_BGR2GRAY)
				
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				#print(faces)
				#faces = [1,2,3]
				#print(len(faces))
				if len(faces) > 0:
					#print("FACE FOUND _ RR")

					face_flag = 1

					frame  = cv2.cvtColor(np.array(input_img), cv2.COLOR_BGR2RGB)
			
					detectionFrame = frame[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):int(realWidth-int(videoWidth/2)), :]


					sample[idx] = buildGauss(detectionFrame, levels+1)[levels]
				
					freqs, signals = applyFFT(sample, videoFrameRate)
					signals = bandPass(freqs, signals, (0.2, 0.8))
					respiratoryRate = searchFreq(freqs, signals, sample, videoFrameRate)

					#frame[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):(realWidth-int(videoWidth/2)), :] = outputFrame
					
					idx = (idx + 1) % 10 		

					respRate.append(respiratoryRate)

				else:
					print("Face not found")

			if face_flag == 1:
				l = []
				a = max(respRate)
				b = mean(respRate)
				if b < 0:
					b = 5
				l.append(a)
				l.append(b)

			
				rr = mean(l)
				rr = round(rr,2)
			else:
				rr = "Face not recognised!"



			return(rr)	


		# Webcam Parameters
		realWidth = 320
		realHeight = 240
		videoWidth = 160
		videoHeight = 120
		videoChannels = 3
		videoFrameRate = 15


		# Color Magnification Parameters
		levels = 3
		alpha = 170
		minFrequency = 1.0
		maxFrequency = 2.0
		bufferSize = 150
		bufferIndex = 0

		# Output Display Parameters
		font = cv2.FONT_HERSHEY_SIMPLEX
		loadingTextLocation = (20, 30)
		bpmTextLocation = (videoWidth//2 + 5, 30)
		fontScale = 1
		fontColor = (0,0,0)
		lineType = 2
		boxColor = (0, 255, 0)
		boxWeight = 3

		# Initialize Gaussian Pyramid
		firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
		firstGauss = buildGauss(firstFrame, levels+1)[levels]
		videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
		fourierTransformAvg = np.zeros((bufferSize))

		# Bandpass Filter for Specified Frequencies
		frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
		mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)

		# Heart Rate Calculation Variables
		bpmCalculationFrequency = 15
		bpmBufferIndex = 0
		bpmBufferSize = 10
		bpmBuffer = np.zeros((bpmBufferSize))
		i = 0
		bpm_values = []
		face_flag = 0
		for j in range(len(video_strings)):
			# convert it to a pil image
			input_img = base64_to_pil_image(video_strings[j])

			input_img = input_img.resize((320,240))

			img  = cv2.cvtColor(np.array(input_img), cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(np.array(input_img), cv2.COLOR_BGR2GRAY)
			
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			#faces = [1,2,3]

			if len(faces) > 0:
				face_flag = 1
				#print("FACE FOUND")
				detectionFrame = img[int(videoHeight/2):int(realHeight-videoHeight/2), int(videoWidth/2):int(realWidth-int(videoWidth/2)), :]

				# Construct Gaussian Pyramid
				videoGauss[bufferIndex] = buildGauss(detectionFrame, levels+1)[levels]
				fourierTransform = np.fft.fft(videoGauss, axis=0)
				# Bandpass Filter
				fourierTransform[mask == False] = 0

				# Grab a Pulse
				if bufferIndex % bpmCalculationFrequency == 0:
					i = i + 1
					for buf in range(bufferSize):
						fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
					hz = frequencies[np.argmax(fourierTransformAvg)]
					bpm = 60.0 * hz
					bpmBuffer[bpmBufferIndex] = bpm
					# print("BPM Buffer List: ", bpmBuffer)
					bpmBufferIndex = (bpmBufferIndex + 1) % bpmBufferSize

				# Amplify
				filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
				filtered = filtered * alpha

				# Reconstruct Resulting Frame
				filteredFrame = reconstructFrame(filtered, bufferIndex, levels)
				outputFrame = detectionFrame + filteredFrame
				outputFrame = cv2.convertScaleAbs(outputFrame)

				bufferIndex = (bufferIndex + 1) % bufferSize
				
				if i > bpmBufferSize:
					bpm_values.append(bpmBuffer.mean())
					#print(bpm_values)
			else:
				print("Face not found")

		if face_flag == 1:
			hr = max(bpm_values)
			hr = round(hr)

		else:
			hr = 'Face not found'

		print(hr)

		rr = answer(video_strings)
		print(rr)

		db.child("Appointments").child(user_index).update({"hr":hr,'rr':rr})
		db.child("Consultation").child(user_index).update({"fhr":hr,'frr':rr})
		return (1)


api.add_resource(testabusive, '/hr/<user_index>')

if __name__ == '__main__':
   app.run()
