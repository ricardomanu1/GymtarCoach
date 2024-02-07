import random, keyboard, time, os
import azure.cognitiveservices.speech as speechsdk
from interaction_manager import interaction_manager
from translator import translator
from sentiment import sentiment

def SentimentToEmotion(s):
    global Emotions
    print(s)
    if s <= 1.0:
        e = Emotions[8]  
    if s <= 0.35:
        e = Emotions[7]  
    if s <= 0.15:
        e = Emotions[6]  
    if s <= -0.15:
        e = Emotions[5]  
    if s <= -0.30:
        e = Emotions[4]
    if s <= -0.45:
        e = Emotions[3]
    if s <= -0.60:
        e = Emotions[2]  
    if s <= -0.70:
        e = Emotions[1]  
    if s <= -0.8:
        e = Emotions[0]    
    return e

with open('..\\..\\AzureKeys.txt') as f:
    lines = [line.rstrip() for line in f]
    print(lines)

# Voice Service API key
speech_key = str(lines[0]) #sys.argv[1]
# Translator Service API key
translator_key = str(lines[1]) #sys.argv[2]
# Language Service Api key
sentiment_key = str(lines[2]) #sys.argv[3]
# Tanslator Service Init
Translator = translator(translator_key)
# Audio and image interaction manager
Interaction = interaction_manager()
# Language
Sentiment = sentiment(sentiment_key)

# Sentiments list inputs
Emotions = ['isSad','isAnger','isFear','isAnxious','isTired','isLonely','isBored','isSurprise','isHappy']

# Voice service configuration
service_region = "westeurope"

# Detectable languages
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Set multiple properties by id
speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, "Latency") #'Continuous'
    #property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority, value='Latency')

# Audio input configuration
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

lang = "es-ES"

# Language recognizer
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, 
    language= lang, 
    audio_config=audio_config)               

# Keyword Detection
##model = speechsdk.KeywordRecognitionModel("Keywords/2faffcbd-2030-4c7e-86f3-69bceff47a28.table")
##keyword = "Sonia"
##keyword_recognizer = speechsdk.KeywordRecognizer()

while True:
    ##result_future = keyword_recognizer.recognize_once_async(model)
    ##print('Esperando al comando de voz: "{}"'.format(keyword))

    try:          
        if os.path.exists('listening.txt') or keyboard.is_pressed('q'):          
            #if keyboard.is_pressed('q'): #result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("Di algo...")
            # Waiting for sentence (maximum of 15 seconds of audio)
            start_time = time.time()
            result = recognizer.recognize_once()
            print("--- %s seconds (pickup) ---" % (time.time() - start_time))
            # System to detect emotion from audio
            emotion = random.choice(Emotions)            
            # Language recognition in first iteration
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:   
                start_time = time.time()
                print("Input: {} <{}>".format(result.text,emotion))
                if (str(result.text) == 'Apagar sistema.'):
                    print("Apagando sistema...")
                    os.remove('listening.txt')
                    break  
                # System to detect polarity from audio (positive,negative,neutral)
                # sentiment_analysis = Sentiment.sentiment(result.text,detected_src_lang[0:2])
                sentiment_analysis = 0.0
                # emotion = SentimentToEmotion(sentiment_analysis)
                # Send the spanish translation to Rasa
                text_trans = Translator.translator(result.text,lang,'es')
                print("--- %s seconds (audio processing) ---" % (time.time() - start_time))
                start_time = time.time()
                Interaction.say(text_trans,lang,emotion,sentiment_analysis)
                print("--- %s seconds (Json generation & sending to rasa)---" % (time.time() - start_time))
                os.remove('listening.txt')
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                print("Translation canceled: {}".format(result.cancellation_details.reason))
                if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(result.cancellation_details.error_details))
                    break            
    except Exception as e :
        continue


