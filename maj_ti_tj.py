from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA= group
##couche= vector line
##fichier_temps=file
##temps_musliw=string temps
##temps_troncon=field couche
##depart=boolean true
##champ_ti=string ti
##champ_tj=string tj
##temps_terminal=boolean false

fichier=open(fichier_temps,"r")
reseau=processing.getObject(couche)
champs=reseau.pendingFields()
start=depart
noms_champs=[]

#lecture du noms des champs
for f in champs:
    noms_champs.append(f.name())
#ajout si necessaire champ ti tj
reseau.startEditing()
reseau.beginEditCommand("Maj ti tj")
if  champ_ti not in noms_champs:
    reseau.dataProvider().addAttributes([QgsField(champ_ti,QVariant.Double)])
  
if  champ_tj not in noms_champs:
    reseau.dataProvider().addAttributes([QgsField(champ_tj,QVariant.Double)])

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
        t=elements[colonnes[temps_musliw]].replace(",",".")
        ij=elements[colonnes["ij"]]
        if temps_terminal==False:
            links[str(ij)]=(float(t),0)
        else:
            tatt1=elements[colonnes["tatt1"]].replace(",",".")
            links[str(ij)]=(float(t),float(tatt1))


    
for f in reseau.getFeatures():
    num=f.id()
    temps=float(f[temps_troncon])
    ij=f["ij"]
    if ij in links:
        ti=links[f["ij"]][0]-links[f["ij"]][1]
        if start==True:
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti)
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti-temps)
        else:
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti)
            reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti-temps)
    else:
        ti=NULL
        reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti)
        reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti)

            
reseau.commitChanges()
reseau.endEditCommand()
    