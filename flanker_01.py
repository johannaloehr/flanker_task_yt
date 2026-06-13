# tippe python in den Terminal

import expyriment #wie library () in R

#Bedingungen definieren
conditions = [
    {"label": "left_congruent","direction": "left", "congruency": "congruent", "color": "black"},
    {"label": "right_congruent", "direction": "right", "congruency": "congruent", "color": "black"},
    {"label": "left_incongruent","direction": "left", "congruency": "incongruent", "color": "black"},
    {"label": "right_incongruent","direction": "right", "congruency": "incongruent", "color": "black"},
    {"label": "neutral_up","direction": "neutral", "type": "up"},
    {"label": "neutral_down","direction": "neutral", "type": "down"},
    {"label": "left_green","direction": "left", "congruency": "congruent", "color": "green"},
    {"label": "right_green","direction": "right", "congruency": "congruent", "color": "green"},
    {"label": "left_red","direction": "left", "congruency": "congruent", "color": "red"},
    {"label": "right_red","direction": "right", "congruency": "congruent", "color": "red"},
]

#Anzahl der Trials definieren
#n_trials_block = 0

#for condition in conditions:
 #   if condition["direction"] == "neutral":
  #      n_trials_block += 12
   # else:
    #    n_trials_block +=6

#Variablen definieren
n_trials_block = len(conditions)
n_blocks = 2
durations = 1000 #ms

experiment = expyriment.design.Experiment(name = 'Flanker Task') #Experiment-Objekt
expyriment.control.initialize(experiment) #öffnet Fenster/initialisiert Experiment

canvases = [] #leere Liste

#Canvas erstellen Loop
for condition in conditions:
    canvas = expyriment.stimuli.Canvas(size=(800, 600))
    positions = [-60, -30, 0, 30, 60]
    mid = 2

    #neutraler Stimulus
    if condition["direction"] == "neutral":
        if condition["type"] == "up":
            symbol = "↑"
        elif condition["type"] == "down":
            symbol = "↓"

        for i, x in enumerate(positions):
            stim = expyriment.stimuli.TextLine(symbol, text_size=30, text_colour=(255, 255, 255))
            stim.position = (x, 0)
            stim.plot(canvas)
            
    
    #Bedingungen
    else:
        #Target bestimmen
        if condition["direction"] == "left":
            target = "←"
        else:
            target = "→"

        #Flanker bestimmen
        if condition["congruency"] == "congruent":
            flanker = target
        else:
            flanker = "→" if target == "←" else "←"

        for i, x in enumerate(positions):
            if i == mid:
                symbol = target
            else:
                symbol = flanker

        #Farbe definieren, nur in der Mitte, je nach Bedingung
            if i == mid:
                if condition["color"] == "green":
                    color = (0, 255, 0)
                elif condition["color"] == "red":
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 255)
            else:
                color = (255, 255, 255)

            stim = expyriment.stimuli.TextLine(symbol,text_size=30, text_colour=color)
            stim.position = (x, 0)
            stim.plot(canvas)
        
    canvas.present()

    canvases.append(canvas)

#Mapping definieren
response_mapping = {
    "black": {
        "left": expyriment.misc.constants.K_x,
        "right": expyriment.misc.constants.K_m
    },
    "green": {
        "left": expyriment.misc.constants.K_x,
        "right": expyriment.misc.constants.K_m
    },
    "red": {
        "left": expyriment.misc.constants.K_m,
        "right": expyriment.misc.constants.K_x
    }
}

#neutral ohne Antwort
no_response = None 

#tasten herausfinden
#print(ord('x'))  # → 120
#print(ord('m'))  # → 109

instructions = (
    "Drücken Sie die Taste, die dem Pfeil in der MITTE entspricht -\n" #\n ist ein Zeilenumbruch
    "Versuchen Sie, alle anderen Pfeile zu ignorieren. \n \n" #zweimal \n ist ein doppelter Zeilenumbruch
        "Drücken Sie die X-Taste, wenn der Pfeil nach links zeigt.\n"
            "Drücken Sie die M-Taste, wenn der Pfeil nach rechts zeigt. \n \n"
                "Drücken Sie die Leertaste, um den Test zu beginnen."
                ) #benachbarte String-Literale werden von Python automatisch zusammengefügt, kein zusätzlicher \ nötig

import random

#Trail-Loop
for block in range(n_blocks):
    temp_block = expyriment.design.Block(name=str(block + 1))
    trial_order = list(range(len(conditions)))
    random.shuffle(trial_order)

    for i in range(len(trial_order)):
        idx = trial_order[i]
        curr_condition = conditions[idx]
        curr_stim = canvases[idx]
        temp_trial = expyriment.design.Trial()
        temp_trial.add_stimulus(curr_stim)

        if curr_condition["direction"] == "neutral":
            correctresponse = -1
        else:
            correctresponse = response_mapping[curr_condition["color"]][curr_condition["direction"]]

        temp_trial.set_factor("correctresponse", correctresponse)
        temp_trial.set_factor("trialtype", curr_condition["label"])

        temp_block.add_trial(temp_trial)

    temp_block.shuffle_trials()
    experiment.add_block(temp_block)

experiment.data_variable_names = ["block", "correctresp", "response", "trial",
                                  "RT", "accuracy", "trialtype"] #der Punkt mit () ruft Funktion ab (s.o.); der Punkt mit = speichert eine Eigenschaft, hier: Spaltenüberschriftenliste []

expyriment.control.start(skip_ready_screen=True) #startet das Experiment. skip_ready_screen: expyriment zeigt automatisch einen "ready?"-screen an, da auch =True gesetzt, wird dieser geskippt (wie TRUE/FALSE in R)

fixation_cross = expyriment.stimuli.FixCross() #erstellt fixation cross und speichert es in der Variable fixation_cross #nur erstellt, nicht angezeigt!! Das macht man mit .present()

#TextScreen() erstellt Textbildschirm mit Titel ('Flanker task') und Inhalt (instructions) -> schon vorab definiert s.o.
expyriment.stimuli.TextScreen('Flanker task', instructions).present() #wäre auch möglich statt .present() nochmal screen.present() in der nächsten Zeile # hier zusammengefasst: .present() zeigt ihn sofort an
experiment.keyboard.wait(expyriment.misc.constants.K_SPACE) #wartet darauf, dass TN eine Taste drückt, K_SPACE ist eine vordefinierte Konstante in expyriment, die den Tastencode für die Leertaste enthält #equivalent zu wait(keys=32)
#expyriment ist das Paket, keyboard ist ein Modul des Pakets, wait() ist quasi eine funktion? des Pakets

for block in experiment.blocks:

    for trial in block.trials:

        fixation_cross.present()
        experiment.clock.wait(durations)

        stim = trial.stimuli[0]

        stim.preload()
        stim.present()  

        experiment.clock.reset_stopwatch()

        key, rt = experiment.keyboard.wait(
            keys=[
                expyriment.misc.constants.K_x,
                expyriment.misc.constants.K_m
            ],
            duration=durations
        )

        remaining = max(0, durations - experiment.clock.stopwatch_time)
        experiment.clock.wait(remaining)

        #Accuracy
        correctresponse = trial.get_factor("correctresponse")
        if correctresponse is -1:
            acc = None  # neutral / no-go
        else:
            acc = int(key == correctresponse)

        #Daten speichern
        experiment.data.add([
            block.name,
            correctresponse,
            key,
            trial.id,
            rt,
            acc,
            trial.get_factor("trialtype")
        ])

    #Pause
    if block.name != str(n_blocks):

        expyriment.stimuli.TextScreen(
            "Kurze Pause",
            "Block: " + str(int(block.name) + 1)
        ).present()

        experiment.clock.wait(5000)
expyriment.control.end(goodbye_text= "Vielen Dank für Ihre Teilnahme!",
                       goodbye_delay=5000) #beendet Experiment mit 2s Abschiedstext

#Pfeile größer, entsprechend des Sehwinkels
#Anzahl Trials, siehe Literatur (v.a. wegen errors)
#Übungsblock 
#Randomisierungsbedingung, nicht ehr als 2 hintereinander
#Pause selbst beenden lassen