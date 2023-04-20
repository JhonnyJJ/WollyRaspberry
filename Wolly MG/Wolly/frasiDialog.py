# wake words
wword = ["hey wally", "ciao wally", "ok wally"]

# ------- ARRAYS FOR WOLLY -------

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

posso = ["vuoi che ti dica quello che so fare? ", "vuoi sentire cosa so fare? ", "sei curioso di sapere cosa so fare? "]

ecco = ["D'accordo, ecco una lista di quello che so fare!", "Va bene, ecco cosa so fare!",
        "so fare alcune cose simpatiche tra cui "]

#indovinelli da aggiungere
fare = ["So raccontare le barzellette, so fare gli indovinelli, so fare un gioco di imitazione e so cantare o ballare, "]

vedere = ["vorresti vedermi fare qualcosa?", "ti piacerebbe vedermi fare qualcosa?", "vuoi che faccia qualche azione?",
          "vuoi mettermi alla prova?"]

allora = ["allora vorresti sapere una piccola curiosità su di me?",
          "magari preferisci sentire qualche fatto curioso su di me?",
          "che ne dici di sentire qualche informazione in più su di me?"]

ciao = ["ciao sono wolly, ", "heila ciao, io sono wolly, ", "hey ciao, mi chiamo wolly, "]

ascolto = ["resto in ascolto, ", " ", "sono tutto orecchi, ", "sono a tua disposizione, ", "adesso sono in ascolto, "]

quando = ["quando hai bisogno di me chiamami e ti risponderò", "se avessi bisogno di me chiamami", "se volessi sapere quello che so fare chiamami",
          "se avessi bisogno di me chiamami"]

# ------- ERROR phrases -------
err = ["forse non sono stato programmato per rispondere a questo!", "Mi dispiace, non so darti una risposta precisa.",
       "faccio difficoltà a capire cosa intendi.", "vorrei poterti dare una risposta ma non posso!",
       "ora non so risponderti, quando saprò la risposta sarai la prima persona a cui lo dirò!"]

# ------- not understood phrases -------
notundst = ["non sono riuscito a sentirti! Ripeti quello che hai detto", "come scusa, non ho capito. Ripeti quello che hai detto", "scusa non ho capito. Ripeti quello che hai detto",
            "non riesco a sentirti! Ripeti quello che hai detto"]

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!",
              "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma "]

# ------- HUMAN INPUTS -------

responses = ["hey ciao, ", "ciao, ", "heila ciao, "]

ok = [r"\bok\b", r"\bsì\b", r"\bva bene\b", r"\bcerto\b", r"\bsi\b"]  # r vale a dire la stringa raw, \b...\b invece è la parola singola separata da caratteri e numeri

nonSo = [r"\bnon lo so\b", r"\bnon so\b"]

niente = [r"\bnulla\b", r"\bniente\b", r"\bnon importa\b", r"\blascia stare\b"]

barze = [r"\bbattuta\b", r"\bbarzelletta\b", r"\bridere\b", r"\bbarzellette\b"]

indovina = [r"\bindovinello\b", r"\bindovinelli\b", r"\brompicapo\b", r"\benigma\b"]

ballo = [r"\bballa\b", r"\bballare\b", r"\bballo\b", r"\bdanza\b", r"\bballiamo\b", r"\bdanziamo\b"]

canto = [r"\bcanta\b", r"\bcantare\b", r"\bcantami\b", r"\bcanto\b"]

imita = [r"\bimita\b", r"\bimitare\b", r"\bimitazione\b" r"\mimo\b" r"\mimi\b"]

# ------- DIALOG PHRASES -------
curiosita = ["sono un robottino creato per diventare un insegnante, prima o poi con tanto duro lavoro lo diventerò",
             "sono stato creato utilizzando un computer che si chiama Raspberry, è esattamente come un computer normale, solo un po più piccolo!",
             "sono stato ospite alle ATP finals di Torino, è stato molto divertente!",
             "sono stato creato circa 6 anni fa qui nell'università di Torino; in questi 6 anni sono cambiato moltissimo",
             "ho partecipato a delle attività didattiche nelle scuole, mi sono divertito moltissimo"]

noproblem = ["ok nessun problema, ", "okay , ", " va bene, ", "Va bene, nessun problema! ",
             "D'accordo, ", "Ho capito, ", "perfetto, "]

magarifatto = ["magari posso incuriosirti con un fatto assurdo?",
                "se vuoi posso dirti qualche fatto curioso", "vuoi che ti racconti qualche curiosità?",
                "vuoi per caso sapere qualche curiosità?"]

realfacs = ["Masticare una chewing-gum mentre si pelano le cipolle può frenare il pianto",
            "I fenicotteri sono rosa perché mangiano gamberetti",
            "Il miele è l'unico cibo che non scade mai: lo stesso miele che è stato sepolto con i faraoni in Egitto è ancora commestibile",
            "il ketchup è nato come una medicina",
            "l'altezza della torre eiffel può variare di 15 centimetri in base alla temperatura"]

battuta = ["una mela al giorno leva il medico di torno. una cipolla al giorno leva tutti di torno",
           "Cosa si dicono le galline? ci becchiamo domani",
           "cosa si dicono due casseforti che si incontrano per strada? che combinazione",
           "un uomo entra in un caffè. Splash!",
           "Che rumore fa un maiale quando cade? speck",
           "come disse il cestino? io mi rifiuto",
           "come disse la calcolatrice al ragioniere? conta pure su di me",
           "qual è il colmo per una giraffa? essere nei guai fino al collo!",
           "come si chiama il papà di uno squalo? pasqualo"]

indovinelli = {"cos'è che ha quattro gambe ma non può camminare?": ["tavolo", "sedia"],
               "cosa cade in inverno ma non si fa male?": ["neve", "fiocchi"],
               "cosa esce solo quando piove?": ["ombrello"],
               "cosa arriva solo se hai gli occhi chiusi?": ["sonno", "morte"],
               "chi ha la vita appesa a un filo?": ["ragno"]
               }

indo = ["cos'è che ha quattro gambe ma non può camminare?",
        "cosa cade in inverno ma non si fa male?",
        "cosa esce solo quando piove?",
        "cosa arriva solo se hai gli occhi chiusi?",
        "chi ha la vita appesa a un filo?"]

mimo = {"../../mp3/pipe.mp3": ["tubo", "tubi", "tubatura"],
        "../../mp3/elefante.mp3": ["elefante", "elefanti" ,"proboscide"],
        "../../mp3/simmia.mp3": ["scimmia", "gorilla", "scimpanzè"],
        "../../mp3/chitarra.mp3": ["chitarra", "assolo" , "musica", "basso", "chitarrista"]
    }

mimata = ["../../mp3/pipe.mp3", "../../mp3/elefante.mp3", "../../mp3/simmia.mp3", "../../mp3/chitarra.mp3"]
