
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
##CEREMA=group
##entrepots=vector
##id=field entrepots
##resultat=output file

index=QgsSpatialIndex()
ets=processing.getObject(entrepots)
sortie=open(resultat,"w")
proches={}
res=[]

for i in processing.features(ets):
    index.insertFeature(i)

fs=[f for f in processing.features(ets)]
nb=len(fs)
print(nb)
while len(fs)>1:
    for i,n in enumerate(fs):
        near=index.nearestNeighbor(n.geometry().centroid().asPoint(),2)
        ii=n.id()
        for j in near:
            if not ii==j:
                for  fid,f in enumerate(fs):
                    if ii==f.id():
                        proches[n.attribute("r_id")]=[n.attribute("r_id"),f.attribute("r_id"),n.geometry().distance(f.geometry())]
                        print(fid)
                break

    ids=sorted(proches,key=lambda a: proches[a][2] )[0]
    print(proches[ids][0],proches[ids][1],proches[ids][2])
    res.append((proches[ids][0],proches[ids][1],proches[ids][2]))
    
    index.deleteFeature(n)
    index.deleteFeature(f)
    f.setGeometry(f.geometry().combine(n.geometry()))
    index.insertFeature(f)
    if fid in fs:
        fs.remove(fid)



for i in res:
    sortie.write(str(i[0])+";"+str(i[1])+";"+str(i[2])+"\n")
sortie.close()
    
        
