from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import os
import time
from pyspatialite import dbapi2 as db

##CEREMA=group
##isochrones=vector
##id=field isochrones
##socioeco=vector
##variable=field socioeco
##moyenne=boolean
##resultat=output vector

iso=processing.getObject(isochrones)
insee=processing.getObject(socioeco)
nom_sortie=os.path.basename(resultat)
nom_sortie,ext_sortie=os.path.splitext(os.path.basename(nom_sortie))
rep_sortie=os.path.dirname(resultat)
QgsVectorFileWriter.writeAsVectorFormat(iso, rep_sortie+"/"+iso.name(), "utf-8", None, "ESRI Shapefile")
QgsVectorFileWriter.writeAsVectorFormat(insee, rep_sortie+"/"+insee.name(), "utf-8", None, "ESRI Shapefile")
db_filename = rep_sortie+"/"+iso.name() +".sqlite"
conn = db.connect(":memory:")
c = conn.cursor()
texte='drop table if exists "'+insee.name()+'"'
rs = c.execute(texte)
conn.commit()
texte='drop table if exists "'+iso.name()+'"'
rs = c.execute(texte)
conn.commit()
texte='create virtual table "'+insee.name()+ "\" using VirtualShape( '"+rep_sortie+"/"+insee.name()+"',UTF-8,"+str(insee.crs().postgisSrid())+");"
rs = c.execute(texte)
conn.commit()
texte='create virtual table "'+iso.name()+ "\" using VirtualShape( '"+rep_sortie+"/"+iso.name()+"',UTF-8,"+str(iso.crs().postgisSrid())+");"
rs = c.execute(texte)
conn.commit()
texte='drop table if exists res'
rs = c.execute(texte)
conn.commit()
if moyenne==False:
    texte='create table res as select '+'casttomultipolygon(a.Geometry) as geom,a.'+id+' as id,sum(b.'+variable+'*st_area(st_intersection(a.Geometry,b.Geometry))/st_area(b.Geometry)) as '+variable+' from "'+iso.name()+'" a,"'+insee.name()+'" b where intersects(a.Geometry,b.Geometry) group by a.Geometry,a.'+ id
    

else:
    texte='create table res as select '+'casttomultipolygon(a.Geometry) as geom,a.'+id+' as id ,sum(b.'+variable+'*st_area(st_intersection(a.Geometry,b.Geometry)))/sum(st_area(st_intersection(a.Geometry,b.Geometry))) as '+variable+' from "'+iso.name()+'" a,"'+insee.name()+'" b where intersects(a.Geometry,b.Geometry) group by a.Geometry,a.'+ id

rs=c.execute(texte)
conn.commit()


texte='SELECT RecoverGeometryColumn(\"res\", \'geom\','+str(iso.crs().postgisSrid())+', \'MULTIPOLYGON\',\'XY\')'

rs = c.execute(texte)   
conn.commit()
rs = c.execute('select asWkt(geom),* from res')





texte='select id,'+variable+', asWkt(geom) from res'

rs=c.execute(texte)
res=c.fetchall()

conn.commit()
champs2=QgsFields()
champs2.append(QgsField("id",QVariant.Double))
champs2.append(QgsField(variable,QVariant.Double))

table_lignes=QgsVectorFileWriter(resultat,"UTF-8",champs2,QGis.WKBMultiPolygon,iso.crs(),"ESRI Shapefile")

for r in res:
    f1=QgsFeature(champs2)
    geom=QgsGeometry.fromWkt(r[2])
    f1.setGeometry(geom)
    f1.setAttributes([float(r[0]),float(r[1])])
    table_lignes.addFeature(f1)
conn.close()
del c

del conn
del table_lignes


