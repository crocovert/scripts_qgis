from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##noeuds=vector point
##numero=field noeuds
##pt_depart=point
##pt_arrivee=point
##nb_passagers=number 1.0
##jour=number 1
##heure=string 8:00:00
##depart=boolean true
##fichier_matrice=output file *.txt
if depart==True:
    sens='d'
else:
    sens='a'

nodes=processing.getObject(noeuds)
index=QgsSpatialIndex()
for i in processing.features(nodes):
    index.insertFeature(i)
pt_depart=pt_depart.split(",")
pt_arrivee=pt_arrivee.split(",")
dep=QgsPoint(float(pt_depart[0]), float(pt_depart[1]))
arr=QgsPoint(float(pt_arrivee[0]), float(pt_arrivee[1]))
inode=index.nearestNeighbor(dep,1)
jnode=index.nearestNeighbor(arr,1)
feat=nodes.getFeatures(request=QgsFeatureRequest(inode[0]))
features=[f for f in feat]
d=features[0].attribute(numero)
feat=nodes.getFeatures(request=QgsFeatureRequest(jnode[0]))
features=[f for f in feat]
a=features[0].attribute(numero)
horaire=heure.strip().split(':')
if len(horaire)==3:
    h=int(horaire[0])*60.0+int(horaire[1])+int(horaire[2])/60.0
elif len(horaire)==2:
    h=int(horaire[0])*60.0+int(horaire[1])
elif len(horaire)==1:
    h=float(horaire)


sortie=open(fichier_matrice,"w")
sortie.write(";".join([unicode(d),unicode(a),unicode(nb_passagers),unicode(jour),unicode(h),sens])+"\n")
sortie.close()

    
    

