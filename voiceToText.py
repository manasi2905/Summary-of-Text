#using ibm watson api
#pip3 install --upgrade "ibm-watson>=5.1.0"
from ibm_watson import SpeechToTextV1   
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
from os.path import join, dirname

#authetication
authenticator = IAMAuthenticator('UhIENYMPXTuuukXYROghF8hYWFZSrC3z5HI2tm7iobsw')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/9aa7928c-72da-423d-b870-e415fe6c6478')

model = speech_to_text.get_model('en-US_NarrowbandModel').get_result()
print(json.dumps(model, indent=2))

def generateText():
    #downsampling the audio
    from pydub import AudioSegment as am            #pip3 install pydub
    sound = am.from_file('./resources/sample_audio_2.wav', format='wav')
    sound = sound.set_frame_rate(16000)
    sound.export('./resources/sample_audio.wav', format='wav')

    with open(join(dirname(__file__), './resources/sample_audio_2.wav'),'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            smart_formatting=True,
            continuous=True
        ).get_result()
    print(speech_recognition_results)       #output as json 

    #converting the output to string
    # {'results' [{-> 'alternatives' [{-> 'transcripts': ans}]}]}
    #we need to concatenate all the ans to get final result
    final_result = ""
    result_list = speech_recognition_results.get('results')

    for sent_dict in result_list:
        alt = sent_dict.get('alternatives')
        for trans_dict in alt:
            for transcript in trans_dict.get('transcript'):
                final_result = final_result + transcript
        final_result = final_result + ". "

    #writing the converted to text file
    convertedText = open("generatedFile.txt","a")
    convertedText.write(final_result)
    convertedText.close()