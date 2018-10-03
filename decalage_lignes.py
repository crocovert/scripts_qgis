
##CEREMA=group
##lignes=vector 
##id_ligne=field lignes
##i=field lignes
##j=field lignes
##variable_quanti=field lignes
##decalage=field lignes

lines=processing.getObject(lignes)
pr=lines.dataProvider()

decalages={}
for i1 in lines.getFeatures():
    id=i1[id_ligne]
    no=i1[i]
    nd=i1[j]
    nb=i1[variable_quanti]
    if (no,nd) not in decalages:
        decalages[(no,nd)]={}
    if id not in decalages[(no,nd)]:
        decalages[(no,nd)][id]=0
    decalages[(no,nd)][id]+=nb

resultat={}
for j1 in decalages:
    tri=sorted(decalages[j1].items(),key=lambda x:x[1],reverse=True)
    res={}
    tot=0
    for j2 in tri:
        res[j2[0]]=tot
        tot+=j2[1]
    resultat[j1]=res

lines.startEditing()
for i1 in lines.getFeatures():
    id=i1[id_ligne]
    no=i1[i]
    nd=i1[j]
    lines.changeAttributeValue(i1.id(), pr.fieldNameMap()[decalage],resultat[(no,nd)][id])
lines.commitChanges()
        
    