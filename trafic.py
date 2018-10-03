from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from qgis.analysis import *
import math
from pyspatialite import dbapi2 as db

##CEREMA=group
##lignes=vector line
##trafic=field lignes
##echelle=number 0.1
##angle_max=number 90.0
##dist_min=number 50.0
##double_sens=boolean True
##tampons=output vector

def traf(geometry,spatial,lignes,echelle=echelle,angle_max=angle_max,dist_min=dist_min,double_sens=double_sens):
    conn = db.connect(':memory:')
    c = conn.cursor()
    t=geometry[trafic]
    buf=geometry.geometry().buffer(echelle*t*1.0,25,1,1,10)
    buf_poly=buf
    proj=str(lines.crs().postgisSrid())
    buf=buf.convertToType(QGis.Line,False)
    
    buf_sav=buf
    buf_l=buf.length()
    l2=QgsLineStringV2()
    l2.fromWkt(geometry.geometry().exportToWkt())
    pt1=QgsGeometry(l2.startPoint())
    pt2=QgsGeometry(l2.endPoint())
    ###point debut
    debut=spatial.intersects(QgsGeometry.buffer(pt1,10,3).boundingBox())
    fe= [f for f in debut]

    feats=[]
    for f in fe:
        ff=QgsLineStringV2()

        ff.fromWkt(l[f].geometry().exportToWkt())
        #print(pt1.distance(QgsGeometry(ff.startPoint())))
        if pt1.distance(QgsGeometry(ff.startPoint()))<10:
            if l[f] not in feats:
                feats.append(f)
        elif pt1.distance(QgsGeometry(ff.endPoint()))<10:
            if l[f] not in feats:
                feats.append(f)


            
        
    distances={}
    angles={}
    for i in feats:
        longueur=lignes[i].geometry().length()
        if not(geometry.id()==i):
            distances[i]=lignes[i].geometry().lineLocatePoint(pt1)
            if distances[i]<dist_min:
                angles[i]=((lignes[i].geometry().interpolateAngle(min(dist_min,longueur))*180/math.pi)+180)%360
            else:
                angles[i]=lignes[i].geometry().interpolateAngle(longueur-min(dist_min,longueur))*180/math.pi
        else:
            angle1=lignes[i].geometry().interpolateAngle(min(dist_min,longueur))*180/math.pi
    angle_maxi=1e38
    voisin=None
    angle_voisin=None
    angle2=None
    if len(distances)==0:
        angle=(angle1)%360
        angle2=angle1
        angle_voisin=angle2
    for i in distances:
        if distances[i]<dist_min:
            angle=(angles[i])%360
            min_angle=min(abs((angle+180)%360-(angle1+180)%360),abs(angle-angle1))
            if min_angle<angle_maxi:
                angle_maxi=min_angle
                angle_voisin=angle
                voisin=i
        else:
            angle=angles[i]
            min_angle=min(abs((angle+180)%360-(angle1+180)%360),abs(angle-angle1))
            if min_angle<angle_maxi:
                angle_maxi=min_angle
                angle_voisin=angle
                voisin=i

    if  min(abs((angle_voisin+180)%360-(angle1+180)%360),abs(angle_voisin-angle1))<angle_max:
        if abs((angle_voisin+180)%360-(angle1+180)%360)<abs(angle_voisin-angle1):
            angle2=(0.5*(((angle_voisin+180)%360+(angle1+180)%360))+180)%360
        else:
            angle2=0.5*(angle_voisin+angle1)
    else:
        angle2=angle1

    if angle2==None:
        angle2=(angle1)%360
    
    start_line=QgsGeometry.fromPolyline([QgsPoint(pt1.asPoint().x()-40*echelle*t*math.cos((180-angle2)*math.pi/180),pt1.asPoint().y()-40*echelle*t*math.sin((180-angle2)*math.pi/180)),QgsPoint(pt1.asPoint().x(),pt1.asPoint().y())])
    int1=buf.intersection(start_line)
    start_line2=QgsGeometry.fromPolyline([QgsPoint(pt1.asPoint().x()+40*echelle*t*math.cos((180-angle2)*math.pi/180),pt1.asPoint().y()+40*echelle*t*math.sin((180-angle2)*math.pi/180)),QgsPoint(pt1.asPoint().x(),pt1.asPoint().y())])
    int3=buf.intersection(start_line2)
    if int1.isMultipart():
        points=int1.asMultiPoint()
        dmax=1e38
        for p in points:
            d=pt1.distance(QgsGeometry.fromPoint(p))
            if d<dmax:
                dmax=d
                pmax=p
        int1=QgsGeometry.fromPoint(pmax)
    if int3.isMultipart():
        points=int3.asMultiPoint()
        dmax=1e38
        for p in points:
            d=pt1.distance(QgsGeometry.fromPoint(p))
            if d<dmax:
                dmax=d
                pmax=p
        int3=QgsGeometry.fromPoint(pmax)

    

    ###point fin

        
    debut=spatial.intersects(QgsGeometry.buffer(pt2,10,3).boundingBox())
    fe= [f for f in debut]
    for f in fe:
        ff=QgsLineStringV2()
        ff.fromWkt(l[f].geometry().exportToWkt())
        if pt2.distance(QgsGeometry(ff.startPoint()))<10:
            if l[f] not in feats:
                feats.append(f)
        elif pt2.distance(QgsGeometry(ff.endPoint()))<10:
            if l[f] not in feats:
                feats.append(f)
    distances={}
    angles={}
    for i in feats:
        longueur=lignes[i].geometry().length()
        if not(geometry.id()==i):
            distances[i]=lignes[i].geometry().lineLocatePoint(pt2)
            if distances[i]<dist_min:
                angles[i]=(lignes[i].geometry().interpolateAngle(min(dist_min,longueur))*180/math.pi)%360
            else:
                angles[i]=(((lignes[i].geometry().interpolateAngle(longueur-min(dist_min,longueur))*180)/math.pi)+180)%360
        else:
             angle1=((lignes[i].geometry().interpolateAngle(longueur-min(dist_min,longueur))*180/math.pi))
    angle_maxi=1e38
    voisin=None
    angle_voisin=None
    angle2=None
    if len(distances)==0:
        angle=(angle1)%360
        angle2=angle1
        angle_voisin=angle2
    for i in distances:
        if distances[i]<dist_min:
            angle=(angles[i])
            min_angle=min(abs((angle+180)%360-(angle1+180)%360),abs(angle-angle1))
            if min_angle<angle_maxi:
                angle_maxi=min_angle
                angle_voisin=angle
                voisin=i
        else:
            angle=(angles[i])
            min_angle=min(abs((angle+180)%360-(angle1+180)%360),abs(angle-angle1))
            if min_angle<angle_maxi:
                angle_maxi=min_angle
                angle_voisin=angle
                voisin=i

    if  min(abs((angle_voisin+180)%360-(angle1+180)%360),abs(angle_voisin-angle1))<angle_max:
        if abs((angle_voisin+180)%360-(angle1+180)%360)<abs(angle_voisin-angle1):
            angle2=(0.5*(((angle_voisin+180)%360+(angle1+180)%360))+180)%360
        else:
            angle2=0.5*(angle_voisin+angle1)
    else:
        angle2=angle1
    if angle2==None:
        angle2=(angle1)%360


    end_line=QgsGeometry.fromPolyline([QgsPoint(pt2.asPoint().x()-40*echelle*t*math.cos((180-angle2)*math.pi/180),pt2.asPoint().y()-40*echelle*t*math.sin((180-angle2)*math.pi/180)),QgsPoint(pt2.asPoint().x(),pt2.asPoint().y())])
    int2=buf.intersection(end_line)
    end_line2=QgsGeometry.fromPolyline([QgsPoint(pt2.asPoint().x()+40*echelle*t*math.cos((180-angle2)*math.pi/180),pt2.asPoint().y()+40*echelle*t*math.sin((180-angle2)*math.pi/180)),QgsPoint(pt2.asPoint().x(),pt2.asPoint().y())])
    int4=buf.intersection(end_line2)
    
    int5=start_line.intersection(end_line)
    int6=start_line2.intersection(end_line2)
    m5=-1
    m6=-1
    
    if int5.type()==0:
        if int5.within(buf_poly):
            m5=1
    if int6.type()==0:
        if int6.within(buf_poly):
            m6=1
    
    if int2.isMultipart():
        points=int2.asMultiPoint()
        dmax=1e38
        for p in points:
            d=pt2.distance(QgsGeometry.fromPoint(p))
            if d<dmax:
                dmax=d
                pmax=p
        int2=QgsGeometry.fromPoint(pmax)
    if int4.isMultipart():
        points=int4.asMultiPoint()
        dmax=1e38
        for p in points:
            d=pt2.distance(QgsGeometry.fromPoint(p))
            if d<dmax:
                dmax=d
                pmax=p
        int4=QgsGeometry.fromPoint(pmax)


    #print(int1.exportToWkt(),int2.exportToWkt(),int3.exportToWkt(),int4.exportToWkt())
    
    texte="select astext(st_snap(st_geomfromtext('"+buf.exportToWkt()+"',"+proj+"),st_geomfromtext('"+int1.exportToWkt()+"',"+proj+"),1))"
    rs = c.execute(texte)
    resultat=c.fetchall()
    conn.commit()
    buf= resultat[0][0]
    texte="select astext(st_snap(st_geomfromtext('"+buf+"',"+proj+"),st_geomfromtext('"+int2.exportToWkt()+"',"+proj+"),1))"
    rs = c.execute(texte)
    resultat=c.fetchall()
    conn.commit()
    buf= resultat[0][0]
    texte="select astext(st_snap(st_geomfromtext('"+buf+"',"+proj+"),st_geomfromtext('"+int3.exportToWkt()+"',"+proj+"),1))"
    rs = c.execute(texte)
    resultat=c.fetchall()
    conn.commit()
    buf= resultat[0][0]
    texte="select astext(st_snap(st_geomfromtext('"+buf+"',"+proj+"),st_geomfromtext('"+int4.exportToWkt()+"',"+proj+"),1))"
    rs = c.execute(texte)
    resultat=c.fetchall()
    conn.commit()
    buf= QgsGeometry.fromWkt(resultat[0][0])

    m1=buf.lineLocatePoint(int1)        
    m2=buf.lineLocatePoint(int2)
    m3=buf.lineLocatePoint(int3)        
    m4=buf.lineLocatePoint(int4)

#creation epaisseur

    buf_l=buf.length()
    m1=m1/buf_l
    m2=m2/buf_l
    m3=m3/buf_l
    m4=m4/buf_l


    if m2<m1:
        texte="select asText(st_line_substring(st_geomfromtext('"+buf.exportToWkt()+"',"+proj+")"+','+str(m2)+','+str(m1)+"))"

        rs = c.execute(texte)
        resultat=c.fetchall()
        conn.commit()
        buf1= QgsGeometry.fromWkt(resultat[0][0])


    else:
        texte="select astext(st_union(st_snap(st_line_substring(geomfromtext('"+buf.exportToWkt()+"',"+proj+"),0,"+str(m1)+"),st_line_substring(geomfromtext('"+buf.exportToWkt()+"',"+proj+"),"+str(m3)+",1),1),st_line_substring(geomfromtext('"+buf.exportToWkt()+"',"+proj+"),"+str(m2)+",1)))"
        rs = c.execute(texte)
        resultat=c.fetchall()
        conn.commit()
        buf1= QgsGeometry.fromWkt(resultat[0][0])
        
    if m3<m4:
        texte="select asText(st_line_substring(st_geomfromtext('"+buf.exportToWkt()+"',"+proj+")"+','+str(m3)+','+str(m4)+"))"
        rs = c.execute(texte)
        resultat=c.fetchall()
        conn.commit()
        buf2= QgsGeometry.fromWkt(resultat[0][0])


    else:

        texte="select astext(st_union(g)) from (select st_line_substring(st_geomfromtext('"+buf.exportToWkt()+"',"+proj+"),0,"+str(m4)+") as \"g\" union all select st_line_substring(st_geomfromtext('"+buf.exportToWkt()+"',"+proj+"),"+str(m3)+",1) as \"g\" )"
        rs = c.execute(texte)
        resultat=c.fetchall()
        conn.commit()
        buf2= QgsGeometry.fromWkt(resultat[0][0])
        texte="select astext(st_union(st_snap(st_line_substring(geomfromtext('"+buf.exportToWkt()+"',"+proj+"),0,"+str(m4)+"),st_line_substring(geomfromtext('"+buf.exportToWkt()+"',"+proj+"),"+str(m3)+",1),1),st_line_substring(geomfromtext('"+buf.exportToWkt()+"',"+proj+"),"+str(m3)+",1)))"

        rs = c.execute(texte)
        resultat=c.fetchall()
        conn.commit()
        buf2= QgsGeometry.fromWkt(resultat[0][0])

    


    


    
    g1=buf
    g2=buf.shortestLine(int1)
    g2=g2.combine(g1)
    g3=buf.shortestLine(int2)
    g3=g3.combine(g2)
    g3=g3.combine(pt1.shortestLine(int1))
    g3=g3.combine(pt2.shortestLine(int2))
    g3=g3.combine(pt1.shortestLine(geometry.geometry()))
    g3=g3.combine(pt2.shortestLine(geometry.geometry()))
    g3=g3.combine(geometry.geometry())
    buf3=buf1.exportToWkt()
    buf4=buf2.exportToWkt()
    if double_sens==False:
        if m5>0:
            texte="select astext(st_union(st_snap(geomfromtext('"+geometry.geometry().exportToWkt()+"',"+proj+"),geomfromtext('"+pt1.shortestLine(int5).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(int5).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(int5).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt2.shortestLine(int5).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]        
        else:
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf1.shortestLine(int1).exportToWkt()+"',"+proj+"),1),geomfromtext('"+buf1.shortestLine(int1).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf1.shortestLine(int2).exportToWkt()+"',"+proj+"),1),geomfromtext('"+buf1.shortestLine(int2).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt1.shortestLine(int1).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(int1).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(int2).exportToWkt()+"'),1),geomfromtext('"+pt2.shortestLine(int2).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt1.shortestLine(geometry.geometry()).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(geometry.geometry()).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]    
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(geometry.geometry()).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt2.shortestLine(geometry.geometry()).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+geometry.geometry().exportToWkt()+"',"+proj+"),1),geomfromtext('"+geometry.geometry().exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
        
        
    else:

        if m5>0:
            texte="select astext(st_union(st_snap(geomfromtext('"+buf4+"',"+proj+"),geomfromtext('"+pt1.shortestLine(int3).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(int3).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(int4).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt2.shortestLine(int4).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt1.shortestLine(int5).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(int5).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(int5).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt2.shortestLine(int5).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]    

        elif m6>0:
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt1.shortestLine(int1).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(int1).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(int2).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt2.shortestLine(int2).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt1.shortestLine(int6).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt1.shortestLine(int6).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+pt2.shortestLine(int6).exportToWkt()+"',"+proj+"),1),geomfromtext('"+pt2.shortestLine(int6).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]        

        else:
            
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf1.shortestLine(int1).exportToWkt()+"',"+proj+"),1),geomfromtext('"+buf1.shortestLine(int1).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
                
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf1.shortestLine(int2).exportToWkt()+"',"+proj+"),1),geomfromtext('"+buf1.shortestLine(int2).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+int3.shortestLine(int1).exportToWkt()+"',"+proj+"),1),geomfromtext('"+int3.shortestLine(int1).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+int4.shortestLine(int2).exportToWkt()+"',"+proj+"),1),geomfromtext('"+int4.shortestLine(int2).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf2.shortestLine(int3).exportToWkt()+"',"+proj+"),1),geomfromtext('"+buf2.shortestLine(int3).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]    
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf2.shortestLine(int4).exportToWkt()+"',"+proj+"),1),geomfromtext('"+buf2.shortestLine(int4).exportToWkt()+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]
            texte="select astext(st_union(st_snap(geomfromtext('"+buf3+"',"+proj+"),geomfromtext('"+buf4+"',"+proj+"),1),geomfromtext('"+buf4+"',"+proj+")))"
            rs = c.execute(texte)
            resultat=c.fetchall()
            conn.commit()
            buf3= resultat[0][0]

    texte="select astext(st_buildarea(st_union(g))) from  ((select geomfromtext('"+buf3+"',"+proj+") as \"g\"))"
    rs = c.execute(texte)
    resultat=c.fetchall()
    conn.commit()

    buf=QgsGeometry.fromWkt(resultat[0][0])

    return(buf)

lines=processing.getObject(lignes)
id=QgsSpatialIndex(lines.getFeatures())
l=[i for i in lines.getFeatures()]
champs=lines.dataProvider().fields()
table_tampons=QgsVectorFileWriter(tampons,"UTF-8",champs,QGis.WKBMultiPolygon,lines.crs(),"ESRI Shapefile")
#table_tampons=QgsVectorFileWriter(tampons,"UTF-8",champs,QGis.WKBMultiLineString,lines.crs(),"ESRI Shapefile")
for f in lines.getFeatures():
    try:
        f.setGeometry(traf(f,id,l,echelle,angle_max,dist_min,double_sens))

        table_tampons.addFeature(f)
    except:
        print(f.geometry().exportToWkt())
del table_tampons
    
    
    