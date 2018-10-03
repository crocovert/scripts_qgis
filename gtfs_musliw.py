# coding: utf-8
import codecs
import re
import os
import os.path

##CEREMA=group
##rep_source=folder
##rep_resultat=folder
##prefixe_reseau=optional string
##uic=boolean true
##split_formula=string [-8:]



def importGTFS(rep,sortie,prefixe,uic,formula):
    arrets={}
    stops=codecs.open(rep+"/stops.txt","r",encoding='utf_8_sig')
    iparent=-1
    for i,ligne in enumerate(stops):
        try:
            test=ligne.startswith(codecs.BOM_UTF8)
            if test:
                ligne=ligne[3:]
        except:
            pass
        ligne=(ligne.replace("\n","")).replace("\r","")
        elements= re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",ligne)
        #elements=ligne.strip().split(',')
        for z,e in enumerate(elements):
            elements[z]=e.strip('"')
        if len(elements)>1:
            if i>0:
                if uic==True:
                    elements[iid]=eval("prefixe+elements[iid]"+formula)
                else:
                    elements[iid]=prefixe+elements[iid].strip("\"")
                
                elements[idx]=elements[idx].strip().strip("\"")
                
                if iparent>=0 and elements[iparent] not in ['',None]:
                    elements[iparent]=prefixe+elements[iparent].strip("\"")
                arrets[elements[iid]]=elements
            else:
                for i1,i2 in enumerate(elements):
                    elements[i1]=i2.strip("\"")
                idx=elements.index('stop_lon')
                idy=elements.index('stop_lat')
                iid=elements.index('stop_id')
                iname=elements.index('stop_name')
                if "parent_station" in elements:
                    iparent=elements.index('parent_station')
                if "stop_desc" in elements:
                    idesc=elements.index('stop_desc')
                hstops=ligne
    stops.close()
                     
                     
    lignes={}
    routes=codecs.open(rep+'/routes.txt','r',encoding='utf_8_sig')
    test_agency='ZZ'
    for i,ligne in enumerate(routes):
        try:
            test=ligne.startswith(codecs.BOM_UTF8)
            if test:
                ligne=ligne[3:]
        except:
            pass
        elements=ligne.strip().split(',')

        for z,e in enumerate(elements):
            elements[z]=e.strip('"')
        if len(elements)>1:
            if i>0:
                if test_agency<>'ZZ':
                    elements=elements+[prefixe_reseau]
                l=[elements[iroute],elements[iagency]]
                l.extend(elements[2:])
                lignes[elements[iroute]]=l
            else:
                if ("agency_id") not in elements:
                    test_agency=prefixe_reseau
                    elements=elements+["agency_id"]
                iroute=elements.index("route_id")
                iagency=elements.index("agency_id")
                hroute=[elements[iroute],elements[iagency]]
                hroute.extend(elements[2:])
                hroute=','.join(hroute)+"\n"
    routes.close()
    
    services={}        
    trips=codecs.open(rep+'/trips.txt','r',encoding='utf_8_sig')
    for i,ligne in enumerate(trips):
        try:
            test=ligne.startswith(codecs.BOM_UTF8)
            if test:
                ligne=ligne[3:]
        except:
            pass
        elements=ligne.strip().split(',')
        for i1,i2 in enumerate(elements):
            elements[i1]=i2.strip('"')
        if len(elements)>1:
            if i>0:
                if elements[iroute] in lignes:
                    if len(elements)>6:
                        if elements[6] not in ['',None]:
                            elements[6]=prefixe+elements[6]
                    t=[elements[iroute],elements[iservice],elements[itrip]]
                    t.extend(elements[3:])
                    services[elements[itrip]]=t
            else:
                for z,e in enumerate(elements):
                    elements[z]=e.strip('"')
                iroute=elements.index("route_id")
                itrip=elements.index("trip_id")
                iservice=elements.index("service_id")
                htrip=[elements[iroute],elements[iservice],elements[itrip]]
                htrip.extend(elements[3:])
                htrip=(','.join(htrip))
                htrip=htrip.encode('cp1252')+"\n"
    trips.close()
    
    horaires={}
    stop_times=codecs.open(rep+'/stop_times.txt','r',encoding='utf_8_sig')
    for i,ligne in enumerate(stop_times):
        #ligne=ligne.decode('utf-8')
        try:
            test=ligne.startswith(codecs.BOM_UTF8)
            if test:
                ligne=ligne[3:]
        except:
            pass
        elements=ligne.strip().split(',')
        for z,e in enumerate(elements):
            elements[z]=e.strip('"')
        if len(elements)>1:
            if i>0:
                if elements[itrip] in services:
                    elements[iarr]=elements[iarr].strip('"').zfill(8)
                    elements[idep]=elements[idep].strip('"').zfill(8)
                    if uic==True:
                        elements[istop]=eval("elements[istop]"+formula)
                        o=[elements[itrip],elements[iarr],elements[idep],elements[istop],elements[iseq]]
                    else:
                        o=[elements[itrip],elements[iarr],elements[idep],elements[istop],elements[iseq]]
                o.extend(elements[5:])
                if elements[0] not in horaires:
                    horaires[elements[0]]={}
                if len(elements)>5 and elements[itrip] in htrip:
                    horaires[elements[itrip]][int(elements[iseq])]=[int(elements[iseq]),elements[istop],elements[iarr],elements[idep],elements[5]]
                else:
                    horaires[elements[itrip]][int(elements[iseq])]=[int(elements[iseq]),elements[istop],elements[iarr],elements[idep]]
            else:
                iarr=elements.index("arrival_time")
                idep=elements.index("departure_time")
                itrip=elements.index("trip_id")
                istop=elements.index("stop_id")
                iseq=elements.index("stop_sequence")
                hstop_times=[elements[itrip],elements[iarr],elements[idep],elements[istop],elements[iseq]]
                hstop_times.extend(elements[5:])
                hstop_times=','.join(hstop_times)
    stop_times.close()
    
    
    
    formes={}
    if (os.path.isfile(rep+'/shapes.txt')==True):
        shapes=codecs.open(rep+'/shapes.txt','r',encoding='utf_8_sig')
        shapes2=codecs.open(sortie+'/shapes.txt','w',encoding='utf_8_sig')
        for i,ligne in enumerate(shapes):
            ligne=ligne.decode('utf-8')
            elements=ligne.strip().split(',')
            if len(elements)>1:
                if i>0:
                    elements[0]=prefixe+elements[0]
                shapes2.write(",".join(elements)+"\n")
        shapes.close()
        shapes2.close()

                
                

    calsem={}
    if ("calendar.txt" in os.listdir(rep)):
        cal=codecs.open(rep+'/calendar.txt','r',encoding='utf_8_sig')
        for i,ligne in enumerate(cal):
            try:
                test=ligne.startswith(codecs.BOM_UTF8)
                if test:
                    ligne=ligne[3:]
            except:
                pass
            elements=ligne.strip().split(',')
            for z,e in enumerate(elements):
                elements[z]=e.strip('"')
            if len(elements)>1:
                if i>0:
                    elements[0]=prefixe+elements[0]
                    calsem[elements[0]]=elements
                else:
                    hcalsem=ligne
        cal.close()
    
    caldates={}
    if ("calendar_dates.txt" in os.listdir(rep)):
        cald=codecs.open(rep+'/calendar_dates.txt','r',encoding='utf_8_sig')
        for i,ligne in enumerate(cald):
            try:
                test=ligne.startswith(codecs.BOM_UTF8)
                if test:
                    ligne=ligne[3:]
            except:
                pass
            if ligne not in ['\n',None,'',u'\r\n']:
                elements=ligne.strip().split(',')
                for z,e in enumerate(elements):
                    elements[z]=e.strip('"')
                elements[1]=elements[1].zfill(8)
                if len(elements)>1:
                    if i>0:
                        elements[0]=prefixe+elements[0]
                        caldates[(elements[0],elements[1])]=elements
                    else:
                        hcaldate=ligne
        cald.close()
    
    chainages={}
    for service in services:
        if service in horaires:
            horaires[service]=sorted(horaires[service].values(),key=lambda x:x[0])
            chaine=zip(*(horaires[service]))[1]
            if chaine not in chainages:
                chainages[chaine]=[]
            chainages[chaine].append(service)
    
    if not os.path.isdir(sortie+"/"+prefixe):
        os.mkdir(sortie+"/"+prefixe)
        
    routes2=codecs.open(sortie+"/"+prefixe+'/routes.txt','w',encoding='utf_8_sig')
    #if test_agency<>'ZZ':
    #hroute=",".join(hroute.split(",")[:-1])
    routes2.write(hroute)
    #trips2=open(sortie+'/trips.txt','w')
    trips2=codecs.open(sortie+"/"+prefixe+"/trips.txt","w",encoding='utf_8_sig')
    trips2.write(htrip)
    #stops2=open(sortie+'/stops.txt','w')
    stops2=codecs.open(sortie+"/"+prefixe+"/stops.txt","w",encoding='utf_8_sig')
    stops2.write(hstops+"\n")
    stop_times2=codecs.open(sortie+"/"+prefixe+'/stop_times.txt','w',encoding='utf_8_sig')
    stop_times2.write(hstop_times+"\n")
    if ("calendar.txt" in os.listdir(rep)):
        cal2=codecs.open(sortie+"/"+prefixe+'/calendar.txt','w',encoding='utf_8_sig')
        cal2.write(hcalsem)
    if ("calendar_dates.txt" in os.listdir(rep)):
        cald2=codecs.open(sortie+"/"+prefixe+'/calendar_dates.txt','w',encoding='utf_8_sig')
        cald2.write(hcaldate)

    
    
    for i,chaine in enumerate(chainages):
        s=chainages[chaine][0]
        trip=services[s]
        route=lignes[services[s][0]]
        if test_agency<>'ZZ':
            route=route[:-1]
        routes2.write((prefixe+str(i)+","+",".join(route[1:])+"\n"))
        for j,service in enumerate(chainages[chaine]):
            trip=services[service]
            trips2.write((prefixe+str(i)+","+prefixe+trip[1]+","+prefixe+trip[2]+','+",".join(trip[3:])+"\n"))
            hh=horaires[service]
            for h in hh:
                if len(h)>4:
                    stop_times2.write((prefixe+trip[2]+","+h[2]+","+h[3]+","+prefixe+h[1]+","+str(h[0])+","+h[4]+"\n"))
                else:
                    stop_times2.write((prefixe+trip[2]+","+h[2]+","+h[3]+","+prefixe+h[1]+","+str(h[0])+"\n"))
    routes2.close()
    trips2.close()
    stop_times2.close()
    
    
    for stop in arrets:
        arrets[stop][iname]='"'+arrets[stop][iname]+'"'
        if "stop_desc" in hstops:
             arrets[stop][idesc]='"'+arrets[stop][idesc]+'"'
        stops2.write((",".join(arrets[stop])+"\n"))
    stops2.close()
    
    
    for c in calsem:
        cal2.write((",".join(calsem[c])+"\n"))
    for c in caldates:
        cald2.write((",".join(caldates[c])+"\n"))
    if ("calendar.txt" in os.listdir(rep)):
        cal2.close()
    if ("calendar_dates.txt" in os.listdir(rep)):
        cald2.close()


importGTFS(rep_source,rep_resultat,prefixe_reseau,uic,split_formula)