# Author: Julie BOGOIN

import pandas
import numpy
import os


print('\n**********************')
print('**** CONCATING BM ****')
print('**********************\n')


# Fichiers
fc = 'sortie/fc_dft_sorted.txt'
dosage = 'entree/dosages.csv'
dosage_final = 'sortie/dosages_final.txt'
bm_concat = 'sortie/bm_concat.txt'
bm_final = 'sortie/bm_final.txt'
sortie = 'fc_bm_dft.txt'


if os.path.exists('fc_bm_dft.txt'):
    os.remove('fc_bm_dft.txt')
    print('Precedent fichier de sortie supprime.\n')

if os.path.exists("sortie/bm_concat.txt"):
    os.remove("sortie/bm_concat.txt")
    print('Precedent fichier bm_concat supprime.\n')

if os.path.exists("sortie/bm_final.txt"):
    os.remove("sortie/bm_final.txt")
    print('Precedent fichier bm_final supprime.\n')


if os.path.exists("sortie/dosages_final.txt"):
    os.remove("sortie/dosages_final.txt")
    print('Precedent fichier dosages_final supprime.\n')


# Concatener tous les fichiers de sortie BM

comparaison = 0
fichier = 0

files = os.listdir("sortie")

with open(bm_concat, "w") as new_file:

    new_file.write('RECEPTION\tAPPROBATION\tDELAI\tNC\tPATIENT\tDDN\tID\tSEXE\t\
        FAMILLE\tDEMANDE\tINDICATIONS\tACTION\tREACTIFS\tGENE_RESULTAT\t\
        ABM_NEURO\tPATHOLOGIE\tTITRE\tPRESCRIPTEUR\tORIGINE\tSERVICE\n')

    compteur = 0

    for filename in files:

        if filename != 'fc_dft_sorted.txt':

            fichier = fichier + 1

            print(filename)

            with open("sortie/" + filename) as f:

                for line in f:
                    
                    if not line.startswith('RECEPTION'):

                            new_file.write(line)
                            compteur = compteur + 1
                    
                new_file.write("\n")


print('Nombre de fichiers BM : {}.'.format(fichier))
print('\nNombre de lignes fichier bm_concat : {}.'.format(compteur))


print('\n*************************')
print('**** MERGING BM + FC ****')
print('*************************\n')


### FICHES CLINIQUES
df_fc = pandas.read_csv(fc, encoding='utf-8', sep="\t", header=[0])
df_fc.dropna(how = 'all', inplace = True)

print('Nombre de lignes Fiches Cliniques : {}.'.format(len(df_fc)))


### BM 
### UNE SEULE LIGNE PAR PATIENT
df_bm = pandas.read_csv(bm_concat, sep="\t", header=[0])
df_bm.dropna(how = 'all', inplace = True)

print('\nNombre de lignes BM depart = {}.'.format(len(df_bm)))


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


### TRIER LES LIGNES PAR PATIENTS
df_bm.sort_values(by=['ID'], inplace=True)
df_bm.reset_index(inplace=True, drop=True)

df_bm.rename(columns={"        FAMILLE": "FAMILLE"}, inplace=True)
df_bm.rename(columns={"        ABM_NEURO": "ABM_NEURO"}, inplace=True)


print('Nombre de lignes BM apres curation = {}.'.format(len(df_bm)))


### RECUPER UN DF AVEC LES DOUBLONS

ids = df_bm["ID"]
dup = df_bm[ids.isin(ids[ids.duplicated()])].sort_values("ID")

# RECUPERER LES INDEX
index_list = dup.index.tolist()

dup.reset_index(drop=True, inplace=True)

### COPIER LES LIGNES UNIQUES DANS LE FICHIER DE SORTIE

# CREATION FICHIER SORTIE
fichier = open(bm_final, "a")

fichier.write("RECEPTION\tAPPROBATION\tDELAI\tNC\tPATIENT\tDDN\tID\tSEXE\tFAMILLE\t\
       DEMANDE\tINDICATIONS\tACTION\tREACTIFS\t\
       GENE_RESULTAT\tABM_NEURO\tPATHOLOGIE\tTITRE\tPRESCRIPTEUR\tORIGINE\t\
       SERVICE\n")


### PARCOURS FICHIER INITAL

# COPIE DES LIGNES SOLO

comptage_solo = 0

for i in range(len(df_bm)):

    if i not in index_list:

        fichier.write(df_bm['RECEPTION'][i]+'\t'+\
        df_bm['APPROBATION'][i]+'\t'+\
        df_bm['DELAI'][i]+'\t'+\
        df_bm['NC'][i]+'\t'+ df_bm['PATIENT'][i]+'\t'+\
        df_bm['DDN'][i]+'\t'+ df_bm['ID'][i]+'\t'+\
        df_bm['SEXE'][i]+'\t'+\
        df_bm['FAMILLE'][i]+'\t'+ df_bm['DEMANDE'][i]+'\t'+\
        df_bm['INDICATIONS'][i]+'\t'+ df_bm['ACTION'][i]+'\t'+\
        df_bm['REACTIFS'][i]+'\t'+\
        df_bm['GENE_RESULTAT'][i]+'\t'+ df_bm['ABM_NEURO'][i]+'\t'+\
        df_bm['PATHOLOGIE'][i]+'\t'+ df_bm['TITRE'][i]+'\t'+\
        df_bm['PRESCRIPTEUR'][i]+'\t'+\
        df_bm['ORIGINE'][i]+'\n')   

        comptage_solo = comptage_solo + 1    


print('Nombre de lignes solo = {}.'.format(comptage_solo))
print('Nombre de doublons = {}.'.format(len(index_list)))


### PARCOURIR LE DF DUP

index_list_doub = []


for i in range(len(index_list)-2) : 
    
    if (dup['ID'][i] == dup['ID'][i+1]) and \
    (dup['ID'][i+1] != dup['ID'][i+2]):

        reqd_Index = dup[dup['ID']==dup['ID'][i]].index.tolist()
        index_list_doub.append(reqd_Index)


for liste in index_list_doub:
    
    reception = []
    approbation = []
    delai = []
    nc = []
    patient = []
    ddn = []
    ids = []
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


    if len(liste) == 2:

        reception.append(dup['RECEPTION'][liste[0]])
        reception.append(dup['RECEPTION'][liste[1]])
        approbation.append(dup['APPROBATION'][liste[0]])
        approbation.append(dup['APPROBATION'][liste[1]])
        nc.append(dup['NC'][liste[0]])
        nc.append(dup['NC'][liste[1]])
        delai.append(dup['DELAI'][liste[0]])
        delai.append(dup['DELAI'][liste[1]])
        patient.append(dup['PATIENT'][liste[0]])
        patient.append(dup['PATIENT'][liste[1]])
        ddn.append(dup['DDN'][liste[0]])
        ddn.append(dup['DDN'][liste[1]])
        ids.append(dup['ID'][liste[0]])
        ids.append(dup['ID'][liste[1]])
        sexe.append(dup['SEXE'][liste[0]])
        sexe.append(dup['SEXE'][liste[1]])
        famille.append(dup['FAMILLE'][liste[0]])
        famille.append(dup['FAMILLE'][liste[1]])
        demande.append(dup['DEMANDE'][liste[0]])
        demande.append(dup['DEMANDE'][liste[1]])
        indications.append(dup['INDICATIONS'][liste[0]])
        indications.append(dup['INDICATIONS'][liste[1]])
        action.append(dup['ACTION'][liste[0]])
        action.append(dup['ACTION'][liste[1]])
        reactifs.append(dup['REACTIFS'][liste[0]])
        reactifs.append(dup['REACTIFS'][liste[1]])
        resultat.append(dup['GENE_RESULTAT'][liste[0]])
        resultat.append(dup['GENE_RESULTAT'][liste[1]])
        abm.append(dup['ABM_NEURO'][liste[0]])
        abm.append(dup['ABM_NEURO'][liste[1]])
        patho.append(dup['PATHOLOGIE'][liste[0]])
        patho.append(dup['PATHOLOGIE'][liste[1]])
        titre.append(dup['TITRE'][liste[0]])
        titre.append(dup['TITRE'][liste[1]])
        prescripteur.append(dup['PRESCRIPTEUR'][liste[0]])
        prescripteur.append(dup['PRESCRIPTEUR'][liste[1]])        
        origine.append(dup['ORIGINE'][liste[0]])
        origine.append(dup['ORIGINE'][liste[1]])

        comptage_solo = comptage_solo + 1

    else:

        for indice in range(len(liste)):

            reception.append(dup['RECEPTION'][liste[indice]])
            approbation.append(dup['APPROBATION'][liste[indice]])
            nc.append(dup['NC'][liste[indice]])
            delai.append(dup['DELAI'][liste[indice]])
            patient.append(dup['PATIENT'][liste[indice]])
            ddn.append(dup['DDN'][liste[indice]])
            ids.append(dup['ID'][liste[indice]])
            sexe.append(dup['SEXE'][liste[indice]])
            famille.append(dup['FAMILLE'][liste[indice]])
            demande.append(dup['DEMANDE'][liste[indice]])
            indications.append(dup['INDICATIONS'][liste[indice]])
            action.append(dup['ACTION'][liste[indice]])
            reactifs.append(dup['REACTIFS'][liste[indice]])
            resultat.append(dup['GENE_RESULTAT'][liste[indice]])
            abm.append(dup['ABM_NEURO'][liste[indice]])
            patho.append(dup['PATHOLOGIE'][liste[indice]])
            titre.append(dup['TITRE'][liste[indice]])
            prescripteur.append(dup['PRESCRIPTEUR'][liste[indice]])       
            origine.append(dup['ORIGINE'][liste[indice]])

        comptage_solo = comptage_solo + 1


    reception = list(set(reception))
    approbation = list(set(approbation))
    delai = list(set(delai))
    nc = list(set(nc))
    patient = list(set(patient))
    ddn = list(set(ddn))
    ids = list(set(ids))
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


    fichier.write(" & ".join(reception)+'\t'+\
            " & ".join(approbation)+'\t'+\
            " & ".join(delai)+'\t'+\
            " & ".join(nc)+'\t'+" & ".join(patient)+'\t'+\
            " & ".join(ddn)+'\t'+" & ".join(ids)+'\t'+\
            " & ".join(sexe)+'\t'+\
            " & ".join(famille)+'\t'+" & ".join(demande)+'\t'+\
            " & ".join(indications)+'\t'+" & ".join(action)+'\t'+\
            " & ".join(reactifs)+'\t'+\
            " & ".join(resultat)+'\t'+" & ".join(abm)+'\t'+\
            " & ".join(patho)+'\t'+" & ".join(titre)+'\t'+\
            " & ".join(prescripteur)+'\t'+\
            " & ".join(origine)+'\n')


fichier.close()


print('Nombre de lignes fichier bm_final = {}.\n'.format(comptage_solo))


### CREATION DF BM FINAL
bm_final = pandas.read_csv(bm_final, sep="\t", header=[0])

### TRIER LES LIGNES PAR PATIENTS
bm_final.sort_values(by=['ID'], inplace=True)
bm_final.reset_index(inplace=True)

bm_final.rename(columns={"       DEMANDE": "DEMANDE"}, inplace=True)
bm_final.rename(columns={"       GENE_RESULTAT": "GENE_RESULTAT"}, inplace=True)
bm_final.rename(columns={"       SERVICE": "SERVICE"}, inplace=True)


### MERGING
merge = df_fc.merge(bm_final, how='outer',\
 left_on='ID', right_on='ID', \
 suffixes=('_fc', '_bm'))

del merge['index']

print('Nombre de lignes mergees = {}.'.format(len(merge)))

merge.drop_duplicates(subset=['ID'], inplace=True, keep='first', ignore_index=True)

print('Nombre de lignes fichier final sans dosage: {}.'.format(len(merge)))


cols = ['PATIENT', 'NOM', 'PRENOM','DDN_fc', 'DDN_bm', 'ID','SEXE',
        'PATHOLOGIE_fc', 'PATHOLOGIE_bm','FAMILLE_fc', 'FAMILLE_bm', 'DEMANDE_fc',
        'DEMANDE_bm', 'RECEPTION_fc', 'RECEPTION_bm', 'INDICATIONS', 'DFTAGEXAM', 
        'DFTAGDEB', 'DFTATCFAM', 'DFTATCPRES', 'DFTMOD', 'DFTMODAUTRE', 'DFTFORMCLIN',
        'DFTTC', 'DFTTCPRES', 'DFTTL', 'DFTTLPRES', 'DFTTM', 'DFTTMPRES', 
        'DFTPARK', 'DFTHALLU', 'DFTAPRAX', 'DFTTO', 'DFTTOPRES', 'DFTMVAN', 
        'DFTMVANPRES', 'DFTSLA', 'DFTSLADEB', 'DFTSLADEBAGE', 'DFTSLADEBEMG',
        'DFTAUT', 'DFTAUTPRES', 'DFTPLS', 'DFTPLSPREC', 'DFTLCRAB', 
        'DFTLCRABPREC', 'DFTLCRT', 'DFTLCRTPREC', 'DFTLCRPT', 'DFTLCRPTPREC',
        'DFTLCRAUT', 'DFTLCRAUTPREC', 'DFTNEURTEST', 'DFTNEURTESTPREC',
        'DFTNEURIRM', 'DFTNEURIRMPREC', 'DFTNEURSPECT', 'DFTNEURSPECTPREC',
        'APPROBATION', 'DELAI', 'NC', 'ACTION', 'REACTIFS', 'GENE_RESULTAT', 'ABM_NEURO',  'TITRE',
        'PRESCRIPTEUR', 'ORIGINE', 'SERVICE']

merge = merge[cols]


### TRIER LES LIGNES PAR PATIENTS
merge.sort_values(by=['ID'], inplace=True)


print('\n***********************')
print('**** AJOUT DOSAGES ****')
print('***********************\n')


### LECTURE DU FICHIER EXPORT GENNO
dosage = pandas.read_csv(dosage, sep=";", header=[0], encoding="ISO-8859-1")

print('Nombre de lignes dosages depart = {}.'.format(len(dosage)))


### AJOUTER UNE COLONNE ID
dosage['ID'] = dosage['NOM'].str.replace(' ', '') +\
 dosage['PRENOM'].str.replace(' ', '') + dosage['DDN'].str.replace('/', '')


del dosage['NOM']
del dosage['PRENOM']
del dosage['DDN']
del dosage['DATE RECEPTION']
del dosage['NOM PRESC.']
del dosage['VILLE']
dosage.rename(columns={"COMMENTAIRE": "DOSAGE_PGRN"}, inplace=True)


### SUPPRIMER LES DOUBLONS
dosage.drop_duplicates(keep = 'first', inplace=True)


### SUPPRIMER LES LIGNES DOSAGES OU IDS VIDES
dosage = dosage.dropna(axis = 0, how ='any')


### TRIER LES LIGNES PAR PATIENTS
dosage.sort_values(by=['ID'], inplace=True)
dosage.reset_index(inplace=True, drop=True)


### NOUVEAU DF AVEC SEULEMENT DES LIGNES DE DOSAGES
dosage_reel = dosage[dosage["DOSAGE_PGRN"].str.contains('pgrn =')]
dosage_reel.reset_index(inplace=True, drop=True)

print('Nombre de lignes avec dosages reels = {}.'.format(len(dosage_reel)))


### DUPIER S'IL Y A DES DOUBLONS
dup = dosage_reel['ID'].duplicated()


### RECUPERER LES INDEX DES DOUBLONS
dup_list = []
dupmoinsun = []

for i in range(len(dup)) : 
    if dup[i] == True : 
        dup_list.append(i)

        if i-1 not in dup_list : 
            dupmoinsun.append(i-1)
        
        dupmoinsun.append(i)


# Trier
dupmoinsun = sorted(dupmoinsun)


### ECRITURE FICHIER SORTIE

solo = 0
stop = []
ids = []
ids_ligne = []
pgrn = []
pgrn_ligne = []


with open(dosage_final, "w") as dosage_file:

    dosage_file.write('ID\tDOSAGE_PGRN\n')

    ### SOLO
    for i in range(len(dosage_reel)):

        if i not in dupmoinsun:

            dosage_file.write(dosage_reel['ID'][i]+'\t'+\
            dosage_reel['DOSAGE_PGRN'][i]+'\n')   

            solo = solo + 1


    ## DOUBLONS
    for i in dupmoinsun :

        if i+1 not in dupmoinsun : 
            stop.append(i+1)


    dup_final = dupmoinsun + stop
    dup_final = sorted(dup_final)

    
    for i in dup_final :

        if i+1 in dup_final :

            if dosage_reel['ID'][i] == dosage_reel['ID'][i+1] :

                ids.append(dosage_reel['ID'][i])
                pgrn.append(dosage_reel['DOSAGE_PGRN'][i])

            else :

                ids.append(dosage_reel['ID'][i])
                pgrn.append(dosage_reel['DOSAGE_PGRN'][i])
                ids_ligne.append(ids)
                pgrn_ligne.append(pgrn)
                ids = []
                pgrn = []


    # Unifier les noms dans chaque liste ids
    ids_final = []
        
    for element in ids_ligne : 

        ids_final.append(element[0]) 


    # Ecrire dans le fichier
    for i in range(len(ids_final)) :

        pgrn_i = " & ".join(pgrn_ligne[i])  
        dosage_file.write( (ids_final[i]) + '\t' + pgrn_i + '\n')


dosage_file.close()

        
print('Nombre de lignes solo = {}.'.format(solo))
print('Nombre de doublons = {}.'.format(len(ids_final)))
print('Nombre de lignes fichier dosages_final = {}.'.format(solo + len(ids_final)))


print('\n*********************************')
print('**** MERGING BM/FC + DOSAGES ****')
print('*********************************\n')

### LECTURE DU FICHIER dosages_final
dosage_tri = pandas.read_csv(dosage_final, sep="\t", header=[0], encoding="ISO-8859-1")


### MERGING
fifi = merge.merge(dosage_tri, how='left',\
 left_on='ID', right_on='ID', \
 suffixes=('_fc_bm', '_pgrn'))

print('Nombre de lignes mergees = {}.'.format(len(fifi)))

### TRIER LES LIGNES PAR PATIENTS
fifi.sort_values(by=['ID'], inplace=True)


### Exporter csv
fifi.to_csv(sortie, index=False, encoding='utf-8', sep='\t')


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')