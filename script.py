import json
import requests
from time import sleep

url = "https://api.symbl.ai/v1/process/audio"

payload = None
numberOfBytes = 0

try:
   audio_file = open('/Users/neerajchaudhary/Downloads/y2hindi.mp3', 'rb')  # use (r"path/to/file") when using windows path
   payload = audio_file.read()
   numberOfBytes = len(payload)
except FileNotFoundError:
   print("Could not read the file provided.")
   exit()

# set your access token here. See https://docs.symbl.ai/docs/developer-tools/authentication
access_token = ''
headers = {
   'Authorization': 'Bearer ' + access_token,
   'Content-Length': str(numberOfBytes)  # This should correctly indicate the length of the request body in bytes.
   #'Content-Type': 'audio/mp3'
   # This is OPTIONAL field which describes the format and codec of the provided audio data. Accepted values are audio/wav, audio/mpeg, audio/mp3 and audio/wave only. If your audio is in formats other than don't use this field.
}

params = {
   #'name': "BusinessMeeting",
   # <Optional, string| your_conversation_name | Your meeting name. Default name set to conversationId.>

   # 'webhookUrl': "https://yourdomain.com/jobs/callback",
   # <Optional, string| your_webhook_url| Webhook url on which job updates to be sent. (This should be post API)>

   # 'customVocabulary': ['Platform', 'Discussion', 'Targets'],
   # <Optional, list| custom_vocabulary_list> |Contains a list of words and phrases that provide hints to the speech recognition task.

   #'confidenceThreshold': 0.6,
   # <Optional, double| confidence_threshold | Minimum required confidence for the insight to be recognized.>

   # 'detectPhrases': True,
   # <Optional, boolean| detect_phrases> |Accepted values are true & false. It shows Actionable Phrases in each sentence of conversation. These sentences can be found in the Conversation's Messages API.

   # 'enableSeparateRecognitionPerChannel': True,
   # "<Optional, boolean| enable_separate_recognition_per_channel> |Enables Speaker Separated Channel audio processing. Accepts true or false.

   # 'channelMetadata': [{"channel": 1, "speaker": {"name": "Robert Bartheon", "email": "robertbartheon@gmail.com"}}],
   # ["<Optional, boolean| channel_metadata> |This object parameter contains two variables speaker and channel to specific which speaker corresponds to which channel. This object only works when enableSeparateRecognitionPerChannel query param is set to true."

   'languageCode':"hi-IN"
   # <Optional, boolean| language_code> |code of language of recording.
}

responses = {
   400: 'Bad Request! Please refer docs for correct input fields.',
   401: 'Unauthorized. Please generate a new access token.',
   404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
   429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
   500: 'Something went wrong! Please contact support@symbl.ai'
}

response = requests.request("POST", url, headers=headers, data=payload, params=params)
jobId=''

if response.status_code == 201:
   # Successful API execution
   print("conversationId => " + response.json()['conversationId'])  # ID to be used with Conversation API.
   print("jobId => " + response.json()['jobId'])  # ID to be used with Job API.
   jobId=response.json()['jobId']
   conversationId=response.json()['conversationId']
   counter=0

   url = "https://api.symbl.ai/v1/job/"+jobId

   payload={}
   headers = {
       'x-api-key': access_token,
       'Content-Type': 'application/json'
   }
   response = requests.request("GET", url, headers=headers, data=payload)

   while(counter==0):
       print(response.text)
       if(response.json()['status']!='completed'):
           sleep(20)
           response = requests.request("GET", url, headers=headers, data=payload)
       elif(response.json()['status']=='completed'):
           counter=1
           print ("Job is completed now")

   url = "https://api.symbl.ai/v1/conversations/"+conversationId+"/messages"

   payload={}
   headers = {
   'x-api-key': access_token}
   response = requests.request("GET", url, headers=headers, data=payload)
   print(response.text)




elif response.status_code in responses.keys():
   print(responses[response.status_code])  # Expected error occurred
else:
   print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))




exit()
