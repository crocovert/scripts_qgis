from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from osgeo import gdal
import numpy
import math
from pyspatialite import dbapi2 as db

##CEREMA=group
##raster=raster
##bande=number 1
##mini=number 0.0
##maxi=number 60.0
##intervalle=number 10.0
##novalue=number  -9999.0
##polygones=boolean true
##resultat=output vector 


def contours(grille, p,q,s):
    lignes={}
    points={}
    bords={}
    cadreu={}
    cadred={}
    cadrel={}
    cadrer={}
    cadre={}
    bordu={}
    bordd={}
    bordl={}
    bordr={}
    lu=grille[p,q]
    ld=grille[p,q+1]
    ru=grille[p+1,q]
    rd=grille[p+1,q+1]
    if lu>novalue:
        ilu=int(math.floor(lu/s))
    else:
        ilu=novalue
    if ld>novalue:
        ild=int(math.floor(ld/s))
    else:
        ild=novalue
    if ru>novalue:
        iru=int(math.floor(ru/s))
    else:
        iru=novalue
    if rd>novalue:
        ird=int(math.floor(rd/s))
    else:
        ird=novalue
    if ilu>novalue:
        ilu=min(max(ilu,int(math.floor(mini/s))),int(math.floor(maxi/s)))
    if ild>novalue:
        ild=min(max(ild,int(math.floor(mini/s))),int(math.floor(maxi/s)))
    if iru>novalue:
        iru=min(max(iru,int(math.floor(mini/s))),int(math.floor(maxi/s)))
    if ird>novalue:
        ird=min(max(ird,int(math.floor(mini/s))),int(math.floor(maxi/s)))
    if ilu==ild and ilu!=novalue:
        if ilu not in bordl:
            bordl[ilu]=[]
        bordl[ilu].append([p,q])
        if ilu+1 not in bordl:
            bordl[ilu+1]=[]
        bordl[ilu+1].append([p,q+1])
    if ild==ird and ild!=novalue:
        if ild not in bordd:
            bordd[ild]=[]
        bordd[ild].append([p,q+1])
        if ild+1 not in bordd:
            bordd[ild+1]=[]
        bordd[ild+1].append([p+1,q+1])
    if iru==ird and iru!=novalue:
        if ird not in bordr:
            bordr[ird]=[]
        bordr[ird].append([p+1,q])
        if ird+1 not in bordr:
            bordr[ird+1]=[]
        bordr[ird+1].append([p+1,q+1])
    if ilu==iru and ilu!=novalue:
        if ilu not in bordu:
            bordu[ilu]=[]
        bordu[ilu].append([p,q])
        if ilu+1 not in bordu:
            bordu[ilu+1]=[]
        bordu[ilu+1].append([p+1,q])
    if ilu<ild:
        if lu==novalue:
            if ild not in bordl:
                bordl[ild]=[]
            bordl[ild].append([p,q])
            bordl[ild].append([p,q+1])
        else:
            for i in range(ilu,ild):
                if i not in points:
                    points[i]=[]
                points[i].append([p,q+((i+1)*s-lu)/(ld-lu)])
                if i==ilu:
                    if i not in bordl:
                        bordl[i]=[]
                    bordl[i].append([p,q])
                if i+1 not in bordl:
                    bordl[i+1]=[]
                bordl[i+1].append([p,q+((i+1)*s-lu)/(ld-lu)])
                if i==ild-1:
                    if i+2 not in bordl:
                        bordl[i+2]=[]
                    bordl[i+2].append([p,q+1])
    if ilu>ild:
        if ld==novalue:
            if ilu not in bordl:
                bordl[ilu]=[]
            bordl[ilu].append([p,q])
            bordl[ilu].append([p,q+1])
        else:
            for i in range(ild,ilu):
                if i not in points:
                    points[i]=[]
                points[i].append([p,q+(lu-(i+1)*s)/(lu-ld)])
                if i==ild:
                    if i-1 not in bordl:
                        bordl[i-1]=[]
                    bordl[i-1].append([p,q+1])
                if i not in bordl:
                    bordl[i]=[]
                bordl[i].append([p,q+(lu-(i+1)*s)/(lu-ld)])
                if i==ilu-1:
                    if i+1 not in bordl:
                        bordl[i+1]=[]
                    bordl[i+1].append([p,q])
    if ild<ird:
        if ld==novalue:
            if ird not in bordd:
                bordd[ird]=[]
            bordd[ird].append([p,q+1])
            bordd[ird].append([p+1,q+1])
        else:
            for i in range(ild,ird):
                if i not in points:
                    points[i]=[]
                points[i].append([p+((i+1)*s-ld)/(rd-ld),q+1])
                if i==ild:
                    if i not in bordd:
                        bordd[i]=[]
                    bordd[i].append([p,q+1])
                if i+1 not in bordd:
                    bordd[i+1]=[]
                bordd[i+1].append([p+((i+1)*s-ld)/(rd-ld),q+1])
                if i==ird-1:
                    if i+2 not in bordd:
                        bordd[i+2]=[]
                    bordd[i+2].append([p+1,q+1])
    if ild>ird:
        if rd==novalue:
            if ild not in bordd:
                bordd[ild]=[]
            bordd[ild].append([p,q+1])
            bordd[ild].append([p+1,q+1])
        else:
            for i in range(ird,ild):
                if i not in points:
                    points[i]=[]
                points[i].append([p+(ld-(i+1)*s)/(ld-rd),q+1])
                if i==ird:
                    if i-1 not in bordd:
                        bordd[i-1]=[]
                    bordd[i-1].append([p+1,q+1])
                if i not in bordd:
                    bordd[i]=[]
                bordd[i].append([p+(ld-(i+1)*s)/(ld-rd),q+1])
                if i==ild-1:
                    if i+1 not in bordd:
                        bordd[i+1]=[]
                    bordd[i+1].append([p,q+1])
    if ird<iru:
        if rd==novalue:
            if iru not in bordr:
                bordr[iru]=[]
            bordr[iru].append([p+1,q])
            bordr[iru].append([p+1,q+1])
        else:
            for i in range(ird,iru):
                if i not in points:
                    points[i]=[]
                points[i].append([p+1,q+(ru-(i+1)*s)/(ru-rd)])
                if i==iru-1:
                    if i+1 not in bordr:
                        bordr[i+1]=[]
                    bordr[i+1].append([p+1,q])
                if i==ird:
                    if i-1 not in bordr:
                        bordr[i-1]=[]
                    bordr[i-1].append([p+1,q+1])
                if i not in bordr:
                    bordr[i]=[]
                bordr[i].append([p+1,q+(ru-(i+1)*s)/(ru-rd)])
    if ird>iru:
        if ru==novalue:
            if ird not in bordr:
                bordr[ird]=[]
            bordr[ird].append([p+1,q])
            bordr[ird].append([p+1,q+1])
        else:
            for i in range(iru,ird):
                if i not in points:
                    points[i]=[]
                points[i].append([p+1,q+((i+1)*s-ru)/(rd-ru)])
                if i==iru:
                    if i not in bordr:
                        bordr[i]=[]
                    bordr[i].append([p+1,q])
                if i+1 not in bordr:
                    bordr[i+1]=[]
                bordr[i+1].append([p+1,q+((i+1)*s-ru)/(rd-ru)])
                if i==ird-1:
                    if i+2 not in bordr:
                        bordr[i+2]=[]
                    bordr[i+2].append([p+1,q+1])
    if iru<ilu:
        if ru==novalue:
            if ilu not in bordu:
                bordu[ilu]=[]
            bordu[ilu].append([p,q])
            bordu[ilu].append([p+1,q])
        else:
            for i in range(iru,ilu):
                if i not in points:
                    points[i]=[]
                points[i].append([p+(lu-(i+1)*s)/(lu-ru),q])
                if i==iru:
                    if i-1 not in bordu:
                        bordu[i-1]=[]
                    bordu[i-1].append([p+1,q])
                if i==ilu-1:
                    if i+1 not in bordu:
                        bordu[i+1]=[]
                    bordu[i+1].append([p,q])
                if i not in bordu:
                    bordu[i]=[]
                bordu[i].append([p+(lu-(i+1)*s)/(lu-ru),q])
    if iru>ilu:
        if lu==novalue:
            if iru not in bordu:
                bordu[iru]=[]
            bordu[iru].append([p,q])
            bordu[iru].append([p+1,q])
        else:
            for i in range(ilu,iru):
                if i not in points:
                    points[i]=[]
                points[i].append([p+((i+1)*s-lu)/(ru-lu),q])
                if i==ilu:
                    if i not in bordu:
                        bordu[i]=[]
                    bordu[i].append([p,q])
                if i+1 not in bordu:
                    bordu[i+1]=[]
                bordu[i+1].append([p+((i+1)*s-lu)/(ru-lu),q])
                if i==iru-1:
                    if i+2 not in bordu:
                        bordu[i+2]=[]
                    bordu[i+2].append([p+1,q])
    for pt in points:
        mx=sum(float(points[pt][j][0]) for j in range(len(points[pt])))/len(points[pt])
        my=sum(float(points[pt][j][1]) for j in range(len(points[pt])))/len(points[pt])
        for j in range(len(points[pt])):
            n=len(points[pt])
            if n>2:
                p1x=ll[0]+(p+1-0.02*((-1)**(int(j/2))))*pixel_size_x
                p2x=ll[0]+(points[pt][j][0]+0.5)*pixel_size_x
                q1y=ll[1]+(q+1-0.02*((-1)**(int(j/2))))*pixel_size_y
                q2y=ll[1]+(points[pt][j][1]+0.5)*pixel_size_y
                ligne1=QgsGeometry.fromMultiPolyline([[QgsPoint(p1x,q1y),QgsPoint(p2x,q2y)]])
            else:
                p1x=ll[0]+(mx+0.5)*pixel_size_x
                p2x=ll[0]+(points[pt][j][0]+0.5)*pixel_size_x
                q1y=ll[1]+(my+0.5)*pixel_size_y
                q2y=ll[1]+(points[pt][j][1]+0.5)*pixel_size_y
                ligne1=QgsGeometry.fromMultiPolyline([[QgsPoint(p1x,q1y),QgsPoint(p2x,q2y)]])

            f1=QgsFeature()
            f1.setAttributes([pt*s])
            f1.setGeometry(ligne1)
            f2=QgsFeature()
            f2.setAttributes([(pt+1)*s])
            f2.setGeometry(ligne1)
            if min(lu,ld,ru,rd)>novalue:
                if (pt*s,p,q) not in polys:
                    polys[pt*s,p,q]=[]
                polys[pt*s,p,q].append(f1.geometry().asMultiPolyline())
                if ((pt+1)*s,p,q) not in polys:
                    polys[(pt+1)*s,p,q]=[]
                polys[(pt+1)*s,p,q].append(f2.geometry().asMultiPolyline())
                

    if len(bordu)>0:
        bords=sorted(bordu.items(),key=lambda x:x[1][0])
        for pt in range(len(bords)-1):
            p1=ll[0]+(bords[pt][1][0][0]+0.5)*pixel_size_x
            p2=ll[0]+(bords[pt+1][1][0][0]+0.5)*pixel_size_x
            q1=ll[1]+(bords[pt][1][0][1]+0.5)*pixel_size_y
            q2=ll[1]+(bords[pt+1][1][0][1]+0.5)*pixel_size_y
            ligne1=QgsGeometry.fromMultiPolyline([[QgsPoint(p1,q1),QgsPoint(p2,q2)]])
            f1=QgsFeature()
            f1.setAttributes([bords[pt][0]*s])
            f1.setGeometry(ligne1)
            if q>0:
                if q<ny-1:
                    if (bords[pt][0]*s, p,q) not in polys:
                        polys[bords[pt][0]*s,p,q]=[]
                    polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())
            else:
                if (bords[pt][0]*s, p,q) not in polys:
                    polys[bords[pt][0]*s,p,q]=[]
                polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())
    if len(bordl)>0:
        bords=sorted(bordl.items(),key=lambda x:x[1][0][1])
        for pt in range(len(bords)-1):
            p1=ll[0]+(bords[pt][1][0][0]+0.5)*pixel_size_x
            p2=ll[0]+(bords[pt+1][1][0][0]+0.5)*pixel_size_x
            q1=ll[1]+(bords[pt][1][0][1]+0.5)*pixel_size_y
            q2=ll[1]+(bords[pt+1][1][0][1]+0.5)*pixel_size_y
            ligne1=QgsGeometry.fromMultiPolyline([[QgsPoint(p1,q1),QgsPoint(p2,q2)]])
            f1=QgsFeature()
            f1.setAttributes([bords[pt][0]*s])
            f1.setGeometry(ligne1)
            if p>0:
                if p<nx-1:
                    if (bords[pt][0]*s, p,q) not in polys:
                        polys[bords[pt][0]*s,p,q]=[]
                    polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())                                
            else:
                if (bords[pt][0]*s, p,q) not in polys:
                    polys[bords[pt][0]*s,p,q]=[]
                polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())                    

    if len(bordr)>0:
        bords=sorted(bordr.items(),key=lambda x:x[1][0][1])
        for pt in range(len(bords)-1):

            p1=ll[0]+(bords[pt][1][0][0]+0.5)*pixel_size_x
            p2=ll[0]+(bords[pt+1][1][0][0]+0.5)*pixel_size_x
            q1=ll[1]+(bords[pt][1][0][1]+0.5)*pixel_size_y
            q2=ll[1]+(bords[pt+1][1][0][1]+0.5)*pixel_size_y
            ligne1=QgsGeometry.fromMultiPolyline([[QgsPoint(p1,q1),QgsPoint(p2,q2)]])
            f1=QgsFeature()
            f1.setAttributes([bords[pt][0]*s])
            f1.setGeometry(ligne1)
            if p<nx-2:
                if q>-1:
                    if (bords[pt][0]*s, p,q) not in polys:
                        polys[bords[pt][0]*s,p,q]=[]
                    polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())                                
            else:
                if (bords[pt][0]*s, p,q) not in polys:
                    polys[bords[pt][0]*s,p,q]=[]
                polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())                    
    if len(bordd)>0:
        bords=sorted(bordd.items(),key=lambda x:x[1][0])
        for pt in range(len(bords)-1):
            p1=ll[0]+(bords[pt][1][0][0]+0.5)*pixel_size_x
            p2=ll[0]+(bords[pt+1][1][0][0]+0.5)*pixel_size_x
            q1=ll[1]+(bords[pt][1][0][1]+0.5)*pixel_size_y
            q2=ll[1]+(bords[pt+1][1][0][1]+0.5)*pixel_size_y
            ligne1=QgsGeometry.fromMultiPolyline([[QgsPoint(p1,q1),QgsPoint(p2,q2)]])
            f1=QgsFeature()
            f1.setAttributes([bords[pt][0]*s])
            f1.setGeometry(ligne1)
            if q<ny-2:
                if q>-1:
                    if (bords[pt][0]*s, p,q) not in polys:
                        polys[bords[pt][0]*s,p,q]=[]
                    polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())                                
            else:
                if (bords[pt][0]*s,p,q) not in polys:
                    polys[bords[pt][0]*s,p,q]=[]
                polys[bords[pt][0]*s,p,q].append(f1.geometry().asMultiPolyline())





novalue=novalue
layer=processing.getObject(raster)
fichier_resultat=resultat
if not layer==None:
    if layer.type()==QgsMapLayer.RasterLayer:
        provider = layer.dataProvider()
        filePath = str(provider.dataSourceUri())
        raster_or = gdal.Open(filePath)
        nb_bands=layer.bandCount()
        sortie=os.path.splitext(resultat)
        nom_sortie=os.path.basename(sortie[0])
        rep_sortie=os.path.dirname(sortie[0])
        grille = raster_or.GetRasterBand(nb_bands).ReadAsArray()
        grille=numpy.rot90(grille,3)
        champs2=QgsFields()
        champs2.append(QgsField("id",QVariant.Double))
        polys={}
        if polygones==True:
            table_lignes=QgsVectorFileWriter(resultat,"UTF-8",champs2,QGis.WKBMultiPolygon,iface.activeLayer().crs(),"ESRI Shapefile")
        else:
            table_lignes=QgsVectorFileWriter(resultat,"UTF-8",champs2,QGis.WKBMultiLineString,iface.activeLayer().crs(),"ESRI Shapefile")


        fenetre=layer.extent()
        a=fenetre.toString().split(":")
        p1=a[0].split(',')
        p2=a[1].split(',')
        ll=(float(p1[0]),float(p1[1]))
        hauteur=float(p2[1])-float(p1[1])
        largeur=float(p2[0])-float(p1[0])
        nx=int(layer.width())
        ny=int(layer.height())
        pixel_size_x=round(largeur/nx,2)
        pixel_size_y=round(hauteur/ny,2)
        for p in range(nx-1):
            for q in range(ny-1):
                contours(grille,p,q,intervalle)


        conn = db.connect(':memory:')
        c = conn.cursor()
        texte='drop table if exists "'+nom_sortie+'_polys"'
        rs = c.execute(texte)
        conn.commit()
        texte='drop table if exists "'+nom_sortie+'_polys2"'
        rs = c.execute(texte)
        conn.commit()
        texte='drop table if exists "'+nom_sortie+'"'
        rs = c.execute(texte)
        conn.commit()
        texte='drop table if exists "'+nom_sortie+'_2"'
        rs = c.execute(texte)
        conn.commit()
        texte='create table '+nom_sortie+' (id double,p integer,q integer, geom geometry)'
        rs = c.execute(texte)
        conn.commit()
        texte='SELECT RecoverGeometryColumn(\''+nom_sortie+'\',\'geom\','+str(layer.crs().postgisSrid())+', \'MULTILINESTRING\', \'XY\')'
        rs = c.execute(texte)
        conn.commit()



        for k,ff in enumerate(polys):
            li=polys[ff] 
            liste1=[QgsGeometry.fromMultiPolyline(l1) for l1 in li]
            for j,i in enumerate(liste1):
    
                texte='insert into '+nom_sortie +' values('+str(float(ff[0]))+','+str(ff[1])+','+str(ff[2])+',st_geomfromtext(\''+i.exportToWkt()+'\',2154))'
                rs = c.execute(texte)
                conn.commit()
                tlignes=NULL
        db_filename = rep_sortie+"/"+nom_sortie +".sqlite"
    
        if polygones==True:
            texte='create table \"'+nom_sortie+"_polys\" as SELECT id, casttomultipolygon(polygonize("+nom_sortie+'.geom)) AS geom FROM \"'+nom_sortie+'\" GROUP BY id,p,q;'
            rs = c.execute(texte)
            conn.commit()
            texte='create table \"'+nom_sortie+'_polys2" as SELECT id,st_union(geom) AS geom FROM \"'+nom_sortie+'_polys\" GROUP BY id;'
            rs = c.execute(texte)
            conn.commit()
            texte='SELECT RecoverGeometryColumn(\"'+nom_sortie+"_polys2\","+'\'geom\','+str(layer.crs().postgisSrid())+', \'MULTIPOLYGON\', \'XY\')'
            rs = c.execute(texte)
            conn.commit()
        else:
            texte='create table \"'+nom_sortie+"_polys2"+'\" as SELECT "'+nom_sortie+'_2".\'id\' as Id, casttomultilinestring(st_union("'+nom_sortie+'_2".\'GEOMETRY\')) AS Geometry FROM \"'+nom_sortie+'_2\" GROUP BY  "'+nom_sortie+'_2".\'id\' ;'
            rs = c.execute(texte)
            conn.commit()
            texte='SELECT RecoverGeometryColumn(\"'+nom_sortie+"_polys2\","+'\'geom\','+str(layer.crs().postgisSrid())+', \'MULTILINESTRING\', \'XY\')'
            rs = c.execute(texte)
            conn.commit()
        
        texte='select id, asWkt(geom) from '+nom_sortie+"_polys2"
        rs=c.execute(texte)
        resultat2=c.fetchall()
        conn.commit()
        for r in resultat2:
            f1=QgsFeature(champs2)
            geom=QgsGeometry.fromWkt(r[1])
            f1.setGeometry(geom)
            f1.setAttributes([float(r[0])])
            table_lignes.addFeature(f1)
       
        conn.close()
        del c
    
        del conn
        del table_lignes
     


            


