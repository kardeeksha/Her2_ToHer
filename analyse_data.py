from data_interactions import drug_rxcui, list_drugs
import pandas as pd
path = "C:\\Users\\Helen Flynn\\Documents\\Github\\Her2_ToHer\\"


def column_get(mut_name):

    mut_fil = pd.read_csv(path+mut_name+".csv")
    df_1 = mut_fil[['Drug', 'Effect size']]
    return df_1


# this is the list of mutations present in the data
list_name = ["BRCA1", "BRCA2"]


def calc_col(list_name):
    d = pd.DataFrame(columns=['Drug', 'Effect size'])
    for x in list_name:
        temp = column_get(x)
        temp = temp.groupby('Drug', as_index=False).mean()
        d = pd.merge(d, temp, how='outer', on='Drug')
    d.to_csv(path+"out.csv")


calc_col(list_name)

out = pd.read_csv(path+"out.csv")
out['sum'] = out['Effect size_y'] + out['Effect size']

drug_suggested = out.nsmallest(20, 'sum')
drug_harm = out.nlargest(5, 'sum')

drug_suggested[['Drug', 'sum']].to_csv(path+"suggested.csv")
drug_harm[['Drug', 'sum']].to_csv(path+"harm.csv")

l_patient = ['lipitor']  # list of drugs given by patient (already taking)
sugg = pd.read_csv(path+"suggested.csv")
for p in l_patient:
    inter = list_drugs(drug_rxcui(p))
    for index, row in sugg.iterrows():
           if row['Drug'] in inter:
                sugg = sugg.drop(index)
sugg=sugg.nsmallest(5,'sum')
print(sugg)
print(",".join(list(sugg[['Drug']].split())))
#.to_csv(path+"suggested.csv")
