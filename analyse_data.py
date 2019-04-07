<<<<<<< HEAD
import pandas as pd
path="C:\\Users\\Helen Flynn\\Documents\\Github\\Her2_ToHer"
=======
"""
inputs: path = document path
list_name= list of mutations present in the data
l_patient= list given by paitent of the drugs they are already taking
"""

path="D:/documents/work/athena_try/"
import pandas as pd
>>>>>>> 2917dc12f934cc1d0d9ff4cd18a617e4d17d554d
def column_get(mut_name):

    mut_fil=pd.read_csv(path+mut_name+".csv")
    df_1=mut_fil[['Drug','Effect size']]
    return df_1

list_name=["BRCA1","BRCA2"] ##this is the list of mutations present in the data
def calc_col(list_name):
<<<<<<< HEAD
=======

>>>>>>> 2917dc12f934cc1d0d9ff4cd18a617e4d17d554d
    d = pd.DataFrame(columns=['Drug','Effect size'])
    for x in list_name:
        temp = column_get(x)
        temp=temp.groupby('Drug', as_index=False).mean()
        d= pd.merge(d, temp, how='outer', on='Drug')
    d.to_csv(path+"out.csv")

calc_col(list_name)

<<<<<<< HEAD
=======

>>>>>>> 2917dc12f934cc1d0d9ff4cd18a617e4d17d554d
out=pd.read_csv(path+"out.csv")
out['sum'] = out['Effect size_y'] + out['Effect size']

drug_suggested= out.nsmallest(20,'sum')
# drug_harm = out.nlargest(5,'sum')

drug_suggested[['Drug','sum']].to_csv(path+"suggested.csv")
<<<<<<< HEAD
drug_harm[['Drug','sum']].to_csv(path+"harm.csv")
=======
# drug_harm[['Drug','sum']].to_csv(path+"harm.csv")


from data_interactions import drug_rxcui,list_drugs
l_patient=['lipitor'] ##list of drugs given by patient (already taking)
sugg=pd.read_csv(path+"suggested.csv")
for p in l_patient:
    inter= list_drugs(drug_rxcui(p))
    for index, row in sugg.iterrows():
           if row['Drug'] in inter:
                sugg=sugg.drop(index)
sugg.to_csv(path+"suggested.csv")
>>>>>>> 2917dc12f934cc1d0d9ff4cd18a617e4d17d554d
