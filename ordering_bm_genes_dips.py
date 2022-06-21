# Author: Julie BOGOIN

import pandas
import numpy
import os


print('\n*******************************')
print('**** FICHES CLINIQUES - BM ****')
print('*******************************\n')


# FICHIERS
entree = 'entree/bm_2018_C9.csv'
sortie = 'sortie/bm_2018_C9_sorted.txt'

if os.path.exists(sortie):
    os.remove(sortie)
    print('Precedent fichier de sortie supprime.\n')


### LECTURE DU FICHIER EXPORT GENNO
raw = pandas.read_csv(entree, encoding='utf-8', sep="\t", header=[0], dtype=str)

raw.rename(columns={"TO_CHAR(DATERECEP,'DD/MM/YYYY')": "RECEPTION"}, inplace=True)
raw.rename(columns={"TO_CHAR(DATEAPPROB,'DD/MM/YYYY')": "APPROBATION"}, inplace=True)
raw.rename(columns={"Indications": "INDICATIONS"}, inplace=True)
raw.rename(columns={"Réactifs": "REACTIFS"}, inplace=True)
raw.rename(columns={"CODEORIGINE": "ORIGINE"}, inplace=True)
raw.rename(columns={"GENE RESULTAT": "GENE_RESULTAT"}, inplace=True)
raw.rename(columns={"ABM NEURO": "ABM_NEURO"}, inplace=True)

raw['PRESCRIPTEUR'] = raw['NOMPRESC'] + ' ' + raw['PRENOMPRESC']
del raw['NOMPRESC']
del raw['PRENOMPRESC']
del raw['GENE ANALYSE']


cols = ['RECEPTION', 'APPROBATION', 'DELAI', 'NC', 'PATIENT', 'DDN', 'SEXE', 'FAMILLE',
       'DEMANDE', 'INDICATIONS', 'ACTION', 'REACTIFS',
       'GENE_RESULTAT', 'ABM_NEURO', 'PATHOLOGIE', 'TITRE', 'PRESCRIPTEUR', 'ORIGINE',
       'SERVICE']
raw = raw[cols]


### REMPLACER LES NA PAR DES - ET SUPPRIMER LES DOUBLONS
raw = raw.fillna('-')
raw.drop_duplicates(keep = 'first', inplace=True)


### TRIER LES LIGNES PAR PATIENTS
raw.sort_values(by=['DDN'], inplace=True)
raw.sort_values(by=['PATIENT'], inplace=True)

print(entree)
print('Nombre de lignes fichier de depart = {}.\n'.format(len(raw)))


### SELECTION DES LIGNES AVEC UN REACTIF = 'Panel DIPS'
panel_dips = raw[raw['PATHOLOGIE'].str.contains('DFT', na=False)]
panel_dips.reset_index(drop=True, inplace=True)

print('Nombre de lignes "Genes DIPS / C9" = {}.'.format(len(panel_dips)))


### RECUPER UN DF AVEC LES DOUBLONS

ids = panel_dips["PATIENT"]
dup = panel_dips[ids.isin(ids[ids.duplicated()])].sort_values("PATIENT")

# RECUPERER LES INDEX
index_list = dup.index.tolist()

dup.reset_index(drop=True, inplace=True)

### COPIER LES LIGNES UNIQUES DANS LE FICHIER DE SORTIE

# CREATION FICHIER SORTIE
fichier = open(sortie, "a")

fichier.write("RECEPTION\tAPPROBATION\tDELAI\tNC\tPATIENT\tDDN\tSEXE\tFAMILLE\t\
       DEMANDE\tINDICATIONS\tACTION\tREACTIFS\t\
       GENE_RESULTAT\tABM_NEURO\tPATHOLOGIE\tTITRE\tPRESCRIPTEUR\tORIGINE\t\
       SERVICE\n")


### PARCOURS FICHIER INITAL

# COPIE DES LIGNES SOLO

comptage_solo = 0

for i in range(len(panel_dips)):

    if i not in index_list:

        fichier.write(panel_dips['RECEPTION'][i]+'\t'+\
        panel_dips['APPROBATION'][i]+'\t'+\
        panel_dips['DELAI'][i]+'\t'+\
        panel_dips['NC'][i]+'\t'+ panel_dips['PATIENT'][i]+'\t'+\
        panel_dips['DDN'][i]+'\t'+ panel_dips['SEXE'][i]+'\t'+\
        panel_dips['FAMILLE'][i]+'\t'+ panel_dips['DEMANDE'][i]+'\t'+\
        panel_dips['INDICATIONS'][i]+'\t'+ panel_dips['ACTION'][i]+'\t'+\
        panel_dips['REACTIFS'][i]+'\t'+\
        panel_dips['GENE_RESULTAT'][i]+'\t'+ panel_dips['ABM_NEURO'][i]+'\t'+\
        panel_dips['PATHOLOGIE'][i]+'\t'+ panel_dips['TITRE'][i]+'\t'+\
        panel_dips['PRESCRIPTEUR'][i]+'\t'+\
        panel_dips['ORIGINE'][i]+'\n')   

        comptage_solo = comptage_solo + 1    


print('Nombre de lignes solo = {}.'.format(comptage_solo))
print('Nombre de doublons = {}.'.format(len(index_list)))


### PARCOURIR LE DF DUP

index_list_doub = []


for i in range(len(index_list)-2) : 
    
    if (dup['PATIENT'][i] == dup['PATIENT'][i+1]) and \
    (dup['PATIENT'][i+1] != dup['PATIENT'][i+2]):

        reqd_Index = dup[dup['PATIENT']==dup['PATIENT'][i]].index.tolist()
        index_list_doub.append(reqd_Index)


for liste in index_list_doub:
    
    reception = []
    approbation = []
    delai = []
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
            approbation.append(dup['APPROBATION'][liste[indice]])
            delai.append(dup['DELAI'][liste[indice]])
            patient.append(dup['PATIENT'][liste[indice]])
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


    fichier.write(",".join(reception)+'\t'+\
            ",".join(approbation)+'\t'+\
            ",".join(delai)+'\t'+\
            ",".join(nc)+'\t'+",".join(patient)+'\t'+\
            ",".join(ddn)+'\t'+",".join(sexe)+'\t'+\
            ",".join(famille)+'\t'+",".join(demande)+'\t'+\
            ",".join(indications)+'\t'+",".join(action)+'\t'+\
            ",".join(reactifs)+'\t'+\
            ",".join(resultat)+'\t'+",".join(abm)+'\t'+\
            ",".join(patho)+'\t'+",".join(titre)+'\t'+\
            ",".join(prescripteur)+'\t'+\
            ",".join(origine)+'\n')


fichier.close()

print('\nNombre de lignes fichier final = {}.'.format(comptage_solo))

print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')