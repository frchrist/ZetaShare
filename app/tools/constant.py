APP_DEBUG=False

from sys import argv
if "debug" in argv:
	APP_DEBUG = True

BUFFER_SIZE = 1024 * 4 # 4 k
SEPARATOR = "<ZETA>"
#ACTION TYPES
START_RECEIVER_SERVER = 1
START_SENDER_SERVER = 2
ETABLISH_CONNECTION = 3

#Colors
BACKGROUND = "#010a1a"
B_BACKGROUND = "#000817"
GREEN = "#248232"
RED = "#8f070e"
BLUE = "#2c1c40"
WHITE = "#E4FDE1"
MAIN_STYLE = {"bg":BACKGROUND, "fg":WHITE}
ENTRY_FONT = {"font":("helvetica", 10)}


#TEXTS
TITLE = "ZetaSHARE"
APP_LABEL=f"POUMA-TECH ({TITLE})"
READY_MSG = "Prêt"
BACK_MSG = "Retour"
WAITING_FOR_FILE_MSG = "En attente de fichier"
SEND_MSG = "Envoyer"
RECEIVE_MSG = "Recevoir"
CONNECTION_FAILED ="[-] Connexion echoué" 
INVALID_USER_MSG = "[-] Utilisateur invalide"
INVALID_PORT_MSG = "[-] Le port entré est invalide"
INVALID_FILE_MSG = "[-] Veillez selectionné fichier"
MODE_ERROR_MSG = "Non Autorisé ! le mode opposé en déjà en cours "
CHOOSE_FILE_MSG = "Choisir un ficher"
STOP_MSG="Arreté"
HISTORY_MSG = "Historique"
CONFIG_MSG = "configuration"
#MAIN MODE
NORMAL="normal"
SEND="send"
RECEIVE="receive"
