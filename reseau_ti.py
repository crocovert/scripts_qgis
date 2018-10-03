# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import codecs

##CEREMA=group
##reseau_routier=vector line
##fenetre=extent
##sens=optional field reseau_routier 
##temps=field reseau_routier
##longueur=field reseau_routier
##noeud_i=field reseau_routier 
##noeud_j=field reseau_routier 
##periode=string -1
##num_plage=string -1
##debut_periode=string -1
##fin_periode=string -1
##calendrier=string -1
##texte_arc=field reseau_routier
##mode=string m
##reseau_musliw=output file


a=fenetre.split(",")
fenetre2=QgsRectangle(float(a[0]),float(a[2]),float(a[1]),float(a[3]))
request=QgsFeatureRequest().setFilterRect(fenetre2)
layer=processing.getObject(reseau_routier)
sortie=codecs.open(reseau_musliw,"w",encoding="utf8")
progress.setText(u"Ecriture du reseau Musliw transport individuel...")
features=[f for f in layer.getFeatures(request)]
n=len(features)
for p,f in enumerate(features):
    
    progress.setPercentage(p*100/n)
    if sens==None:
        s='1'
    else:
        s=f.attribute(sens)
    l=f.attribute(longueur)
    t=f.attribute(temps)
    i=f.attribute(noeud_i)
    j=f.attribute(noeud_j)
    te=f.attribute(texte_arc)
    if s in ('1','3'):
       sortie.write(str(i)+';'+str(j)+';'+str(t)+';'+str(l)+';'+periode+';'+num_plage+';'+debut_periode+';'+fin_periode+';'+calendrier+';'+str(te)+';'+str(mode)+'\n')
    if s in ('2','3'):
       sortie.write(str(j)+';'+str(i)+';'+str(t)+';'+str(l)+';'+periode+';'+num_plage+';'+debut_periode+';'+fin_periode+';'+calendrier+';'+str(te).decode('utf-8')+';'+str(mode)+'\n')
sortie.close()
