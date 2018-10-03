
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import datetime
import codecs

##fichier_DEP80=file
##repertoire_GTFS=folder

def lecture_fichier(nom_fichier):
    fichier80=codecs.open(nom_fichier,"r",encoding="utf8")
    cols={}
    don80=[]
    for i,ligne in enumerate(fichier80):
        if i==0:
            nom_colonnes=ligne[:-1].strip('\"').strip().split(";")
            for j,col in enumerate(nom_colonnes):
                cols[j]=col
        else:
            elements=ligne[:-2].split(";")
            record={}
            for j,eleme in enumerate(elements):
                record[cols[j]]=eleme
            don80.append(record)
    return(don80)

def cree_arrets(donnees,repertoire_GTFS):
    fichier_stops=codecs.open(repertoire_GTFS+"/stops.txt","w",encoding="utf_8_sig")
    arrets={}
    fichier_stops.write("stop_id,stop_name,stop_lat,stop_lon\n")
    for ligne in donnees:
        arrets[ligne["id_arret"]]=[ligne[i] for i in ["id_arret","nom_arret","commune","longitude","lattitude"]]
    for arret in arrets:
        stop=arrets[arret]
        fichier_stops.write('SM'+stop[0]+",\""+stop[2]+"-"+stop[1]+"\","+stop[4]+","+stop[3]+"\n")
    fichier_stops.close()
    return(arrets)
        
        
def cree_chainages(donnees):
    routes={}
    trips={}
    calndars={}
    calendar_dates={}
    stop_times={}
    services={}
    chainages={}
    for ligne in donnees:
        if (ligne["num_ligne"],ligne["num_service"]) not in chainages:
            chainages[(ligne["num_ligne"],ligne["num_service"])]=[]
        chainages[(ligne["num_ligne"],ligne["num_service"])].append(ligne["id_arret"])
    for service in chainages:
        if tuple(chainages[service]) not in services:
            services[tuple(chainages[service])]=[]
        services[tuple(chainages[service])].append(service)
        
    return(services)


def cree_services(donnees):
    services={}
    horaires={}
    for ligne in donnees:
        if (ligne["num_ligne"],ligne["num_service"]) not in services:
            services[tuple([ligne["num_ligne"],ligne["num_service"]])]=[ligne[i] for i in ["num_ligne","num_service","frequence","periode"]]
            horaires[tuple([ligne["num_ligne"],ligne["num_service"]])]=[]
        horaires[tuple([ligne["num_ligne"],ligne["num_service"]])].append([ligne["id_arret"],ligne["horaire"]])
    return([services,horaires])
        
def cree_periodes(donnees):
    cal={}
    vac=[]
    vac.append([datetime.date(2017,10,21),datetime.date(2017,11,5)])
    vac.append([datetime.date(2017,12,23),datetime.date(2018,1,7)])
    vac.append([datetime.date(2018,2,24),datetime.date(2018,3,11)])
    vac.append([datetime.date(2018,4,21),datetime.date(2018,5,6)])

    ete=[]
    ete.append([datetime.date(2017,7,7),datetime.date(2017,9,3)])
    ete.append([datetime.date(2018,7,7),datetime.date(2018,9,2)])
    
    no=[]
    no.append(datetime.date(2017,5,1))
    
    jf=[]
    jf.append(datetime.date(2017,11,1))
    jf.append(datetime.date(2017,11,11))
    jf.append(datetime.date(2017,12,25))
    jf.append(datetime.date(2018,1,1))
    jf.append(datetime.date(2018,4,2))
    jf.append(datetime.date(2018,5,8))
    jf.append(datetime.date(2018,5,10))
    jf.append(datetime.date(2018,5,21))
    
    debut=datetime.date(2017,9,1)
    fin=datetime.date(2018,7,7)
    jour=debut
    periodes=[u'P\xe9riode scolaire',u'P\xe9riode scolaire + petites vacances',u'Et\xe9',u'Petites vacances',u"Toute l'ann\xe9e",u'Petites vacances + \xe9t\xe9',u'P\xe9riode scolaire + \xe9t\xe9']
    for p in periodes:
        cal[p]={}
    while (jour<=fin):
        if jour not in cal:
            cal[u'P\xe9riode scolaire'][jour]='O'
            cal[u'P\xe9riode scolaire + petites vacances'][jour]='O'
            cal[u'Petites vacances + \xe9t\xe9'][jour]='N'
            cal[u'P\xe9riode scolaire + \xe9t\xe9'][jour]='O'
            cal[u'Et\xe9'][jour]='N'
            cal[u'Petites vacances'][jour]='N'
            cal[u"Toute l'ann\xe9e"][jour]='O'
        for v in vac:
            if v[0]<=jour<=v[1]:
                cal[u'P\xe9riode scolaire'][jour]='N'
                cal[u'P\xe9riode scolaire + petites vacances'][jour]='O'
                cal[u'Petites vacances + \xe9t\xe9'][jour]='O'
                cal[u'P\xe9riode scolaire + \xe9t\xe9'][jour]='N'
                cal[u'Et\xe9'][jour]='N'
                cal[u'Petites vacances'][jour]='O'
                cal[u"Toute l'ann\xe9e"][jour]='O'
        if jour in ete:
            cal[u'P\xe9riode scolaire'][jour]='N'
            cal[u'P\xe9riode + petites vacances'][jour]='N'
            cal[u'Petites vacances + \xe9t\xe9'][jour]='O'
            cal[u'P\xe9riode scolaire + \xe9t\xe9'][jour]='O'
            cal[u'Et\xe9'][jour]='O'
            cal[u'Petites vacances'][jour]='N'
            cal[u"Toute l'ann\xe9e"][jour]='O'
        if jour in jf:
            cal[u'P\xe9riode scolaire'][jour]='N'
            cal[u'P\xe9riode scolaire + petites vacances'][jour]='N'
            cal[u'Petites vacances + \xe9t\xe9'][jour]='N'
            cal[u'P\xe9riode scolaire + \xe9t\xe9'][jour]='N'
            cal[u'Et\xe9'][jour]='N'
            cal[u'Petites vacances'][jour]='N'
            cal[u"Toute l'ann\xe9e"][jour]='O'
        if jour in no:
            cal[u'P\xe9riode scolaire'][jour]='N'
            cal[u'P\xe9riode + petites vacances'][jour]='N'
            cal[u'Petites vacances + \xe9t\xe9'][jour]='N'            
            cal[u'P\xe9riode scolaire + \xe9t\xe9'][jour]='N'
            cal[u'Et\xe9'][jour]='N'
            cal[u'Petites vacances'][jour]='N'
            cal[u"Toute l'ann\xe9e"][jour]='N'
        jour=jour+datetime.timedelta(days=1)




    return(cal)
    

def ecrit_routes(chainages,repertoire_GTFS,services,arrets):
    fich_routes=codecs.open(repertoire_GTFS+"/routes.txt","w",encoding="utf_8_sig")
    fich_routes.write("route_id,agency_id,route_short_name,route_long_name,route_type\n")
    for i,chaine in enumerate(chainages):
        service=services[0][chainages[chaine][0]]
        horaire=services[1][chainages[chaine][0]]

        nom_ligne="\"{0} {1}-{2} {3}\"".format(arrets[horaire[0][0]][2],arrets[horaire[0][0]][1],arrets[horaire[len(horaire)-1][0]][2],arrets[horaire[len(horaire)-1][0]][1])
        fich_routes.write("SM{0},SM,{1},{2},{3}\n".format(i,service[0],nom_ligne,3))
    fich_routes.close()


def ecrit_trips(chainages,repertoire_GTFS):
    fich_trips=codecs.open(repertoire_GTFS+"/trips.txt","w",encoding="utf_8_sig")
    fich_trips.write("route_id,service_id,trip_id\n")
    for i,chaine in enumerate(chainages):
        for j in chainages[chaine]:
            fich_trips.write("SM{0},SM{1},SM{2}\n".format(i,i*1000000+int(j[1]),i*1000000+int(j[1])))        
    fich_trips.close()



def ecrit_calendars(chainages,repertoire_GTFS):
    fich_cal=codecs.open(repertoire_GTFS+"/calendar.txt","w",encoding="utf_8_sig")
    fich_cal.write("service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n")
    for i,chaine in enumerate(chainages):
        for j in chainages[chaine]:
            fich_cal.write("SM{0},0,0,0,0,0,0,0,20170901,20180707\n".format((i*1000000+int(j[1]))))        
    fich_cal.close()




def ecrit_calendar_dates(chainages,repertoire_GTFS,calendar,services):
    jsem={1:"Lu",2:"Ma",3:"Me",4:"Je",5:"Ve",6:"Sa",7:"Di"}
    fich_cal=codecs.open(repertoire_GTFS+"/calendar_dates.txt","w",encoding="utf_8_sig")
    fich_cal.write("service_id,date,exception_type\n")
    for i,chaine in enumerate(chainages):
        for j in chainages[chaine]:
            periode=services[0][j][3]
            jours=services[0][j][2]
            for k in calendar[periode]:
                if jsem[k.isoweekday()] in jours and calendar[periode][k]=="O":
                    fich_cal.write("SM{0},{1:02d}{2:02d}{3:02d},1\n".format(i*1000000+int(j[1]),k.year,k.month,k.day))        
    fich_cal.close()


def ecrit_stop_times(chainages,repertoire_GTFS,services):
    fich_cal=codecs.open(repertoire_GTFS+"/stop_times.txt","w",encoding="utf_8_sig")
    fich_cal.write("trip_id,arrival_time,departure_time,stop_id,stop_sequence\n")
    for i,chaine in enumerate(chainages):
        for j in chainages[chaine]:
            horaires=services[1][j]
            for l,k in enumerate(horaires):
                fich_cal.write("SM{0},{1},{2},SM{3},{4}\n".format(i*1000000+int(j[1]),k[1],k[1],k[0],l+1))        
    fich_cal.close()

donnees=lecture_fichier(fichier_DEP80)
arrets=cree_arrets(donnees,repertoire_GTFS)
chainages=cree_chainages(donnees)          
services=cree_services(donnees)
calendar=cree_periodes(donnees)
ecrit_routes(chainages,repertoire_GTFS,services,arrets)
ecrit_trips(chainages,repertoire_GTFS)
ecrit_calendars(chainages,repertoire_GTFS)
ecrit_calendar_dates(chainages,repertoire_GTFS,calendar,services)
ecrit_stop_times(chainages,repertoire_GTFS,services)





     
        
    