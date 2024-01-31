# GYMTAR
Training avatar (Dialog system)
Virtual Environment Anaconda 
## Virtual Environment Installation (Anaconda v23.11.0)
### Manually
```
conda create -n VirtualTrainer python==3.8
conda activate VirtualTrainer
conda install ujson
pip install rasa
pip install --upgrade rasa==2.8.0
pip install protobuf==3.20.0

```
## Spanish Text Fragmenting Component Installation
```
pip3 install rasa[spacy]
python -m spacy download es_core_news_md
```
## Sentiment Component Installation
```
pip install nltk
```
## Database Control Installation
```
pip install mysql-connector-python==8.0.12
```
## Keyboard Activation
```
pip install keyboard
```
## Voice Service Installation (Azure) 
```
pip install azure-cognitiveservices-speech
```
## Azure AI Services Installation
```
pip install azure-ai-textanalytics
```
## Bidirectional Communication Channel Installation
```
pip install websocket-client
pip install websocket_server
```
## Virtual Environment Installation
### Automatically
```
conda env create -f dependencies\GymtarCoach.yml
```
# Execution
## Consola 1
```
rasa run -m models --enable-api --credentials credentials.yml --debug
```
## Consola 2
```
rasa run actions
```
## Consola 3
```
cd VoiceManager
python STT.py
```
## Consola 4
```
cd VoiceManager
python TTS.py
```

# Custom configurations 
## After downloading the project it is necessary to perform a training
## Rasa Train
```
rasa train --domain domains
```

# Construction of Json messages
## Json message address: http://localhost:5005/webhooks/myio/webhook
## Example message: examples\inputs.txt

## Requires an AzureKey.txt document with the following content:
VoiceServiceKey<br/> TranslatorServiceKey<br/> LanguageKey<br/>
