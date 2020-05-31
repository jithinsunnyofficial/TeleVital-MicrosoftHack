import pyrebase
from flask import Flask, request
from flask_restful import Resource, Api
import spacy
from nltk.stem import PorterStemmer

app = Flask(__name__)
api = Api(app)
 
class testabusive(Resource):
	def get(self, user_index):
		config = {
		    "apiKey": "AIzaSyDfnSG9PFjBl-7WzfqNXEsmeUADZUjoNbY",
		    "authDomain": "televital-omachack-c1db6.firebaseapp.com",
		    "databaseURL": "https://televital-omachack-c1db6.firebaseio.com",
		    "projectId": "televital-omachack-c1db6",
		    "storageBucket": "televital-omachack-c1db6.appspot.com",
		    "messagingSenderId": "1016790452467",
		    "appId": "1:1016790452467:web:23c537c7dba61f8a83cf86",
		    "measurementId": "G-DF84JXFTQH"
				}

		firebase = pyrebase.initialize_app(config)
		db = firebase.database()
		nm = db.child("Appointments").child(user_index).get()
		res = nm.val()
		voice_text = res['vtext']

		nlp = spacy.load('en_core_web_sm')

		# nlp.Defaults.stop_words -= {"call"}
		# voice_text = "Sam is diagnosed with fever and cough I prescribe Dolo and paracetamol with the dosage 111 I also advise to take rest"
		ps = PorterStemmer()
		try:
			advice_text = voice_text.split('advice ')[1]
		except:
			advice_text = voice_text.split('advise ')[1]

		voice_text = voice_text.lower()
		doc = nlp(voice_text)
		stopWords = []
		for token in doc:
			if token.is_stop == True:
				stopWords.append(token)

		properNouns = []

		for token in doc:
			if token.pos_ == 'PROPN':
				properNouns.append(token)

		preprocessed_words = []
		for token in doc:
			# print(token)
			# print(token.pos_)
			if (token not in stopWords):
				preprocessed_words.append(ps.stem(str(token)))

		print(preprocessed_words)

		diag_start = 0
		prescrib_start = 0
		medicines = []
		dosages = []
		for index,word in enumerate(preprocessed_words):
			if word == 'diagnos':
				diag_start = index + 1
			elif word == 'prescrib':
				diag_end = index
				diagnosis = preprocessed_words[diag_start:diag_end]

				med_start = index + 1
			elif word == 'dosag':
				med_end = index
				medicines = preprocessed_words[med_start:med_end]
				dosage = ''
				for i in str(preprocessed_words[index + 1]):
					dosage = dosage + i + '-'

				dosage = dosage[:-1]
				dosages.append(dosage)
				med_start = index + 2


		diag_text = '' 
		for index, diag in enumerate(diagnosis):
			if index == 0:
				diag_text = diag_text + diag
			else:
				diag_text = diag_text + ", " + diag

		med_text = ''
		for index, med in enumerate(medicines):
			if index == 0:
				med_text = med_text + med
			else:
				med_text = med_text + ", " + med	


		dosag_text = ''
		for index, dosage_count in enumerate(dosages):
			if index == 0:
				dosag_text = dosag_text + dosage_count
			else:
				dosag_text = dosag_text + ", " + dosage_count	


		print(diag_text)
		print(med_text)
		print(dosag_text)
		print(advice_text)

		db.child("Appointments").child(user_index).update({'diagnosis':diag_text, 'medicines':med_text, 'dosages':dosag_text,'advices':advice_text})
		db.child("Consultation").child(user_index).update({"idiagnosis":diag_text})
		return (1)

api.add_resource(testabusive, '/prescribe/<user_index>')

if __name__ == '__main__':
   app.run()