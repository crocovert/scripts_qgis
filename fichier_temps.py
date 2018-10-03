
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import codecs 

##CEREMA=group
##fichier_temps=file
##variable=string temps
##temps_attente_terminal=boolean
##fichier_resultat=output file


fichier=codecs.open(fichier_temps,"r",encoding="utf8")
res=codecs.open(fichier_resultat,"w",encoding='utf8')
cols={}
links={}

for i,ligne in enumerate(fichier):
    elements=ligne.strip().replace(',','.').split(';')
    if i==0:
        for j,e in enumerate(elements):
            cols[e]=j
    else:
        elements[cols[variable]]=elements[cols[variable]].replace(',','.')
        if temps_attente_terminal==True and 'tatt1' in cols:
            elements[cols[variable]]=float(elements[cols[variable]])-float(elements[cols['tatt1']])
        if elements[cols['ij']] not in links:
            pole=(elements[cols['pole']],1)

            
            links[elements[cols['ij']]]=[elements[cols['ij']],float(elements[cols[variable]]),1.0,float(elements[cols[variable]]),float(elements[cols[variable]]),elements[cols['pole']],elements[cols['pole']],[elements[cols['heureo']]],[elements[cols['heured']]],float(elements[cols[variable]])**2,elements[cols['o']],elements[cols['o']]]
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
                links[elements[cols['ij']]][10]=elements[cols['o']]
            if float(elements[cols[variable]])>float(links[elements[cols['ij']]][4]):
                links[elements[cols['ij']]][4]=float(elements[cols[variable]])
                links[elements[cols['ij']]][6]=elements[cols['pole']]
                links[elements[cols['ij']]][11]=elements[cols['o']]            
res.write('ij;moy;nb;min;max;pole_min;pole_max;nb_dep;nb_arr;sd;o_min;o_max\n')
for i in links:
        try:
            res.write(links[i][0].decode('utf8')+";"+unicode(links[i][1]/links[i][2])+";"+unicode(links[i][2])+";"+unicode(links[i][3])+";"+unicode(links[i][4])+";"+links[i][5].decode('utf8')+";"+links[i][6].decode('utf8')+";"+unicode(len(links[i][7]))+";"+unicode(len(links[i][8]))+";"+unicode((abs(-((links[i][1]**2)/links[i][2])+links[i][9]))**0.5)+";"+links[i][10].decode('utf8')+";"+links[i][11].decode('utf8')+"\n")
        except:
            progress.setText('élément ignoré')
res.close()
        
        
            
            
