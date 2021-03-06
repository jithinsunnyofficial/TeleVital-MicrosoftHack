# Project TeleVital
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![homepage](homepage.png)

**TeleVital WebApp:** https://televital.azurewebsites.net/

**TeleVital Video:** https://www.youtube.com/watch?v=dIN5DZ0KZKs&feature=youtu.be

## Description
TeleVital is an AI powered platform designed to help users do preliminary analysis for COVID-19 contraction (COVID-19 assessment test, Vitals test, COVID-19 X-Ray Analyzer) right at the comfort of their homes.  

TeleVital also provides a platform for hospital / doctors to prioritise on their patients based on their criticality and henceforth schedule appointments. Further patients are able to take video consulations with their preferred doctor through the TeleVital platform.

We have also built a kiosk module for the same, keeping in mind the necessity to measure vitals contactless, of people entering hospitals, office buildings, shopping malls, etc. The kiosk module works entirely through the intergrated smart voice commands.

## Components of TeleVital WebApp Platform (Contactless Assessment)
1. **AI Chatbot:**  	
	The chatbot is capable of conducting a Covid-19 assessment test based on the WHO guidelines and classify the user into three categories (Normal, Moderate, High) of risk of being infected. 
	The chatbot also studies the mental health of users and provides with live mental health therapy. 
2. **Vitals Test:**
	Vitals test helps users in measuring the readings of the users' SpO$_2$, Heart rate and Respiratory rate with just the help of a webcam. This helps the patients in early detection of symptoms of Covid-19, also at the same time reduce the number of people visiting the hospital for preliminary tests.
3. **X-Ray Analyzer:**
	This component of TeleVital allows a user to upload his/her Chest X-Ray as an image, and our pre-trained COVID-19 Chest X-Ray model predicts whether the X-Ray shows signs of COVID-19 or not. A confidence ratio is displayed to the user as well.
4. **Digital Prescription:**
	To ease doctors with providing patients, hand-written prescriptions, the digital prescription portal enables the doctors to voice record prescription for patients, and it will further be converted to text and sent directly to patients as a PDF via mail.
5. **Patient Prioritizer:** 
Understanding the rapid increase in cases of Covid-19, patient prioritizer portal enables hospitals in identifying the high risk patients and giving them the care accordingly.

## Components of TeleVital Kiosk (Contactless Assessment)
1. **Voice-based commands**  	
	The kiosk is powered by smart voice commands and is able to engage with the users through it.
2. **Face mask detection**  	
	This module of the kiosk identifies if the user is wearing a mask or not before he/she enters the building. If the user is identified to be not wearing a mask, the user is adviced to wear one.
3. **Face recognition**  	
	The face recognition module will help companies in punching attendance of their employees or enable hospitals to check for records on the patients before he/she even enters the building.
## Technology stack

1. **Frontend**: 
	* HTML 
	* CSS 
	* Angular.js
2. **Backend**: 
	* Python - Tensorflow, OpenCV, Flask, Spacy, NLTK, Numpy, Pandas, Scikit-learn, Pillow
	* WebRTC
	* Node.js
3. **Database**: 
	* Azure SQL Database

## Models
To download the models for Face recognition, Mask detection and X-Ray analyzer kindly download from this url: [Models data](https://drive.google.com/drive/folders/1ZZXm9gnbYv_a2QAabLy1eAai79i4xPdG?usp=sharing)


## Contributors

- Jithin Sunny (jithin_sunny@yahoo.com)
- Rohan Rout (rohan.rout98@gmail.com)
- Rakshit Naidu (rakshit.naidu07@gmail.com)
- Syed Farhan Ahmad (farhan.tuba@gmail.com)
- Joel Jogy (joeljogy07@gmail.com)
