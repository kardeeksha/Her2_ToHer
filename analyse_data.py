path="D:/documents/work/athena_try/"
def column_get(mut_name):
    import pandas as pd
    mut_fil=pd.read_csv(path+mut_name+".csv")
    df_1=mut_fil[['Drug','Effect size']]
    return df_1

list_name=["BRCA1","BRCA2"] ##this is the list of mutations present in the data
def calc_col(list_name):
    import glob2
    import pandas as pd
    d = pd.DataFrame(columns=['Drug','Effect size'])
    for x in list_name:
        temp = column_get(x)
        temp=temp.groupby('Drug', as_index=False).mean()
        d= pd.merge(d, temp, how='outer', on='Drug')
    d.to_csv(path+"out.csv")

calc_col(list_name)

import pandas as pd
out=pd.read_csv(path+"out.csv")
out['sum'] = out['Effect size_y'] + out['Effect size']

drug_suggested= out.nsmallest(5,'sum')
drug_harm = out.nlargest(5,'sum')

drug_suggested[['Drug','sum']].to_csv(path+"suggested.csv")
drug_harm[['Drug','sum']].to_csv(path+"harm.csv")

