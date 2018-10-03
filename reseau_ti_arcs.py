
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##reseau=vector
##i=field reseau
##j=field reseau
##concatenateur=string -
##arcs=output vector
fichier_sortie=arcs
links=processing.getObject(reseau)
nom_sortie=os.path.basename(arcs)
rep_sortie=os.path.dirname(arcs)
champs2=QgsFields()
champs2.append(QgsField("i",QVariant.String))
champs2.append(QgsField("j",QVariant.String))
champs2.append(QgsField("ij",QVariant.String))
sortie=QgsVectorFileWriter(fichier_sortie,"UTF-8",champs2,QGis.WKBMultiLineString,links.crs(),"ESRI Shapefile")
for f in links.getFeatures():
    a=QgsFeature()
    a.setGeometry(f.geometry())
    a.setAttributes([unicode(f[i]),unicode(f[j]),unicode(f[i])+concatenateur+unicode(f[j])])
    sortie.addFeature(a)
    
