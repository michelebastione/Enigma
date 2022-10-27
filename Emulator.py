#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, copy, pygame
import enigma               #'enigma' è il modulo da me creato contenente la struttura della Macchina Enigma.      
from string import ascii_uppercase as alfabeto

pygame.init()               #inizializiamo il modulo 'pygame'
directory = os.getcwd()

#Carichiamo tutte le immagini e i suoni che ci serviranno:
titolo=pygame.image.load(os.path.join(directory,'resources','logo.png'))                    #immagine del titolo (per evitare che il font non venga letto dal pc);        
tasto=pygame.image.load(os.path.join(directory,'resources','tasto.png'))                    #texture dei tasti della tastiera;
ingranaggio=pygame.image.load(os.path.join(directory,'resources','gear.png'))               #icona delle impostazioni;
ingr=pygame.image.load(os.path.join(directory,'resources','ingr.png'))                      #icona del settaggio dei rotori;
icona=pygame.image.load(os.path.join(directory,'resources','icona.png'))                    #icona della finestra principale;
plug_i=pygame.image.load(os.path.join(directory,'resources','plug.png'))                    #icona della finestra plugboard;

#numeri romani:
n0=pygame.image.load(os.path.join(directory,'resources','1.png'))                           
n1=pygame.image.load(os.path.join(directory,'resources','2.png'))                         
n2=pygame.image.load(os.path.join(directory,'resources','3.png'))                         
n3=pygame.image.load(os.path.join(directory,'resources','4.png'))                        
n4=pygame.image.load(os.path.join(directory,'resources','5.png'))                           

freccia=pygame.image.load(os.path.join(directory,'resources','freccia.png'))                #icona tasto indietro;
press=pygame.mixer.Sound(os.path.join(directory,'resources','keystroke.wav'))               #suono dei tasti;
pygame.mixer.music.load(os.path.join(directory,'resources','tig.wav'))                      #colonna sonora.

#font vari da utilizzare per tasti, scritte e bottoni:
font1=pygame.font.SysFont('couriernew',66,True)                                            
font2=pygame.font.SysFont('candara',36)                                                     
font3=pygame.font.SysFont('lucidaconsole',16)                                               
font4=pygame.font.SysFont('copperplategothic',82)                                           
font5=pygame.font.SysFont('bookantiqua',30)
font6=pygame.font.SysFont('timesnewroman',36)

press.set_volume(0.4)                                                                       #regoliamo il volume del suono
pygame.mixer.music.set_volume(0.7)                                                          #regoliamo il volume della musica
tastiera="QWERTYUIOPASDFGHJKLZXCVBNM"                                                       #stringa rappresentante la tastiera QWERTY
bottoni={f"pygame.K_{carattere.lower()}": carattere for carattere in tastiera}           #dizionario che lega ad ogni tasto sulla tastiera il relativo carattere

class key():
    " Classe dei tasti di Enigma "
    
    def __init__(self,lettera):
        self.texture=copy.copy(tasto)                                                       #copiamo la texture del tasto e la aggiungiamo
        self.tasto_bianco=font1.render(lettera,True,(255,255,255))                          #texture del tasto spento
        self.tasto_giallo=font1.render(lettera,True,(255,255,0))                            #texture del tasto acceso
    def spento(self):
        "Metodo che aggiunge la texture della lettera spenta a quella del tasto"    
        self.texture.blit(self.tasto_bianco,(30,12)) 
    def acceso(self):
        "Metodo che aggiunge la texture della lettera accesa a quella del tasto"
        self.texture.blit(self.tasto_giallo,(30,12))

class button():
    """ Classe dei bottoni delle impostazioni:

'pos' - coppia di valori per la posizione del bottone;
'dim' - coppia di valori per la dimensione del bottone;
'testo' - stringa che rappresenta il testo del bottone.
'font' - font del testo. """
    
    def __init__(self, pos, dim, testo, font, colore=(0,0,0)):
        self.on=True                                                              #segnalatore di accensione o spegnimento dell'interruttore
        self.pos=pos
        self.dim=dim
        self.testo=font.render(testo,True,colore)                                 #renderizziamo il solo testo del bottone
        self.testo_on=font.render(testo+": ON",True,colore)                       #renderizziamo il testo ON del bottone
        self.testo_off=font.render(testo+": OFF",True,colore)                     #renderizziamo il testo OFF del bottone
        self.hitbox=(range(pos[0],pos[0]+dim[0]),range(pos[1],pos[1]+dim[1]))     #creiamo una hitbox per il bottone, ossia i range orizzontale e verticale
    def stampa(self):
        " Meteodo che disegna i bottoni e integra il tasto semplice "
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0],self.pos[1],self.dim[0],self.dim[1]),2)   #disegna il bottone
        pygame.display.get_surface().blit(self.testo,(self.pos[0]+5,self.pos[1]+9))                                             #integra il testo        
    def acceso(self):
        " Metodo che disegna i bottoni e integra il testo di acceso "
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0],self.pos[1],self.dim[0],self.dim[1]),2)   #disegna il bottone
        pygame.display.get_surface().blit(self.testo_on,(self.pos[0]+5,self.pos[1]+9))                                          #integra il testo
        self.on=True                                                                                                            #accende il segnalatore
    def spento(self):
        " Metodo che disegna i bottoni e integra il testo di acceso "
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0],self.pos[1],self.dim[0],self.dim[1]),2)   #disegna il bottone
        pygame.display.get_surface().blit(self.testo_off,(self.pos[0]+5,self.pos[1]+9))                                         #integra il testo
        self.on=False                                                                                                           #spegne il segnalatore
    def switch(self):                                                                                                           #scambia self.acceso() e self.spento()
        " Metodo che funge da interruttore per il bottone " 
        if self.on:
            self.spento()
        else:
            self.acceso()
    def stato(self):                                                                                                            #stampa l'immagine corrispondente...
        " Metodo che conferma lo stato di accensione o spegnimento del bottone "                                                #...all'attuale config. del bottone
        if self.on:
            self.acceso()
        else:
            self.spento()

class rotori():
    """ Classe dei rotori, comprende le istanze degl'oggetto 'Rotore' del modulo enigma e le relative informazioni grafiche:
'rotore' - istanza di Rotore di enigma;
'pos' - coppia delle coordinate (in lista, non tupla) dell'immagine;
'id' - numero o lettera identificante il rotore/rifelttore;
'lun' - dimensione del'immagine. """
    
    def __init__(self, rotore, pos, idn, lun):                                                      
        self.rotore=rotore
        self.pos=pos                                            #questo attributo salverà in memoria le coordinate dell'immagine al variare della sua posizione
        self.pos_bckp=(pos[0],pos[1])                           #questo attributo salverà in memoria le coordinate della posizione iniziale dell'immagine
        self.id=idn
        self.lun=lun
        #questo attributo è una coppia di range rappresentanti l'estensione spaziale dell'immagine
        self.hitbox=(range(self.pos[0],self.pos[0]+lun[0]),range(self.pos[1],self.pos[1]+82))  
    def stampa_solo_rotori(self):
        " Metodo che stampa a video l'immagine del rotore "
        impostazione.blit(eval('n'+str(self.id)),(self.pos[0],self.pos[1]))
    def stampa_riflettori(self):
        " Metodo che stampa a video l'immagine del riflettore "
        impostazione.blit(font4.render(self.id.upper(),True,(0,0,0)),(self.pos[0],self.pos[1]))        
    def reset(self):
        " Metodo che resetta le coordinate e le impostazioni inizali del rotore"
        self.pos=[self.pos_bckp[0],self.pos_bckp[1]]            
        if type(self.rotore)!=dict:                             #esegue il seguente codice se l'oggetto rotore non è un dizionario
            while self.rotore.sequenza[0]!=self.rotore.pl:      #questo ciclo permette di ruotare il rotore finchè non torna alla posizione di partenza
                self.rotore.ruota()
            self.rotore.alf='A'                                 #resettiamo anche l'offset
            self.rotore.offset()                                #aggiorniamo le impostazioni
        

class plugboard():
    """  Classe della plugboard, comprende qualsiasi istanza dell'oggetto Plugboard del modulo Enigma e le relative informazioni grafiche:
'pos' - coppia di coordinate che rappresentano le componenti spaziale dell'oggetto. """
    
    def __init__(self, pos):
        self.cp={}                                              #dizionario inseriremo le coppie della plugboard
        self.pos=pos
        self.riferimento={}                                     #dizionario dove associeremo ad ogni hitbox orizzontale un oggetto identificativo del bottone
        self.hitbox=[]                                          #lista delle coppie dei range delle hitbox ogni bottone della plugboard
        self.hitbox_o=[]                                        #lista delle hitbox orizzontali dei bottoni della plugboard
        self.hitbox_v=[range(pos[1]+45,pos[1]+90)]*26           #lista delle hitbox verticali di ogni bottone dell plugboard
        self.n=0                                                #contatore delle coppie inserite
        for i in range(26):
            exec(f'self.hitbox{i}=(range(pos[0]+45*i,pos[0]+45*(i+1)),range(pos[1]+45,pos[1]+90))')  #creiamo le hitbox perogni bottone e inseriamole nella lista
            exec(f'self.h{i}=None')                                                                  #creiamo dei valori da inserire in 'riferimento'
            self.hitbox_o.append(range(pos[0]+45*i,pos[0]+45*(i+1)))                                 #aggiungiamo le hitbox orizzontali alla lista                                       
            self.riferimento[self.hitbox_o[i]]=(f'self.h{i}',i)                                      #aggiungiamo chiavi e valori a 'riferimento'

    def reset(self):
        " Metodo che resetta la plugboard "
        for i in range(26):
            exec(f'self.h{i}=None')                       #resettiamo la posizione
        self.n=0                                          #resettiamo il contatore
            
    def disegna(self):
        " Metodo che disegna lo schema della plugboard e le lettere"
        for i in range(26):

            #disegniamo i rettangoli superiori:
            pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0]+45*i,self.pos[1],45,45),3)
            #disegniamo le lettere al loro interno:
            pygame.display.get_surface().blit(font6.render(alfabeto[i],True,(0,0,0)),(self.pos[0]+10+45*i,self.pos[1]))
            #disegniamo i rettangoli inferiori:
            pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0]+45*i,self.pos[1]+45,45,45),3)

    def assegna(self, alfa, beta):
        """ Questo metodo è breve ma FONDAMENTALE!
Assegna ad uno degli spazi definiti sopra un rotore o un riflettore passato come parametro:

'alfa' - è una stringa che rappresenta lo spazio a cui associare;
'beta' - è una stringa che rappresenta l'oggetto da associare. """

        #siccome i parametri sono due stringhe utilizziamo la funzione 'exec' per trasformarle in comandi
        exec(f'{alfa}={beta}')    
        
class cruscotto():
    """ Classe del 'cruscotto' di Enigma, dove andremo ad inserire i rotori:
'pos' - è una coppia di numeri per la posizione del cruscotto a video. """

    def __init__(self,pos):
        self.pos=pos

        #i successivi 3 attributi comprendono una coppia di range (estensione spaziale) per i primi 3 spazi del cruscotto
        self.hitbox1=(range(self.pos[0],self.pos[0]+110),range(self.pos[1],self.pos[1]+120))
        self.hitbox2=(range(self.pos[0]+110,self.pos[0]+220),range(self.pos[1],self.pos[1]+120))
        self.hitbox3=(range(self.pos[0]+220,self.pos[0]+330),range(self.pos[1],self.pos[1]+120))

        #i seguenti 2 attributi sono le liste delle hitbox orizzontali e verticali dei rotori
        self.hitbox_o=[self.hitbox1[0],self.hitbox2[0],self.hitbox3[0]] 
        self.hitbox_v=[self.hitbox1[1]]*3

        #il seguente attributo è un dizionario che associa ad ogni hitbox orizzontale una coppia:
        #il primo elemento è una stringa che rappresenterà, una volta eseguito, il rotore (o riflettore) che occupa lo spazio associato;
        #il secondo è semplicemte il numero ordinale dello spazio occupato nel cruscotto di cui sopra.
        self.riferimento={self.hitbox1[0]:('self.u',0),self.hitbox2[0]:('self.d',1),self.hitbox3[0]:('self.t',2)}

        self.u=None                 #oggetto nel primo spazio
        self.d=None                 #oggetto nel secondo spazio
        self.t=None                 #oggetto nel terzo spazio
        self.q=None                 #oggetto nel quarto spazio
        
    def reset(self):
        " Metodo che svuota le caselle del cruscotto, di fatto resettandole "
        
        self.u=None                 
        self.d=None                 
        self.t=None                 
        self.q=None          

    def disegna(self):
        """ Questo metodo disegnerà lo scheletro del cruscotto e le scritte associate """
        
        #i seguenti 4 comandi disegnano i rettangoli
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0],self.pos[1],110,120),3)
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0]+110,self.pos[1],110,120),3)                         
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0]+220,self.pos[1],110,120),3)
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),pygame.Rect(self.pos[0]+350,self.pos[1],110,120),3)

        #questo ciclo mette le scritte dei rotori
        for i in range(1,4):
            pygame.display.get_surface().blit(font3.render(f'Rotore {i}',True,(0,0,0)),(self.pos[0]+16+110*(i-1),self.pos[1]-16))

        #e questo comando scrive la scritta del riflettore
        pygame.display.get_surface().blit(font3.render('Riflettore',True,(0,0,0)),(self.pos[0]+356,self.pos[1]-16))

    def assegna(self, a_cosa, cosa):
        """ Questo metodo è breve ma FONDAMENTALE!
Assegna ad uno degli spazi definiti sopra un rotore o un riflettore passato come parametro:

'a_cosa' - è una stringa che rappresenta lo spazio a cui associare;
'cosa' - è una stringa che rappresenta lìoggetto da associare. """

        #siccome i parametri sono due stringhe utilizziamo la funzione 'exec' per trasformarle in comandi
        exec(a_cosa+'='+cosa)           
        

class tasti_plug():
    """ Classe dei tasti della plugboard:

'idn' - carattere corrispondente alla lettera del tasto;
'pos' - coordinate della posizione del tasto. """
    
    def __init__(self,idn, pos):
        self.idn=idn
        self.pos=pos                                        #questo attributo salverà in memoria le coordinate dell'immagine al variare della sua posizione                                    
        self.pos_bckp=(pos[0],pos[1])                       #questo attributo salverà in memoria le coordinate della posizione iniziale dell'immagine
        self.hitbox=(range(self.pos[0],self.pos[0]+36),range(self.pos[1],self.pos[1]+36))   #coppia di range delle hitbox del tasto
        self.lun=(36,36)                                    #estensione dei tasti

    def stampa(self):
        " Metodo che stampa a video l'immagine il tasto "
        pygame.display.get_surface().blit(font6.render(self.idn,True,(0,0,0)),((self.pos[0]),self.pos[1]))

    def reset(self):
        " Metodo che resetta le coordinate iniziali del tasto "
        self.pos=[self.pos_bckp[0],self.pos_bckp[1]]


def schermata(nome, dimensioni, title, icon):
    """ Funzione che apre una finestra interattiva:

'nome' - stringa per il nome da assegnare alla finestra;
'dimensioni' - coppia di dimensioni della finestra;
'title' - stringa della caption della finestra;
'icon' - icona della finestra. """
    
    globals()[nome]=pygame.display.set_mode((dimensioni[0],dimensioni[1]))                          #aggiungiamo la finestra alle variabili globali                       
    pygame.display.set_caption(title)                                                               #aggiungiamo il titolo alla finestra
    pygame.display.set_icon(icon)                                                                   #aggiungiamo l'icona alla finestra


def impostazioni():
    """ Questa non è una funzione generica, bensì una funzione molto specifica:
serve ad inizializzare la finestra delle impostazioni """
    
    impostazione.fill((255,255,255))                                                                #coloriamo lo schermo di bianco
    lunotto.disegna()                                                                               #disegnamo il lunotto (istanza della classe cruscotto)
    impostazione.blit(freccia,(8,425))                                                              #sovrapponiamo la freccia
    impostazione.blit(font3.render('Indietro',True,(0,0,0)),(12,490))                               #sovrapponiamo la scritta 'indietro'
    immagini_rotori()                                                                               #stampiamo le immagini dei rotori
    Suono.stato()                                                                                   #stampiamo il bottone 'Suono'
    Musica.stato()                                                                                  #stampiamo il bottone 'Musica'
    plug_b.stampa()                                                                                 #stampiamo il bottone 'Plugboard'
    globals()['res']=button((550,300),(110,45),'RESET',font2,(230,0,0))                             #aggiungiamo il bottone 'RESET' alle variabili globali
    res.stampa()                                                                                    #stampiamo il bottone 'RESET'
    pygame.draw.rect(impostazione,(0,0,0),pygame.Rect(20,-1,320,205),1)                             #disegniamo il 'contenitore' dei rotori
    pygame.draw.rect(impostazione,(0,0,0),pygame.Rect(383,10,280,100),1)                            #disegniamo il 'contenitore' dei riflettori
    impostazione.blit(font5.render('Rotori',True,(0,0,0)),(135,202))                                #disegniamo la scritta 'Rotori'
    impostazione.blit(font5.render('Riflettori',True,(0,0,0)),(465,108))                            #disegniamo la scritta 'Riflettori'
    for i in range(3):
        impostazione.blit(ingr,(70+110*i,400))                                                      #disegniamo i bottoni per le impostazioni dei rotori


def plug_board():
    """ Anche questa è una funzione molto specifica:
serve ad inizializzare la finestra della plugboard """

    centralina.fill((255,255,255))                                                                  #coloriamo lo schermo di bianco
    plug.disegna()                                                                                  #disegniamo la plugboard
    centralina.blit(freccia,(8,285))                                                                #disegniamo la freccia indietro
    centralina.blit(font3.render('Indietro',True,(0,0,0)),(12,355))                                 #disegniamo la scritta 'Indietro'
    globals()['res']=button((535,320),(110,45),'RESET',font2,(230,0,0))                             #aggiungiamo il bottone 'RESET' alle variabili globali
    res.stampa()                                                                                    #stampiamo il bottone 'RESET'
    immagini_plug()                                                                                 #stampiamo i tasti della plugboard


def imp_rot(rotore):
    """ Questa è una funzione un po' più generica:
serve ad inizializzare la finestra delle impostazioni dei rotori

'rotore' - istanza della classe rotori """

    imp_rotori.fill((255,255,255))                                                                  #coloriamo lo schermo di bianco 
    pygame.draw.line(imp_rotori,(0,0,0),(256,0),(256,300),3)                                        #dividiamo la finestra in due parti
    imp_rotori.blit(font5.render('Posizione',True,(230,0,0)),(70,15))                               #stampiamo la scritta 'Posizione'
    imp_rotori.blit(font5.render('Cablaggio',True,(230,0,0)),(320,15))                              #stampiamo la scritta 'Cablaggio'
    imp_rotori.blit(font1.render(rotore.rotore.alfabeto[0],True,(0,0,0)),(110,100))                 #stampiamo la lettera corrispondente all'offset alfabetico

    #il seguente codice stampa a video il numero corrispondente alla rotazione di partenza del rotore
    if rotore.rotore.sequenza.index(rotore.rotore.pl)==0:                                           
        imp_rotori.blit(font1.render('1',True,(0,0,0)),(375,100))
    else:
        imp_rotori.blit(font1.render(str((26-rotore.rotore.sequenza.index(rotore.rotore.pl)+1)),True,(0,0,0)),(375,100))  #machecazzo


def click(evento,larghezza, altezza):
    """Metodo che restituisce 'True' se il mouse viene cliccato entro un determinato spazio:

'evento' - evento di pygame;
'larghezza' - range della boundary orizzontale;
'altezza' - range della boundary verticale. """
    
    if evento.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:                       #controlliamo che ci sia un click
         if (pygame.mouse.get_pos()[0] in larghezza and pygame.mouse.get_pos()[1] in altezza):      #controlliamo le boundary
                return True
    return False


def click_av(evento, larghezza, altezza):
    """Metodo simile al precedente ma più avanzato, controlla più spazi contemporaneamente e restituisce l'intervallo orizzontale cliccato oltre a 'True':

'evento' - evento di pygame;
'larghezza' - lista di più range della boundary orizzontale;
'altezza' - lista di più range della boundary verticale. """                                        
    
    if evento.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:                       #controlliamo che ci sia un click
        for intervallo in larghezza:                                                                #controlliamo i range di tutti gli oggetti
            if pygame.mouse.get_pos()[0] in intervallo:                                             #controlliamo la boundary orizzontale
                if pygame.mouse.get_pos()[1] in altezza[larghezza.index(intervallo)]:               #controlliamo la boundary verticale corrispondente
                    return (True,intervallo)
    return (False,)


def scambia(primo_click, oggetti, schema, check_oggetti, check_schema, diz_schema,pos_in, dim):   
    """ Questa funzione è un vero e proprio incubo, serve a spostare un rotore o un tasto plugboard nello spazio assegnato:  
    
'primo_click' - range orizzontale del primo oggetto cliccato (riflettore o tasto plugboard);
'oggetti' - specifica se l'oggetto è un rotore o un tasto plugboard;
'schema' - specifica se il luogo dove spostare è il lunotto (istanza di cruscotto) o la centralina (istanza di plugboard);
'check_oggetti' - hitbox orizzontale di 'oggetti';
'check_schema' - hitbox di 'schema';
'diz_schema' - dizionario di riferimento tra 'schema' e 'oggetti';
'pos_in' - coordinate della posizione iniziale di 'schema';
'dim' - dimensioni di 'schema'. """
    
    sposta=oggetti+str(check_oggetti.index(primo_click))

    #lo scambio avviene all'interno del loop
    while True:

        pygame.time.delay(10)                                                                       #settiamo il refresh a 10ms                                                                                        
        snap=click_av(pygame.event.wait(),check_schema[0],check_schema[1])                          #assegniamo una variabile alle hitbox del tasto cliccato

        if snap[0]:                                                                                 #se questi viene cliccato:

            if oggetti=='alf_':                                                                     #se l'oggetto è un tasto plugboard:
                specchio='alf_'+str(eval(diz_schema+'[snap[1]][1]'))                                #identifichiamo il tasto plugboard corrispondente alla casella
                if sposta==specchio:                                                                #se proviamo ad appaiare una lettera con sè stessa:
                    plug.n-=1                                                                       #indietreggiamo col contatore
                    break                                                                           #interrompe il ciclo
                if getattr(plug,'n')>=10 and getattr(plug,'h'+specchio.strip('alf_'))==None:        #se il contatore è >=10 e la casella è vuota:
                    break                                                                           #interrompi il ciclo
                if getattr(plug,'h'+specchio.strip('alf_'))!=None:                                  #se invece la casella non è vuota (contatore <10):
                    exec('plug.h'+specchio.strip('alf_')+'.reset()')                                #resetta la posizione dei tasti specchio precedentemente inseriti
                plug.assegna('plug.h'+sposta.strip('alf_'),specchio)                                #assegna ala casella i nuovi tasti specchio
                exec(specchio+'.pos[0]='+str(pos_in[0]+dim[0]*eval(sposta.strip('alf_'))+(dim[0]-eval(specchio+'.lun[0]'))//2)) #aggiorna la posizione dei tasti...
                exec(specchio+'.pos[1]='+str(pos_in[1]+(dim[1]-eval(specchio+'.lun[1]'))//2))                                   #...sia orizzontale che verticale

            if getattr(eval(schema),eval(diz_schema+'[snap[1]][0]').strip('self.'))!=None:          #se la casella non è vuota (vale anche per i rotori):
                exec(schema+'.'+eval(diz_schema+"[snap[1]][0].strip('self.')")+'.reset()')          #resetta la posizione dell'oggetto precedentemente inserito
            exec(schema+'.assegna('+diz_schema+'[snap[1]][0]'+',sposta)')                           #assegna l'oggetto alla casella
            exec(sposta+'.pos[0]='+str(pos_in[0]+dim[0]*eval(diz_schema+'[snap[1]][1]')+(dim[0]-eval(sposta+'.lun[0]'))//2)) #aggiorna la posizione dell'oggetto...
            exec(sposta+'.pos[1]='+str(pos_in[1]+(dim[1]-eval(sposta+'.lun[1]'))//2))                                        #...sia orizzontale che verticale
            break                                                                                   #interrompi il ciclo
               
        if evento.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:                   #se clicchiamo il mouse da qualche altra parte:                                            
            break                                                                                   #il loop si interrompe e non succede altro

        
def immagini_rotori():
    " Funzione che stampa le immagini di tutti i rotori "
    
    for r in rotori_tutti:
        if rotori_tutti.index(r)<5:                                     #questo stampa i rotori
            r.stampa_solo_rotori()      
        else:                                                           #e questo stampa i riflettori
            r.stampa_riflettori()

def immagini_plug():
    " Funzione che stampa le immagini di tutti i tasti plugboard "
    
    for p in plug_tutti:
        p.stampa()

rotori_tutti=[]                                                         #inizializziamo una lista che contenga tutte le istanze di 'rotori'                        

for i in range(6):                                                      #creiamo tutte le istanze di 'rotori', riempiendo al contempo la lista di cui sopra 
    if i<5:
        if i<3:
            exec(f'rotori_{i}=rotori(enigma.rot{i+1},[35+100*i,10],{i},({32*(i+1)},82))')          #creiamo i rotori dall'uno al tre
        else:
            exec(f'rotori_{i}=rotori(enigma.rot{i+1},[72+150*(i-3),115],{i},({98-29*(i-3)},82))')  #creiamo i rotori 4 e 5
        rotori_tutti.append(eval(f'rotori_{i}'))                                                                               #aggiungiamoli a 'rotori_tutti'
    else:
        for e in 'abc':
            exec('riflettori_'+e+'=rotori(enigma.rif'+e+",[390+100*'abc'.index(e),10],"+"'"+e+"'"+f',({"80"},)*2)')          #creiamo i riflettori
            rotori_tutti.append(eval('riflettori_'+e))                                                                            #aggiungiamoli a 'rotori_tutti'


def reset(oggetti):
    """ Funzione che resetta posizione e impostazione degli oggetti inseriti come parametri: 

'oggetti - possono essere rotori o tasti 'plugboard'; """
    
    for o in eval(oggetti+'_tutti'):           
        o.reset()                                                       #utilizziamo il metodo 'reset' corrispondente all'oggetto in questione
    exec('immagini_'+oggetti+'()')                                      #stampiamo a video gli oggetti resettati

    
hitbox_rotori_o=[i.hitbox[0] for i in rotori_tutti]                     #list comprehension contenente le hitbox orizzontali dei rotori 
hitbox_rotori_v=[i.hitbox[1] for i in rotori_tutti]                     #list comprehension contenente le hitbox verticali dei rotori 
hitbox_rot_imp=[range(70,102),range(180,212),range(290,322)]            #lista che contenente le hitbox orizzontali dei tasti per le impostazioni dei rotori

lunotto=cruscotto((30,275))                                             #istanza di 'cruscotto', dove inseriremo i rotori
plug=plugboard((15,160))                                                #istanza i 'plugboard', dove inseriremo le coppie di lettere della plugboard appunto

istruzioni=button((1040,3),(155,50),'Istruzioni',font2,(0,0,155))       #crea un bottone per le istruzioni
Suono=button((513,397),(200,50),'Suono',font2)                          #crea un bottone per il suono
Musica=button((513,455),(200,50),'Musica',font2)                        #crea un bottone per la musica
plug_b=button((525,195),(152,50),'Plugboard',font5,(0,0,0))             #crea un bottone per la plugboard

r_diz={0:'u',1:'d',2:'t'}

for car in tastiera:                                                    #aggiungiamo tutti le immagini dei tasti alle variabili globali:
    globals()[car]=key(car)                                             #a lettera maiuscola corrisponde l'istanza di 'key' relativa a quella lettera;
    exec(car+".spento()")                                               #usiamo il comando 'exec' per eseguire il metodo 'spento()', che renderizza il tasto bianco.

plug_tutti=[]                                                           #inizializziamo una lista che conterrà tutte le istanze di 'tasti_plug'
for i in range(26):
    if i<13:
        globals()['alf_'+str(i)]=tasti_plug(alfabeto[i],[150+70*i,15])  #creiamo tutte le istanze di 'tasti_plug'...
        plug_tutti.append(eval('alf_'+str(i)))                          #...e aggiungiamole a 'plug_tutti'
    else:
        #le ultime 13 (quelle inferiori) sono spostate di un pixel per evitare un conflitto di hitbox orizzontali con quelle superiori:
        globals()['alf_'+str(i)]=tasti_plug(alfabeto[i],[151+70*(i-13),75])
        plug_tutti.append(eval('alf_'+str(i)))

hitbox_plug_o=[h.hitbox[0] for h in plug_tutti]                         #list comprehension delle hitbox orizzontali delle istanze di 'tasti_plug'
hitbox_plug_v=[h.hitbox[1] for h in plug_tutti]                         #list comprehension delle hitbox verticali delle istanze di 'tasti_plug'
    
attivo=True                                                             #variabile di controllo dell'esecuzione del programma            
pygame.mixer.music.play(-1)                                             #riproduciamo la colonna sonora
schermata('schermo',(1200,650),'nigma Machine Emulator',icona)          #apriamo la schermata principale    

#loop principale, il programma vero e proprio viene eseguiti al suo interno:
while attivo:
    
    pygame.time.delay(10)                                               #refresh dei segnali di input
                                                        
    schermo.fill((255,255,255))                                         #coloriamo uniformemente lo schermo di bianco
    schermo.blit(titolo,(600-titolo.get_width()//2,10))                 #sovrapponiamo il titolo
    schermo.blit(ingranaggio,(1100,550))                                #sovrapponiamo l'icona impostazioni
    istruzioni.stampa()

    #i successivi tre loop aggiungono le immagini dei tasti sullo schermo distribuendole appunto su tre righe nel modo seguente:
    for c in range(10):             #prima riga   

        #la prima riga crea la texture
        schermo.blit(eval(tastiera[c]+".texture"),(55+100*c+10*c,310))
        
        #la seconda riga crea l'attributo hitbox del tasto
        exec(tastiera[c]+".hitbox=(range(55+100*c+10*c,55+100*c+10*c+100),range(310,410))")
        
    for c in range(9):              #seconda riga
        schermo.blit(eval(tastiera[c+10]+".texture"),(120+100*c+10*c,425))
        exec(tastiera[c+10]+".hitbox=(range(120+100*c+10*c,120+100*c+10*c+100),range(425,525))")
    for c in range(7):              #terza riga
        schermo.blit(eval(tastiera[c+19]+".texture"),(200+100*c+10*c,540))
        exec(tastiera[c+19]+".hitbox=(range(200+100*c+10*c,200+100*c+10*c+100),range(540,640))")

    intervallix=[]                                                      #inizializziamo due liste, relativamente per le hitbox orizzontali...
    intervalliy=[]                                                      #... e per quelle verticali di ogni singola istanza di 'key' (i tasti)
    for i in range(26):                                                 #riempiamo le liste di cui sopra tramite questo ciclo for
        intervallix+=[eval(tastiera[i]+".hitbox[0]")]                   
        intervalliy+=[eval(tastiera[i]+".hitbox[1]")]  

    pygame.display.flip()                                               #aggiorniamo lo schermo
    evento=pygame.event.wait()                                          #assegniamo una variabile evento
   
    if evento.type==pygame.QUIT or (evento.type==pygame.KEYDOWN and evento.key==pygame.K_ESCAPE):
        attivo=False                                                    #termina il loop e chiude il programma se si preme ESC o la X

    if click(evento,istruzioni.hitbox[0],istruzioni.hitbox[1]):
        os.popen(os.path.join(directory,'resources', 'istruzioni.txt'))
        
    if not any([lunotto.u==None,lunotto.d==None,lunotto.t==None, lunotto.q==None]):
        
        if (evento.type==pygame.KEYDOWN and evento.key in bottoni):         #esegue i seguenti comandi se premiamo un tasto registrato:
            press.play()                                                    #riproduciamo il suono del tasto;                 

            #utilizziamo la funzione 'codifica' del modulo enigma per cifrare la lettera cliccata:
            fin_cod=enigma.codifica(finalmente_enigma,bottoni[evento.key])  

            exec(fin_cod+".acceso()")                                       #"accende" il tasto codificato;
            pygame.display.flip()                                           #aggiorna il display.
        if evento.type==pygame.KEYUP and evento.key in bottoni:             #quando smettiamo di premere il tasto:
            for b in tastiera:
                exec(b+".spento()")                                         #"spegne" tutti i tasti;
            pygame.display.flip()                                           #aggiorna il display.

        if click_av(evento, intervallix, intervalliy)[0]:                   #se clicchiamo nelle boundaries:
            press.play()                                                    #riproduce il suono del tasto;

            #utilizziamo la funzione 'codifica' del modulo enigma per cifrare la lettera cliccata:
            fin_cod=enigma.codifica(finalmente_enigma,tastiera[intervallix.index(click_av(evento, intervallix, intervalliy)[1])])

            exec(fin_cod+".acceso()")                                       #"accende" il tasto codificato;
            pygame.display.flip()                                           #aggiorna il display.

        if evento.type==pygame.MOUSEBUTTONUP:                               #se smettiamo di cliccare:
            for b in tastiera:                                              #"spegne" tutti i tasti;
                exec(b+".spento()")
            pygame.display.flip()                                           #aggiorna lo schermo.

    if click(evento,range(1100,1200),range(550,650)):                   #se clicchiamo sull'ingranaggio:
        pygame.display.quit()                                           #chiude la finestra corrente;
        schermata('impostazione',(720,512),'Impostazioni',ingr)         #apre la finestra impostazioni tramite una chiamata alla funzione schermata();
        setting=True                                                    #variabile di controllo dell'esecuzione della finestra impostazioni.

        #ciclo in cui viene eseguita la finestra impostazioni
        while setting:
            
            pygame.time.delay(10)                                       #settaggio del refresh dei segnali di input
            impostazioni()                                              #carichiamo il contenuto della finestra tramite la chiamata alla funzione impostazione() 
            
            pygame.display.flip()                                       #aggiorniamo lo schermo
            imp_ev=pygame.event.wait()                                  #assegniamo un'altra variabile evento

            if imp_ev.type==pygame.QUIT:                                #se clicchiamo sulla X:
                setting=False                                           #termina entrambi i loop (vedi in fondo) e chiude il programma

            if imp_ev.type==pygame.KEYDOWN and imp_ev.key==pygame.K_RETURN: #se clicchiamo su INVIO:
                break                                                   #termina solo il loop delle impostazioni e ritorna alla finestra principale
                 
            if click(imp_ev,Suono.hitbox[0],Suono.hitbox[1]):           #se clicchiamo sul bottone Suono:
                impostazione.fill((255,255,255))                        #riempiamo lo schermo di bianco;
                Suono.switch()                                          #accendiamo/spegniamo l'interruttore;
                if Suono.on:                                            #se è acceso:
                    press.set_volume(0.4)                               #alziamo il volume; 
                else:                                                   #se è spento:
                    press.set_volume(0)                                 #azzeriamo il volume;
                pygame.display.flip()                                   #aggiorniamo il display.

            if click(imp_ev,Musica.hitbox[0],Musica.hitbox[1]):         #se clicchiamo sul bottone Musica:
                impostazione.fill((255,255,255))                        #riempiamo lo schermo di bianco;
                Musica.switch()                                         #accendiamo/spegniamo l'interruttore;
                if Musica.on:                                           #se è acceso:
                    pygame.mixer.music.play(-1)                         #riproduciamo la musica; 
                else:                                                   #se è spento:
                    pygame.mixer.music.stop()                           #fermiamo la riproduzione della musica;
                pygame.display.flip()                                   #aggiorniamo il display.

            if click(imp_ev,res.hitbox[0],res.hitbox[1]):               #se clicchiamo sul bottone "RESET":
                reset('rotori')                                         #resetta impostazioni e posizioni di tutti i rotori
                lunotto.reset()                                         #svuota il lunotto

            click_1=click_av(imp_ev,hitbox_rotori_o,hitbox_rotori_v)                    #assegniamo una variabile al click (se c'è)
            if click_1[0]:                                                              #se clicchiamo su uno dei rotori o riflettori:

                if hitbox_rotori_o.index(click_1[1])<5:                                 #se è un rotore:
                    #La seguente funzione posiziona il rotore cliccato nello spazio del lunotto che si cliccherà successivamente
                    scambia(click_1[1],'rotori_','lunotto',hitbox_rotori_o,(lunotto.hitbox_o,lunotto.hitbox_v),'lunotto.riferimento',(30,275),(110,120))

                else:                                                                   #se invece è un riflettore:
                    sposta='riflettori_'+'abc'[hitbox_rotori_o.index(click_1[1])-5]     #assegniamo il rotore in questione alla variabile 'sposta';
                    if getattr(lunotto,'q')!=None:                                      #se lo spazio è già occupato:
                        lunotto.q.reset()                                               #resetta alla posizione iniziale il rotore attuale;
                    lunotto.assegna('self.q',sposta)                                    #inseriamo il riflettore cliccato nello spazio selezionato;
                    exec(sposta+'.pos[0]=403')                                          #aggiorniamo la posizione...
                    exec(sposta+'.pos[1]=290')                                          #...del riflettore appena inserito;

                immagini_rotori()                                                       #stampa a video le immagini dei rotori e riflettori aggiornate.
                                                                  
            r_imp=click_av(imp_ev,hitbox_rot_imp,[range(400,432)]*3)                    #assegniamo una variabile che corrisponda alla hitbox cliccata          
            if r_imp[0] and eval('lunotto.'+r_diz[hitbox_rot_imp.index(r_imp[1])])!=None:   #se dove si è cliccato è già inserito un rotore:
                pygame.display.quit()                                                   #chiudiamo la schermata impostazioni 
                schermata('imp_rotori',(512,200),'Rotore '+str(hitbox_rot_imp.index(r_imp[1])+1),ingr) #apriamo una schermata per le impostazioni del rotore
                rots=True                                                               #variabile di controllo

                #ciclo all'interno del quale vengono eseguite le impostazioni
                while rots:                                                 
                    pygame.time.delay(10)                                               #tempo di aggiornamento dello schermo fissato a 10ms
                    pygame.display.flip()                                               #aggiorna lo schermo
                    
                    imp_rot(eval('lunotto.'+r_diz[hitbox_rot_imp.index(r_imp[1])]))     #chiama la funzione 'imp_rot' per inizializzare la nuova finestra
                    r_ev=pygame.event.wait()                                            #assegniamo una variabile evento


                    if r_ev.type==pygame.KEYDOWN:                                                   #se premiamo un tasto:
                        if r_ev.key==pygame.K_UP:                                                   #se è la freccia su:    
                            eval('lunotto.'+r_diz[hitbox_rot_imp.index(r_imp[1])]).rotore.ruota()   #ruotiamo il rotore in avanti
                        if r_ev.key==pygame.K_DOWN:                                                 #se è la freccia giù:
                            eval('lunotto.'+r_diz[hitbox_rot_imp.index(r_imp[1])]).rotore.inverti_ruota()   #ruotiamo il rotore all'indietro
                        if r_ev.key in bottoni:                                                     #se è una letera dell'alfabeto:
                            eval('lunotto.'+r_diz[hitbox_rot_imp.index(r_imp[1])]).rotore.alf=bottoni[r_ev.key]  #spostiamo l'offset del rotore a quella lettera
                            eval('lunotto.'+r_diz[hitbox_rot_imp.index(r_imp[1])]).rotore.offset()  #aggiorniamo il rotore
                        if r_ev.key==pygame.K_RETURN:                                               #se premiamo INVIO:
                            pygame.display.quit()                                                   #chiudiamo la schermata corrente
                            break                                                                   #usciamo dal loop

                    if r_ev.type==pygame.QUIT:                                                      #se clicchiamo la X
                        pygame.display.quit()                                                       #chiudiamo la schermata corrente
                        rots=False                                                                  #disattiviamo la variabile di controllo

                if rots:                                                         #se la variabile di controllo è attiva:
                    schermata('impostazione',(720,512),'Impostazioni',ingr)      #apre la finestra impostazioni tramite una chiamata alla funzione schermata();
                else:                                                            #altrimenti:
                    setting=False                                                #disattiva la variabile di controllo
                    break                                                        #esce dal loop e termina l'esecuzione del programma

            if click(imp_ev,plug_b.hitbox[0],plug_b.hitbox[1]):                 #se clicchiamo sul bottone 'Plugboard':
                pygame.display.quit()                                           #chiudiamo la corrente schermata
                schermata('centralina',(1200,375),'Plugboard',plug_i)           #apriamo la schermata 'centralina'
                cent=True                                                       #variabile di controllo

                #ciclo entro il quale viene eseguita la plugboard
                while cent:
                    pygame.time.delay(10)                                       #settiamo il refresh della schermata a 10ms
                    pygame.display.flip()                                       #aggiorniamo lo schermo
                    plug_board()                                                #inizializziamo la schermata tramite la funzione 'plug_board()'
                    plug_ev=pygame.event.wait()                                 #aspettiamo che venga registrato un evento

                    if click(imp_ev,res.hitbox[0],res.hitbox[1]):               #se clicchiamo sul bottone 'RESET':           
                        reset('plug')                                           #resettiamo i tasti
                        plug.reset()                                            #svuotiamo la plugboard

                    click_2=click_av(plug_ev,hitbox_plug_o,hitbox_plug_v)       #assegniamo una variabile alle hitbox del tasto cliccato
                    if click_2[0]:                                              #se viene cliccato un tasto:
                
                        #la seguente chiamata alla complicatissima funzione permette di posizionare la coppia di lettere nella plugboard
                        scambia(click_2[1],'alf_','plug',hitbox_plug_o,(plug.hitbox_o,plug.hitbox_v),'plug.riferimento',(20,202),(45,45))
                        plug.n+=1                                               #il contatore aumenta di 1 (arrivato a 10 non si potranno inserire nuove coppie)
                        for i in range(26):
                            if eval('plug.h'+str(i))!=None:                     #se c'è una casella non vuota:
                                exec('plug.cp[alfabeto['+str(i)+']]=plug.h'+str(i)+'.idn')  #inseriamo la coppia che rappresenta nel dizionario delle coppie
                        
                    #se clicchiamo sulla freccia o premiamo invio
                    if click(plug_ev,range(85),range(285,475)) or (plug_ev.type==pygame.KEYDOWN and plug_ev.key==pygame.K_RETURN):
                        break       #torniamo alla schermata impostazioni

                    #se clicchiamo sulla X
                    if plug_ev.type==pygame.QUIT:
                        cent=False  #disattiva la variabile di controllo 

                if cent:                                                         #se la variabile di controllo è attiva:
                    pygame.display.quit()                                        #chiude la schermata plugboard;
                    schermata('impostazione',(720,512),'Impostazioni',ingr)      #ritorna alla finestra impostazioni tramite una chiamata alla funzione schermata();
                else:                                                            #se la variabile di controllo è inattiva:
                    setting=False                                                #chiude tutti i loop e termina il programma

            
            if click(imp_ev,range(80),range(440,500)):                                  #se clicchiamo sulla freccia:
                break                                                                   #terminiamo il loop e torniamo alla schermata principale.
            
        if setting:                                                                     #se la variabile di controllo è attivata:
            pygame.display.quit()                                                       #chiude la schermata impostazioni;
            schermata('schermo',(1200,650),'Enigma Machine Emulator',icona)             #riapre la finestra principale 

            #se tutte le caselle di rotori e riflettore sono state occupate
            if not any([lunotto.u==None,lunotto.d==None,lunotto.t==None, lunotto.q==None]):
                finalmente_rotore_1=lunotto.u.rotore                                    #crea il primo rotore della macchina con le impostazioni stabilite
                finalmente_rotore_2=lunotto.d.rotore                                    #crea il secondo rotore della macchina con le impostazioni stabilite
                finalmente_rotore_3=lunotto.t.rotore                                    #crea il terzo rotore della macchina con le impostazioni stabilite
                finalmente_riflettore=lunotto.q.rotore                                  #crea il riflettore della macchina
                finalmente_plugboard=enigma.Plugboard(plug.cp)                          #crea la plugboard della macchina con le impostazioni stabilite

                #crea l'istanza di 'Enigma' del modulo enigma che utilizzeremo per codificare le lettere:
                finalmente_enigma=enigma.Enigma(finalmente_rotore_1,finalmente_rotore_2,finalmente_rotore_3,finalmente_riflettore,finalmente_plugboard)
        else:   #altrimenti:
            attivo=False                                                                #disattiviamo la variabile di controllo

pygame.quit()                                                                           #terminiamo il modulo pygame e chiudiamo il programma
