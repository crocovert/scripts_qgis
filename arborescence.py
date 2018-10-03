
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
##fichier_chemins=file
##arborescence=output vector
##par_lignes=boolean false
##encodage=string utf_8_sig

links=processing.getObject(arcs)
aff=codecs.open(fichier_chemins,"r",encoding=encodage)
champs={}
valeurs=links.getFeatures()
fij={}
trafic={}
od={}
if par_lignes==True:
    champs2=QgsFields()
    champs2.append(QgsField("i",QVariant.String,len=15))
    champs2.append(QgsField("j",QVariant.String,len=15))
    champs2.append(QgsField("line",QVariant.String,len=30))
    champs2.append(QgsField("ij",QVariant.String,len=30))
    champs2.append(QgsField("volume",QVariant.Double))
    champs2.append(QgsField("type",QVariant.String,len=30))
else:
    champs2=QgsFields()
    champs2.append(QgsField("i",QVariant.String,len=15))
    champs2.append(QgsField("j",QVariant.String,len=15))
    champs2.append(QgsField("ij",QVariant.String,len=30))
    champs2.append(QgsField("volume",QVariant.Double))
    champs2.append(QgsField("type",QVariant.String,len=30))
    
iti=QgsVectorFileWriter(arborescence,"UTF-8",champs2,QGis.WKBMultiLineString,links.crs(),"ESRI Shapefile")

for i,j in enumerate(valeurs):
    try:
        fij[j[ij]]=j
    except:
        fij[j['i']+'-'+j['j']]=j


#filtre=iface.activeLayer().selectedFeatures()
filtre=links.selectedFeatures()
        
sel=[f['ij'] for f in filtre]



for k,i in enumerate(aff):
    elements=i.strip("\r").strip("\n").split(";")
    if k==0:
        for ide, e in enumerate(elements):
            champs[e.strip("\"").strip("\r").strip("\n")]=ide

    else:

        if par_lignes==True:
            cle=[elements[champs["i"]].strip("\""),elements[champs["j"]].strip("\""),elements[champs["ligne"]].strip("\"")]
        else:
            cle=[elements[champs["i"]].strip("\""),elements[champs["j"]].strip("\"")]

        volau=elements[champs[volume]].replace(",",".")
        type2=elements[champs[type_arc]]

        if elements[champs["id"]] not in od:
            test_od=False
            for trip in od:
                for arc in od[trip]:
                    if arc[3] in sel:
                        test_od=True
                if test_od==True:
                    for arc in od[trip]:
                        if par_lignes==True:

                            if (arc[0],arc[1],arc[2]) not in trafic:
                                trafic[(arc[0],arc[1],arc[2])]=(arc[0],arc[1],arc[2],arc[0]+'-'+arc[1],0,arc[5])
                            trafic[(arc[0],arc[1],arc[2])]=(arc[0],arc[1],arc[2],arc[0]+'-'+arc[1],trafic[(arc[0],arc[1],arc[2])][4]+arc[4],trafic[(arc[0],arc[1],arc[2])][5])
                        else:
                            if (arc[0],arc[1]) not in trafic:
                                trafic[(arc[0],arc[1])]=(arc[0],arc[1],arc[2],arc[0]+'-'+arc[1],0,arc[4])
                            trafic[(arc[0],arc[1])]=(arc[0],arc[1],arc[2],arc[0]+'-'+arc[1],trafic[(arc[0],arc[1])][4]+arc[4],trafic[(arc[0],arc[1])][5])

            
            od.clear()
            test_od=False
            od[elements[champs["id"]]]=[]
        od[elements[champs["id"]]].append([elements[champs["i"]].strip("\""),elements[champs["j"]].strip("\""),elements[champs["ligne"]].strip("\""),elements[champs["i"]].strip("\"")+'-'+elements[champs["j"]].strip("\""), float(volau),elements[champs[type_arc]]])


for i in trafic:
    if trafic[i][3] in fij:
        f=QgsFeature()
        f.setGeometry(fij[trafic[i][3]].geometry())
        if par_lignes==True:
            f.setAttributes([trafic[i][j] for j in range(6)])
        else:
            f.setAttributes([trafic[i][j] for j in [0,1,3,4,5]])
        iti.addFeature(f)
        
del(iti)
aff.close()        
        
        
        

