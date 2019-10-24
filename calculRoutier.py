from dictionnaire import villes
from datetime import datetime

def conversionSeconde(secondes):
    minutes = 0
    heures = 0

    while secondes >= 60 :
        secondes -= 60
        minutes += 1
        if minutes == 60:
            heures += 1
            minutes = 0

    if secondes > 0:
        minutes += 1

    if len(str(heures)) < 2:
        heures = '0' + str(heures)
    if len(str(minutes)) < 2:
        minutes = '0' + str(minutes)
    
    resulat = str(heures) + ':' + str(minutes)

    return resulat





def calculTempsDistance(villeDepart, villeArrivee):
    distanceTotale = villes[str(villeDepart).capitalize()][str(villeArrivee).capitalize()] * 1000  #en metre
    distanceParcourue = 0 #en metre
    secondes = 0
    m_sec = 0
    acceleration = True
    pause = False
    minutesPause = 0
    compteurPause = 0 # en secondes
    nbrPauses = 0
    resulat = [] #Ce tableau contient dans l'ordre. la ville de départ, la ville d'arrivée, la distance parcourue et le temps mis pour parcourir la distance en secondes

    while distanceParcourue < distanceTotale:
        if pause == False:
            secondes += 60
            compteurPause += 60

            if compteurPause == 111*60:
                acceleration = False

            if acceleration:
                if m_sec < 25:
                    m_sec += 25/9
            else:
                if m_sec > 25/9:
                    m_sec -= 25/9
                elif m_sec < 25/9: #car sinon on est pas exactement à zero
                    m_sec = 0
            
            distanceParcourue += m_sec * 60

            if int(distanceParcourue) + 6000 == distanceTotale: # + 6 car le nbr de km parcouru en décélérant de 90 pour arriver pile à 0 est de 6 km
                secondes += 9*60
                distanceParcourue += 6000
                break

            if compteurPause == 120*60:
                pause = True
                compteurPause = 0
        else:
            minutesPause += 1
            if minutesPause == 15:
                minutesPause = 0
                pause = False
                secondes += 15*60
                acceleration = True
                nbrPauses += 1          

    resulat = [villeDepart, villeArrivee, int(distanceParcourue/1000), secondes]

    return resulat
            


    

def start():

    listeVilles = []
    villeInsere = None
    compteur = 1
    tempsTotal = 0 #en secondes
    distanceTotal = 0

    print("Insérez autant de villes que vous le souhaitez. Quand vous aurez inséré toutes les villes voulu, appuyez juste sur Entrée sans rien écrire pour lancer le calcul")

    while villeInsere != '' :
        print('Ville{} : '.format(compteur))
        villeInsere = input().lower().capitalize()
        print(villeInsere)
        if villeInsere != '':
            if villeInsere in villes:
                listeVilles.append(villeInsere)
                compteur += 1
            else:
                print("Cette ville n'est pas dans notre base de donnée. Vérifiez peut être l'ortographe. \n")

    if len(listeVilles) < 2:
        print('Veuillez insérer au moin 2 villes')
        return start()

    for i in range(len(listeVilles) - 1):

        resultatParEtape = calculTempsDistance(listeVilles[i], listeVilles[i+1])

        tempsTotal += resultatParEtape[3]
        tempsTotal += 45*60 #ce sont les 45 min de pause à chaque étape. Ils seront donc visible au temps total.
        distanceTotal += resultatParEtape[2]

        print('--------------------------------------------------')
        print('{} >>> {} | {} km | {}'.format(resultatParEtape[0], resultatParEtape[1], resultatParEtape[2], conversionSeconde(resultatParEtape[3])))
        print('--------------------------------------------------')          

    tempsTotal -= 45*60 # la ville finale n'est pas une étape, on enlève donc les 45 min en trop ajouté pendant la boucle
    print('\n--------------------------------------------------')
    print('Total de {} à {} | {} km | {}'.format(listeVilles[0], resultatParEtape[1], distanceTotal, conversionSeconde(tempsTotal)))
    print('--------------------------------------------------')          






start()