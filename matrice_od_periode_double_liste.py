import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##poles_o=vector point
##id_o=field poles_o
##poles_d=vector point
##id_d=field poles_d
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

nodes_a=processing.getObject(poles_o)
nodes_b=processing.getObject(poles_d)
liste_nodes_a=set()
liste_nodes_b=set()
if d=="d":
    for i in nodes_a.getFeatures():
        liste_nodes_a.add(i[id_o])
    for i in nodes_b.getFeatures():
        liste_nodes_b.add(i[id_d])
    for n,i in enumerate(liste_nodes_a):
        progress.setPercentage(100*n/len(liste_nodes_a))
        for k in range(debut_periode,fin_periode,intervalle) :
            for j in liste_nodes_b:
                matrice.write(";".join([str(z) for z in [i,j,nb_passagers,jour,k,d,str(i)+"-"+str(j)]])+"\n")
elif d=="a":
    for i in nodes_a.getFeatures():
        liste_nodes_a.add(i[id_o])
    for i in nodes_b.getFeatures():
        liste_nodes_b.add(i[id_d])
    for n,i in enumerate(liste_nodes_a):
        progress.setPercentage(100*n/len(liste_nodes_a))
        for k in range(debut_periode,fin_periode,intervalle) :
            for j in liste_nodes_b:
                matrice.write(";".join([str(z) for z in [j,i,nb_passagers,jour,k,d,str(i)+"-"+str(j)]])+"\n")

matrice.close()
          
    