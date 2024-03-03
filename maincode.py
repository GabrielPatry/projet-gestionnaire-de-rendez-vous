#from transitions import Machine
import pandas as pd
#le code principal du projet médecin
#d'abord, les classes qui seront amenées à être utilisées

class PassWord:
    def __init__(self,password):
        self.password = password
    
    def __str__(self):
        return len(self.password)*'*'


class User:
    @property
    def nom(self):
        return self._nom
    @property
    def prenom(self):
        return self._prenom
    @property
    def age(self):
        return self._age
    @property
    def password(self):
        return self._password
    @property
    def Noccurence(self):
        return self._Noccurence
    @property
    def identifiant(self):
        return self._nom + self._prenom + self._Noccurence
    @property
    def status(self):
        return self._status
    @property
    def sexe(self):
        return self._status
    @Noccurence.setter
    def Noccurence(self,newNoccurence):
        self._Noccurence =  newNoccurence
    @status.setter
    def status(self,newstatus):
        self._status =  newstatus
    @nom.setter
    def nom(self,newnom):
        self._nom = newnom
    @prenom.setter
    def prenom(self,newprenom):
        self._prenom =  newprenom
    @age.setter
    def age(self,newage):
        self._age = newage
    @password.setter
    def password(self,newpassword):
        self._password =  newpassword
    @sexe.setter
    def sexe(self,newsexe):
        if (newsexe == 'F') or (newsexe == 'H'):
            self._sexe = newsexe



    def __init__(self,nom,prenom,age,password,Noccurence,status,sexe):
        self._nom = 'Jean'
        self._prenom = 'Bon'
        self._age = 0
        self._password = '1234'
        self._Noccurence = 0
        self._status = False
        self._sexe = 'F'
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.password = password
        self.Noccurence = Noccurence
        self.status = status
        self.sexe = sexe
    #nom prénom age mot de passe (why not faire un système de récupération de mot de passe) 
    #identifiant qui sera set par défaut à prénom.nomN°d'occurence (et pas modifiable pour le début)

class Doc(User):
    #chaque médecin à un attribut de classe EmploiDuTemps pour savoir son...emploi du temps 

#petit rajout pour la classe Doc
    @property
    def specialite(self):
        return self._specialite
    @specialite.setter
    def specialite(self,newspecialite):
        self._specialite = newspecialite #on peut à cet endroit facilement forcer le choix d'une spécialité parmis des spécialités existantes

    def __init__(self,nom,prenom,age,password,Noccurence,status,sexe,specialite):
        super().__init__(nom,prenom,age,password,Noccurence,status,sexe)
        self._specialite = 'non renseignée'
        self.specialite = specialite
        self.agenda = {} #ne passe pas dans le dataframe

    def ajouter_evenement(self, date, evenement):
        if date in self.agenda : 
            self.agenda[date].append(evenement) #ici je propose que évènement soit un identifiant faisant reférence à une ligne d'un dataframe/csv spécifique qui contienne toutes les info relatives à l'évènement qui sera sans doute de la classe rendez vous
        else :          #date sous la forme 'JJ/MM/AAAA' je propose
            self.agenda[date] = [evenement]

    def emploi_du_temps(self):
        print(f"Emploi du temps du Dr. {self.nom} ({self.specialite}):")
        if not self.agenda : 
            print("Aucun évènement prévu.")
            return
        for date, evenements in self.agenda.items():
            print(f"\n{date}:")
            for evenement in evenements:
                print(f"- {evenement}") #deviendra print(df[evenement]) (bien vu le str de RendezVous)


class Patient(User):
# rajout class patient 

    def __init__(self,nom,prenom,age,password,Noccurence,status, sexe, numero_secu, pathologie):
        super().__init__(nom,prenom,age,password,Noccurence,status,sexe)
        self.numero_secu = numero_secu
        self.pathologie = pathologie

    def __str__(self) : 
        return f"Patient: {self.nom} {self.prenom}, Age: {self.age}, Sexe: {self.sexe}, Numéro Sécurité Sociale: {self.numero_securite_sociale}, Pathologie : {self.pathologie}"

class RendezVous:
    #l'idée est ici d'avoir une heure de début et une heure de fin, aussi un jour, on pourra utiliser la classe datetime du module datetime pour les dates

#Rajout pour la classe rendez-vous
    def __init__(self, medecin, patient, jour, heure_debut, heure_fin, salle=None):
        self.medecin = medecin
        self.patient = patient
        self.jour = jour
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.salle = salle

    def __str__(self):
        salle_info = f", Salle: {self.salle}" if self.salle else ""
        return f"Rendez-vous le {self.jour} de {self.heure_debut} à {self.heure_fin} avec Dr. {self.medecin.nom} pour {self.patient.prenom} {self.patient.nom}{salle_info}"

#et on peut ensuite importer datetime du module datetime

class EmploiDuTemps:
    """classe pour décrire l'emploi du temps du médecin, ou du patient"""
    pass
    #l'idée est ici de définir le cadre dans lequel les rendez vous doivent s'inscrire, aussi une erreur si deux rendez-vous se superposent,
    # et aussi un timestep pour évier d'avoir des horaires abérrants (genre on réserve au min des rdv d'un quart d'heure et on divise la journée en section de 9-00 9-15 9-30 ...)
    #on peut appliquer une transformation sur l'objet RendezVous qu'on rentre quand on veut ajouter un RendezVous pour qu'il s'inscrive dans cette discrétisation de la journée

#ici les procédures associés à chaque action élémentaire

#procédures pour l'écran d'accueil
def create_user_account(doctor = False):
    """va inclure le fait qu l'utilisateur est médecin ou patient"""
    pass

def connect(*args) ->User:
    pass

def disconnect():
    pass

#procédures pour les patients
def show_rendez_vous():
    pass

def make_rendez_vous():
    pass

def delete_rendez_vous():
    pass
def show_next_disponibility():
    pass
#procédures pour les médecins
def rendez_vous_by_date():
    pass


def manage_agenda():
    pass
#le reste...

def userchoice(status,user = None):
    if status == 'Disconnected' : 
        print("1. Creer un compte utilisateur \n2. Creer un compte medecin \n3. S authentifier")
        saisie_effectuée = False
        user_choice = 0
        while (saisie_effectuée == False) or (not 0<user_choice<4):  
            user_choice = input('Choisissez une option (1-3) :')
            saisie_effectuée = True
            try:
                user_choice = int(user_choice)
            except :    
                print('saisie invalide')
                saisie_effectuée = False
                user_choice = 0
    else :
        print("\n1. Se deconnecter \n2. Voir les rendez-vous disponibles \n3. Prendre un rendez-vous \n4. Annuler un rendez-vous\n5. Voir les rendez-vous planifies\n6. Rechercher des rendez-vous par date\n7. Gerer l emploi du temps (Infirmiers)\n8. Consultation sur place") #to change whether it is a doctor or a patient
        saisie_effectuée = False
        user_choice = 0
        while (saisie_effectuée == False) or (not 0<user_choice<12):  
            user_choice = input('Choisissez une option (1-8) :')
            saisie_effectuée = True
            try:
                user_choice = int(user_choice)
            except :    
                print('saisie invalide')
                saisie_effectuée = False
                user_choice = 0


#quelques lignes pour initialiser les dataframes(inactivés ensuite et à réactiver si on souhaite ajouter les attributs)
Bernarddoc = Doc('bernard','jojo',5,'njjjrjjg$$ùgù^^^^-',1,True,'H','gostrologue')
Bernardpat = Patient('bernard','jojo',5,'njjjrjjg$$ùgù^^^^-',1,True,'H',47,'les cramptés')

DOCTEURS_INIT = pd.DataFrame(data = Bernarddoc.__dict__,index = [0])
PATIENTS_INIT = pd.DataFrame(data = Bernardpat.__dict__,index = [0])
DOCTEURS_INIT.to_csv('docteurs.csv')
PATIENTS_INIT.to_csv('patients.csv')
#et la le code
PATIENTS = pd.read_csv('patients.csv')
DOCTEURS = pd.read_csv('docteurs.csv') 
print(PATIENTS)
print(DOCTEURS)
MACHINE_STATUS = 'Disconnected' #au lancement du programme, personne n'est connecté
CURRENT_USER_CONNECTED = None #l'utilisateur qui est connecté au système(on ne pourra bien sûr avoir que 1 utilisateur à la fois)
list_actions_doctor = [disconnect,show_rendez_vous,delete_rendez_vous,rendez_vous_by_date,manage_agenda] #list that contain all the functions associated with users choices when he is connected to its own space, it is likely to evolve because it is not the same for a doctor and a patient 
list_actions_patient = [] #à compléter

while True:
    if MACHINE_STATUS == 'Disconnected':
        c = userchoice(MACHINE_STATUS)
        if c == 1:create_user_account()
        elif c == 2:create_user_account(doctor = True)
        else:CURRENT_USER_CONNECTED = connect(True)
    else:
        if type(CURRENT_USER_CONNECTED) == Doc:
            c = userchoice(MACHINE_STATUS,user = 'Doc')
        else:
            c = userchoice(MACHINE_STATUS,user = 'Patient')
