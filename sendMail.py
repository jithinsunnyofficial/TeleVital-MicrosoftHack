import flask
from flask import *
from flask_mail import Mail,Message
import pyrebase
import pickle
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)


class testabusive(Resource):
	def get(self,user_index):
		credentials_json = open("credentials.json","rb")
		config = pickle.load(credentials_json)
		credentials_json.close()

		firebase = pyrebase.initialize_app(config)
		db = firebase.database()

		nm = db.child("Appointments").child(user_index).get()
		res=nm.val()
		#print(res)
		vale1= res['spo2']
		vale2= res['hr']
		vale3= res['rr']
		evale= res['semail']

		app.config.update(
			DEBUG=True,
			#EMAIL SETTINGS
			MAIL_SERVER='smtp.gmail.com',
			MAIL_PORT=465,
			MAIL_USE_SSL=True,
			MAIL_USERNAME = 'projecttelevital@gmail.com',
			MAIL_PASSWORD = 'destruction@televital'
			)

		mail = Mail(app)

		try:
				msg = Message("Vitals Report",
				  sender="projecttelevital@gmail.com",
				  recipients=[evale])
				msg.body = "The results of the vitals test are as follows:\n\n\nSpO2 level (in %): "+str(vale1)+"\n\nHeart Rate (in bpm): "+str(vale2)+"\n\nResp Rate (per min): "+str(vale3)           
				mail.send(msg)
				return 'Mail sent!'
		except Exception as e:
				return(str(e))
		

		return (1)


api.add_resource(testabusive, '/mail/<user_index>')

if __name__ == '__main__':
	app.run(debug=False)



