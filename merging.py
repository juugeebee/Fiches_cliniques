# Author: Julie BOGOIN

import pandas
import numpy

print('\n*****************')
print('**** MERGING ****')
print('*****************\n')


# Fichiers
fc = 'sortie/fc_dft_sorted.txt'
bm = 'sortie/bm_2021_panel_DIPS_sorted.txt'
sortie = 'fc_bm_dft.txt'

### FICHES CLINIQUES
df_fc = pandas.read_csv(fc, encoding='utf-8', sep="\t", header=[0])

print('Nombre de lignes Fiches Cliniques : {}.'.format(len(df_fc)))


### BM
df_bm = pandas.read_csv(bm, sep="\t", header=[0])

print('Nombre de lignes BM : {}.'.format(len(df_bm)))


### MERGING
merge = df_fc.merge(df_bm, how='outer',\
 left_on='DEMANDE', right_on='       DEMANDE', \
 suffixes=('_fc', '_bm'))

print('Nombre de lignes final : {}.'.format(len(merge)))


# Exporter csv
merge.to_csv(sortie, index=False, encoding='utf-8', sep='\t')


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')