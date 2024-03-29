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
    """on utilise ici la redaction avec property et value.setter pour anticiper de possibles demandes du client sur la forme que doivent adopter ces attributs"""
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
        return self._prenom + self._nom + str(self._Noccurence)
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
        self._status = not self._status #le status individuel n'est finalement pas utiliser car peu pratique dans une application locale sur une seule machine

class Doc(User):
    @property
    def specialite(self):
        return self._specialite #on pourrait à l'avenir contraindre le choix de la spécialité parmi une liste de spécialités prédéfinies
    @specialite.setter
    def specialite(self,newspecialite):
        self._specialite = newspecialite #on peut à cet endroit facilement forcer le choix d'une spécialité parmis des spécialités existantes

    def __init__(self,_nom,_prenom,_age,_password,_Noccurence,_status,_sexe,_specialite,**kwargs):
        super().__init__(_nom,_prenom,_age,_password,_Noccurence,_status,_sexe)
        self._specialite = 'non renseignée'
        self.specialite = _specialite
        #dans la mesure où chaque rendez vous a l'information du nom(l'identifiant) du médecin, il n'est pas nécéssaire de faire apparaître son agenda en temps qu'attribut 

    def ajouter_evenement(self, date, evenement):
        if date in self.agenda : 
            self.agenda[date].append(evenement) 
        else :          
            self.agenda[date] = [evenement]

    def emploi_du_temps(self):
        print(f"Emploi du temps du Dr. {self.nom} ({self.specialite}):")
        if not self.agenda : 
            print("Aucun évènement prévu.")
            return
        for date, evenements in self.agenda.items():
            print(f"\n{date}:")
            for evenement in evenements:
                print(f"- {evenement}") 
    #ces deux methodes n'ont finalement pas été utilisées du fait de la difficulté de stocker des dictionnaires dans des dataframes

class Patient(User):

    def __init__(self,_nom,_prenom,_age,_password,_Noccurence,_status, _sexe, numero_secu, pathologie,**kwargs):
        super().__init__(_nom,_prenom,_age,_password,_Noccurence,_status,_sexe)
        self.numero_secu = numero_secu
        self.pathologie = pathologie

    def __str__(self) : 
        return f"Patient: {self.nom} {self.prenom}, Age: {self.age}, Sexe: {self.sexe}, Numéro Sécurité Sociale: {self.numero_securite_sociale}, Pathologie : {self.pathologie}"

class RendezVous:

    def __init__(self, medecin, patient, jour, heure_debut, heure_fin, salle=None,*args,**kwargs):
        self.medecin = medecin #l'identifiant du médecin
        self.patient = patient #l'identifiant du patient
        self.jour = dt.date(*[int(n) for n in re.split('-',str(jour))]) #on effectue ici une conversion en objet datetime.date pour avoir une dte se manipulant comme un float(nottament pour les comparaisons)
        self.heure_debut = dt.time(*[int(n) for n in re.split(':',str(heure_debut))]) #de même ici
        self.heure_fin = dt.time(*[int(n) for n in re.split(':',str(heure_fin))]) #de même ici
        self.salle = salle

    def __str__(self):
        salle_info = f", Salle: {self.salle}" if self.salle else ""
        return f"Rendez-vous le {self.jour} de {self.heure_debut} à {self.heure_fin} avec Dr. {self.medecin} pour {self.patient}.{salle_info}" #utile pour l'affichage des rendez vous planifiés


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
    #l'idée etait ici de définir le cadre dans lequel les rendez vous doivent s'inscrire, ie pas de superposition, et pas de rendez vous en dehors de certaines plages horaires(pauses repas et soir)
    #non n'avons toutefois pas utilié cette classe au final. Pour un meilleur contrôle sur l'emploi du temps, il serait approprié de la réintroduire

#ici les procédures associées à chaque action élémentaire

#fonctions pour l'écran d'accueil
def create_user_account(patients,docteurs,doctor = False):
    """crée un profil utilisateur et l'intègre dans la base de données"""
    nom = input('nom:')
    prenom = input('prenom:')
    age = input('age:')
    password = input('password:')
    sexe = input("sexe(H/F):") 
    status = False  
    if doctor:
        Noccurence = len(docteurs[(docteurs._nom == nom)&(docteurs._prenom == prenom)].to_dict(orient = 'records')) + 1 #on attribue à chaque utilisateur le nombre d'occurences de son patronyme pour pouvoir ensuite créer des identifiants uniques en fonction de si docteur ou patient
        print("vôtre identifiant de connection sera:",prenom+nom+str(Noccurence))
        specialite = input("specialite:")
        newuser = Doc(nom,prenom,age,password,Noccurence,status,sexe,specialite)
        docteurs = pd.concat([docteurs,pd.DataFrame(newuser.__dict__,index = [0])],ignore_index = True)
    else:
        Noccurence = len(patients[(patients._nom == nom)&(patients._prenom == prenom)].to_dict(orient = 'records')) + 1 
        print("vôtre identifiant de connection sera:",prenom+nom+str(Noccurence))
        num_secu = input('ton num de secu:')
        pathos = input("pourquoi tu consulte?")
        newuser = Patient(nom,prenom,age,password,Noccurence,status,sexe,num_secu,pathos)
        patients = pd.concat([patients,pd.DataFrame(newuser.__dict__, index = [0])],ignore_index = True)
    return patients,docteurs


def connect(patients,docteurs) ->User:
    """récupère les identifiants de connexion de l'utilisateur et renvoie un objet user correspondant à celui-ci"""
    est_docteur = input('docteur?(oui/non)') 
    if est_docteur == 'oui':
        liste_identifiants_doc = list(docteurs['_identifiant'])
        input_identifiant = input("identifiant:")
        while not input_identifiant in liste_identifiants_doc: 
            print('identifiant invalide')
            input_identifiant = input("identifiant:")
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
    
#procédures pour les utilisateurs
def show_rendez_vous(df_rendez_vous,userID,doctor = False,**kwargs):
    """affiche les rendez-vous de l'utilisateur"""
    if doctor:
        print(userID)
        df_rendez_vous_user = df_rendez_vous[df_rendez_vous.medecin == userID]
        rendez_vous_user = df_rendez_vous_user.to_dict(orient = 'records')
        for rdv in rendez_vous_user:
            print(RendezVous(**rdv))
    else:
        df_rendez_vous_user = df_rendez_vous[df_rendez_vous.patient == userID]
        rendez_vous_user = df_rendez_vous_user.to_dict(orient = 'records')
        for rdv in rendez_vous_user:
            print(RendezVous(**rdv))  
    return df_rendez_vous  #toutes les fonctions renvoient df_rendez_vous pour pouvoir accéder aux fonctions par la liste    

def make_rendez_vous(df_rendez_vous,userID,**kwargs):
    """créer une instance rendez vous avec les informations saisies par le patient et renvoie une version
    mise à jour de la database des rendez-vous. Seul le patient peut prendre rendez-vous"""
    medecin = input("avec quel médecin tu veux te soigner(écrit son identifiant):")
    patient = userID
    jour = input("quel jour(format AAAA-MM-JJ):")
    heure_debut = input("quelle heure de début(format hh:mm)?")
    heure_fin = input("quelle heure de fin(format hh:mm)?")
    new_rdv = RendezVous(medecin, patient,jour,heure_debut,heure_fin)
    df_rendez_vous_p = pd.concat([df_rendez_vous,pd.DataFrame(data = new_rdv.__dict__,index = [0])],ignore_index = True)

    #quelques lignes pour vérifier que ce nouveau rendez-vous n'est pas en conflit avec d'autres
        #d'abord pour le docteur
    df_rendez_vous_doc = df_rendez_vous_p[df_rendez_vous_p.medecin == medecin]
    rendez_vous_doc = df_rendez_vous_doc.to_dict(orient = 'records')
    rendez_vous_doc_rdv = [RendezVous(**dico) for dico in rendez_vous_doc]
    if conflicts(rendez_vous_doc_rdv):
        print("vous ne pouvez pas avoir un rendez-vous ici")
        return df_rendez_vous
        #puis pour le patient
    df_rendez_vous_pat = df_rendez_vous_p[df_rendez_vous_p.patient == userID]
    rendez_vous_pat = df_rendez_vous_pat.to_dict(orient = 'records')
    rendez_vous_pat_rdv = [RendezVous(**dico) for dico in rendez_vous_pat]
    if conflicts(rendez_vous_pat_rdv):
        print("vous ne pouvez pas avoir un rendez-vous ici")
        return df_rendez_vous
    return df_rendez_vous_p

def delete_rendez_vous(df_rendez_vous,userID,doctor = False,**kwargs):
    """supprime un rendez-vous de la database. Le rendez-vous à annuler est choisi par l'utilisateur"""
    if doctor:
        df_rendez_vous_user = df_rendez_vous[df_rendez_vous.medecin == userID]
        rendez_vous_user = df_rendez_vous_user.to_dict(orient = 'records')
        n = len(rendez_vous_user)
        for i,rdv in enumerate(rendez_vous_user):
            print(i+1,":",RendezVous(**rdv))
        saisie_effectuee = False 
        c = 0
        while (not saisie_effectuee) or (not 0<c<n+1):
            
            print("saisie invalide")
            c = input(f"quel rendez-vous souhaitez vous supprimer(1-{n}):")
            saisie_effectuee = True
            try:
                c  = int(c)
            except:
                print("saisie invalide")
                saisie_effectuee  = False
                c = 0
        #il faut ensuite retrouver l'index du rendez-vous que l'utilisateur souhaite supprimer dans la dataframe des rendez-vous globale
        index_to_drop = df_rendez_vous_user.index[c-1]        
        df_rendez_vous.drop(labels = index_to_drop,inplace = True)
        return df_rendez_vous
    
    else:
        df_rendez_vous_user = df_rendez_vous[df_rendez_vous.patient == userID]
        rendez_vous_user = df_rendez_vous_user.to_dict(orient = 'records')
        n = len(rendez_vous_user)
        for i,rdv in enumerate(rendez_vous_user):
            print(i+1,":",RendezVous(**rdv))
        saisie_effectuee = False 
        c = 0
        while (not saisie_effectuee) or (not 0<c<n+1):
            c = input(f"quel rendez-vous souhaitez vous supprimer(1-{n}):")
            saisie_effectuee = True
            try:
                c  = int(c)
            except:
                print("saisie invalide")
                saisie_effectuee  = False
                c = 0
        #il faut ensuite retrouver l'index du rendez-vous que l'utilisateur souhaite supprimer dans la dataframe des rendez-vous globale
        index_to_drop = df_rendez_vous_user.index[c-1]        
        df_rendez_vous.drop(labels = index_to_drop,inplace = True)
        return df_rendez_vous
    
def show_next_disponibilities(df_rendez_vous,**kwargs):
    """renvoie l'emploi du temps du médecin avc lequel l'utilisateur souhaite prendre rendez-vous"""
    doctorID = input("saissisez l'ID du docteur avec lequel vous souhaitez prendre rendez-vous:")
    show_rendez_vous(df_rendez_vous,doctorID,doctor = True)
    return df_rendez_vous

#le reste...
def conflicts(liste_rdv)->bool:
    """renvoie True si certains rendez-vous de la liste donnée en argument se superposent, sinon renvoie False"""
    def intersect(rdv1,rdv2):
        """return True si rdv1 et rdv2 s'intersectent, sinon return False"""
        if rdv1.jour == rdv2.jour:
            if (rdv1.heure_debut < rdv2.heure_fin and rdv1.heure_fin > rdv2.heure_debut)or (rdv1.heure_fin > rdv2.heure_debut and rdv2.heure_fin>rdv1.heure_debut):
                return True
        return False
    
    for i,rdv in enumerate(liste_rdv):
        for j,rdv2 in enumerate(liste_rdv):
            if  i!=j and intersect(rdv,rdv2):
                return True

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
        return user_choice
    else :
        if user == 'Doc':
            print("\n1. Se deconnecter\n2. Voir les rendez-vous planifies \n3. Annuler un rendez-vous" ) 
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
            print("\n1. Se deconnecter \n2. Voir les rendez-vous disponibles \n3 Voir mes prochains rendez-vous \n4. Prendre un rendez-vous \n5. Annuler un rendez-vous")
            saisie_effectuée = False
            user_choice = 0
            while (saisie_effectuée == False) or (not 0<user_choice<6):  
                user_choice = input('Choisissez une option (1-5) :')
                saisie_effectuée = True
                try:
                    user_choice = int(user_choice)
                except :    
                    print('saisie invalide')
                    saisie_effectuée = False
                    user_choice = 0
            return user_choice

#quelques lignes pour initialiser les dataframes(inactivées normalement, mais à réactiver si on souhaite ajouter des attributs)
"""
Bernarddoc = Doc('bernard','jojo',5,'njjjrjjg$$ùgù^^^^-',1,True,'H','gostrologue')
Bernardpat = Patient('bernard','jojo',5,'njjjrjjg$$ùgù^^^^-',1,True,'H',47,'les cramptés')

DOCTEURS_INIT = pd.DataFrame(data = Bernarddoc.__dict__,index = [0])
PATIENTS_INIT = pd.DataFrame(data = Bernardpat.__dict__,index = [0])
DOCTEURS_INIT.to_csv('docteurs.csv')
PATIENTS_INIT.to_csv('patients.csv')
#quelques lignes pour initialiser le Dataframe qui va contenir les rendez-vous
RDV_0 = RendezVous('doc','pat','2003-11-27','17:30','18:00')
RDV_INIT = pd.DataFrame(data = RDV_0.__dict__,index  = [0])
RDV_INIT.to_csv('rendez_vous.csv')"""
#et la le code
 

MACHINE_STATUS = 'Disconnected' #au lancement du programme, personne n'est connecté
CURRENT_USER_CONNECTED = None #l'utilisateur qui est connecté au système(on ne pourra bien sûr avoir que 1 utilisateur à la fois)
list_actions_doctor = ['disconnect',show_rendez_vous,delete_rendez_vous] #liste qui contient toutes les fonctions associées aux choix de l'utilisateur lorsqu'il est connecté à son propre espace
list_actions_patient = ['disconnect',show_next_disponibilities,show_rendez_vous,make_rendez_vous,delete_rendez_vous] 

while True:
    PATIENTS = pd.read_csv('patients.csv')
    DOCTEURS = pd.read_csv('docteurs.csv')
    RDV = pd.read_csv('rendez_vous.csv')
    if MACHINE_STATUS == 'Disconnected':
        c = userchoice(MACHINE_STATUS)
        if c == 1:PATIENTS,DOCTEURS = create_user_account(PATIENTS,DOCTEURS)
        elif c == 2:PATIENTS,DOCTEURS = create_user_account(PATIENTS,DOCTEURS,doctor = True)
        else:
            CURRENT_USER_CONNECTED = connect(PATIENTS,DOCTEURS)
            MACHINE_STATUS = 'Connected'
    else:
        if type(CURRENT_USER_CONNECTED) == Doc:
            c = userchoice(MACHINE_STATUS,user = 'Doc')
            if c == 1:MACHINE_STATUS = 'Disconnected' #cette action ne nécessite pas un fonction
            else:
                RDV = list_actions_doctor[c-1](df_rendez_vous = RDV,userID = CURRENT_USER_CONNECTED.identifiant,doctor = True) #entre parenthèses tous les arguments nécéssaires au bon fonctionnement de n'importe laquelle des fonctions
        else:
            c = userchoice(MACHINE_STATUS,user = 'Patient')
            if c == 1:MACHINE_STATUS = 'Disconnected'
            else:
                RDV = list_actions_patient[c-1](df_rendez_vous = RDV,userID = CURRENT_USER_CONNECTED.identifiant) #même remarque que pour docteur
    PATIENTS.to_csv('patients.csv')
    DOCTEURS.to_csv('docteurs.csv')
    RDV.to_csv('rendez_vous.csv') #en fin d'exécution, on sauvegarde les datasets mis à jour
