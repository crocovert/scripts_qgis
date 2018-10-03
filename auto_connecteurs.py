from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##noeuds=vector point
##num=field noeuds
##rayon=number 500.0
##connecteurs=output vector
##vitesse=number 4.0
##mode=string m

nom_fichier=connecteurs
index=QgsSpatialIndex()
nodes=processing.getObject(noeuds)
champs=QgsFields()
champs.append(QgsField('i',QVariant.String,len=15))
champs.append(QgsField('j',QVariant.String,len=15))
champs.append(QgsField('longueur',QVariant.Double))
champs.append(QgsField('temps',QVariant.Double))
champs.append(QgsField('mode',QVariant.String,len=10))
f={feature.id(): feature for (feature) in nodes.getFeatures()}

table_connecteurs=QgsVectorFileWriter(nom_fichier,"UTF8",champs, QGis.WKBMultiLineString,nodes.crs(),"ESRI Shapefile")
for i in processing.features(nodes):
    index.insertFeature(i)
for i,n in enumerate(processing.features(nodes)):
    near=index.intersects(QgsRectangle(n.geometry().buffer(rayon,12).boundingBox()))
    if len(near)>0:
        for fid in near:
            g=f[fid]
            if not(n[num]==g[num]):
                l=n.geometry().distance(g.geometry())
                id_node=unicode(g.attribute(num))
                id_stop=unicode(n.attribute(num))
                if l<rayon:
                    gline=QgsGeometry.fromPolyline([QgsPoint(n.geometry().centroid().asPoint()),QgsPoint(g.geometry().centroid().asPoint())])
                    hline=QgsGeometry.fromPolyline([QgsPoint(g.geometry().centroid().asPoint()),QgsPoint(n.geometry().centroid().asPoint())])

                    fline=QgsFeature()
                    fline.setGeometry(gline)
                    ll=gline.length()
                    moda=unicode(mode)
                    if vitesse<=0:
                        fline.setAttributes([id_stop,id_node, ll/1000,0,moda])
                    else:
                        fline.setAttributes([id_stop,id_node, ll/1000,ll*60/(vitesse*1000),moda])
                    table_connecteurs.addFeature(fline)


del table_connecteurs

