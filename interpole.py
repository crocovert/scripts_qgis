from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import numpy
import math

##CEREMA=group
##reseau=vector line
##fenetre=extent
##cout_i=field reseau
##cout_j=field reseau
##sens=field reseau
##diffusion=field reseau
##traversabilite=field reseau
##nb_pixels_x=number 200
##nb_pixels_y=number 200
##taille_pixel_x= number -1.0
##taille_pixel_y=number  -1.0
##decimales=number 5
##rayon=number 500.0
##vitesse_diffusion=number 4.0
##vitesse_variable=optional field reseau 
##intraversable=boolean false
##resultat=output raster 


var_diffusion=diffusion
var_sens=sens
grille=numpy.array([[-9999.0]*nb_pixels_y]*nb_pixels_x)
grille_distance=numpy.array([[1e38]*nb_pixels_y]*nb_pixels_x)
rep=os.path.dirname(resultat)
a=fenetre.split(",")
fenetre2=QgsRectangle(float(a[0]),float(a[2]),float(a[1]),float(a[3]))
p1=[a[0],a[2]]
p2=[a[1],a[3]]
ll=(float(p1[0]),float(p1[1]))
hauteur=float(p2[1])-float(p1[1])
largeur=float(p2[0])-float(p1[0])
if not(taille_pixel_x<=0):
    nb_pixels_x=int(largeur/taille_pixel_x)
else:
    taille_pixel_x=float(largeur/nb_pixels_x)
if not(taille_pixel_y<=0):
    nb_pixels_y=int(hauteur/taille_pixel_y)
else:
    taille_pixel_y=float(hauteur/nb_pixels_y)
layer=processing.getObject(reseau)
if layer.type()==QgsMapLayer.VectorLayer:
    if not layer==None:
        if layer.geometryType()==1:
            simple=QgsSimplifyMethod()
            simple.setMethodType(QgsSimplifyMethod.PreserveTopology)
            simple.setTolerance(min(taille_pixel_x,taille_pixel_y)/2)
            texte='"'+diffusion+'" in (\'1\',\'2\',\'3\') and ("'+cout_j+'" IS NOT NULL and "'+sens+'" in (\'1\',\'3\')) '
            request=(QgsFeatureRequest().setFilterRect(fenetre2)).setFilterExpression(texte).setSimplifyMethod(simple).setFlags(QgsFeatureRequest.ExactIntersect)
            req_intra=(QgsFeatureRequest().setFilterRect(fenetre2)).setFilterExpression('"'+traversabilite+'" in (\'1\',\'2\',\'3\')').setSimplifyMethod(simple).setFlags(QgsFeatureRequest.ExactIntersect)
            features=[f for f in layer.getFeatures(request)]
            if intraversable:
                features_intra=[f for f in layer.getFeatures(req_intra)]
            else:
                features_intra=[]
            for k,i in enumerate(features):
                sens=i.attribute(var_sens)
                diffusion=i.attribute(var_diffusion)
                if  vitesse_variable:
                    speed=60/(1000*i.attribute(vitesse_variable))
                else:
                    if vitesse_diffusion>0:
                        speed=60/(1000*vitesse_diffusion)
                    else:
                        speed=0
                if sens in ['1','2','3'] :
                    geom=i.geometry()
                    zone=geom.buffer(rayon,12).boundingBox()
                    deltax=int((zone.xMinimum()-ll[0])/taille_pixel_x)
                    deltay=int((zone.yMinimum()-ll[1])/taille_pixel_y)
                    dx=int(zone.width()/taille_pixel_x)
                    dy=int(zone.height()/taille_pixel_y)
                    l1=geom.length()
                    if geom.isMultipart():
                        geom_l=geom.asMultiPolyline()
                    else:
                        geom_l=geom.asPolyline()
                    
                    for p in range(dx):
                        d2x=deltax+p
                        for q in range(dy):
                            d2y=deltay+q
                            if 0<=d2x<nb_pixels_x and 0<=d2y<nb_pixels_y:
                                pt1=QgsGeometry.fromPoint(QgsPoint(ll[0]+(d2x+0.5)*taille_pixel_x,ll[1]+(d2y+0.5)*taille_pixel_y))
                                res=geom.closestSegmentWithContext(pt1.asPoint())
                                d=round(res[0],decimales)
                                if d<=grille_distance[d2x,d2y] and d<rayon*rayon:
                                    if d>0 and l1>0:
                                        pt2=res[1]
                                        if geom.isMultipart():
                                            num_poly=-1
                                            npts=0
                                            for id_poly in geom_l:
                                                if res[2]<npts+len(id_poly):
                                                    num_poly=(id_poly,npts)
                                                else:
                                                    npts+=len(id_poly)
                                            geom_a=[num_poly][:(res[2]-npts)]+[pt2]
                                        else:
                                            geoma=geom_l[:res[2]]+[pt2]
                                        #geoma=QgsGeometry(geom)
                                        #geoma.insertVertex(pt2[0],pt2[1],res[2])
                                        l2=QgsGeometry.fromPolyline(geoma).length()
                                        if res[2]==0:
                                            pt3=geom.vertexAt(res[2])
                                            pt4=geom.vertexAt(res[2]+1)
                                        else:
                                            try:
                                                pt3=geom.vertexAt(res[2]-1)
                                                pt4=geom.vertexAt(res[2])
                                            except:
                                                print(res,geom_l)
                                                pt3=geom_l[res[2]-1]
                                                pt4=geom_l[res[2]]
                                        p1=pt1.asPoint()
                                        test_sens=(pt4.x()-pt3.x())*(p1.y()-pt2.y())-(p1.x()-pt2.x())*(pt4.y()-pt3.y())
                                        if sens in ['1','3'] and not i.attribute(cout_j)==None:
                                            if (diffusion in ['1','3'] and test_sens<=0) or (diffusion in ['2','3'] and test_sens>=0):
                                                tj=i.attribute(cout_j)
                                                if not tj==None:
                                                    ti=i.attribute(cout_i)
                                                    if not ti==None:
                                                        t=tj*(l2/l1)+ti*(1-(l2/l1))+math.sqrt(d)*speed
                                                        l3=QgsGeometry.fromPolyline([pt1.asPoint(),QgsPoint(pt2)])
                                                result_test=False
                                                if l3!=None:
                                                    if len(features_intra)>0:
                                                        for intra in features_intra:
                                                            if intra.geometry().intersects(l3):
                                                                result_test=True
                                                                break
                                                if result_test==False:
                                                    if (t<grille[d2x,d2y] and d==grille_distance[d2x,d2y]) or d<grille_distance[d2x,d2y]:
                                                        grille_distance[d2x,d2y] =d
                                                        grille[d2x,d2y] =t

            sortie=os.path.splitext(resultat)
            fichier_grille=open(sortie[0]+sortie[1],'w')
            fichier_grille.write("NCOLS {0:d}\nNROWS {1:d}\nXLLCORNER {2}\nYLLCORNER {3}\nDX {4}\nDY {5}\nNODATA_VALUE -9999\n".format(nb_pixels_x,nb_pixels_y,ll[0],ll[1],taille_pixel_x,taille_pixel_y))
            fichier_grille2=open(sortie[0]+"_dist"+sortie[1],'w')
            fichier_grille2.write("NCOLS {0:d}\nNROWS {1:d}\nXLLCORNER {2}\nYLLCORNER {3}\nDX {4}\nDY {5}\nNODATA_VALUE -9999\n".format(nb_pixels_x,nb_pixels_y,ll[0],ll[1],taille_pixel_x,taille_pixel_y))
            g1=numpy.rot90(grille,1)
            #g1=numpy.flipud(g1)
            g2=numpy.rot90(grille_distance,1)
            #g2=numpy.flipud(g2)
            for i in g1:
                fichier_grille.write(" ".join([str(ii) for ii in i])+"\n")
            fichier_grille.close()
            for i in g2:
                fichier_grille2.write(" ".join([str(math.sqrt(ii)) for ii in i])+"\n")
            fichier_grille2.close()

            fichier_prj=open(sortie[0]+".prj",'w')
            fichier2_prj=open(sortie[0]+"_dist.prj",'w')
            fichier_prj.write(layer.crs().toWkt())
            fichier2_prj.write(layer.crs().toWkt())
            fichier_prj.close()
            fichier2_prj.close()
            nom_sortie=os.path.basename(sortie[0])
            rlayer=QgsRasterLayer(resultat,nom_sortie)

#                    nom_fichier_iso=sortie[0]+"_iso.shp"
#                    champs=QgsFields()
#                    champs.append(QgsField("Id",QVariant.String))
#                    self.table_lignes=QgsVectorFileWriter(nom_fichier_iso,"UTF-8",champs,QGis.WKBMultiLineString
#                    ,self.iface.activeLayer().crs(),"ESRI Shapefile")
#                    for p in range(self.nx-1):
#                        for q in range(self.ny-1):
#                            self.contours(grille,p,q,0.1)
#                    iso_layer=QgsVectorLayer(nom_fichier_iso,nom_sortie+"_iso",'ogr')
#                    QgsMapLayerRegistry.instance().addMapLayer(iso_layer)
#                    del self.table_lignes
