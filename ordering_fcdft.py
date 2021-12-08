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
entree = 'fcdft.csv'
sortie = 'fcdft_sorted.csv'


### LECTURE DU FICHIER EXPORT GENNO
raw = pandas.read_csv(entree, encoding='utf-16', sep="\t", header=[0])
raw.rename(columns={"DATE RECEPTION": "RECEPTION"}, inplace=True)


# Creer la liste stop
longueur_raw = raw.index.stop
stop = []


# Trier les lignes par noms de patients
raw.sort_values(by=['NOM'], inplace=True)
raw.reset_index(drop=True, inplace=True)


for i in range(longueur_raw-1):

    if (raw["NOM"][i] != raw["NOM"][i+1]) and \
        (raw["PRENOM"][i] != raw["PRENOM"][i+1]) and \
        (raw["DDN"][i] != raw["DDN"][i+1]):

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
    final_new.append(new_list)

patient = pandas.DataFrame(data=final_new,columns=["PATHOLOGIE", "RECEPTION", "DEMANDE",\
    "FAMILLE", "NOM", "PRENOM", "DDN"])


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


# Exporter csv
final.to_csv(sortie, index=False)


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')