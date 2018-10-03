
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import codecs
##CEREMA=group
##arcs=vector
##ij=field arcs
##volume=string volau
##type_arc=string type
##fichier_aff=file
##affectation=output vector
##encodage=string utf_8_sig

links=processing.getObject(arcs)
aff=codecs.open(fichier_aff,"r",encoding=encodage)
champs={}
valeurs=processing.features(links)
fij={}
trafic={}
champs2=QgsFields()
champs2.append(QgsField("ij",QVariant.String))
champs2.append(QgsField("volume",QVariant.Double))
champs2.append(QgsField("type",QVariant.String))
iti=QgsVectorFileWriter(affectation,"UTF-8",champs2,QGis.WKBMultiLineString,links.crs(),"ESRI Shapefile")

for i,j in enumerate(valeurs):
    try:
        fij[j[ij]]=j
    except:
        fij[j['i']+'-'+j['j']]=j

for k,i in enumerate(aff):
    elements=i.split(";")
    if k==0:
        for ide, e in enumerate(elements):
            champs[e.strip("\"").strip("\n").strip("\r")]=ide

    else:

        cle=elements[champs["i"]].strip("\"")+"-"+elements[champs["j"]].strip("\"")

        volau=elements[champs[volume]].replace(",",".")
        type2=elements[champs[type_arc]]


        if cle not in trafic:
            trafic[cle]=(0,'0')
        trafic[cle]=(trafic[cle][0]+float(volau),type2)

for i in trafic:
    if i in fij:
        f=QgsFeature()
        f.setGeometry(fij[i].geometry())
        f.setAttributes([i,trafic[i][0],trafic[i][1]])
        iti.addFeature(f)
aff.close()        
        