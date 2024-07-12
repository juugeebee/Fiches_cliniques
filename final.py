import pandas
import numpy
import os


print('\n********************')
print('**** FINAL 2022 ****')
print('********************\n')


# Fichiers
entree = 'entree/synthese_FC_BM_PGRN_02062023.csv'
sortie = 'final_2022.txt'

if os.path.exists('final_2022.txt'):
    os.remove('final_2022.txt')
    print('Precedent fichier de sortie supprime.\n')


df = pandas.read_csv(entree, encoding='utf-8', sep="\t", header=[0])


cols_ini = df.columns.tolist()


del df['DFTSLA_final.1']


df['GENE_RESULTAT_final'] = df['GENE_RESULTAT_final'].fillna('-')
df['GENE_RESULTAT_final'] = df['GENE_RESULTAT_final'].astype(str)


df['GENE_RESULTAT_fc_bm_pgrn'] = df['GENE_RESULTAT_fc_bm_pgrn'].fillna('-')
df['GENE_RESULTAT_fc_bm_pgrn'] = df['GENE_RESULTAT_fc_bm_pgrn'].astype(str)


df['GENE_RESULTAT'] = df['GENE_RESULTAT_final'] + ' ; ' + df['GENE_RESULTAT_fc_bm_pgrn']


del df['GENE_RESULTAT_final']
del df['GENE_RESULTAT_fc_bm_pgrn']


cols_final = ['ID', 'DDN_fc_final', 'DDN_bm_final', 'Sexe_final', 'PATHOLOGIE_fc_final', 'PATHOLOGIE_bm_final', 'FAMILLE_fc_final', \
    'FAMILLE_bm_final', 'DEMANDE_fc_final', 'DEMANDE_bm_final', 'RECEPTION_fc_final', 'RECEPTION_bm_final', 'INDICATIONS_final', \
    'ACTION_final', 'GENE_RESULTAT', 'APPROBATION_final', 'DELAI_final', 'NC_final', 'REACTIFS_final', 'ABM_NEURO_final', \
    'TITRE_final', 'PRESCRIPTEUR_final', 'ORIGINE_final', 'SERVICE_final', 'DOSAGE_PGRN_final',  'DFTAGDEB_final', 'DFTAGEXAM_final', \
    'DFTAPRAX_final', 'DFTATCFAM_final', 'DFTATCPRES_final', 'DFTAUT_final', 'DFTAUTPRES_final', 'DFTFORMCLIN_final', 'DFTHALLU_final', \
    'DFTLCRAB_final', 'DFTLCRABPREC_final', 'DFTLCRAUT_final', 'DFTLCRAUTPREC_final', 'DFTLCRPT_final', 'DFTLCRPTPREC_final', 'DFTLCRT_final', \
    'DFTLCRTPREC_final', 'DFTMOD_final', 'DFTMODAUTRE_final', 'DFTMVAN_final', 'DFTMVANPRES_final', 'DFTNEURIRM_final', 'DFTNEURIRMPREC_final', \
    'DFTNEURSPECT_final', 'DFTNEURSPECTPREC_final', 'DFTNEURTEST_final', 'DFTNEURTESTPREC_final', 'DFTPARK_final', 'DFTPLS_final', \
    'DFTPLSPREC_final', 'DFTSLA_final', 'DFTSLADEB_final', 'DFTSLADEBAGE_final', 'DFTSLADEBEMG_final', 'DFTTC_final', 'DFTTCPRES_final', \
    'DFTTL_final', 'DFTTLPRES_final', 'DFTTM_final', 'DFTTMPRES_final', 'DFTTO_final', 'DFTTOPRES_final', 'DFTAPSLA', 'DDN_fc_fc_bm_pgrn', \
    'DDN_bm_fc_bm_pgrn', 'SEXE', 'PATHOLOGIE_fc_fc_bm_pgrn', 'PATHOLOGIE_bm_fc_bm_pgrn', 'FAMILLE_fc_fc_bm_pgrn', 'FAMILLE_bm_fc_bm_pgrn',\
    'DEMANDE_fc_fc_bm_pgrn', 'DEMANDE_bm_fc_bm_pgrn', 'RECEPTION_fc_fc_bm_pgrn', 'RECEPTION_bm_fc_bm_pgrn', 'INDICATIONS_fc_bm_pgrn', \
    'ACTION_fc_bm_pgrn', 'APPROBATION_fc_bm_pgrn', 'DELAI_fc_bm_pgrn', 'NC_fc_bm_pgrn', 'REACTIFS_fc_bm_pgrn',\
    'ABM_NEURO_fc_bm_pgrn', 'TITRE_fc_bm_pgrn', 'PRESCRIPTEUR_fc_bm_pgrn', 'ORIGINE_fc_bm_pgrn', 'SERVICE_fc_bm_pgrn', 'DOSAGE_PGRN_fc_bm_pgrn', \
    'DFTAGDEB_fc_bm_pgrn', 'DFTAGEXAM_fc_bm_pgrn', 'DFTAPRAX_fc_bm_pgrn', 'DFTATCFAM_fc_bm_pgrn', 'DFTATCPRES_fc_bm_pgrn', 'DFTAUT_fc_bm_pgrn', \
    'DFTAUTPRES_fc_bm_pgrn', 'DFTFORMCLIN_fc_bm_pgrn', 'DFTHALLU_fc_bm_pgrn', 'DFTLCRAB_fc_bm_pgrn', 'DFTLCRABPREC_fc_bm_pgrn', \
    'DFTLCRAUT_fc_bm_pgrn', 'DFTLCRAUTPREC_fc_bm_pgrn', 'DFTLCRPT_fc_bm_pgrn', 'DFTLCRPTPREC_fc_bm_pgrn', 'DFTLCRT_fc_bm_pgrn', \
    'DFTLCRTPREC_fc_bm_pgrn', 'DFTMOD_fc_bm_pgrn', 'DFTMODAUTRE_fc_bm_pgrn', 'DFTMVAN_fc_bm_pgrn', 'DFTMVANPRES_fc_bm_pgrn', \
    'DFTNEURIRM_fc_bm_pgrn', 'DFTNEURIRMPREC_fc_bm_pgrn', 'DFTNEURSPECT_fc_bm_pgrn', 'DFTNEURSPECTPREC_fc_bm_pgrn', 'DFTNEURTEST_fc_bm_pgrn', \
    'DFTNEURTESTPREC_fc_bm_pgrn', 'DFTPARK_fc_bm_pgrn', 'DFTPLS_fc_bm_pgrn', 'DFTPLSPREC_fc_bm_pgrn', 'DFTSLA_fc_bm_pgrn', 'DFTSLADEB_fc_bm_pgrn', \
    'DFTSLADEBAGE_fc_bm_pgrn', 'DFTSLADEBEMG_fc_bm_pgrn', 'DFTTC_fc_bm_pgrn', 'DFTTCPRES_fc_bm_pgrn', 'DFTTL_fc_bm_pgrn', 'DFTTLPRES_fc_bm_pgrn', \
    'DFTTM_fc_bm_pgrn', 'DFTTMPRES_fc_bm_pgrn', 'DFTTO_fc_bm_pgrn', 'DFTTOPRES_fc_bm_pgrn',  'Transmission', 'Infos cliniques suffisantes', \
    'Commentaires', 'Variant', 'Ajout de la sÃ©rie 145']


df = df[cols_final]


### Exporter csv
df.to_csv(sortie, index=False, encoding='utf-8', sep='\t')


print('\n**********************')
print('***** JOB DONE ! *****')
print('**********************\n')