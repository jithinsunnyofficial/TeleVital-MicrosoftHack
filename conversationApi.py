import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private-key.json'

DIALOGFLOW_PROJECT_ID = 'televital-hack-4dd77'
DIALOGFLOW_LANGUAGE_CODE = 'en'

def analyze_text(input_text = 'Hi',session_id = 'random'):
    SESSION_ID = session_id
    text_to_be_analyzed = input_text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)
    return response.query_result.fulfillment_text

#analyze_text('Hi my name is Farhan', 'session1')
