import numpy as np
from PIL import Image
import pyrebase
from flask import Flask, request
from flask_restful import Resource, Api
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from util import base64_to_pil
import pickle


app = Flask(__name__)
api = Api(app)



class testabusive(Resource):
	def get(self, user_index):

		credentials_json = open("credentials.json","rb")
		config = pickle.load(credentials_json)
		credentials_json.close()

		MODEL_PATH = 'models/covid_new_model1.model'

		# Load your own trained model
		model = load_model(MODEL_PATH)
		model._make_predict_function() 


		firebase = pyrebase.initialize_app(config)
		db = firebase.database()
		nm = db.child("Appointments").child(user_index).get()
		res= nm.val()
		xray_frame = res['xraybase64']


		image = base64_to_pil(xray_frame)

		if image.mode != "RGB":
			image = image.convert("RGB")

		image = image.resize((224, 224))
		image = img_to_array(image)
		image /= 255
		image = np.expand_dims(image, axis=0)
		
		# Be careful how your trained model deals with the input
		# otherwise, it won't make correct prediction!

		preds = model.predict(image)

		pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
		pred_class = preds
		print(pred_proba)
		print(pred_class)
		if pred_class[0][0] >= 0.5:
				result = "Covid-19 tested positive. [Confidence ratio: " + str(round(pred_class[0][0]*100,2)) + "%]"
				# result += str(pred_class[0][0])
		else:
				result = "Covid-19 tested negative. [Confidence ratio: " + str(round((1-pred_class[0][0])*100,2)) + "%]"

				# result += str(pred_class[0][1])	

		print(result)
		db.child("Appointments").child(user_index).update({"report":result})

		return (1)
				

api.add_resource(testabusive, '/xray/<user_index>')

if __name__ == '__main__':
   app.run()
