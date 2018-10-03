
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import codecs

##CEREMA=group
##fichier_temps=file
##variable=string temps
##temps_attente_terminal=boolean
##tc_seul=boolean
##fichier_resultat=output file


fichier=codecs.open(fichier_temps,"r",encoding='utf_8_sig')
res=open(fichier_resultat,"w")
cols={}
links={}

for i,ligne in enumerate(fichier):
    elements=ligne.strip().replace(',','.').split(';')
    if i==0:
        for j,e in enumerate(elements):
            cols[e]=j
#        cols['ij']=len(elements)

        cols['ij']=cols['id']


    else:
        if (tc_seul==True and float(elements[cols['tveh']])>0) or (tc_seul==False):
        #elements.append(elements[cols['o']]+"-"+elements[cols['d']])
            if temps_attente_terminal==True:
                elements[cols['temps']]=float(elements[cols['temps']])-float(elements[cols['tatt1']])
            if elements[cols['ij']] not in links:
                pole=(elements[cols['pole']],1)

                
                links[elements[cols['ij']]]=[elements[cols['ij']],float(elements[cols[variable]]),1.0,float(elements[cols[variable]]),float(elements[cols[variable]]),elements[cols['pole']],elements[cols['pole']],[elements[cols['heureo']]],[elements[cols['heured']]],float(elements[cols[variable]])**2]
            else:
                hd=elements[cols['heureo']]
                if hd not in links[elements[cols['ij']]][7]:
                        links[elements[cols['ij']]][7].append(hd)
                hf=elements[cols['heured']]
                if hf not in links[elements[cols['ij']]][8]:
                        links[elements[cols['ij']]][8].append(hf)
                links[elements[cols['ij']]][1]+=float(elements[cols[variable]])
                links[elements[cols['ij']]][9]+=float(elements[cols[variable]])**2
                links[elements[cols['ij']]][2]+=1
                if float(elements[cols[variable]])<float(links[elements[cols['ij']]][3]):
                    links[elements[cols['ij']]][3]=float(elements[cols[variable]])
                    links[elements[cols['ij']]][5]=elements[cols['pole']]
                if float(elements[cols[variable]])>float(links[elements[cols['ij']]][4]):
                    links[elements[cols['ij']]][4]=float(elements[cols[variable]])
                    links[elements[cols['ij']]][6]=elements[cols['pole']]
            
res.write('id;moy;nb;min;max;pole_min;pole_max;nb_dep;nb_arr;sd\n')
for i in links:
        res.write(str(links[i][0])+";"+str(links[i][1]/links[i][2])+";"+str(links[i][2])+";"+str(links[i][3])+";"+str(links[i][4])+";"+links[i][5]+";"+links[i][6]+";"+str(len(links[i][7]))+";"+str(len(links[i][8]))+";"+str((abs(-((links[i][1]**2)/links[i][2])+links[i][9]))**0.5)+"\n")
res.close()
        
        
            
            
