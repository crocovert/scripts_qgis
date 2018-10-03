from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import numpy
import math


##CEREMA=group
##reseau=vector line
##resultat=output vector 
##ajouter_au_reseau=boolean false

layer=processing.getObject(reseau)
features=[i for i in layer.getFeatures()]
champs=layer.dataProvider().fields()
noms_champs=[i.name() for i in champs]
table_inverse=QgsVectorFileWriter(resultat,"UTF-8",champs,QGis.WKBMultiLineString,layer.crs(),"ESRI Shapefile")
if ajouter_au_reseau:
    layer.startEditing()
    layer.beginEditCommand(QCoreApplication.translate("Ajout sens2","Ajout sens 2"))
for f in features:
    geom = f.geometry()
    geom.convertToMultiType()
    nodes = geom.asMultiPolyline()
    nodes.reverse()
    for points in nodes:
        points.reverse() 
    newgeom = QgsGeometry.fromMultiPolyline(nodes)
    f.setGeometry(newgeom)
    if 'i' in noms_champs and 'j' in noms_champs:
        k=(f['i'],f['j'])
        f['j'],f['i']=k
        if 'ij' in noms_champs:
            f['ij']=f['i']+'-'+f['j']
    table_inverse.addFeature(f)
    if ajouter_au_reseau:
        layer.addFeature(f)
if ajouter_au_reseau:
    layer.endEditCommand()

    