# tippe python in den Terminal

import expyriment #wie library () in R

#Variablen definieren
n_trials_block = 4
n_blocks = 6
durations = 2000 #ms

flanker_stimuli = ['<<<<<<<', '>>>>>>>', '<<<><<<', '>>><>>>'] #eine Liste wie in R c(...) #Python zählt ab 0, nicht ab 1
# 0 congruent links, 1 congruent rechts, 2 inkongruent rechts, 3 inkongruent links

#tasten herausfinden
print(ord('x'))  # → 120
print(ord('m'))  # → 109

instructions = (
    "Drücken Sie die Taste, die dem Pfeil in der MITTE entspricht -\n" #\n ist ein Zeilenumbruch
    "Versuchen Sie, alle anderen Pfeile zu ignorieren. \n \n" #zweimal \n ist ein doppelter Zeilenumbruch
        "Drücken Sie die X-Taste, wenn der Pfeil nach links zeigt.\n"
            "Drücken Sie die M-Taste, wenn der Pfeil nach rechts zeigt. \n \n"
                "Drücken Sie die Leertaste, um den Test zu beginnen."
                ) #benachbarte String-Literale werden von Python automatisch zusammengefügt, kein zusätzlicher \ nötig

experiment = expyriment.design.Experiment(name = 'Flanker Task') #Experiment-Objekt
expyriment.control.initialize(experiment) #öffnet Fenster/initialisiert Experiment

#Schleife
for block in range (n_blocks): #range(n_blocks) (0, 1, 2, 3, 4, 5)
    temp_block = expyriment.design.Block(name=str(block + 1)) #benennt Blöcke 1-6
    for trial in range(n_trials_block): #vier trials pro block
        curr_stim = flanker_stimuli[trial] #Indices 0-3
        temp_stim = expyriment.stimuli.TextLine(text=curr_stim, text_size=40) #curr_stim = flanker_stimuli[trials] #Indices 0-3
        temp_trial = expyriment.design.Trial()
        temp_trial.add_stimulus(temp_stim) #verknüpft Text-Stimulus mit trial-objekt temp_trial
        
        if trial <= 1:
            trialtype = 'congruent' #python zählt ab 0, deshalb congruent 0 und 1
        elif trial > 1: #wie ifelse() in R?
            trialtype = 'incongruent'
        if curr_stim[3] == '<':
            correctresponse = 120
        elif curr_stim[3] == '>':
            correctresponse = 109
        
        temp_trial.set_factor ('trialtype', trialtype) #Faktoren setzen, wie Spalten in einem dataframe?
        temp_trial.set_factor ('correctresponse', correctresponse)

        temp_block.add_trial(temp_trial) #trial zum block hinzufügen

    temp_block.shuffle_trials () #block mischen #der punkt kann wie $ in R genutzt werden, hier wird der Punkt genutzt, um eine Funktion des Objekts aufzurufen
    experiment.add_block(temp_block) #zum Experiment hinzufügen #der Punkt greift auf alles zu, was zu einem Objekt gehört: Eigenschaften und Funktionen (universeller als $)

experiment.data_variable_names = ["block", "correctresp", "response", "trial",
                                  "RT", "accuracy", "trialtype"] #der Punkt mit () ruft Funktion ab (s.o.); der Punkt mit = speichert eine Eigenschaft, hier: Spaltenüberschriftenliste []

expyriment.control.start(skip_ready_screen=True) #startet das Experiment. skip_ready_screen: expyriment zeigt automatisch einen "ready?"-screen an, da auch =True gesetzt, wird dieser geskippt (wie TRUE/FALSE in R)
fixation_cross = expyriment.stimuli.FixCross() #erstellt fixation cross und speichert es in der Variable fixation_cross #nur erstellt, nicht angezeigt!! Das macht man mit .present()

#TextScreen() erstellt Textbildschirm mit Titel ('Flanker task') und Inhalt (instructions) -> schon vorab definiert s.o.
expyriment.stimuli.TextScreen('Flanker task', instructions).present() #wäre auch möglich statt .present() nochmal screen.present() in der nächsten Zeile # hier zusammengefasst: .present() zeigt ihn sofort an
experiment.keyboard.wait(expyriment.misc.constants.K_SPACE) #wartet darauf, dass TN eine Taste drückt, K_SPACE ist eine vordefinierte Konstante in expyriment, die den Tastencode für die Leertaste enthält #equivalent zu wait(keys=32)
#expyriment ist das Paket, keyboard ist ein Modul des Pakets, wait() ist quasi eine funktion? des Pakets

for block in experiment.blocks: #die äußere Schleife geht durch alle 6 Blöcke, die innere durch alle 4 trials pro Block 
    for trial in block.trials: #experiment.blocks und block.trials sind Listen, die expyriment automatisch befüllt
        fixation_cross.present() #zeigt fixation cross, das vorhin als objekt fixation_cross gespeichert wurde
        trial.stimuli[0].preload() #preload () lädt den Stimulus vorab in den Speicher, damit er später ohne Verzögerung erscheint. [0] = der erste und einzige Stimulus des Trials

        experiment.clock.wait(durations) #wartet 2000ms (zeigt Fixationskreuz an), vorab unter durations gespeichert
        trial.stimuli[0].present() #zeigt Flanker Stimulus an
        experiment.clock.reset_stopwatch() #startet Stoppuhr: ab hier wird Reaktionszeit gemessen
        key, rt = experiment.keyboard.wait(keys=[expyriment.misc.constants.K_x,  #wartet auf Tastendruck, aber NUR X oder M
                                            expyriment.misc.constants.K_m], #gibt zwei werte zurück key = welche Taste und rt= Reaktionszeit in ms
                                            duration = durations)
        experiment.clock.wait(durations - experiment.clock.stopwatch_time) #wartet die restliche Zeit bis 2000ms vergangen sind, so ist jeder Trial gleich lang

        if key == trial.get_factor ('correctresponse'): #vergleicht die gedrückte Taste mit der gespeicherten richtigen Antwort
            acc = 1 #richtig
        else:
            acc = 0 #falsch #correctresponse oben in innerer Schleife bei congruent/inkongruent definiert # außerdem bei set_factor 
        
        experiment.data.add([block.name, trial.get_factor('correctresponse'), #schreibt Ausgabedatei, entspricht Spaltennamen data_variable_name wir rbind() in R
                             key, trial.id, rt, acc,
                             trial.get_factor("trialtype")])
    
    if block.name != '6': #nach jedem Block außer dem letzten (!='6' bedeutet ungleich 6) wird eine Pause angezeigt
        expyriment.stimuli.TextScreen("Kurze Pause", "Block:"
                                      + str(int(block.name)+1) #+ verbindet strings wie paste0() in R
                                      ).present() #int macht string zur zahl wie as.integer() in R, damit +1 gerechnet werden kann; dann str() macht es zurück zu string wie as.character() in R
        experiment.clock.wait(5000) #dann 3s warten
expyriment.control.end(goodbye_text= "Vielen Dank für Ihre Teilnahme!",
                       goodbye_delay=5000) #beendet Experiment mit 2s Abschiedstext

