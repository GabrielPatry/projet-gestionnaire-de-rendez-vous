from transitions import Machine

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
        pass
    @property
    def identifiant(self):
        return self._nom + self._prenom + self._Noccurence
    
    #nom prénom age mot de passe (why not faire un système de récupération de mot de passe) 
    #identifiant qui sera set par défaut à prénom.nomN°d'occurence (et pas modifiable pour le début)

class Doc(User):
    pass
    #chaque médecin à un attribut de classe EmploiDuTemps pour savoir son...emploi du temps 

class Patent(User):
    pass

class RendezVous:
    pass
    #l'idée est ici d'avoir une heure de début et une heure de fin, aussi un jour, on pourra utiliser la classe datetime du module datetime pour les dates

class EmploiDuTemps:
    """classe pour décrire l'emploi du temps du médecin, ou du patient"""
    pass
    #l'idée est ici de définir le cadre dans lequel les rendez vous doivent s'inscrire, aussi une erreur si deux rendez-vous se superposent,
    # et aussi un timestep pour évier d'avoir des horaires abérrants (genre on réserve au min des rdv d'un quart d'heure et on divise la journée en section de 9-00 9-15 9-30 ...)
    #on peut appliquer une transformation sur l'objet RendezVous qu'on rentre quand on veut ajouter un RendezVous pour qu'il s'inscrive dans cette discrétisation de la journée

#ici les fonctions utiles

def create_user_account():
    """va inclure le fait qu l'utilisateur est médecin ou patient"""
    pass

def connect(User):
    pass

def disconnect(User):
    pass

def show_rendez_vous():
    pass

def make_rendez_vous():
    pass

def delete_rendez_vous():
    pass

def show_rendez_vous():
    pass

def rendez_vous_by_date():
    pass

def show_next_disponibility():
    pass



#et la le code


print("1. Creer un compte utilisateur \n2. Creer un compte medecin \n3. S authentifier \n4. Se deconnecter \n5. Voir les rendez-vous disponibles \n6. Prendre un rendez-vous \n7. Annuler un rendez-vous\n8. Voir les rendez-vous planifies\n9. Rechercher des rendez-vous par date\n10. Gerer l emploi du temps (Infirmiers)\n11. Consultation sur place")
saisie_effectuée = False
user_choice = 0
while (saisie_effectuée == False) or (not 0<user_choice<12):  
    user_choice = input('Choisissez une option (1-11) :')
    saisie_effectuée = True
    try:
        user_choice = int(user_choice)
    except :    
        print('saisie invalide')
        saisie_effectuée = False
        user_choice = 0
