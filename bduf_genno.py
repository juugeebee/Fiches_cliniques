# Author: Julie BOGOIN

import pandas
import numpy
import os


print('\n*******************')
print('**** BDUF BM ****')
print('*******************\n')


# Fichiers
entree = 'entree/bm_2017_bduf.csv'
sortie = 'sortie/bm_2017_bduf_2017_sorted.txt'


if os.path.exists(sortie):
    os.remove(sortie)
    print('Precedent fichier bm_bduf supprime.\n')


bduf = pandas.read_csv(entree, encoding='utf-8', sep="\t", header=[0])
print('Nombre de lignes depart : {}.'.format(len(bduf)))


cols_ini = ['Numero_UF','Nature_prelevement','Date_prelevement','RECEPTION',\
'Date_extraction', 'Demande_renseignement', 'Date_programmation',\
'APPROBATION', 'PATIENT', 'DDN', 'PATHOLOGIE', 'FAMILLE', 'Num_patient_famille',\
'Provenance', 'Analyses_Code_Patho', 'REACTIFS', 'ACTION', 'Technique',\
'BouBHN', 'Codification', 'Prog_Resultat', 'GENE_RESULTAT',\
'Date_saisie_resultat', 'INDICATIONS', 'ABM_NEURO',	'PRESCRIPTEUR',\
'ORIGINE', 'Statut_PATIENT', 'Prlvt_Rang']


bduf.columns = cols_ini


cols_fin = ['RECEPTION', 'APPROBATION', 'PATIENT', 'DDN', 'FAMILLE',
    'INDICATIONS', 'ACTION', 'REACTIFS',
    'GENE_RESULTAT', 'ABM_NEURO', 'PATHOLOGIE', 'PRESCRIPTEUR', 'ORIGINE',
    'Numero_UF','Nature_prelevement','Date_prelevement', 'Date_extraction',
    'Demande_renseignement', 'Date_programmation', 'Num_patient_famille', 
    'Provenance', 'Analyses_Code_Patho', 'Technique', 'BouBHN', 'Codification',
    'Prog_Resultat', 'Date_saisie_resultat', 'Statut_PATIENT', 'Prlvt_Rang']


bduf = bduf[cols_fin]


### TRIER LES LIGNES PAR PATIENTS
bduf.sort_values(by=['DDN'], inplace=True)
bduf.sort_values(by=['PATIENT'], inplace=True)


### REMPLACER LES NA PAR DES - ET SUPPRIMER LES DOUBLONS
bduf = bduf.fillna('-')
bduf.drop_duplicates(keep = 'first', inplace=True)


### SELECTION DES LIGNES AVEC UN REACTIF = 'Panel DIPS'
bduf  = bduf [bduf ['Analyses_Code_Patho'].str.contains('DFT', na=False)]
bduf .reset_index(drop=True, inplace=True)


print('Nombre de lignes DFT : {}.'.format(len(bduf)))


# Exporter csv
bduf.to_csv(sortie, index=False, encoding='utf-8', sep='\t')


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')