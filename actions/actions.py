import csv, json, os, typing
from pickle import NONE
import datetime as dt
import xml.etree.cElementTree as ET
import numpy as np

from EBDI.emotions_manager import emotions_manager
from EBDI.belief_manager import belief_manager
from EBDI.desires_manager import desires_manager
from EBDI.intents_manager import intents_manager 

from DDBB.SQL import database 

from os import listdir
from typing import Any, Text, Dict, List

from rasa_sdk import events
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, BotUttered, UserUttered, EventType
from rasa.shared.nlu.training_data.formats.rasa_yaml import RasaYAMLReader
from rasa.shared.nlu.training_data.loading import load_data

if typing.TYPE_CHECKING:
    from rasa_sdk.trackers import DialogueStateTracker
    from rasa_sdk.dispatcher import Dispatcher
    from rasa_sdk.domain import Domain

# Variables globales
user_intent = ''
count = 0
Bi = ''
Be = ''
lang = 'es-ES'
polarity = 0
inter1 = False
date = ''

## Kinect
watch = False
watchResponse = ''

## Interface
interface = False
interfaceResponse = ''

## Database
routine_say = False
exercises = []
animations = []

## Coach
exercise_say = False
exercise_current = ''
exercise_i = 0
rutina_len = 0

# Gestor EBDI
Emotions = emotions_manager()
Beliefs = belief_manager()
Desires = desires_manager()        
Intents = intents_manager()
context = Intents.get_context()


# Memoria del Bot
slot_name = ''
slot_daytime = ''
slot_rol = ''
slot_avatar = 'Carlos'
slot_ejercicio = ''
slot_animacion = ''
id_user = 0

ejercicio = ''
slot_user = 0
avatar = 'm'
session_today = []
ejercicios_lista = []
animaciones_lista = []

# DDBB
db = database()
#db.connection()

# Methods
def __init__(self):
    self.agent_id = 'actions'

# Number of responses
def contador():    
    global count
    count = count + 1
    return []

# Last event that has been generated to capture the response that has been selected from the Domain file
def get_latest_event(events):    
    latest_actions = []
    for e in events:
        if e['event'] == 'bot':
            latest_actions.append(e)
    return latest_actions

# Time of day
def part_of_day(x):    
    if (x > 4) and (x <= 12 ):
        return 'morning'
    elif (x > 12) and (x <= 16):
        return'afternoon'
    elif (x > 16) and (x <= 24) :
        return 'evening'
    elif (x > 24) and (x <= 4):
        return'none'

# The day in spanish
def the_day(x):
    if x == "Monday":
        return 'lunes'
    if x == "Tuesday":
        return 'martes'
    if x == "Wednesday":
        return 'miercoles'
    if x == "Thursday":
        return 'jueves'
    if x == "Friday":
        return 'viernes'
    if x == "Saturday":
        return 'sabado'
    if x == "Sunday":
        return 'domingo'

## Estructura BOT
class ChatBot(Action):
    def name(self) -> Text:
        return "chatbot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        # Acceso a variables globales
        global Bi, Be, lang, polarity, inter1, date
        global slot_name, slot_daytime, slot_rol, slot_avatar, slot_ejercicio, slot_animacion
        global id_user, ejercicio

        print("-------------------------------------------------------------------------------")
        
        inter1 = True

        # Actualizacion de fecha
        now = dt.datetime.now()
        date = now.strftime("%Y-%m-%d")
        
        # Almacena la intencion y el nivel de confianza
        intent = tracker.latest_message['intent']
        # Almacena el mensaje de entrada
        text = tracker.latest_message['text']
        # Almacena las entidades adjuntas al texto
        entities = tracker.latest_message['entities']
        # Almacena metadatos agjuntos al mensaje
        metadata = tracker.latest_message['metadata']  

        # Almacena la intencion
        Bi = intent['name']
        # Almacena el tipo de evento del metadato (say/know)
        id_event = metadata['event']     
        
        # Almacena en slot la entidad 'avatar' solo si se usa y se mantiene hasta el cambio
        slot_avatar = tracker.get_slot('avatar')       
        # Almacena en slot la fecha actual
        slot_daytime = part_of_day(int(f"{dt.datetime.now().strftime('%H')}"))   
        
        # Entities:
        for e in entities:
            print("Entidad: {} = {}".format(e['entity'],e['value']))

        # Metadata:
        for key, value in metadata.items():
            print("Metadatos: {} = {}".format(key, value))

        # Metadata: entrada de voz  
        if (id_event == 'say'):
            if 'emotion' in metadata:
                Be = metadata['emotion']            
            if 'language' in metadata:
                lang = metadata['language']
            if 'polarity' in metadata:
                polarity = metadata['polarity']                  
            if Bi not in context:
                Bi = 'out_of_scope'
            user_event = [id_event,Bi,Be,text,slot_name,entities,lang,polarity]               
                
        # Metadata: entrada de comando
        elif (id_event == 'know'):
            if 'id' in metadata:
                id_user = metadata['id']       
            if 'ejercicio' in metadata:
                ejercicio = metadata['ejercicio'] 
                slot_ejercicio = ejercicios_lista[ejercicio]
                slot_animacion = animaciones_lista[ejercicio]           
            objInterest = None                    
            user_event = [id_event,text,objInterest,'']             
        
        # Gestion de dialogo
        print('EVENT: ' + str(user_event)) 
        EBDI.run(self, dispatcher, tracker, domain, user_event)
        
        return [SlotSet("daytime", slot_daytime),
                SlotSet("rol", slot_rol), SlotSet("avatar", slot_avatar),
                SlotSet("name", slot_name), SlotSet("ejercicio", slot_ejercicio)]

## Gestion de dialogo con estructura EBDI
class EBDI(Action):

    def name(self) -> Text:
        return "ebdi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            user_event) -> List[Dict[Text, Any]]:          
        # Conjunto E B D I
        global Emotions, Beliefs, Desires, Intents, inter1

        # Se confirma primera iteracion
        Beliefs.inter = inter1
        inter1 = False

        # Establecen las nuevas creencias a partir del evento
        newBelief = Beliefs.new_belief(user_event)     
        
        # Se elimina el anterior estado emocional
        Beliefs.del_belief(Emotions.estado)
        for e in Beliefs.emotionalBeliefs:
            Beliefs.del_belief(e)

        # Primera gestion del estado emocional
        E1 = Emotions.euf1(Intents,newBelief)
        print('PRIMARY EMOTION: ' + E1)
        # Se añade la nueva emocion como creencia
        newBelief.append(['know',E1,True]) 
        
        # BDI actualizacion de las creencias, deseos e intenciones    
        BDI.bdi(self,newBelief)             

        # Segunda gestion del estado emocional
        E2 = Emotions.euf2(Intents,Beliefs)
        print('SECONDARY EMOTION: ' + E2) 

        #if (inTime and E1 != E2):
        #   BDI.bdi(self,Beliefs.agent_beliefs)

        # Mostramos las acciones que se realizaran
        print('ACTIONS:') 
        p = Plan.plan(self, Intents.agent_intents)  
        if Intents.agent_intents:
            del Intents.agent_intents[0]

        # Ejecutamos todas las acciones    
        for i in p:
            print('   > ' + i)
            exec(i) 

        return []

## Actualizacion Beliefs Desires Intents
class BDI:

    def bdi(self,newBelief):     
        ## Conjunto E B D I
        global Emotions, Beliefs, Desires, Intents 

        #Se actualizan las creencias B = brf_in(E,I,Bm)
        Beliefs.brf_in(Emotions,Intents,newBelief)
        print('BELIEFS:')
        for belief in Beliefs.agent_beliefs:
            print(" -", belief[0], belief[1], belief[2])

        #Se crean los deseos D = options(B,I)
        Desires.options(Beliefs,Intents)
        print('DESIRES:')
        for desire in Desires.agent_desires:
            print(" -", desire[0], desire[1], desire[2])     

        #Se filtran las intenciones I = filterI(E,B,D,I)
        Intents.filterI(Emotions,Beliefs,Desires.agent_desires)
        print('INTENTS:')
        for intent in Intents.agent_intents:
            print(" -", intent)

        # se estan manteniendo deseos, asi que esta linea los elimina, pero... ¿se pueden mantener deseos?
        Desires.agent_desires = [] 

        return []

## Interpretacion de planes
class Plan:

    def plan(self, Intents):
        p = []    
        for intent in Intents:
            for idx, val in enumerate(intent):    
                # Seleccionamos la primera intencion y las acciones correspondientes        
                if val == 'a_say':  
                    resp = intent[idx+1]
                    s = "Say.run(self, dispatcher, tracker, domain,'{0}')".format(str(resp))
                    p.append((s))
                # Nueva creencia
                if val == 'a_nB':
                    user_event = ['say',intent[idx+1],'none','','','','']   
                    s = "EBDI.run(self, dispatcher, tracker, domain,{0})".format(user_event)
                    p.append((s))
                # Eliminar creencia
                if val == 'a_dB':
                    s = "Beliefs.del_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                # Creencia cumplida
                if val == 'a_fB':
                    s = "Beliefs.fulfill_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                # Solicitud de camara
                if val == 'ki':
                    s = "Kinect.name('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                # Solicitud de interfaz
                if val == 'in':
                    s = "Interface.name('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                # Solicitud de base de datos
                if val == 'db':
                    s = "Database.name('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                # Solicitud de entrenador
                if val == 'co':
                    s = "Coach.name('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                if val == 'li':
                    s = "Listening.name('{0}')".format(str(intent[idx+1]))
                    p.append(s)
        return p

## Generar los ficheros de salida
class To_Speech(Action):

    def name(self) -> Text:
        return "to_speech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
       
        global msg, count, Emotions        

        print('----RESPONSES----')  
        tracker.get_slot('daytime') 
        tracker.get_slot('rol') 
        tracker.get_slot('ejercicio') 

        if count > 0:
            msg = get_latest_event(tracker.applied_events())     
            responses = msg[-count:]  
            CSV().name(responses) 
        count = 0

        return []

## Acciones ##

## Accion de hablar
class Say(Action):

    def name(self) -> Text:
        return "say"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            resp) -> List[Dict[Text, Any]]:
        
        hours = str(f"{dt.datetime.now().strftime('%H:%M')}")
        day = the_day(str(f"{dt.datetime.now().strftime('%A')}"))  
        nday = dt.datetime.now().strftime('%d')

        contador()
        print("   Dispatcher: " + str(count))   

        # Rasa dispara la respuesta junto a los valores de los slots        
        dispatcher.utter_message(response = resp, ejercicio = slot_ejercicio, day = day,
            daytime = slot_daytime, name = slot_name, rol = slot_rol, nday = nday,
            avatar = slot_avatar, hours = hours)

        return []

# Accion para usar la camara
class Kinect():
    def name(response):
        global watch, watchResponse
        watch = True
        watchResponse = response
        return "echo"

# Accion para usar la interfaz
class Interface():
    def name(response):
        global interface, interfaceResponse
        interface = True
        interfaceResponse = response
        return "echo"

'''
CLASE: BASE DE DATOS - acciones locales
'''
class Database():

    def name (response):
        global slot_user, date 
        global Beliefs,Emotions,Intents
        now = dt.datetime.now()
        # Seleccion de ejercicio
        if response == "select_exercise":
            print("select_exercise")
        if response == "update_data":
            print("update_data")
            Database.update_data()
        if response == "check_session":
            date = now.strftime("%Y-%m-%d")
            Database.routine_today(slot_user)                 
        # Seleccion de rutina de hoy
        if response == "select_routine" :         
            print("select_routine")
            date = now.strftime("%Y-%m-%d")
            contenido_user = getattr(db, "select_routine")(slot_user,date)
            if contenido_user is not None: 
                Database.routine(contenido_user)              
            else:
                print("No hay datos para esta fecha")
        # Seleccion de rutina del proximo dia
        if response == "select_next_routine" :  
            next_day = now + dt.timedelta(days=1)
            next_date = next_day.strftime("%Y-%m-%d")
            contenido_user = getattr(db, "select_routine")(slot_user,next_date)
            if contenido_user is not None: 
                Database.routine(contenido_user)
            else:
                print("No hay datos para esta fecha")
        # Seleccion de rutina del dia anterior
        if response == "select_previous_routine" :   
            previous_day = now - dt.timedelta(days=1)
            previous_date = previous_day.strftime("%Y-%m-%d")
            contenido_user = getattr(db, "select_routine")(slot_user,previous_date)
            if contenido_user is not None: 
                Database.routine(contenido_user)
            else:
                print("No hay datos para esta fecha")
        return "echo"

    def routine(contenido_user):
        global routine_say, exercises, animations
        exercises = []
        animations = []
        routine_say = True        
        print(contenido_user)       
        e = contenido_user['ejercicios']
        e_array = [int(x) for x in e.split(",")]        
        r = contenido_user['repeticiones']        
        r_array = [int(x) for x in r.split(",")]
        t = contenido_user['tiempos']        
        t_array = [int(x) for x in t.split(",")]
        select_exercise = "select_exercise"
        select_animation = "select_animation"
        for i in range(len(e_array)):                   
            e_name = getattr(db, select_exercise)(e_array[i])
            e_animation = getattr(db, select_animation)(e_array[i])
            if r_array[i] != 1:
                new_string = "{} con {} repeticiones de {} segundos.".format(
                e_name['name'],r_array[i],t_array[i])
            else:
                new_string = "{} con {} repetición de {} segundos.".format(
                e_name['name'],r_array[i],t_array[i])
            exercises.append(new_string)
            animations.append(e_animation['name'])
    
    # Acceso a la base de datos: Identificacion
    def login(user_id,user_pass):
        global slot_name, slot_rol, slot_user        
        login_user = getattr(db, "login")(user_id,user_pass)
        if login_user is not None:
            slot_name = login_user['name']
            slot_rol = login_user['rol']
            slot_user = user_id  
            return True
        else:
            return False

    # Acceso a la base de datos: Rutina para hoy
    def routine_today(user_id):
        global session_today, date
        global Beliefs,Emotions,Intents
        date = dt.datetime.now().strftime("%Y-%m-%d")
        session_today = getattr(db, "select_routine")(slot_user,date)
        if session_today is not None: 
            Beliefs.del_belief('without_routine')   
            user_event = ['know','with_routine',None,'']
            newBelief = Beliefs.new_belief(user_event)     
            Beliefs.brf_in(Emotions,Intents,newBelief)
            print("Sesión de Hoy: " + str(session_today))
            return True
        else:
            Beliefs.del_belief('with_routine')
            user_event = ['know','without_routine',None,'']
            newBelief = Beliefs.new_belief(user_event)     
            Beliefs.brf_in(Emotions,Intents,newBelief)  
            print("No hay Sesión para hoy")
            return False
   
    def update_data():
        global slot_ejercicio, slot_animacion, rutina_len, ejercicios_lista, animaciones_lista
        ejercicios_id = [int(x) for x in session_today['ejercicios'].split(',')]
        ejercicios_lista, animaciones_lista = Database.exercises_today(ejercicios_id)
        rutina_len = len(ejercicios_lista)
        slot_ejercicio = ejercicios_lista[0]
        slot_animacion = animaciones_lista[0]

    # Acceso a la base de datos: nombres y animaciones de los ejercicios
    def exercises_today(exercises_id):
        exercises,animations = getattr(db, "select_exercises")(exercises_id)
        if exercises is not None: 
            return exercises,animations
        else:
            return None

'''
CLASE: COACH
'''
# Accion para usar la demo
class Coach():
    def name (response):        
        global exercise_say, exercise_current, exercise_i       
        if exercise_i < rutina_len:
            exercise_current = ejercicios_lista[exercise_i]
            exercise_i += 1 
            exercise_say = True  
        print("Coach")

class Listening():
    def name (response):        
        listen = open("VoiceManager/listening.txt","w") 
        listen.close()
        print("Modo: escucha")


## Salida de las respuestas csv
class CSV():
    def name(self,responses):
        global watch, watchResponse, slot_animacion
        global interface, interfaceResponse
        global routine_say, exercises, animations
        global exercise_say, exercise_current
        output_csv = open('speech.csv','w+',newline='')
        writer = csv.writer(output_csv, delimiter =',')
        writer.writerow(['action','response','emotion','language','animation','emotionAzure','video','length','avatar'])
        animation_tag = 'informar'  
        video = ''  
        length = 0        
        for response in responses:
            if 'metadata' in response['metadata']:
                if 'subtext' in response['metadata']['metadata']:
                    animation_tag = str(response['metadata']['metadata']['subtext'])                    
                else:
                    animation_tag = slot_animacion
                if 'img' in response['metadata']['metadata']:
                    video = str(response['metadata']['metadata']['img'])
                else:
                    video = ''
                if 'length' in response['metadata']['metadata']:
                    length = float(response['metadata']['metadata']['length'])
                else:
                    length = 0
            else:
                animation_tag = slot_animacion
            print(' - ' + str(response['text']))
            writer.writerow(['say',str(response['text']), str(Emotions.estado),lang,animation_tag,str(Emotions.tag()),str(video),length,avatar])
        if(watch):
            writer.writerow(['watch',str(watchResponse)])
            watch = False
        elif(interface):
            writer.writerow(['interface',str(interfaceResponse)])
            interface = False
        elif(routine_say):
            for i,exercise in enumerate(exercises):
                writer.writerow(['say',str(exercise), str(Emotions.estado),lang,animations[i],str(Emotions.tag()),str(video),length,avatar])
            routine_say = False
            writer.writerow(['listen'])
        elif(exercise_say):            
            text_exercise = "Realizaremos unas " + str(exercise_current)
            writer.writerow(['say',str(text_exercise), str(Emotions.estado),lang,animation_tag,str(Emotions.tag()),str(video),length,avatar])
            exercise_say = False
            writer.writerow(['listen'])
        else:
            writer.writerow(['listen'])
        output_csv.close()

## Se ejecuta una sola vez al principio de una conversacion
class Dictionary:

    def get_synonym_mapper():
        result_dict = {}
        for nlu_md in os.listdir("data"):
            if nlu_md == 'nlu.md':
                path_md = "data/{0}".format(nlu_md)
                nlu_md_file = load_data(path_md)
                nlu_md_json = nlu_md_file.nlu_as_json()
                for item in json.loads(nlu_md_json)['rasa_nlu_data']['entity_synonyms']:
                    result_dict[item['value']] = item['synonyms']
        return result_dict
    
# EJECUCION INICIAL
slot_daytime = part_of_day(int(f"{dt.datetime.now().strftime('%H')}"))  
# Funcion Login Local
if Database.login("101","127"):
    # Funcion Rutine_today Local: Hay sesion para hoy
    if(Database.routine_today("101")):
        #user_event = ['know','with_routine',True]
        Database.update_data()
    # No hay sesion para hoy
    #else:
        #user_event = ['know','without_routine',True]   
    # Añade la creencia de rutina para hoy o no
    #Beliefs.agent_beliefs.append(user_event)
 
print("slot_name: " + str(slot_name))
print("slot_rol: " + str(slot_rol))
print("slot_user: " + str(slot_user))