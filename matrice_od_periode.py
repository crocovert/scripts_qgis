import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##poles=vector point
##id=field poles
##nb_passagers=number 1
##jour=number 1
##debut_periode=number 0.0
##fin_periode=number 1440.0
##intervalle=number 15.0
##depart=boolean true
##fichier_matrice=output file

matrice=open(fichier_matrice,"w")
if depart==True:
    d="d"
else:
    d="a"

nodes=processing.getObject(poles)
liste_nodes=set()
if d=="d":
    for i in nodes.getFeatures():
        liste_nodes.add(i[id])
    for n,i in enumerate(liste_nodes):
        progress.setPercentage(100*n/len(liste_nodes))
        for k in range(debut_periode,fin_periode,intervalle) :
            for j in liste_nodes:
                matrice.write(";".join([str(z) for z in [i,j,nb_passagers,jour,k,d,str(i)+"-"+str(j)]])+"\n")
elif d=="a":
    for i in nodes.getFeatures():
        liste_nodes.add(i[id])
    for n,i in enumerate(liste_nodes):
        progress.setPercentage(100*n/len(liste_nodes))
        for k in range(debut_periode,fin_periode,intervalle) :
            for j in liste_nodes:
                matrice.write(";".join([str(z) for z in [j,i,nb_passagers,jour,k,d,str(i)+"-"+str(j)]])+"\n")

matrice.close()
          
    