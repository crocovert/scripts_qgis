from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

##CEREMA=group
##reseau=vector line
##prefixe=optional string
##sens= field reseau
##fichier_noeuds=output vector



layer=processing.getObject(reseau)
nom_champs=[]
for i in layer.dataProvider().fields():
    nom_champs.append(i.name())
if ("i" not in nom_champs):
    layer.dataProvider().addAttributes([QgsField("i",QVariant.String,len=15)])
if ("j" not in nom_champs):
    layer.dataProvider().addAttributes([QgsField("j",QVariant.String,len=15)])
if ("ij" not in nom_champs):
    layer.dataProvider().addAttributes([QgsField("ij",QVariant.String,len=31)])
layer.updateFields()
layer.commitChanges()
ida=layer.fieldNameIndex("i")
idb=layer.fieldNameIndex("j")
idij=layer.fieldNameIndex("ij")
lines=layer.getFeatures()
noeuds={}
nom_fichier=fichier_noeuds
champs=QgsFields()
champs.append(QgsField("num",QVariant.String,len=35))
champs.append(QgsField("nb",QVariant.Int))
table_noeuds=QgsVectorFileWriter(nom_fichier,"UTF-8",champs,QGis.WKBPoint,layer.crs(),"ESRI Shapefile")
src=QgsCoordinateReferenceSystem(layer.crs())
dest=QgsCoordinateReferenceSystem(4326)
xtr=QgsCoordinateTransform(src,dest)
for ligne in lines:
    gligne=ligne.geometry()
    if ligne[sens]=='1':
        if gligne.wkbType()==QGis.WKBMultiLineString:
            g=gligne.asMultiPolyline()
            na=g[0][0]
            liba=str(int(xtr.transform(na)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(na)[1]*1e6+180*1e6)).zfill(9)
            nb=g[-1][-1]
            libb=str(int(xtr.transform(nb)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(nb)[1]*1e6+180*1e6)).zfill(9)
            
        elif gligne.wkbType()==QGis.WKBLineString:
            g=gligne.asPolyline()
            na=g[0]
            liba=str(int(xtr.transform(na)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(na)[1]*1e6+180*1e6)).zfill(9)
            nb=g[-1]
            libb=str(int(xtr.transform(nb)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(nb)[1]*1e6+180*1e6)).zfill(9)
        if (na not in noeuds):
            noeuds[na]=(prefixe+liba,1)
        else:
            noeuds[na]=(prefixe+liba,noeuds[na][1]+1)
        if (nb not in noeuds):
            noeuds[nb]=(prefixe+libb,1)
        else:
            noeuds[nb]=(prefixe+libb,noeuds[nb][1]+1)
#outs=open("c:/temp/noeuds.txt","w")
for i,n in enumerate(noeuds):
    node=QgsFeature()
    node.setGeometry(QgsGeometry.fromPoint(QgsPoint(n[0],n[1])))
    #node.setAttributes([noeuds[n]])
    node.setAttributes([noeuds[n][0],noeuds[n][1]])
    table_noeuds.addFeature(node)
#outs.write(str(n)+";"+str(noeuds[n])+"\n")
del table_noeuds
#outs.close()
lines=layer.getFeatures()
layer.startEditing()
layer.beginEditCommand(QCoreApplication.translate("Building graph","Building graph"))
for ligne in lines:
    if ligne[sens]==1:
        gligne=ligne.geometry()
        if gligne.wkbType()==QGis.WKBMultiLineString:
            
            g=gligne.asMultiPolyline()

            na=g[0][0]
            nb=g[-1][-1]
            liba=str(int(xtr.transform(na)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(na)[1]*1e6+180*1e6)).zfill(9)
            libb=str(int(xtr.transform(nb)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(nb)[1]*1e6+180*1e6)).zfill(9)
        elif gligne.wkbType()==QGis.WKBLineString:

            g=gligne.asPolyline()
            na=g[0]
            nb=g[-1]
            liba=str(int(xtr.transform(na)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(na)[1]*1e6+180*1e6)).zfill(9)

            libb=str(int(xtr.transform(nb)[0]*1e6+180*1e6)).zfill(9)+str(int(xtr.transform(nb)[1]*1e6+180*1e6)).zfill(9)


        id=ligne.id()
        #valid={ida : noeuds[na], idb: noeuds[nb]}

        layer.changeAttributeValue(id,ida, noeuds[na])
        layer.changeAttributeValue(id,idb, noeuds[nb])
        layer.changeAttributeValue(id,idij, noeuds[na]+"-"+noeuds[nb])

layer.endEditCommand()
layer.commitChanges()
