import pyrebase
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
		nm = db.child("Appointments/").child(user_index).get()
		res = nm.val()
		##print(res)


		try:
			age = int(res['age'])
		except:
			age = 44.0
		try:
			cough = int(res['cough'])
		except: 
			cough = 0.0
		try:
			gender = res['gender']
		except:
			gender = 'male'
		try:
			height = int(res['height'])
		except:
			height = '170'
		try:
			pregnant = res['pregnant']
		except:
			pregnant = 'no' 
		try:
			spo2 = int(res['spo2'])
		except:
			spo2 = 96
		try:
			weight = int(res['weight'])
		except:
			weight = 68
		try:
			tired = int(res['tiredness'])
		except:
			tired = 0.0
		try:
			temp = int(res['temp'])
		except:
			temp = 98
		try:
			sorethroat = int(res['sorethroat'])
		except:
			sorethroat = 0.0
		try:
			resp = int(res['rr'])
		except:
			resp = 13.0
		try:
			precond = res['precon']
		except: 
			precond = 'no'
		try:
			heart = int(res['hr'])
		except:
			heart = 50.0
		try:
			breathing = int(res['breathingdiff'])
		except:
			breathing = 0.0




		body_mass_index = 0.0
		death_rate_age = 0.0
		bmi_weight = 0.0
		death_rate_gender = 0.0
		death_rate_heart = 0.0
		death_rate_resp = 0.0

		if pregnant.lower() == "yes":
		        death_rate_preg = 6.0
		else:
		        death_rate_preg = 0.0
		if precond.lower() == "yes":
		        death_rate_preconding = 6.0
		else:
		        death_rate_preconding = 0.0


		height = int(height) * 0.393701
		weight = int(weight) * 2.20462
		body_mass_index = (int(weight) * 703) / (int(height) ** 2)



		if body_mass_index < 18.5:
		        bmi_weight=.05
		elif body_mass_index < 24.9:
		        bmi_weight=0
		elif body_mass_index > 25.0 and body_mass_index < 28.9:
		        bmi_weight=.07
		elif body_mass_index > 28.9 and body_mass_index < 34.9:
		        bmi_weight=.08
		elif body_mass_index > 34.9 and body_mass_index < 39.9:
		        bmi_weight=.09
		else:
		        bmi_weight=1.0

		#print("The death_rate_preg is " + str(death_rate_preg))
		        
		#print("The death_rate_preexisting is " + str(death_rate_preexisting))

		#print("A person with a BMI of " + str(body_mass_index ))
		if int(age) < 9:
		        death_rate_age=0.0
		elif int(age) < 39:
		        death_rate_age=1.0
		elif int(age) < 49:
		        death_rate_age=3.0
		elif int(age) < 59:
		        death_rate_age=3.0
		elif int(age) < 69:
		        death_rate_age=6.0
		elif int(age) < 79:
		        death_rate_age=7.0
		else:
		        death_rate_age=10.0
		#print("The death_rate_age is " + str(death_rate_age))
		if gender.lower() == "male":
		        death_rate_gender=6.0
		else:
		        death_rate_gender=4.0



		#print("The death_rate_gender is " + str(death_rate_gender))
		#athletes have heart rate of 40(implies good functioning of heart)
		#less than 40 is abnormal
		if int(heart) < 40:
		        death_rate_heart=5.0
		elif int(heart) <60 and heart > 40:
		        death_rate_heart=0.0
		elif int(heart) > 60 and heart < 100 :
		        death_rate_heart=0.0
		else:
		        death_rate_heart=5.0
		#print("The death_rate_heart is " + str(death_rate_heart))
		#given more imporance to respiratory rate


 
		if int(resp) < 10:
		        death_rate_resp=10.0
		elif int(resp) < 12:
		        death_rate_resp=9.0
		elif int(resp) > 12 and int(resp) < 20 :
		        death_rate_resp=0.0
		elif int(resp) > 20 and int(resp) < 25 :
		        death_rate_resp=5.0
		elif int(resp) > 25 and int(resp) < 27 :
		        death_rate_resp=9.0
		elif int(resp) > 27 :
		        death_rate_resp=10.0
		#print("The death_rate_resp is " + str(death_rate_resp))
		if int(spo2) < 90:
		        death_rate_spo=7.0
		elif int(spo2) >90 and int(spo2) <100:
		        death_rate_spo=0.0
		else:
		        death_rate_spo=7.0



		#print("The death_rate_spo is " + str(death_rate_spo))
		if int(temp) < 97:
		        death_rate_temp = 1.0
		elif int(temp) > 97 and int(temp) < 97.7:
		        death_rate_temp = 0.0
		elif int(temp) > 97.7 and int(temp) < 100.5:
		        death_rate_temp = 3.0
		else:
		        death_rate_temp = 6.0
		#print("The death_rate_temp is " + str(death_rate_temp))



		if int(cough) == 0:
		        death_rate_cough = 0.0
		elif int(cough) == 1:
		        death_rate_cough = 2.0
		elif int(cough) == 2:
		        death_rate_cough = 5.0
		else:
		        death_rate_cough = 8.0


		#print("The death_rate_cough is " + str(death_rate_cough))
		if int(sorethroat) == 0:
		        death_rate_throat = 0.0
		elif int(sorethroat) == 1:
		        death_rate_throat = 2.0
		elif int(sorethroat) == 2:
		         death_rate_throat = 5.0
		else:
		        death_rate_throat = 8.0


		#print("The death_rate_throat is " + str(death_rate_throat))
		if int(breathing) == 0:
		        death_rate_breath = 0.0
		elif int(breathing) == 1:
		        death_rate_breath = 2.0
		elif int(breathing) == 2:
		        death_rate_breath = 5.0
		else:
		        death_rate_breath = 8.0


		if int(tired) == 0:
		        death_rate_tired = 0.0
		elif int(tired) == 1:
		        death_rate_tired = 2.0
		elif int(tired) == 2:
		        death_rate_tired = 5.0
		else:
		        death_rate_tired = 8.0

		    
		    
		score = death_rate_tired+death_rate_breath+death_rate_throat+death_rate_cough+death_rate_temp+death_rate_spo+death_rate_resp+death_rate_heart+death_rate_gender+death_rate_age+bmi_weight+death_rate_preconding+death_rate_preg
		
		print(score)

		db.child("Appointments/").child(user_index).update({"score":score})
		db.child("Consultation/").child(user_index).update({"gscore":score})

		return (1)


api.add_resource(testabusive, '/score/<user_index>')

if __name__ == '__main__':
   app.run()
