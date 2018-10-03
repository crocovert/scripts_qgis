from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *


##STS=group
##fichier_nodes=vector point
##stop_id=field fichier_nodes
##fichier_arcs=vector line
##arc_id=field fichier_arcs
##rayon=number 50
arcs=processing.getObject(fichier_arcs)
nodes=processing.getObject(fichier_nodes)

nodes.startEditing()
nodes.beginEditCommand("Maj ti tj")

index=QgsSpatialIndex()
for i in processing.features(arcs):
    index.insertFeature(i)

for i in  processing.features(nodes):
    rectangle=i.geometry().buffer(rayon,12).boundingBox()
    indices=index.intersects(rectangle)
    distance_max=1e38
    for indice in indices:
        ligne=arcs.getFeatures(request=QgsFeatureRequest(indice))
        for l in ligne:
            distance=i.geometry().distance(l.geometry())
            if distance<distance_max:
                distance_max=distance
                ligne_min=l
    nodes.changeAttributeValue(i.id(), nodes.dataProvider().fieldNameMap()['section_id'],ligne_min.attribute(arc_id))
    
nodes.updateFields()
    
    
    