# Author: Julie BOGOIN

import pandas
import numpy

print('\n**************************')
print('**** FICHES CLINIQUES ****')
print('**************************')


### LISTE DES COLONNES CHAMPS
champs_total = ['DFTAGEXAM', 'DFTAGDEB', 'DFTATCFAM', 'DFTATCPRES', 'DFTMOD'\
    , 'DFTMODAUTRE', 'DFTFORMCLIN', 'DFTTC', 'DFTTCPRES', 'DFTTL', 'DFTTLPRES'\
    , 'DFTTM', 'DFTTMPRES', 'DFTPARK', 'DFTHALLU', 'DFTAPRAX', 'DFTTO', 'DFTTOPRES'\
    , 'DFTMVAN', 'DFTMVANPRES', 'DFTSLA', 'DFTSLADEB', 'DFTSLADEBAGE'\
    , 'DFTSLADEBEMG', 'DFTAUT', 'DFTAUTPRES', 'DFTPLS', 'DFTPLSPREC', 'DFTLCRAB'\
    , 'DFTLCRABPREC', 'DFTLCRT', 'DFTLCRTPREC', 'DFTLCRPT', 'DFTLCRPTPREC'\
    , 'DFTLCRAUT', 'DFTLCRAUTPREC', 'DFTNEURTEST', 'DFTNEURTESTPREC', 'DFTNEURIRM'\
    , 'DFTNEURIRMPREC', 'DFTNEURSPECT', 'DFTNEURSPECTPREC']


# Fichiers
entree = 'entree/fc_dft_2022.csv'
sortie = 'sortie/fc_dft_2022_sorted.txt'


### LECTURE DU FICHIER EXPORT GENNO
raw = pandas.read_csv(entree, sep="\t", header=[0], encoding="ISO-8859-1")

print('\nNombre de lignes fichier de depart = {}.'.format(len(raw)))


raw.rename(columns={"DATE RECEPTION": "RECEPTION"}, inplace=True)


# Creer la liste stop
longueur_raw = raw.index.stop
stop = []


### AJOUTER UNE COLONNE ID
raw['ID'] = raw['NOM'].str.replace(' ', '') +\
 raw ['PRENOM'].str.replace(' ', '') + raw['DDN'].str.replace('/', '')


# Trier les lignes par noms de patients
raw.sort_values(by=['ID'], inplace=True)
raw.reset_index(drop=True, inplace=True)


for i in range(longueur_raw-1):

    if (raw["ID"][i] != raw["ID"][i+1]):

        stop.append(i)


# Inserer la derniere valeur
stop.append(longueur_raw-1)


# Creer la liste start
start = []
for i in range(len(stop)-1):
    start.append(stop[i]+1)


# Inserer un 0 en debut de liste
start.insert(0,0)


# Creer une liste d'info par patient
final_new = []

for i in start:
    new_list = []
    new_list.append(raw["PATHOLOGIE"][i])
    new_list.append(raw["RECEPTION"][i])
    new_list.append(raw["DEMANDE"][i])
    new_list.append(raw["FAMILLE"][i])
    new_list.append(raw["NOM"][i])
    new_list.append(raw["PRENOM"][i])
    new_list.append(raw["DDN"][i])
    new_list.append(raw["ID"][i])
    final_new.append(new_list)

patient = pandas.DataFrame(data=final_new,columns=["PATHOLOGIE", "RECEPTION", "DEMANDE",\
    "FAMILLE", "NOM", "PRENOM", "DDN", "ID"])


# Recuperer les champs/valeurs
df_list = []

for i in range(len(start)):

    ligne_list = []
    
    # Creer des dicos avec champs et valeurs pour chaque patient
    dico = {}
    for j in range(start[i],stop[i]+1):
        dico[raw["CHAMP"][j]]=raw["VALEUR"][j]

    for j in champs_total:
    
    # Recuperer la valeur de chaque champ ou ajouter "" si n'existe pas
        valeur = dico.get(j,"")
        ligne_list.append(valeur)

    df_list.append(ligne_list)

col_vc = pandas.DataFrame(df_list, columns=champs_total)


# Structure dataframe final
final = pandas.concat([patient,col_vc], axis=1)


### ENLEVER LES G DES NUMEROS DE DEMANDE
final['DEMANDE'] = final['DEMANDE'].str.replace('G', '')


print('Nombre de lignes fichier de sortie = {}.'.format(len(final)))


# Exporter csv
final.to_csv(sortie, index=False, encoding='utf-8', sep='\t')


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')