#!/usr/bin/python
# -*- coding: utf-8 -*-

import string                                                       #importiamo il modulo string per le funzioni su

class Rotore:
    """ Oggetto rotore, che ha 3 parametri:

"sequenza" - una lista di caratteri corrispondenti al cifrario;
"cambio" - un carattere corrispondente al 'notch', il punto del rotore che fa scattare anche il successivo. """

    def __init__(self, sequenza, prima_lettera, cambio):
        self.alf=1
        self.pl=prima_lettera
        self.alfabeto=string.ascii_uppercase
        self.sequenza=sequenza                                      #questa diventa una stringa     
        self.cambio=cambio
    def ruota(self):
        self.sequenza=self.sequenza[1:]+[self.sequenza[0]]          #il rotore ruota di una posizione e di conseguenza anche la cablatura del cifrario
    def inverti_ruota(self):
        self.sequenza=[self.sequenza[25]]+self.sequenza[:25]
    def impostazione(self,imp):                                     #impostazione di partenza del rotore, stabilisce la cablatura iniziale del cifrario
        for i in range(imp-1):
            self.ruota()
    def offset(self):
        while self.alfabeto[0]!=self.alf:
            self.alfabeto=self.alfabeto[1:]+self.alfabeto[0]        #stringa completa dell'alfabeto del rotore a partire dall'offset

class Plugboard:
    """ Oggetto plugboard, ossia dove sono accoppiate due lettere alla volta per un massimo di 10 coppie,
per essere scambiate tra loro durante la codifica; ha come parametro "coppie", un dizionario delle suddette coppie. """

    def __init__(self, coppie):
        self.coppie=coppie     
    def scambio(self,lettera):                                      #metodo che scambia le coppie inserite nel dizionario
        if lettera in self.coppie:
            return self.coppie[lettera]
        return lettera
        

rot1=Rotore("E,K,M,F,L,G,D,Q,V,Z,N,T,O,W,Y,H,X,U,S,P,A,I,B,R,C,J".split(','),'E','R')      #rotori canonici di Enigma I
rot2=Rotore("A,J,D,K,S,I,R,U,X,B,L,H,W,T,M,C,Q,G,Z,N,P,Y,F,V,O,E".split(','),'A','F')
rot3=Rotore("B,D,F,H,J,L,C,P,R,T,X,V,Z,N,Y,E,I,W,G,A,K,M,U,S,Q,O".split(','),'B','W')
rot4=Rotore("E,S,O,V,P,Z,J,A,Y,Q,U,I,R,H,X,L,N,F,T,G,K,D,C,M,W,B".split(','),'E','K')
rot5=Rotore("V,Z,B,R,G,I,T,Y,U,P,S,D,N,H,L,X,A,W,M,J,Q,O,F,E,C,K".split(','),'V','A')

rifa={string.ascii_uppercase[n]:'EJMZALYXVBWFCRQUONTSPIKHGD'[n] for n in range(26)}    #riflettori canonici di Enigma I 
rifb={string.ascii_uppercase[n]:'YRUHQSLDPXNGOKMIEBFZCWVJAT'[n] for n in range(26)}   
rifc={string.ascii_uppercase[n]:'FVPJIAOYEDRZXWGCTKUQSBNMHL'[n] for n in range(26)}   

class Enigma:
    """ Oggetto Enigma, la macchina vera e propria. Ha 5 parametri:

"r1" - il primo (oggetto) rotore che viene attraversato dalla corrente elettrica;
"r2" - il secondo rotore attraversato dalla corrente;
"r3" - il terzo rotore;
"rif" - il riflettore (che è anch'esso un oggetto riflettore);
"plug" - la plugboard (oggetto plugboard). """

    def __init__(self,r1,r2,r3,rif,plug):
        self.r1=r1
        self.r2=r2
        self.r3=r3
        self.pp={self.r1.alfabeto[n]:self.r1.sequenza[n] for n in range(26)}     #crea un dizionario che associa all'alfabeto del rotore la corrispondente cifratura
        self.ppr={self.pp[x]:x for x in self.pp}                                 #dizionario inverso del precedente
        self.sp={self.r2.alfabeto[n]:self.r2.sequenza[n] for n in range(26)}     #idem
        self.spr={self.sp[x]:x for x in self.sp}
        self.tp={self.r2.alfabeto[n]:self.r3.sequenza[n] for n in range(26)}     #idem
        self.tpr={self.tp[x]:x for x in self.tp}
        self.rif=rif
        self.plug=plug
        
    def aggiorna(self):
        "Metodo che aggiorna gli attributi dei rorori dopo averli ruotati"

        self.pp={self.r1.alfabeto[n]:self.r1.sequenza[n] for n in range(26)}
        self.ppr={self.pp[x]:x for x in self.pp}
        self.sp={self.r1.alfabeto[n]:self.r2.sequenza[n] for n in range(26)}
        self.spr={self.sp[x]:x for x in self.sp}
        self.tp={self.r1.alfabeto[n]:self.r3.sequenza[n] for n in range(26)}
        self.tpr={self.tp[x]:x for x in self.tp}
        
    def rotori(self,carattere):
        "Metodo che restituisce il parametro 'carattere' codificato"
        
        self.r1.ruota()                                                    #ruota il primo rotore ad ogni chiamata
        if self.r1.sequenza[0]==self.r1.cambio:                            #ruota il secondo rotore una volta per rotazione completa del primo
            self.r2.ruota()
        if self.r2.sequenza[0]==self.r2.cambio:                            #ruota il secondo e il terzo rotore una volta per rotazione completa del secondo
            self.r2.ruota()
            self.r3.ruota()
                
        self.aggiorna()
        lettera=self.tp[self.sp[self.pp[carattere]]]                       #simula il passaggio di corrente attraverso i rotori all'andata
        return self.ppr[self.spr[self.tpr[self.rif[lettera]]]]             #simula il passaggio di corrente attraverso il riflettore e i rotori al ritorno 


def codifica(macchina,lettera):
    """ Funzione che prende in input una stronga e la codifica attraverso Enigma, restituendo la stringa criptata. Ha due parametri:

"macchina" - è istanza dell'oggetto Enigma, la macchina Enigma che abbiamo creato con impostazioni prestabilite;
"testo" - la stringa di testo da codificare. """

    lettera=macchina.plug.scambio(lettera.upper())                         #simula il passaggi di corrente nella plugboard all'andata
    lettera=macchina.rotori(lettera)                                       #mette in funzione il resto della macchina
    lettera=macchina.plug.scambio(lettera)                                 #simula il passaggi di corrente nella plugboard al ritorno
    return lettera
