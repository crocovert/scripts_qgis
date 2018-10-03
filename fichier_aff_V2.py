
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import codecs


##CEREMA=group
##arcs=vector
##ij=field arcs 
##ligne=optional field arcs  
##volume=string volau
##type_arc=string type
##fichier_aff=file
##affectation=output vector
##encodage=string utf_8_sig
##par_lignes=boolean false

links=processing.getObject(arcs)
aff=codecs.open(fichier_aff,"r",encoding=encodage)

champs={}
valeurs=processing.features(links)
fij={}
trafic={}
if par_lignes==False:
    champs2=QgsFields()
    champs2.append(QgsField("i",QVariant.String,len=15))
    champs2.append(QgsField("j",QVariant.String,len=15))
    champs2.append(QgsField("ij",QVariant.String,len=35))
    champs2.append(QgsField("volume",QVariant.Double))
    champs2.append(QgsField("type",QVariant.String,len=35))
else:
    champs2=QgsFields()
    champs2.append(QgsField("i",QVariant.String,len=15))
    champs2.append(QgsField("j",QVariant.String,len=15))
    champs2.append(QgsField("ij",QVariant.String,len=35))
    champs2.append(QgsField("ligne",QVariant.String,len=35))
    champs2.append(QgsField("volume",QVariant.Double))
    champs2.append(QgsField("decalage",QVariant.Double))
    champs2.append(QgsField("type",QVariant.String,len=35))
    

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
        if par_lignes==False:
            cle=tuple([elements[champs['i']],elements[champs['j']]])
        else:
            cle=tuple([elements[champs['i']],elements[champs['j']],elements[champs[ligne]].strip("\"")])

        volau=elements[champs[volume]].replace(",",".")
        type2=elements[champs[type_arc]]

        if cle not in trafic:
            trafic[cle]=(0,'0')
        trafic[cle]=(trafic[cle][0]+float(volau),type2)

for i in trafic:
    cle_ij= i[0]+"-"+i[1]
    if cle_ij in fij:
        f=QgsFeature()
        f.setGeometry(fij[cle_ij].geometry())
        if par_lignes==False:
            f.setAttributes([i[0],i[1],cle_ij,trafic[i][0],trafic[i][1]])
        else:
            f.setAttributes([i[0],i[1],cle_ij,i[2],trafic[i][0],0.0,trafic[i][1]])
        iti.addFeature(f)
aff.close()        
        