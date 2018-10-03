from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##fichier_temps= file
##iti=output vector

features={}
fic_temps=open(fichier_temps)
col_temps={}
temps={}
tij={}
for i,j in enumerate(fic_temps):
    elem=j.split(";")
    if i==0:
        for k,l in enumerate(elem):
            col_temps[l]=k
    else:
        temps[elem[col_temps["numtrc"]]]=elem
        tij[elem[col_temps["ij"]]]=elem
links=iface.activeLayer()

if 'ij' in [j.name() for j in links.pendingFields()]:
    index=QgsSpatialIndex()
    for i in links.getFeatures():
        index.insertFeature(i)
        features[i['ij']]=i

    feat=links.selectedFeatures()
        
    feats=[f for f in feat]
    if len(feats)>0:
        d=feats[0]['ij']


        champs=QgsFields()

        champs.append(QgsField('o',QVariant.String,len=30))
        champs.append(QgsField('ij',QVariant.String,len=30))
        champs.append(QgsField('ligne',QVariant.Int))
        champs.append(QgsField('numtrc',QVariant.Int))
        champs.append(QgsField('jour',QVariant.Int))
        champs.append(QgsField('heureo',QVariant.Double))
        champs.append(QgsField('heured',QVariant.Double))
        champs.append(QgsField('temps',QVariant.Double))
        champs.append(QgsField('tveh',QVariant.Double))
        champs.append(QgsField('tmap',QVariant.Double))
        champs.append(QgsField('tatt',QVariant.Double))
        champs.append(QgsField('tcorr',QVariant.Double))
        champs.append(QgsField('ncorr',QVariant.Double))
        champs.append(QgsField('tatt1',QVariant.Double))
        champs.append(QgsField('cout',QVariant.Double))
        champs.append(QgsField('longueur',QVariant.Double))
        champs.append(QgsField('pole',QVariant.String,len=15))
        champs.append(QgsField('type',QVariant.String,len=15))
        champs.append(QgsField('toll',QVariant.Double))

        sortie=QgsVectorFileWriter(iti,"UTF-8",champs,QGis.WKBMultiLineString,links.crs(),"ESRI Shapefile")


        for feat in feats:
            d=feat['ij']
            id_iti=d
            while int(tij[d][col_temps['precedent']])>0:
                f=QgsFeature(champs)
                liste=[id_iti]
                liste.extend(tij[d][i] for i in [2,3,4,5,6,7,8,9,10,11,14,15,16,17,20,21])
                f.setAttributes(liste)
                
                if tij[d][col_temps['ij']] in features:
                    f.setGeometry(features[d].geometry())
                    sortie.addFeature(f)
                d=temps[tij[d][col_temps['precedent']]][col_temps['ij']]
        del sortie

