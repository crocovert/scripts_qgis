
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##noeuds=vector point
##numero=field noeuds
##reseau_musliw=file
##reseau_complet=output file

fichier_complet=open(reseau_complet,"w")
fichier_complet.write(u"t nodes\n")

nodes=processing.getObject(noeuds)
for i in nodes.getFeatures():
    n=i[numero]
    x=i.geometry().centroid().asPoint().x()
    y=i.geometry().centroid().asPoint().y()
    fichier_complet.write(";".join([unicode(j) for j in [n,x,y,x]])+"\n")
    
fichier_complet.write(u"t links\n")

fichier_musliw=open(reseau_musliw)
for i in fichier_musliw:
    fichier_complet.write(i)
    
fichier_musliw.close()
fichier_complet.close()
    
    
    
