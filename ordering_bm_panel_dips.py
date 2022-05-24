# Author: Julie BOGOIN

import pandas
import numpy
import os


print('\n*******************************')
print('**** FICHES CLINIQUES - BM ****')
print('*******************************\n')


# FICHIERS
entree = 'entree/bm_2018_panel_DIPS.csv'
sortie = 'sortie/bm_2018_panel_DIPS_sorted.txt'

if os.path.exists(sortie):
    os.remove(sortie)
    print('Precedent fichier de sortie supprimé.')


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


cols = ['RECEPTION', 'APPROBATION', 'NC', 'PATIENT', 'DDN', 'SEXE', 'FAMILLE',
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

print('Nombre de lignes fichier de départ = {}.'.format(len(raw)))


### SELECTION DES LIGNES AVEC UN REACTIF = 'Panel DIPS'
panel_dips = raw[raw['REACTIFS'].str.contains('Panel DIPS|PANEL DFT_SLA_PAR_ITD', na=False)]
panel_dips.reset_index(drop=True, inplace=True)

print('Nombre de lignes "PANEL DIPS" = {}'.format(len(panel_dips)))


### RECUPER LES INDEX DES DOUBLONS
dup = panel_dips['PATIENT'].duplicated()

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
fichier = open(sortie, "a")

fichier.write("RECEPTION\tAPPROBATION\tNC\tPATIENT\tDDN\tSEXE\tFAMILLE\t\
       DEMANDE\tINDICATIONS\tACTION\tREACTIFS\t\
       GENE_RESULTAT\tABM_NEURO\tPATHOLOGIE\tTITRE\tPRESCRIPTEUR\tORIGINE\t\
       SERVICE\n")


### PARCOURS FICHIER INITAL

# COPIE DES LIGNES SOLO

comptage_solo = 0

for i in range(len(panel_dips)):

    if i not in index_list_doub:

        fichier.write(panel_dips['RECEPTION'][i]+'\t'+\
        panel_dips['APPROBATION'][i]+'\t'+\
        panel_dips['NC'][i]+'\t'+panel_dips['PATIENT'][i]+'\t'+\
        panel_dips['DDN'][i]+'\t'+panel_dips['SEXE'][i]+'\t'+\
        panel_dips['FAMILLE'][i]+'\t'+panel_dips['DEMANDE'][i]+'\t'+\
        panel_dips['INDICATIONS'][i]+'\t'+panel_dips['ACTION'][i]+'\t'+\
        panel_dips['REACTIFS'][i]+'\t'+\
        panel_dips['GENE_RESULTAT'][i]+'\t'+panel_dips['ABM_NEURO'][i]+'\t'+\
        panel_dips['PATHOLOGIE'][i]+'\t'+panel_dips['TITRE'][i]+'\t'+\
        panel_dips['PRESCRIPTEUR'][i]+'\t'+\
        panel_dips['ORIGINE'][i]+'\n')   

        comptage_solo = comptage_solo + 1    


print('Nombre de lignes solo = {}.'.format(comptage_solo))
print('Nombre de doublons = {}.'.format(len(index_list_doub)))


start_list = []
stop_list = []


for i in index_list_doub:

    if (panel_dips['PATIENT'][i] != panel_dips['PATIENT'][i+1]):
        stop_list.append(i)

    else :
        
        if (panel_dips['PATIENT'][i] != panel_dips['PATIENT'][i-1]):
            start_list.append(i)


for h in range(len(start_list)) : 

    for i in range(start_list[h], stop_list[h]+1,1):

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
            
        reception.append(panel_dips['RECEPTION'][i])
        approbation.append(panel_dips['APPROBATION'][i])
        nc.append(panel_dips['NC'][i])
        patient.append(panel_dips['PATIENT'][i])
        ddn.append(panel_dips['DDN'][i])
        sexe.append(panel_dips['SEXE'][i])
        famille.append(panel_dips['FAMILLE'][i])
        demande.append(panel_dips['DEMANDE'][i])
        indications.append(panel_dips['INDICATIONS'][i])
        action.append(panel_dips['ACTION'][i])
        reactifs.append(panel_dips['REACTIFS'][i])
        resultat.append(panel_dips['GENE_RESULTAT'][i])
        abm.append(panel_dips['ABM_NEURO'][i])
        patho.append(panel_dips['PATHOLOGIE'][i])
        titre.append(panel_dips['TITRE'][i])
        prescripteur.append(panel_dips['PRESCRIPTEUR'][i])
        origine.append(panel_dips['ORIGINE'][i])

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


fichier.close()



print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')