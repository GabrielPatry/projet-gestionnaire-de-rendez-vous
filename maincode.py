from transitions import Machine

#le code principal du projet médecin
#d'abord, les classes qui seront amenées à être utilisées

class PassWord:
    pass


class User:
    pass
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





#et la le code

Etat_appli = Machine(model = None,states = ['auth_screen','user_screen'],transitions = [{'trigger' : 'press connect','source':'auth_screen','dest':'user_screen'},{'trigger':'press disconnect','source':'user_screen','dest':'auth_screen'}],initial = 'auth_screen')



