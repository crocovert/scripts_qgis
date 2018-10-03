##CEREMA=group
##source=file
##fichier_musliw=output file

fichiers=source.split(";")
sortie=open(fichier_musliw,"w")
for nom_fichier in fichiers:
    fichier=open(nom_fichier)
    for fiche in fichier:
        sortie.write(fiche)
    fichier.close()
sortie.close()