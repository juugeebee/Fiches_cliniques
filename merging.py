# Author: Julie BOGOIN

import pandas
import numpy
import os


print('\n**********************')
print('**** CONCATING BM ****')
print('**********************\n')


# Fichiers
fc = 'sortie/fc_dft_sorted.txt'
bm = 'sortie/bm_concat.txt'
bm_final = 'sortie/bm_final.txt'
sortie = 'fc_bm_dft.txt'

if os.path.exists('fc_bm_dft.txt'):
    os.remove('fc_bm_dft.txt')
    print('Precedent fichier de sortie supprime.\n')

if os.path.exists("sortie/bm_concat.txt"):
    os.remove("sortie/bm_concat.txt")
    print('Precedent fichier concat supprime.\n')

if os.path.exists("sortie/bm_final.txt"):
    os.remove("sortie/bm_final.txt")
    print('Precedent fichier bm_final supprime.\n')


# Concatener tous les fichiers de sortie BM

comparaison = 0
fichier = 0

files = os.listdir("sortie")

with open("sortie/bm_concat.txt", "w") as new_file:

    new_file.write('RECEPTION\tAPPROBATION\tNC\tPATIENT\tDDN\tSEXE\t\
        FAMILLE\tDEMANDE\tINDICATIONS\tACTION\tREACTIFS\tGENE_RESULTAT\t\
        ABM_NEURO\tPATHOLOGIE\tTITRE\tPRESCRIPTEUR\tORIGINE\tSERVICE\n')

    compteur = 0

    for filename in files:

        if filename != 'fc_dft_sorted.txt':

            fichier = fichier + 1

            with open("sortie/" + filename) as f:
                
                for line in f:
                    text=f.readlines()
                    comparaison = comparaison + (len(text)-1)

            with open("sortie/" + filename) as f:

                for line in f:
                    
                    if not line.startswith('RECEPTION'):
                        new_file.write(line)
                        compteur = compteur + 1

                new_file.write("\n")


print('Nombre de fichiers BM : {}.'.format(fichier))
print('Nombre de lignes dans les fichiers : {}.'.format(comparaison))
print('Nombre de lignes concatenees : {}.'.format(compteur))


print('\n*****************')
print('**** MERGING ****')
print('*****************\n')


### FICHES CLINIQUES
df_fc = pandas.read_csv(fc, encoding='utf-8', sep="\t", header=[0])
print('Nombre de lignes Fiches Cliniques : {}.'.format(len(df_fc)))


### BM 
### UNE SEULE LIGNE PAR PATIENT
df_bm = pandas.read_csv(bm, sep="\t", header=[0])

### Supprimer les espaces en debut de noms de patients
df_bm['PATIENT'] = df_bm['PATIENT'].str.strip(to_strip = None)

### REMPLACER LES NA PAR DES - ET SUPPRIMER LES DOUBLONS
df_bm = df_bm.fillna('-')
df_bm.drop_duplicates(keep = 'first', inplace=True)

### Supprimer les lignes où le patient est vide ou -

# Get names of indexes for which column Stock has value No
indexNames = df_bm[ df_bm['PATIENT'] == '' ].index
# Delete these row indexes from dataFrame
df_bm.drop(indexNames , inplace=True)

indexNames = df_bm[ df_bm['PATIENT'] == '-' ].index
df_bm.drop(indexNames , inplace=True)


### TRIER LES LIGNES PAR PATIENTS
df_bm.sort_values(by=['DDN'], inplace=True)
df_bm.sort_values(by=['PATIENT'], inplace=True)
df_bm.reset_index(inplace=True)


print('\nNombre de lignes BM depart = {}.'.format(len(df_bm)))


### RECUPER LES INDEX DES DOUBLONS
dup = df_bm['PATIENT'].duplicated()

index_list = []

for i,e in enumerate(dup):
    if e is True:
        index_list.append(i)

index_list_doub = []

if len(index_list) != 0: 

    for i in range(len(index_list)-1):
        
        if (index_list[i] + 1 == index_list[i+1]) and\
            (index_list[i] - 1 not in index_list_doub):
            
            index_list_doub.append(index_list[i] - 1)
            index_list_doub.append(index_list[i])
        
        else : 
            
            if (index_list[i] + 1 != index_list[i+1]) and\
            (index_list[i] - 1 != index_list[i-1]):

                index_list_doub.append(index_list[i] - 1)
                index_list_doub.append(index_list[i])

            else :

                index_list_doub.append(index_list[i])

    if index_list[-1] - 1 not in index_list_doub :
        index_list_doub.append(index_list[-1] - 1)

    index_list_doub.append(index_list[-1])


### COPIER LES LIGNES UNIQUES DANS LE FICHIER DE SORTIE

# CREATION FICHIER SORTIE
fichier = open(bm_final, "a")

fichier.write("RECEPTION\tAPPROBATION\tNC\tPATIENT\tDDN\tSEXE\tFAMILLE\t\
       DEMANDE\tINDICATIONS\tACTION\tREACTIFS\t\
       GENE_RESULTAT\tABM_NEURO\tPATHOLOGIE\tTITRE\tPRESCRIPTEUR\tORIGINE\t\
       SERVICE\n")


### PARCOURS FICHIER INITAL

# COPIE DES LIGNES SOLO

comptage_solo = 0

for i in range(len(df_bm)):

    if i not in index_list_doub:

        fichier.write(df_bm['RECEPTION'][i]+'\t'+\
        df_bm['APPROBATION'][i]+'\t'+\
        df_bm['NC'][i]+'\t'+df_bm['PATIENT'][i]+'\t'+\
        df_bm['DDN'][i]+'\t'+df_bm['SEXE'][i]+'\t'+\
        df_bm['        FAMILLE'][i]+'\t'+df_bm['DEMANDE'][i]+'\t'+\
        df_bm['INDICATIONS'][i]+'\t'+df_bm['ACTION'][i]+'\t'+\
        df_bm['REACTIFS'][i]+'\t'+\
        df_bm['GENE_RESULTAT'][i]+'\t'+df_bm['        ABM_NEURO'][i]+'\t'+\
        df_bm['PATHOLOGIE'][i]+'\t'+df_bm['TITRE'][i]+'\t'+\
        df_bm['PRESCRIPTEUR'][i]+'\t'+\
        df_bm['ORIGINE'][i]+'\n')   

        comptage_solo = comptage_solo + 1    


print('Nombre de lignes solo = {}.'.format(comptage_solo))
print('Nombre de doublons = {}.'.format(len(index_list_doub)))


start_list = []
stop_list = []

for i in index_list_doub:

    if i != index_list_doub[-1]:

        if (df_bm['PATIENT'][i] != df_bm['PATIENT'][i+1]):
            stop_list.append(i)

        else :
            
            if (df_bm['PATIENT'][i] != df_bm['PATIENT'][i-1]):
                start_list.append(i)

nombre = 0

for h in range(len(start_list)-1) : 

    for i in range(start_list[h], stop_list[h],1):            

        if i in start_list:
            ligne_list = []
            reception = []
            approbation = []
            nc = []
            patient = []
            ddn = []
            sexe = []
            famille = []
            demande = []
            indications = []
            action = []
            reactifs = []
            analyse = []
            resultat = []
            abm = []
            patho = []
            titre = []
            prescripteur = []
            origine = []
                    
        reception.append(df_bm['RECEPTION'][i])
        approbation.append(df_bm['APPROBATION'][i])
        nc.append(df_bm['NC'][i])
        patient.append(df_bm['PATIENT'][i])
        ddn.append(df_bm['DDN'][i])
        sexe.append(df_bm['SEXE'][i])
        famille.append(df_bm['        FAMILLE'][i])
        demande.append(df_bm['DEMANDE'][i])
        indications.append(df_bm['INDICATIONS'][i])
        action.append(df_bm['ACTION'][i])
        reactifs.append(df_bm['REACTIFS'][i])
        resultat.append(df_bm['GENE_RESULTAT'][i])
        abm.append(df_bm['        ABM_NEURO'][i])
        patho.append(df_bm['PATHOLOGIE'][i])
        titre.append(df_bm['TITRE'][i])
        prescripteur.append(df_bm['PRESCRIPTEUR'][i])
        origine.append(df_bm['ORIGINE'][i])

    reception = list(set(reception))
    approbation = list(set(approbation))
    nc = list(set(nc))
    patient = list(set(patient))
    ddn = list(set(ddn))
    sexe = list(set(sexe))
    famille = list(set(famille))
    demande = list(set(demande))
    indications = list(set(indications))
    action = list(set(action))
    reactifs = list(set(reactifs))
    resultat = list(set(resultat))
    abm = list(set(abm))
    patho = list(set(patho))
    titre = list(set(titre))
    prescripteur = list(set(prescripteur))
    origine = list(set(origine))


    fichier.write("".join(reception)+'\t'+\
        ",".join(approbation)+'\t'+\
        ",".join(nc)+'\t'+",".join(patient)+'\t'+\
        ",".join(ddn)+'\t'+",".join(sexe)+'\t'+\
        ",".join(famille)+'\t'+",".join(demande)+'\t'+\
        ",".join(indications)+'\t'+",".join(action)+'\t'+\
        ",".join(reactifs)+'\t'+\
        ",".join(resultat)+'\t'+",".join(abm)+'\t'+\
        ",".join(patho)+'\t'+",".join(titre)+'\t'+\
        ",".join(prescripteur)+'\t'+\
        ",".join(origine)+'\n')

    nombre = nombre +1

fichier.close()

print('Nombre de lignes BM final = {}.'.format(nombre + comptage_solo))


### MERGING
merge = df_fc.merge(df_bm, how='outer',\
 left_on='DEMANDE', right_on='DEMANDE', \
 suffixes=('_fc', '_bm'))

print('\nNombre de lignes fichier final : {}.'.format(len(merge)))


# Exporter csv
merge.to_csv(sortie, index=False, encoding='utf-8', sep='\t')




print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')