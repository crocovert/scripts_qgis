import os

##fichier_temps_TC=file
##fichier_temps_VP=file
##resultat=string 
##t_tc=number 30
##t_vp=number 15

t0=t_tc
t1=t_vp

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


fichiers=[(fichier_temps_TC,'tc'),(fichier_temps_VP,'vp')]

'lit fichier temps TC'
for fich in fichiers:
    with open(fich[0]) as fich_temps:
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
                if fich[1] not in zones_equip[zone][equip]:
                    zones_equip[zone][equip][fich[1]]={}
                    zones_equip[zone][equip][fich[1]]['tmin']=float(e[cols['temps']])-float(e[cols['tatt1']])
                    zones_equip[zone][equip][fich[1]]['tmax']=float(e[cols['temps']])-float(e[cols['tatt1']])
                    zones_equip[zone][equip][fich[1]]['tsum']=float(e[cols['temps']])-float(e[cols['tatt1']])
                    zones_equip[zone][equip][fich[1]]['tsum2']=(float(e[cols['temps']])-float(e[cols['tatt1']]))**2
                    zones_equip[zone][equip][fich[1]]['tmsum']=1/(float(e[cols['temps']])-float(e[cols['tatt1']]))
                    zones_equip[zone][equip][fich[1]]['ncorr']=float(e[cols['ncorr']])
                    zones_equip[zone][equip][fich[1]]['n']=1
                    zones_equip[zone][equip][fich[1]]['heureo']=set()
                    zones_equip[zone][equip][fich[1]]['heured']=set()
                    zones_equip[zone][equip][fich[1]]['heureo'].add(float(e[cols['heureo']]))
                    zones_equip[zone][equip][fich[1]]['heured'].add(float(e[cols['heured']]))
                    zones_equip[zone][equip][fich[1]]['pole']=e[cols['pole']]

                   
                else:
                    if float(e[cols['temps']])-float(e[cols['tatt1']])<zones_equip[zone][equip][fich[1]]['tmin']:
                        zones_equip[zone][equip][fich[1]]['tmin']=float(e[cols['temps']])-float(e[cols['tatt1']])
                        zones_equip[zone][equip][fich[1]]['pole']=e[cols['pole']]
                    if float(e[cols['temps']])-float(e[cols['tatt1']])>zones_equip[zone][equip][fich[1]]['tmax']:
                        zones_equip[zone][equip][fich[1]]['tmax']=float(e[cols['temps']])-float(e[cols['tatt1']])
                    zones_equip[zone][equip][fich[1]]['tsum']+=float(e[cols['temps']])-float(e[cols['tatt1']])
                    zones_equip[zone][equip][fich[1]]['tsum2']+=(float(e[cols['temps']])-float(e[cols['tatt1']]))**2
                    zones_equip[zone][equip][fich[1]]['tmsum']+=1/(float(e[cols['temps']])-float(e[cols['tatt1']]))
                    zones_equip[zone][equip][fich[1]]['ncorr']+=float(e[cols['ncorr']])
                    zones_equip[zone][equip][fich[1]]['n']+=1
                    zones_equip[zone][equip][fich[1]]['heureo'].add(float(e[cols['heureo']]))
                    zones_equip[zone][equip][fich[1]]['heured'].add(float(e[cols['heured']]))

            


"""with open(resultat+"_synthese_zone_equip.txt","w") as fich_zonesequip:
    for  k,v in zones_equip.items():
        for k2,v2 in v.items():
            v2['stdev']=max((((v2['tsum2'])/v2['n'])-(v2['tsum']/v2['n'])**2),0)**0.5
            fich_zonesequip.write(";".join([str(s) for s in [k,k2,v2['tmin'],v2['tsum']/v2['n'],1/(v2['tmsum']/nb_horaires),v2['tmax'],len(v2['heureo']),len(v2['heured']),v2["stdev"],v2['ncorr']/v2['n'],v2['pole']]])+"\n")"""


for  k,v in zones_equip.items():
    if k in carres:
        for k2,v2 in v.items():
            if k2 not in equipements:
                equipements[k2]={}
                if 'tc'not in equipements[k2]:
                    if 'tc' in v2:
                        equipements[k2]['tc']={}
                        equipements[k2]['tc']['nb']=1
                        equipements[k2]['tc']['pop']=carres[k]['pop']-carres[k]['pvp']
                        equipements[k2]['tc']['w_n']=2**(-(((v2['tc']['tsum']/v2['tc']['n'])/t0)**2))
                        equipements[k2]['tc']['w_pop']=carres[k]['pop']*(2**(-(((v2['tc']['tsum']/v2['tc']['n'])/t0)**2)))
                        equipements[k2]['tc']['w_pop2']=0
                else:
                    if 'tc' in v2:
                        equipements[k2]['tc']['nb']+=1
                        equipements[k2]['tc']['pop']+=carres[k]['pop']-carres[k]['pvp']
                        equipements[k2]['tc']['w_n']+=2**(-((v2['tc']['tsum']/v2['tc']['n'])/t0)**2)
                        equipements[k2]['tc']['w_pop']+=(carres[k]['pop']-carres[k]['pvp'])*(2**(-((v2['tc']['tsum']/v2['tc']['n'])/t0)**2))

                if 'vp'not in equipements[k2]:
                    if 'vp' in v2:
                        equipements[k2]['vp']={}
                        equipements[k2]['vp']['nb']=1
                        equipements[k2]['vp']['pop']=carres[k]['pvp']
                        equipements[k2]['vp']['w_n']=2**(-(((v2['vp']['tsum']/v2['vp']['n'])/t1)**2))
                        equipements[k2]['vp']['w_pop']=carres[k]['vp']*(2**(-(((v2['vp']['tsum']/v2['vp']['n'])/t1)**2)))
                        equipements[k2]['vp']['w_pop2']=0
                else:
                    if 'vp' in v2:
                        equipements[k2]['tc']['nb']+=1
                        equipements[k2]['tc']['pop']+=carres[k]['pvp']
                        equipements[k2]['tc']['w_n']+=2**(-((v2['vp']['tsum']/v2['vp']['n'])/t1)**2)
                        equipements[k2]['tc']['w_pop']+=carres[k]['pvp']*(2**(-((v2['vp']['tsum']/v2['vp']['n'])/t1)**2))
                
print('ok1')
            
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

    
    