from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA= group
##couche= vector 
##fichier_temps=file
##vitesse_troncon_km_h=field couche
##depart=boolean true
##champ_ti=string ti
##champ_tj=string tj

fichier=open(fichier_temps,"r")
reseau=processing.getObject(couche)
champs=reseau.pendingFields()
start=depart
noms_champs=[]

#lecture du noms des champs
for f in champs:
    noms_champs.append(f.name())
#ajout si nÃÂÃÂ©cessaire des champs ti,tj,ij
reseau.startEditing()
reseau.beginEditCommand("Maj ti tj")
if  u"ti" not in noms_champs:
    reseau.dataProvider().addAttributes([QgsField(champ_ti,QVariant.Double)])
  
if  u"tj" not in noms_champs:
    reseau.dataProvider().addAttributes([QgsField(champ_tj,QVariant.Double)])
    reseau.addAttribute(QgsField("tj",QVariant.Double))

if  u"ij" not in noms_champs:
    reseau.dataProvider().addAttributes([QgsField("ij",QVariant.String)])
    reseau.addAttribute(QgsField("ij",QVariant.String))
    for f in reseau.getFeatures():
        num=f.id()
        lab_ij=f['i']+'-'+f['j']
        reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()['ij'],lab_ij)


reseau.updateFields()




colonnes={}
links={}
for k,i in enumerate(fichier):
    elements=i.strip('\n').split(";")
    ncols=len(elements)
    if k==0:
        for j in range(ncols):
            colonnes[elements[j]]=j
    else:
        t=elements[colonnes["temps"]]
        ij=elements[colonnes["ij"]]
        links[str(ij)]=float(t)


    
for f in reseau.getFeatures():
    longueur=float(f.geometry().length())/1000
    num=f.id()
    temps=60*longueur/float(f[vitesse_troncon_km_h])
    ij=f["ij"]
    if ij in links:
        ti=links[f["ij"]]
        if start==True:
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti)
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti-temps)
        else:
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti)
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti-temps)
            
reseau.commitChanges()
reseau.endEditCommand()
    