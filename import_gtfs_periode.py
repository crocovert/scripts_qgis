from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import processing
import os
import datetime
import re

##CEREMA=group
##rep_GTFS=folder
##debut_periode=string 01/01/2018
##fin_periode=string 07/01/2018
##t1=string 00:00:00
##t2=string 23:59:59
##prefixe=string
##proj=crs EPSG:2154
##rep_sortie=folder
##encodage=string "utf8"


debut_periode=QDate.fromString(debut_periode, "d/M/yyyy").toPyDate()
fin_periode=QDate.fromString(fin_periode, "d/M/yyyy").toPyDate()


t1=QTime.fromString(t1,"h:m:s")
t2=QTime.fromString(t2,"h:m:s")
nom_rep=rep_GTFS
lname=prefixe
isnodes=True
islines=True


if "stops.txt" in os.listdir(nom_rep) :
    fich_noeuds=open(nom_rep+"/stops.txt","r")
    t_noeuds=QgsFields()
    t_noeuds.append(QgsField("ident",QVariant.String,len=15))
    t_noeuds.append(QgsField("nom",QVariant.String,len=40))
    t_noeuds.append(QgsField("arrivals",QVariant.Double))
    t_noeuds.append(QgsField("departures",QVariant.Double))
    
    t_links=QgsFields()
    t_links.append(QgsField("Num_Ligne",QVariant.String,len=15))
    t_links.append(QgsField("Nom_Ligne",QVariant.String,len=50))
    t_links.append(QgsField("i",QVariant.String,len=15))
    t_links.append(QgsField("j",QVariant.String,len=15))
    t_links.append(QgsField("nb_lignes",QVariant.Int))
    t_links.append(QgsField("nb_services",QVariant.Int))
    t_links.append(QgsField("delta1",QVariant.Int))
    t_links.append(QgsField("delta2",QVariant.Int))
    
    src=QgsCoordinateReferenceSystem(4326)
    dest=QgsCoordinateReferenceSystem(proj)
    xtr=QgsCoordinateTransform(src,dest)
        
    t_arcs=QgsFields()
    t_arcs.append(QgsField("i",QVariant.String,len=15))
    t_arcs.append(QgsField("j",QVariant.String,len=15))
    t_arcs.append(QgsField("ij",QVariant.String,len=40))
    l_noeuds=QgsVectorFileWriter(rep_sortie+"/"+lname+"_stops.shp","UTF-8",t_noeuds,QGis.WKBPoint,dest,"ESRI Shapefile")
    l_arcs=QgsVectorFileWriter(rep_sortie+"/"+lname+"_arcs.shp","UTF-8",t_arcs,QGis.WKBMultiLineString,dest,"ESRI Shapefile")
    l_links=QgsVectorFileWriter(rep_sortie+"/"+lname+"_lines.shp","UTF-8",t_links,QGis.WKBMultiLineString,dest,"ESRI Shapefile")
    
    
    arrets={}
    progress.setText("Lecture des stops")
    for i,ligne in enumerate(fich_noeuds):
        if i==0:
            if ligne.startswith(codecs.BOM_UTF8):
                ligne=ligne[3:]
            entete=re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",ligne[:-1])
            for e1,e in enumerate(entete):
                entete[e1]=entete[e1].strip("\"")
            idx=entete.index('stop_lon')
            idy=entete.index('stop_lat')
            iid=entete.index('stop_id')
            iname=entete.index('stop_name')
        else:

            elements=re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",ligne[:-1])
            arrets[elements[iid]]=[elements[iid],elements[iname].strip("\""),elements[idx].strip("\""),elements[idy].strip("\""),0.0,0.0]


calendar={}
if ("calendar.txt" in  os.listdir(nom_rep)):
    fich_calendar=open(nom_rep+"/calendar.txt","r")
    progress.setText("Lecture des calendriers")
    for i,cal in enumerate(fich_calendar):
        if i==0:
            if cal.startswith(codecs.BOM_UTF8):
                cal=cal[3:]
            entete=cal.strip().split(',')
            iid=entete.index('service_id')
            idato=entete.index('start_date')
            idatd=entete.index('end_date')
            i1=entete.index('monday')
            i2=entete.index('tuesday')
            i3=entete.index('wednesday')
            i4=entete.index('thursday')
            i5=entete.index('friday')
            i6=entete.index('saturday')
            i7=entete.index('sunday')
        else:

            elements=cal.strip().split(",")
            dato=elements[idato]
            dato=datetime.date(int(dato[0:4]),int(dato[4:6]),int(dato[6:8]))
            datd=elements[idatd]
            datd=datetime.date(int(datd[0:4]),int(datd[4:6]),int(datd[6:8]))
            calendar[elements[iid]]=[elements[iid],dato,datd,elements[i1],elements[i2],elements [i3],elements[i4],elements[i5],elements[i6],elements[i7]]
            

calendar_dates={}
if ("calendar_dates.txt" in  os.listdir(nom_rep)):
    fich_calendar_dates=open(nom_rep+"/calendar_dates.txt","r")
    progress.setText("Lecture des dates")
    for i,calendar_date in enumerate(fich_calendar_dates):
        if i==0:
            if calendar_date.startswith(codecs.BOM_UTF8):
                calendar_date=calendar_date[3:]
            calendar_date=calendar_date.replace("\xFFFD", "")
            entete=calendar_date.strip().split(',')
            for i1,i2 in enumerate(entete):
                entete[i1]=i2.strip('"')
            iid=entete.index('service_id')
            idate=entete.index('date')
            iex=entete.index('exception_type')
        else:

            elements=calendar_date.strip().split(",")
            vdate=elements[idate].strip('"')
            vdate=datetime.date(int(vdate[0:4]),int(vdate[4:6]),int(vdate[6:8]))
            calendar_dates[(elements[iid],vdate,elements[iex])]=[elements[iid],vdate,elements[iex]]


routes={}
test_l=int(("routes.txt" in os.listdir(nom_rep))*("trips.txt" in os.listdir(nom_rep))* ("stop_times.txt" in os.listdir(nom_rep)))
if test_l==1 and islines:
    fich_routes=open(nom_rep+"/routes.txt","r")
    progress.setText("Lecture des routes")
    for i,route in enumerate(fich_routes):
        if i==0:
            if route.startswith(codecs.BOM_UTF8):
                route=route[3:]
            entete=route.strip().split(',')
            for i1,i2 in enumerate(entete):
                entete[i1]=i2.strip('"')
            iid=entete.index('route_id')
            if 'route_short_name' not in entete:
                iname=entete.index('route_long_name')
            else:
                iname=entete.index('route_short_name')
            if 'route_long_name' not in entete:
                ilong=entete.index('route_desc')
            else:
                ilong=entete.index('route_long_name')
        else:

            elements=route.strip().split(",")
            if elements[iname]=="":
                elements[iname]=u' '
            if elements[ilong]=="":
                elements[ilong]=u' '
            routes[elements[iid]]=[elements[iid],elements[iname],elements[ilong]]
    trips={}
    fich_trips=open(nom_rep+"/trips.txt","r")
    progress.setText("Lecture des trips")
    for i,trip in enumerate(fich_trips):
        if i==0:
            if trip.startswith(codecs.BOM_UTF8):
                trip=trip[3:]
            entete=trip.strip(" ").split(',')
            for i1,i2 in enumerate(entete):
                entete[i1]=i2.strip('"')
                entete[i1]=i2.strip('\n').strip('\r')
            iid=entete.index('route_id')
            itrip=entete.index('trip_id')
            iservice=entete.index('service_id')
            if 'shape_id' in entete:
                ishape=entete.index('shape_id')
        else:

            elements=trip.strip(" ").strip('\n').strip('\r').split(",")

            trips[elements[itrip]]=[elements[itrip],elements[iid],elements[iservice]]
    stop_times={}
    fich_stop_times=open(nom_rep+"/stop_times.txt","r")
    id_trip=None
    id_stop=None
    hi2=None
    segments={}
    links={}
    progress.setText("Lecture des stop_times")
    nb=float(os.stat(nom_rep+"/stop_times.txt").st_size)
    for i,stop_time in enumerate(fich_stop_times):
        if i==0:
            if stop_time.startswith(codecs.BOM_UTF8):
               stop_time=stop_time[3:]
            entete=stop_time.strip().split(",")
            iid=entete.index('trip_id')
            iharr=entete.index('arrival_time')
            ihdep=entete.index('departure_time')
            istop=entete.index('stop_id')
            iseq=entete.index('stop_sequence')
        else:
            #progress.setPercentage(float(fich_stop_times.tell())*100/nb)
            elements=stop_time.strip().split(',')
            if elements[istop] in arrets and trips[elements[iid]][1] in routes:
                id_stop2=elements[istop]
                id_trip2=elements[iid]
                ligne=trips[elements[iid]][1]
                num_ligne=routes[ligne][1].strip()
                descr=routes[ligne][2].strip()
                hi1=QTime(int(elements[ihdep][0:2]),int(elements[ihdep][3:5]),int(elements[ihdep][6:8]))
                hj=QTime(int(elements[iharr][0:2]),int(elements[iharr][3:5]),int(elements[iharr][6:8]))
                if (id_trip2==id_trip):
                    nbservices=0
                    nbs1=0
                    nbs2=0
                    if ("calendar.txt" in  os.listdir(nom_rep)):
                        if trips[elements[iid]][2] in calendar:
                            dp=calendar[trips[elements[iid]][2]][1]
                            fp=calendar[trips[elements[iid]][2]][2]
                            nb_jours=(fin_periode-debut_periode).days
                            for k in range(nb_jours+1):
                                date_offre=debut_periode+datetime.timedelta(days=k)
                                if dp<=date_offre<=fp:
                                    jour=date_offre.isoweekday()
                                    if int(calendar[trips[id_trip][2]][2+jour])==1:
                                        nbservices+=1
                                    if (trips[id_trip][2],date_offre,'1') in calendar_dates:
                                            nbservices+=1
                                    if (trips[id_trip][2],date_offre,'2') in calendar_dates:
                                            nbservices+=0
                            
                    elif (trips[id_trip][2],date_offre,'1') in calendar_dates:
                        nbservices+=1
                    segment_id=(num_ligne, id_stop,id_stop2)
                    if (t1<=hi2<=t2):
                        nbs1=nbservices
                    if (t1<=hj<=t2):
                        nbs2=nbservices
                    if (id_stop,id_stop2) not in links:
                        links[(id_stop,id_stop2)]={}
                    if num_ligne not in links[(id_stop,id_stop2)]:
                        links[(id_stop,id_stop2)][num_ligne]=(1,nbs1,descr)
                    else:
                        seg= links[(id_stop,id_stop2)][num_ligne]
                        links[(id_stop,id_stop2)][num_ligne]=(1,seg[1]+nbs1,descr)
                        
                    arrets[id_stop][5]+=nbs1
                    arrets[id_stop2][4]+=nbs2
                hi2=hi1
                id_stop=id_stop2
                id_trip=id_trip2
    progress.setText("Creation des lignes et des arcs")
    for i,s in enumerate(links):
        i1=0
        i2=0
        g_links=QgsFeature()
        g_arcs=QgsFeature()
        #print([unicode(s[0]),unicode(s[1]),unicode(s[0])+"-"+unicode(s[1])])
        g_links.setGeometry(QgsGeometry.fromPolyline([(xtr.transform(QgsPoint(float(arrets[s[0]][2]),float(arrets[s[0]][3])))),xtr.transform(QgsPoint(float(arrets[s[1]][2]),float(arrets[s[1]][3])))]))
        g_arcs.setAttributes([s[0].decode(encodage),s[1].decode(encodage),s[0].decode(encodage)+"-"+s[1].decode(encodage)])
        g_arcs.setGeometry(g_links.geometry())
        if g_arcs.geometry().length()<1600000:
            l_arcs.addFeature(g_arcs)
        for t in links[s]:

            if t=="" or t==None:
                tt= " "
            else:
                tt=t
            #print([tt.decode("cp1252"),links[s][t][2].decode("cp1252"),unicode(s[0]),unicode(s[1]),links[s][t][0],links[s][t][1],i1,i2])
            try:
                g_links.setAttributes([t.decode(encodage),links[s][t][2].decode(encodage),s[0].decode(encodage),s[1].decode(encodage),links[s][t][0],links[s][t][1],i1,i2])
            except:
                print(t,links[s][t][2])
            
            i1+=1
            i2+=links[s][t][1]
            if g_links.geometry().length()<1600000:
                l_links.addFeature(g_links)

    del(stop_times)
    del(trips)
    del(routes)
    del(calendar)
    del(calendar_dates)

if (isnodes):
    for s in arrets:
        g_noeuds=QgsFeature()
        g_noeuds.setGeometry(QgsGeometry.fromPoint(xtr.transform(QgsPoint(float(arrets[s][2]),float(arrets[s][3])))))
        #print([unicode(arrets[s][0]),arrets[s][1].decode('cp1252'),arrets[s][4],arrets[s][5]])
        try:
            g_noeuds.setAttributes([arrets[s][0].decode(encodage),arrets[s][1].decode(encodage),arrets[s][4],arrets[s][5]])
        except:
            print(arrets[s][1])
        l_noeuds.addFeature(g_noeuds)

del(arrets)
del(l_noeuds)
del(l_links)
del(l_arcs)
