import os
import gc

##fichier_temps=file
##resultat=string 
##t0=number 30

os.chdir('F:/Etudes/CGET/Reseaux')

nb_horaires=8.0

#fich_temps=open('test.txt')

carres={}
equip={}
cols={}
zones_equip={}
equipements={}
zones={}

with open('carpop.txt') as fich_car:
    for i,car in enumerate(fich_car):
        if i>0:
            e=car.split(';')
            if e[0] not in carres:
                carres[e[0]]={}
            carres[e[0]]['pop']=float(e[1])
fich_car.close()
del(fich_car)


with open(fichier_temps) as fich_temps:
    for i,od in enumerate(fich_temps):
        if i==0:
            e=od.strip('\n').strip('\r').split(";")
            for g,f in enumerate(e):
                cols[f]=g
        else:
            e=od.strip('\n').strip('\r').split(";")
            zone=e[cols['ij']].split('-')[0]
            equip=e[cols['o']]
            if zone not in zones_equip:
                zones_equip[zone]={}
            if  equip not in zones_equip[zone]:
                zones_equip[zone][equip]={}
                zones_equip[zone][equip]['tmin']=float(e[cols['temps']])-float(e[cols['tatt1']])
                zones_equip[zone][equip]['tmax']=float(e[cols['temps']])-float(e[cols['tatt1']])
                zones_equip[zone][equip]['tsum']=float(e[cols['temps']])-float(e[cols['tatt1']])
                zones_equip[zone][equip]['tsum2']=(float(e[cols['temps']])-float(e[cols['tatt1']]))**2
                zones_equip[zone][equip]['tmsum']=1/(float(e[cols['temps']])-float(e[cols['tatt1']]))
                zones_equip[zone][equip]['ncorr']=float(e[cols['ncorr']])
                zones_equip[zone][equip]['n']=1
                zones_equip[zone][equip]['heureo']=set()
                zones_equip[zone][equip]['heured']=set()
                zones_equip[zone][equip]['heureo'].add(float(e[cols['heureo']]))
                zones_equip[zone][equip]['heured'].add(float(e[cols['heured']]))
                zones_equip[zone][equip]['pole']=e[cols['pole']]

               
            else:
                if float(e[cols['temps']])-float(e[cols['tatt1']])<zones_equip[zone][equip]['tmin']:
                    zones_equip[zone][equip]['tmin']=float(e[cols['temps']])-float(e[cols['tatt1']])
                    zones_equip[zone][equip]['pole']=e[cols['pole']]
                if float(e[cols['temps']])-float(e[cols['tatt1']])>zones_equip[zone][equip]['tmax']:
                    zones_equip[zone][equip]['tmax']=float(e[cols['temps']])-float(e[cols['tatt1']])
                zones_equip[zone][equip]['tsum']+=float(e[cols['temps']])-float(e[cols['tatt1']])
                zones_equip[zone][equip]['tsum2']+=(float(e[cols['temps']])-float(e[cols['tatt1']]))**2
                zones_equip[zone][equip]['tmsum']+=1/(float(e[cols['temps']])-float(e[cols['tatt1']]))
                zones_equip[zone][equip]['ncorr']+=float(e[cols['ncorr']])
                zones_equip[zone][equip]['n']+=1
                zones_equip[zone][equip]['heureo'].add(float(e[cols['heureo']]))
                zones_equip[zone][equip]['heured'].add(float(e[cols['heured']]))
fich_temps.close()     
del(fich_temps)
gc.collect()

with open(resultat+"_synthese_zone_equip.txt","w") as fich_zonesequip:
    for  k,v in zones_equip.items():
        for k2,v2 in v.items():
            v2['stdev']=max((((v2['tsum2'])/v2['n'])-(v2['tsum']/v2['n'])**2),0)**0.5
            fich_zonesequip.write(";".join([str(s) for s in [k,k2,v2['tmin'],v2['tsum']/v2['n'],1/(v2['tmsum']/nb_horaires),v2['tmax'],len(v2['heureo']),len(v2['heured']),v2["stdev"],v2['ncorr']/v2['n'],v2['pole']]])+"\n")
fich_zonesequip.close()

for  k,v in zones_equip.items():
    if k in carres:
        for k2,v2 in v.items():
            if k2 not in equipements:
                equipements[k2]={}
                equipements[k2]['nb']=1
                equipements[k2]['pop']=carres[k]['pop']
                equipements[k2]['w_n']=2**(-(((v2['tsum']/v2['n'])/t0)**2))
                equipements[k2]['w_pop']=carres[k]['pop']*(2**(-(((v2['tsum']/v2['n'])/t0)**2)))
                #equipements[k2]['w_n']=1/(v2['tsum']/v2['n'])**2
                #equipements[k2]['w_pop']=carres[k]['pop']/(v2['tsum']/v2['n'])**2
                equipements[k2]['w_pop2']=0
                
            else:
                equipements[k2]['nb']+=1
                equipements[k2]['pop']+=carres[k]['pop']
                equipements[k2]['w_n']+=2**(-((v2['tsum']/v2['n'])/t0)**2)
                equipements[k2]['w_pop']+=carres[k]['pop']*(2**(-((v2['tsum']/v2['n'])/t0)**2))
                

            
for k,v in zones_equip.items():
    if k in carres:
        for k2,v2 in v.items():
            if k not in zones:
                zones[k]={}
                zones[k]['equip']=k2
                zones[k]['pole']=v2['pole']
                zones[k]['nb']=1
                zones[k]['pop']=carres[k]['pop']
                zones[k]['w_n']=(2**(-(((v2['tsum']/v2['n'])/t0)**2)))/equipements[k2]['w_n']
                zones[k]['n_tot']=2**(-(((v2['tsum']/v2['n'])/t0)**2))
                zones[k]['w_pop']=(2**(-(((v2['tsum']/v2['n'])/t0)**2)))/equipements[k2]['w_pop']
                zones[k]['tmoy']=(v2['tsum']/v2['n'])
                zones[k]['th']=1/(v2['tmsum']/nb_horaires)
                zones[k]['stdev']=v2['stdev']
                zones[k]['ncorr']=v2['ncorr']/v2['n']
                zones[k]['nb_dep']=len(v2['heureo'])
                zones[k]['nb_arr']=len(v2['heured'])

                
            else:
                zones[k]['nb']+=1
                zones[k]['w_n']+=(2**(-(((v2['tsum']/v2['n'])/t0)**2)))/equipements[k2]['w_n']
                zones[k]['w_pop']+=(2**(-(((v2['tsum']/v2['n'])/t0)**2)))/equipements[k2]['w_pop']
                zones[k]['n_tot']+=2**(-(((v2['tsum']/v2['n'])/t0)**2))
                if (v2['tsum']/v2['n'])<zones[k]['tmoy']:
                    zones[k]['equip']=k2
                    zones[k]['pole']=v2['pole']
                    zones[k]['tmoy']=(v2['tsum']/v2['n'])
                    zones[k]['th']=1/(v2['tmsum']/nb_horaires)
                    zones[k]['stdev']=v2['stdev']
                    zones[k]['ncorr']=v2['ncorr']/v2['n']
                    zones[k]['nb_dep']=len(v2['heureo'])
                    zones[k]['nb_arr']=len(v2['heured'])

for  k,v in zones_equip.items():
    if k in carres:
        for k2,v2 in v.items():
            equipements[k2]['w_pop2']+=carres[k]['pop']*((2**(-((v2['tsum']/v2['n'])/t0)**2))/zones[k]['n_tot'])


del(zones_equip)

fich_zones=open("synthese_"+resultat+"_zones.txt","w")
for k,i in enumerate(zones.items()):
    if k==0:
        fich_zones.write("zone;"+";".join([str(l) for l in i[1]])+"\n")
    fich_zones.write(i[0]+";"+";".join([str(l) for l in i[1].values()])+"\n")
fich_zones.close()



fich_equip=open("synthese_"+resultat+"_equip.txt","w")
for k,i in enumerate(equipements.items()):
    if k==0:
        fich_equip.write("equip;"+";".join([str(l) for l in i[1]])+"\n")
    fich_equip.write(i[0]+";"+";".join([str(k) for k in i[1].values()])+"\n")
fich_equip.close()
            

del(zones)
del(carres)
del(equip)
del(cols)
del(equipements)

    
    