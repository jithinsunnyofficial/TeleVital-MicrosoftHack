'''
After you've set your subscription key, run this application from your working
directory with this command: python TTSSample.py
'''
import os, requests, time
from xml.etree import ElementTree

#subscription key for the Cognitive Service. Do not share with anyone.
subscription_key = '<cognitive-subscription-key>'
'''
if 'SPEECH_SERVICE_KEY' in os.environ:
    subscription_key = os.environ['SPEECH_SERVICE_KEY']
else:
    print('Environment variable for your subscription key is not set.')
    exit()
'''
class TextToSpeech(object):
    def __init__(self, subscription_key, text_input, file_name):
        self.subscription_key = subscription_key
        self.tts = text_input
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.file_name = file_name

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', 'en-US-Guy24kRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        file_name_path = self.file_name+'.wav'
        if response.status_code == 200:
            with open(file_name_path, 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
            audio.close()
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")

    def get_voices_list(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

def convert_and_play(text_input, file_name):
    app = TextToSpeech(subscription_key, text_input, file_name)
    app.get_token()
    app.save_audio()
    from playsound import playsound
    print('Playing sound')
    file_name_path = file_name+'.wav'
    playsound(file_name_path)
    # Get a list of voices https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices
    # app.get_voices_list()

#Usage of API
#convert_and_play('Hey man')