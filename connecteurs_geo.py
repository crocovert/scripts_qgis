from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import os
import codecs

##CEREMA=group
##arrets=vector point
##stop_id=field arrets
##noeuds=vector point
##node_id=field noeuds
##rayon=number 1000
##mode_i=string t
##mode_j=string m
##vitesse=number 4.0
##nb_max=number 1
##connecteurs=output vector



nom_fichier=connecteurs
index=QgsSpatialIndex()
stops=processing.getObject(arrets)
nodes=processing.getObject(noeuds)
champs=QgsFields()
champs.append(QgsField('i',QVariant.String,len=15))
champs.append(QgsField('j',QVariant.String,len=15))
champs.append(QgsField('longueur',QVariant.Double))
champs.append(QgsField('temps',QVariant.Double))
champs.append(QgsField('mode',QVariant.String,len=10))


table_connecteurs=QgsVectorFileWriter(nom_fichier,"UTF8",champs, QGis.WKBLineString,stops.crs(),"ESRI Shapefile")

fichier_connecteurs=os.path.splitext(nom_fichier)[0]+".txt"
sortie=codecs.open(fichier_connecteurs,"w",encoding="utf-8")
nb=len(processing.features(stops))
nbc=0
for i in processing.features(nodes):
    index.insertFeature(i)
for i,n in enumerate(processing.features(stops)):
    near=index.nearestNeighbor(n.geometry().centroid().asPoint(),nb_max)
    if len(near)>0:
        for k,nearest in enumerate(near):
            if k<nb_max:
                f=nodes.getFeatures(request=QgsFeatureRequest(nearest))
                for j, g in enumerate(f):
                    if j==0:
                        l=n.geometry().distance(g.geometry())
                        id_node=unicode(g.attribute(node_id))
                        id_stop=unicode(n.attribute(stop_id))
                        if l<rayon:
                            nbc+=1
                            gline=QgsGeometry.fromPolyline([QgsPoint(n.geometry().centroid().asPoint()),QgsPoint(g.geometry().centroid().asPoint())])
                            hline=QgsGeometry.fromPolyline([QgsPoint(g.geometry().centroid().asPoint()),QgsPoint(n.geometry().centroid().asPoint())])

                            fline=QgsFeature()
                            fline.setGeometry(gline)
                            ll=gline.length()
                            moda=unicode(mode_i)+unicode(mode_j)
                            if vitesse<=0:
                                fline.setAttributes([id_stop,id_node, ll/1000,0.0,moda])
                            else:
                                fline.setAttributes([id_stop,id_node, ll/1000,ll*60/(vitesse*1000),moda])
                            fline2=QgsFeature()
                            fline2.setGeometry(hline)
                            modb=unicode(mode_j)+unicode(mode_i)
                            if vitesse<=0:
                                fline2.setAttributes([id_node,id_stop, ll/1000,0,modb])
                            else:
                                fline2.setAttributes([id_node,id_stop, ll/1000,ll*60/(vitesse*1000),modb])
                            table_connecteurs.addFeature(fline)
                            table_connecteurs.addFeature(fline2)
                            if vitesse>0:
                                sortie.write(id_node+';'+id_stop+';'+str((60/vitesse)*(ll/1000.0))+';'+str(ll/1000.0)+';-1;-1;-1;-1;-1;'+modb+';'+modb+'\n')
                                sortie.write(id_stop+';'+id_node+';'+str((60/vitesse)*(ll/1000.0))+';'+str(ll/1000.0)+';-1;-1;-1;-1;-1;'+moda+';'+moda+'\n')
                            else:
                                sortie.write(id_node+';'+id_stop+';'+str(0.0)+';'+str(ll/1000.0)+';-1;-1;-1;-1;-1;'+modb +';'+modb+'\n')
                                sortie.write(id_stop+';'+id_node+';'+str(0.0)+';'+str(ll/1000.0)+';-1;-1;-1;-1;-1;'+moda+';'+moda+'\n')
progress.setText(unicode(nbc)+"/"+unicode(nb)+" noeuds connectes")
sortie.close()
del table_connecteurs

              



