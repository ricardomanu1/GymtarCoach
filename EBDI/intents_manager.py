import numpy as np

class intents_manager(object):

    def __init__(self):
        self.agent_id = 'intents_manager'

        # Estado inicial de las intenciones, en este caso vacio
        self.agent_intents = []
        self.intents = []
        self.intentsData()

# Biblioteca de planes
    def intentsData(self):
        ### PLANS ###
        ## User: me saluda        
        self.intents.append(('say','utter_saludar',['saludar'],'a_say','utter_saludar','a_dB','saludar','a_say','utter_interes','a_nB','espero_respuesta'))
       
        ## YO: voy a empatizar con el estado de animo del usuario  
        self.intents.append(('say','utter_empatizar_bien',['espero_respuesta','estado_bien'],'a_dB','espero_respuesta','a_dB','estado_bien','a_say','utter_empatizar_bien','a_say','utter_solicitar'))
        self.intents.append(('say','utter_empatizar_mal',['espero_respuesta','estado_mal'],'a_dB','espero_respuesta','a_dB','estado_mal','a_say', 'utter_empatizar_mal','a_say','utter_solicitar'))
                
        ## Identidad del avatar 
        self.intents.append(('say','utter_identidad',['identidad'],'a_dB','identidad','a_say','utter_identidad'))

        ## Identidad user
        self.intents.append(('say','utter_identidad_user',['identidad_user'],'a_dB','identidad_user','a_say','utter_identidad_user'))
        
        ## User: me ha dicho como se siente
        self.intents.append(('say','utter_empatizar_bien',['estado_bien'],'a_say','utter_empatizar_bien','a_dB','estado_bien'))
        self.intents.append(('say','utter_empatizar_mal',['estado_mal'],'a_say','utter_empatizar_mal','a_dB','estado_mal'))
        self.intents.append(('say','utter_empatizar_cansancio',['estado_cansancio'],'a_say','utter_empatizar_cansancio','a_dB','estado_cansancio'))
        self.intents.append(('say','utter_empatizar_emocion',['estado_emocion'],'a_say','utter_empatizar_emocion','a_dB','estado_emocion'))
        
        ## Rutina
        self.intents.append(('say','utter_rutina',['rutina'],'a_dB','rutina','db','check_session','a_nB','select_session'))
        self.intents.append(('say','utter_rutina',['select_session','with_routine'],'a_dB','select_session','a_say','utter_rutina','db','select_routine'))
        self.intents.append(('say','utter_rutina',['select_session','without_routine'],'a_dB','select_session','a_say','utter_no_rutina'))

        self.intents.append(('say','utter_rutina_proxima',['rutina_proxima'],'a_dB','rutina_proxima','a_say','utter_rutina_proxima','db','select_next_routine'))
        self.intents.append(('say','utter_rutina_anterior',['rutina_anterior'],'a_dB','rutina_anterior','a_say','utter_rutina_anterior','db','select_previous_routine'))
        
        self.intents.append(('say','utter_con_rutina',['rutina_comprobacion'],'db','check_session','a_dB','rutina_comprobacion','a_nB','check_session'))
        self.intents.append(('say','utter_con_rutina',['check_session','with_routine'],'a_dB','check_session','a_say','utter_con_rutina'))
        self.intents.append(('say','utter_sin_rutina',['check_session','without_routine'],'a_dB','check_session','a_say','utter_sin_rutina'))

        self.intents.append(('say','iniciar_rutina',['iniciar_rutina'],'a_dB','iniciar_rutina','db','check_session','a_nB','start_session'))
        self.intents.append(('say','iniciar_rutina',['start_session','with_routine'],'a_dB','start_session','db','update_data','a_say','utter_iniciar_rutina','a_say','utter_reloj','a_nB','a_reloj'))
        self.intents.append(('say','iniciar_rutina',['start_session','without_routine'],'a_dB','start_session','a_say','utter_no_rutina'))
     
        self.intents.append(('say','reloj', ['a_reloj','afirmar'],'a_dB','a_reloj','a_dB','afirmar','a_say','utter_afirmativo','a_say','utter_preparado','a_nB','a_preparado')) 
        self.intents.append(('say','reloj', ['a_reloj','negar'],'a_dB','a_reloj','a_dB','negar','a_say','utter_afirmativo','a_say','utter_no_reloj','a_say','utter_preparado','a_nB','a_preparado')) 
        
        self.intents.append(('say','preparado', ['a_preparado','afirmar'],'a_dB','a_preparado','a_dB','afirmar','a_say','utter_afirmativo','a_say','utter_ejercicio','a_say','utter_eje','ki','k_observa')) 
        self.intents.append(('say','preparado', ['a_preparado','negar'],'a_dB','a_preparado','a_dB','negar','a_say','utter_avisado','a_nB','a_esperando')) 
        
        self.intents.append(('say','preparado', ['a_esperando','listo'],'a_dB','a_esperando','a_dB','listo','a_say','utter_afirmativo','a_say','utter_ejercicio','a_say','utter_eje','ki','k_observa')) 

        ## Instrucciones Gymtar Interface

        self.intents.append(('know','inicio',['inicio'],'a_fB','inicio','a_say','utter_saludar','a_say','utter_solicitar','in','i_inicio'))
      
        self.intents.append(('say','utter_login',['login'],'a_say','utter_login','a_dB','login','in','i_login'))
        self.intents.append(('know','login',['login'],'a_dB','login','db','login','a_say','utter_interes','a_nB','espero_respuesta'))
                
        self.intents.append(('say','utter_register',['register'],'a_say','utter_register','a_dB','register','in','i_register'))
        self.intents.append(('know','register',['register'],'a_dB','register','a_say','utter_registro'))
        
        ## De UNREAL
        self.intents.append(('say','demo_rutina',['demo_rutina','with_routine'],'a_dB','demo_rutina','a_say','utter_demo_rutina','a_say','utter_ejercicio','co','siguiente_ejercicio',
                             'a_say','utter_descanso','co','siguiente_ejercicio','a_say','utter_descanso','co','siguiente_ejercicio','a_say','utter_fin_rutina'))
        self.intents.append(('know','solicito_ejercicio',['solicito_ejercicio'],'a_dB','solicito_ejercicio','a_say','utter_eje','ki','k_observa')) #utter_eje_preparate
        self.intents.append(('know','solicito_descanso',['solicito_descanso'],'a_dB','solicito_descanso','a_say','utter_descanso','ki','k_observa')) 

        self.intents.append(('know','descanso',['descanso'],'a_dB','descanso','a_say','utter_descanso'))
   
        ## User:'hace preguntas básicas'
        self.intents.append(('say','utter_responder_hora',['pregunta_hora'],'a_say','utter_responder_hora','a_dB','pregunta_hora'))
        self.intents.append(('say','utter_responder_dia',['pregunta_dia'],'a_say','utter_responder_dia','a_dB','pregunta_dia'))
       
        ## User:'se despide'
        self.intents.append(('say','utter_despedir',['despedir'],'a_dB','saludar','a_dB','despedir','a_say','utter_despedir')) 

        ## Regla: Fuera de dominio
        self.intents.append(('say', 'out_of_scope', ['out_of_scope'],'a_dB','out_of_scope','a_say', 'utter_out_of_scope'))
        ## Regla: No se ha oido
        self.intents.append(('know', 'nlu_fallback', ['nlu_fallback'],'a_dB','nlu_fallback','a_say', 'utter_please_rephrase'))
        
        ## Comprobacion: Animaciones
        self.intents.append(('say', 'a_narrar', ['a_narrar'],'a_dB','a_narrar','a_say', 'utter_a_narrar'))
        self.intents.append(('say', 'a_informar', ['a_informar'],'a_dB','a_informar','a_say', 'utter_a_informar'))
        self.intents.append(('say', 'a_saludar', ['a_saludar'],'a_dB','a_saludar','a_say', 'utter_a_saludar'))
        self.intents.append(('say', 'a_preguntar', ['a_preguntar'],'a_dB','a_preguntar','a_say', 'utter_a_preguntar'))
        self.intents.append(('say', 'a_despedir', ['a_despedir'],'a_dB','a_despedir','a_say', 'utter_a_despedir'))

        ## Comprobacion: Camara
        self.intents.append(('say', 'k_observa', ['k_observa'],'a_dB','k_observa','ki', 'k_observa'))

        self.intents.append(('know', 'k_escucha', ['k_escucha'],'a_dB','k_escucha','li','k_escucha'))
                
        
    def filterI(self, Emotions, Beliefs, Desires):
        desires_fulfill = []
        intents_selected = [i for i in self.intents if i[1] in [d[1] for d in Desires]]
        for intent in intents_selected:
            if intents_manager.check(self, intent[2], Beliefs, Emotions):
                self.agent_intents.append(intent) 
                desires_fulfill.append(intent[1])
        for idx,ele in enumerate(Desires):
            if ele[1] in desires_fulfill:
                del Desires[idx]     
                
        # print("El conjunto de intenciones es: " +  str(len(self.agent_intents)))
        # en el caso de varias intenciones hay que tomar la prioritaria
        if len(self.agent_intents) > 1:
            aux = 1
            for i in self.agent_intents:            
                if len(i[2])>=aux:
                    aux = len(i[2])
                    aux_intent = i
            self.agent_intents = []
            self.agent_intents.append(aux_intent)
                    
        if(len(self.agent_intents)==0 and Beliefs.inter):
            print("la creencia sin nada es:")
            for b in Beliefs.belief_events:       
                #print(" ",b[1])
                Beliefs.del_belief(b[1])
            Beliefs.belief_events.clear()

    def check(self, terms, Beliefs, Emotions):
        beliefs = [b[1] for b in Beliefs.agent_beliefs]
        Belief_check = Beliefs.agent_beliefs
        for i in terms:
           if i not in beliefs:
                return False
           elif Belief_check[beliefs.index(i)][2] == False:
                return False
        return True
           
    def get_context(self):
        context_intents = [x[2] for x in self.intents]        
        context = set(np.concatenate(context_intents))
        return context
