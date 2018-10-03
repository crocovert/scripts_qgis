from pyspatialite import dbapi2 as db
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *


##couche=vector

layer=processing.getObject(couche)

QgsVectorFileWriter.writeAsVectorFormat(layer,"F:/temp/"+layer.name() +".sqlite","utf-8", None, "SQLite", False, None ,["SPATIALITE=YES",])



db_filename = "F:/temp/"+layer.name() +".sqlite"
conn = db.connect(db_filename)
c = conn.cursor()
texte='drop table if exists tata'
rs = c.execute(texte)
texte='create table \"'+'tata'+'\" as SELECT '+layer.name()+'.\'id\' as Id, casttomultipolygon(buildarea(\"'+layer.name()+'\".\'GEOMETRY\')) AS Geometry FROM \"'+layer.name()+'\" GROUP BY  '+layer.name()+'.\'id\' ;'
rs = c.execute(texte)
texte='SELECT RecoverGeometryColumn(\'tata\', \'Geometry\',  2154, \'MULTIPOLYGON\', \'XY\')'
rs = c.execute(texte)