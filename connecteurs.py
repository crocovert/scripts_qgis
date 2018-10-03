
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

import codecs

##CEREMA=group
##arrets=vector
##stop_id=field arrets
##texte_ori=string TC
##mode_ori=string TC
##noeuds=vector
##node_id=field noeuds
##texte_des=string MAP
##mode_des=string MAP
##rayon=number 1000
##vitesse=number 4.0
##connecteurs=output file

index=QgsSpatialIndex()
stops=processing.getObject(arrets)
nodes=processing.getObject(noeuds)
sortie=codecs.open(connecteurs,"w",encoding="utf-8")
nb=len(processing.features(stops))
nbc=0
for i in processing.features(nodes):
    index.insertFeature(i)
for i,n in enumerate(processing.features(stops)):
    near=index.nearestNeighbor(n.geometry().centroid().asPoint(),1)
    nearest=near[0]
    f=nodes.getFeatures(request=QgsFeatureRequest(nearest))
    for j, g in enumerate(f):
        if j==0:
            l=n.geometry().distance(g.geometry())
            id_node=str(g.attribute(node_id))
            id_stop=str(n.attribute(stop_id))
            if l<rayon:
                nbc+=1
                if vitesse>0:
                    sortie.write(id_node+';'+id_stop+';'+str((60/vitesse)*(l/1000.0))+';'+str(l/1000.0)+';-1;-1;-1;-1;-1;'+texte_des+texte_ori +';'+mode_des+mode_ori+'\n')
                    sortie.write(id_stop+';'+id_node+';'+str((60/vitesse)*(l/1000.0))+';'+str(l/1000.0)+';-1;-1;-1;-1;-1;'+texte_ori+texte_des+';'+mode_ori+mode_des+'\n')
                else:
                    sortie.write(id_node+';'+id_stop+';'+str(0.0)+';'+str(l/1000.0)+';-1;-1;-1;-1;-1;'+texte_des+texte_ori +';'+mode_des+mode_ori+'\n')
                    sortie.write(id_stop+';'+id_node+';'+str(0.0)+';'+str(l/1000.0)+';-1;-1;-1;-1;-1;'+texte_ori+texte_des+';'+mode_ori+mode_des+'\n')

progress.setText(unicode(nbc)+"/"+unicode(nb)+" noeuds connectes")
sortie.close()
