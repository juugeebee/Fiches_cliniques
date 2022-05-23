# Author: Julie BOGOIN

import pandas
import numpy

print('\n*****************')
print('**** MERGING ****')
print('*****************\n')


# Fichiers
fc = 'fcdft_sorted.txt'
bm = 'bm_tout_sauf_SCA_sorted.txt'
sortie = 'fc_bm_dft.txt'

### FICHES CLINIQUES
df_fc = pandas.read_csv(fc, encoding='utf-16', sep="\t", header=[0])

# CONCATENER LES NOMS ET PRENOMS
df_fc['PATIENT'] = df_fc['NOM'] + " " + df_fc['PRENOM']
del df_fc['NOM']
del df_fc['PRENOM']

print('Nombre de lignes Fiches Cliniques : {}.'.format(len(df_fc)))


### BM
df_bm = pandas.read_csv(bm, sep="\t", header=[0])

print('Nombre de lignes BM : {}.'.format(len(df_bm)))


### MERGING
merge = df_fc.merge(df_bm, how='left', on=['PATIENT', 'DDN', 'FAMILLE',\
 'PATHOLOGIE', 'RECEPTION'])

print('Nombre de lignes final : {}.'.format(len(merge)))


# Exporter csv
merge.to_csv(sortie, index=False, encoding='utf-8', sep='\t')


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')