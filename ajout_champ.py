from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##couche=vector
##nouveau_champ=optional string
##champ_existant=field couche
##type=string String
##taille=number 20
##precision=number 15
##filtre=optional string
##formule=string

table=processing.getObject(couche)
champs=table.pendingFields()

noms_champs=[c.name() for c in champs]

if len(nouveau_champ)>0 and nouveau_champ not in noms_champs:
    table.dataProvider().addAttributes([QgsField(nouveau_champ,eval("QVariant."+type),len=taille,prec=precision)])
    table.updateFields()
    lib_champ=nouveau_champ
else:
    lib_champ=champ_existant
    
if len(filtre)==0:
    request=QgsFeatureRequest()
else:
    expr= QgsExpression(filtre)
    request = QgsFeatureRequest(expr)

exp2 = QgsExpression(formule)
exp2.prepare(table.pendingFields())
id_champ=table.dataProvider().fieldNameMap()[lib_champ]

table.startEditing()
table.beginEditCommand("Maj champ")
features=[f for f in table.getFeatures(request)]
n=len(features)
progress.setText("mise à jour du champ...")
for p,f in enumerate(features):
    num=f.id()
    valeur = exp2.evaluate(f)
    table.changeAttributeValue(num,id_champ,valeur)
    progress.setPercentage(p*100/n)

table.commitChanges()
table.endEditCommand()    
