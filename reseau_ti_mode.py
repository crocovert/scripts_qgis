
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

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
##mode=field reseau_routier
##reseau_musliw=output file


a=fenetre.split(",")
fenetre2=QgsRectangle(float(a[0]),float(a[2]),float(a[1]),float(a[3]))
texte='\"'+sens+'\" in (\'1\',\'2\',\'3\')'
request=QgsFeatureRequest().setFilterRect(fenetre2)
layer=processing.getObject(reseau_routier)
sortie=open(reseau_musliw,"w")
for f in layer.getFeatures(request):
    if sens==None:
        s='1'
    else:
        s=f.attribute(sens)
    l=f.attribute(longueur)
    t=f.attribute(temps)
    i=f.attribute(noeud_i)
    j=f.attribute(noeud_j)
    te=f.attribute(texte_arc)
    mod=f.attribute(mode)
    if s in ('1','3'):
       sortie.write(str(i)+';'+str(j)+';'+str(t)+';'+str(l)+';'+periode+';'+num_plage+';'+debut_periode+';'+fin_periode+';'+calendrier+';'+str(te)+';'+str(mod)+'\n')
    if s in ('2','3'):
       sortie.write(str(j)+';'+str(i)+';'+str(t)+';'+str(l)+';'+periode+';'+num_plage+';'+debut_periode+';'+fin_periode+';'+calendrier+';'+str(te).decode('utf-8')+';'+str(mod)+'\n')
sortie.close()
