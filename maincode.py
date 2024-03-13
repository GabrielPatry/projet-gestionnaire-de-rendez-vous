#from transitions import Machine
import pandas as pd
import datetime as dt
import re
#le code principal du projet médecin
#d'abord, les classes qui seront amenées à être utilisées

class PassWord:
    """classe inutilisée finalement"""
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



    def __init__(self,_nom,_prenom,_age,_password,_Noccurence,_status,_sexe):
        self._nom = 'Jean'
        self._prenom = 'Bon'
        self._age = 0
        self._password = '1234'
        self._Noccurence = 0
        self._status = False
        self._sexe = 'F'
        self.nom = _nom
        self.prenom = _prenom
        self.age = _age
        self.password = _password
        self.Noccurence = _Noccurence
        self.status = _status
        self.sexe = _sexe
        self._identifiant = self.prenom + self.nom + str(self.Noccurence)
    def change_status(self):
        self._status = not self._status
    
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

    def __init__(self,_nom,_prenom,_age,_password,_Noccurence,_status,_sexe,_specialite,**kwargs):
        super().__init__(_nom,_prenom,_age,_password,_Noccurence,_status,_sexe)
        self._specialite = 'non renseignée'
        self.specialite = _specialite
        #self.agenda = {} #ne passe pas dans le dataframe 
        #dans la mesure où chaque rendez vous à l'information du nom(l'identifiant) du médecin, il n'est pas nécéssaire de faire apparaître son agenda en temps qu'attribut 

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

    def __init__(self,_nom,_prenom,_age,_password,_Noccurence,_status, _sexe, numero_secu, pathologie,**kwargs):
        super().__init__(_nom,_prenom,_age,_password,_Noccurence,_status,_sexe)
        self.numero_secu = numero_secu
        self.pathologie = pathologie

    def __str__(self) : 
        return f"Patient: {self.nom} {self.prenom}, Age: {self.age}, Sexe: {self.sexe}, Numéro Sécurité Sociale: {self.numero_securite_sociale}, Pathologie : {self.pathologie}"

class RendezVous:
    #l'idée est ici d'avoir une heure de début et une heure de fin, aussi un jour, on pourra utiliser la classe datetime du module datetime pour les dates

#Rajout pour la classe rendez-vous
    def __init__(self, medecin, patient, jour, heure_debut, heure_fin, salle=None,*args,**kwargs):
        self.medecin = medecin #l'identifiant du médecin
        self.patient = patient #l'identifiant du patient
        self.jour = dt.date(*re.split('/',jour)[::-1])
        self.heure_debut = dt.time(*re.split(':',heure_debut))
        self.heure_fin = dt.time(*re.split(':',heure_fin))
        self.salle = salle

    def __str__(self):
        salle_info = f", Salle: {self.salle}" if self.salle else ""
        return f"Rendez-vous le {self.jour} de {self.heure_debut} à {self.heure_fin} avec Dr. {self.medecin} pour {self.patient}.{salle_info}"


class EmploiDuTemps:
    """classe pour décrire l'emploi du temps du médecin, ou du patient"""
    def __init__(self,liste_rdv,**kwds): 
        self.liste_rdv = liste_rdv

    def add_rendez_vous(self,new_rendez_vous):
        new_liste_rdv = self.liste_rdv + [new_rendez_vous]
        if not conflicts(new_liste_rdv):
            self.liste_rdv = new_liste_rdv
        else:
            print("You can't have a rendez vous during this period!")
    #l'idée est ici de définir le cadre dans lequel les rendez vous doivent s'inscrire, ie pas de superposition, et pas de rendez vous en dehors de certaines plages horaires(pauses repas et soir)
    # et aussi un timestep pour évier d'avoir des horaires abérrants (genre on réserve au min des rdv d'un quart d'heure et on divise la journée en section de 9-00 9-15 9-30 ...)(pas une mauvaise idé mais plus le temps)
    #on peut appliquer une transformation sur l'objet RendezVous qu'on rentre quand on veut ajouter un RendezVous pour qu'il s'inscrive dans cette discrétisation de la journée

#ici les procédures associés à chaque action élémentaire

#procédures pour l'écran d'accueil
def create_user_account(patients,docteurs,doctor = False):
    """va inclure le fait qu l'utilisateur est médecin ou patient"""
    nom = input('nom:')
    prenom = input('prenom:')
    age = input('age:')
    password = input('password:')
    sexe = input("sexe(H/F):") 
    status = False 
    Noccurence = 1 #Noccurence reste à traiter...
    if doctor:
        specialite = input("specialite:")
        newuser = Doc(nom,prenom,age,password,Noccurence,status,sexe,specialite)
        docteurs = pd.concat([docteurs,pd.DataFrame(newuser.__dict__,index = [0])],ignore_index = True)
    else:
        num_secu = input('ton num de secu:')
        pathos = input("pourquoi tu consulte?")
        newuser = Patient(nom,prenom,age,password,Noccurence,status,sexe,num_secu,pathos)
        patients = pd.concat([patients,pd.DataFrame(newuser.__dict__, index = [0])],ignore_index = True)
    return patients,docteurs


def connect(patients,docteurs) ->User:
    est_docteur = input('docteur?(oui/non)') 
    if est_docteur == 'oui':
        liste_identifiants_doc = list(docteurs['_identifiant'])
        input_identifiant = input("identifiant:")
        while not input_identifiant in liste_identifiants_doc: 
            print('identifiant invalide')
            input_identifiant = input("identifiant")
        input_mdp = input("votre mot de passe:")
        while not docteurs[docteurs._identifiant == input_identifiant]['_password'][pd.Index(liste_identifiants_doc).get_loc(input_identifiant)] == input_mdp:    
            print("mot de passe incorrect !")
            input_mdp = input("votre mot de passe:")
        return Doc(**docteurs[docteurs._identifiant == input_identifiant].to_dict(orient = 'records')[0])
    if est_docteur == 'non':
        liste_identifiants_pat = list(patients['_identifiant'])
        input_identifiant = input("identifiant:")
        while not input_identifiant in liste_identifiants_pat: 
            print('identifiant invalide')
            input_identifiant = input("identifiant")
        print(str(patients[patients._identifiant == input_identifiant]['_password'][pd.Index(liste_identifiants_pat).get_loc(input_identifiant)]))
        input_mdp = input("votre mot de passe:")
        while not str(patients[patients._identifiant == input_identifiant]['_password'][pd.Index(liste_identifiants_pat).get_loc(input_identifiant)]) == input_mdp:    
            print("mot de passe incorrect !")
            input_mdp = input("votre mot de passe:")
        print(patients[patients._identifiant == input_identifiant].to_dict(orient = 'records')[0])
        return Patient(**patients[patients._identifiant == input_identifiant].to_dict(orient = 'records')[0])

def disconnect(*args,**kwargs):
    pass

#procédures pour les patients
def show_rendez_vous(df_rendez_vous,userID,doctor = False):
    if doctor:
        df_rendez_vous_user = df_rendez_vous[df_rendez_vous.medecin == userID]
        rendez_vous_user = df_rendez_vous_user.to_dict(orient = 'records')
        for rdv in rendez_vous_user:
            print(RendezVous(**rdv))
    else:
        df_rendez_vous_user = df_rendez_vous[df_rendez_vous.patient == userID]
        rendez_vous_user = df_rendez_vous_user.to_dict(orient = 'records')
        for rdv in rendez_vous_user:
            print(RendezVous(**rdv))  
    return df_rendez_vous      

def make_rendez_vous(df_rendez_vous,patientID):
    """seul le patient peut prendre rendez-vous (et ça fait sens t'imagine c'est le docteur qui t'appelles et qui te dit "mon gars tu va venir dans mon cabinet demain")"""
    medecin = input("avec quel médecin tu veux te soigner(écrit son identifiant):")
    patient = patientID
    jour = input("quel jour(format JJ/MM/AAAA):")
    heure_debut = input("quelle heure de début(format hh:mm)?")
    heure_fin = input("quelle heure de fin(format hh:mm)?")
    new_rdv = RendezVous(medecin, patient,jour,heure_debut,heure_fin)
    df_rendez_vous = pd.concat([df_rendez_vous,pd.DataFrame(data = new_rdv.__dict__,index = [0])],ignore_index = True)
    return df_rendez_vous

def delete_rendez_vous(*args,**kwargs):
    pass
def show_next_disponibilities(*args,**kwargs):
    pass
#procédures pour les médecins
def rendez_vous_by_date(*args,**kwargs):
    pass

#le reste...
def conflicts(liste_rdv)->bool:
    """return False there are no superposition beetween the differents rendez vous, else return True"""
    def intersect(rdv1,rdv2):
        """return True if rdv1 and rdv2 intersect, else return False"""
        if rdv1.jour == rdv2.jour:
            if (rdv1.heure_debut < rdv2.heure_fin and rdv1.heure_fin > rdv2.heure_debut)or (rdv1.heure_fin > rdv2.heure_debut and rdv2.heure_fin>rdv1.heure_debut):
                return False
        return True
    
    for i,rdv in enumerate(liste_rdv):
        for j,rdv2 in enumerate(liste_rdv):
            if  i!=j and intersect(rdv,rdv2):
                return False

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
        if user == 'doc':
            print("\n1. Se deconnecter\n2. Voir les rendez-vous planifies \n3. Annuler un rendez-vous" ) #to change whether it is a doctor or a patient
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
            return user_choice
        else:
            print("\n1. Se deconnecter \n2. Voir les rendez-vous disponibles \n3 Voir mes prochains rendez-vous \n4. Prendre un rendez-vous \n5. Annuler un rendez-vous\n6. Voir les rendez-vous planifies")
            saisie_effectuée = False
            user_choice = 0
            while (saisie_effectuée == False) or (not 0<user_choice<7):  
                user_choice = input('Choisissez une option (1-6) :')
                saisie_effectuée = True
                try:
                    user_choice = int(user_choice)
                except :    
                    print('saisie invalide')
                    saisie_effectuée = False
                    user_choice = 0
            return user_choice

#quelques lignes pour initialiser les dataframes(inactivés ensuite et à réactiver si on souhaite ajouter les attributs)
'''Bernarddoc = Doc('bernard','jojo',5,'njjjrjjg$$ùgù^^^^-',1,True,'H','gostrologue')
Bernardpat = Patient('bernard','jojo',5,'njjjrjjg$$ùgù^^^^-',1,True,'H',47,'les cramptés')

DOCTEURS_INIT = pd.DataFrame(data = Bernarddoc.__dict__,index = [0])
PATIENTS_INIT = pd.DataFrame(data = Bernardpat.__dict__,index = [0])
DOCTEURS_INIT.to_csv('docteurs.csv')
PATIENTS_INIT.to_csv('patients.csv')'''
#quelques lignes pour initialiser le Dataframe qui va contenir les rendez-vous
"""RDV_0 = RendezVous('doc','pat','27/11/2003','17H30','18H00')
RDV_INIT = pd.DataFrame(data = RDV_0.__dict__,index  = [0])
RDV_INIT.to_csv('rendez_vous.csv')"""
#et la le code
 

MACHINE_STATUS = 'Disconnected' #au lancement du programme, personne n'est connecté
CURRENT_USER_CONNECTED = None #l'utilisateur qui est connecté au système(on ne pourra bien sûr avoir que 1 utilisateur à la fois)
list_actions_doctor = [disconnect,show_rendez_vous,delete_rendez_vous] #list that contain all the functions associated with users choices when he is connected to its own space, it is likely to evolve because it is not the same for a doctor and a patient 
list_actions_patient = [disconnect,show_next_disponibilities,show_rendez_vous,make_rendez_vous,delete_rendez_vous] #à compléter

while True:
    PATIENTS = pd.read_csv('patients.csv')
    DOCTEURS = pd.read_csv('docteurs.csv')
    RDV = pd.read_csv('rendez_vous.csv')
    print(PATIENTS)
    if MACHINE_STATUS == 'Disconnected':
        c = userchoice(MACHINE_STATUS)
        print(c)
        if c == 1:PATIENTS,DOCTEURS = create_user_account(PATIENTS,DOCTEURS)
        elif c == 2:PATIENTS,DOCTEURS = create_user_account(PATIENTS,DOCTEURS,doctor = True)
        else:
            CURRENT_USER_CONNECTED = connect(PATIENTS,DOCTEURS)
            MACHINE_STATUS = 'Connected'
    else:
        if type(CURRENT_USER_CONNECTED) == Doc:
            c = userchoice(MACHINE_STATUS,user = 'Doc')
            list_actions_doctor[c-1]() #mettre entre parenthèse tout les arguments nécéssiare au bon fonctionnement de n'importe laquelle des fonctions
        else:
            c = userchoice(MACHINE_STATUS,user = 'Patient')
            RDV = list_actions_patient[c-1](RDV,CURRENT_USER_CONNECTED.identifiant) #même remarque que pour docteur
    PATIENTS.to_csv('patients.csv')
    DOCTEURS.to_csv('docteurs.csv')
    RDV.to_csv('rendez_vous.csv')