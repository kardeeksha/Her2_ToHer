# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from ensemblrest import EnsemblRest
import random
import pandas as pd
from data_interactions import drug_rxcui, list_drugs


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def rand_pt_genes(standards, mutations, pt_genes):
    brca1_pt = random.choice(brca1)
    pt_genes.append(brca1_pt)
    brca2_pt = random.choice(brca2)
    pt_genes.append(brca2_pt)
    chek2_pt = random.choice(chek2)
    pt_genes.append(chek2_pt)
    pten_pt = random.choice(pten)
    pt_genes.append(pten_pt)
    tp53_pt = random.choice(tp53)
    pt_genes.append(tp53_pt)
    return pt_genes


ensRest = EnsemblRest()
server = "http://rest.ensembl.org"

# standard sequence API data
standards = []
brca1_seq = ensRest.getSequenceById(id='ENSG00000012048')
brca2_seq = ensRest.getSequenceById(id='ENSG00000139618')
chek2_seq = ensRest.getSequenceById(id='ENSG00000183765')
pten_seq = ensRest.getSequenceById(id='ENSG00000171862')
tp53_seq = ensRest.getSequenceById(id='ENSG00000141510')

for i in (brca1_seq, brca2_seq, chek2_seq, pten_seq, tp53_seq):
    standards.append(i['seq'])

# mutation dash_table
mutations = []
brca1_mut = ensRest.getSequenceById(id =  'ENST00000357654?content-type=text/x-fasta;type=cdna')
brca2_mut = ensRest.getSequenceById(id = 'ENST00000380152?content-type=text/x-fasta;type=cdna')
chek2_mut = ensRest.getSequenceById(id = 'ENST00000382580?content-type=text/x-fasta;type=cdna')
pten_mut = ensRest.getSequenceById(id = 'ENST00000371953?content-type=text/x-fasta;type=cdna')
tp53_mut = ensRest.getSequenceById(id = 'ENST00000269305?content-type=text/x-fasta;type=cdna')

for i in (brca1_mut, brca2_mut, chek2_mut, pten_mut, tp53_mut):
    mutations.append(i['seq'])

random.randint(1, 20)
brca1 = [standards[0], mutations[0]]
brca2 = [standards[1], mutations[1]]
chek2 = [standards[2], mutations[2]]
pten = [standards[3], mutations[3]]
tp53 = [standards[4], mutations[4]]


pt_genes = []
pt_genes = rand_pt_genes(standards, mutations, pt_genes)
pt_genes_NaN = []


for i in range(len(pt_genes)):
    x = random.randint(1, 10)
    if x < 7:
        pt_genes_NaN.append('NaN')
    else:
        pt_genes_NaN.append('MUT')


df = pd.read_csv('C:\\Users\\Helen Flynn\\Documents\\GitHub\\Her2_ToHer\\cBioPortal_data (1).txt', sep = '\t' ,names = ('Common', 'BRCA1', 'BRCA2', 'CHEK2', 'PTEN', 'TP53'))
df = df[2:]
id1 = 'MB-0350'

def return_muts(id1):
    target = df.loc[id1].notnull()
    return (list(df.columns[target]))

list_name = (return_muts(id1))

df = df.reset_index()

path = "C:\\Users\\Helen Flynn\\Documents\\Github\\Her2_ToHer\\"

def column_get(mut_name):
    mut_fil = pd.read_csv(path+mut_name+".csv")
    df_1 = mut_fil[['Drug', 'Effect size']]
    return df_1

list_name = (list_name) ## this is the list of mutations present in the data
def calc_col(list_name):
    d = pd.DataFrame(columns = ['Drug', 'Effect size'])
    for x in list_name:
        temp = column_get(x)
        temp = temp.groupby('Drug', as_index=False).mean()
        d= pd.merge(d, temp, how = 'outer', on='Drug')
    d.to_csv(path+"out.csv")

calc_col(list_name)

out=pd.read_csv(path+"out.csv")
try:
    out['sum'] = out['Effect size_y'] + out['Effect size']
except KeyError:
    out['sum'] = out['Effect size_y']

drug_suggested = out.nsmallest(20, 'sum')
hugg = out.nlargest(5, 'sum')
df_harm=hugg[['Drug']]


l_patient = ['lipitor']  # list of drugs given by patient (already taking)
sugg = pd.read_csv(path+"suggested.csv")
for p in l_patient:
    inter = list_drugs(drug_rxcui(p))
    for index, row in sugg.iterrows():
           if row['Drug'] in inter:
                sugg = sugg.drop(index)
sugg=sugg.nsmallest(5,'sum')
df2=sugg[['Drug']]

#.to_csv(path+"suggested.csv")


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children = "HER2her: Our Technology, Your Future.",
    style = {
        'textAlign' : 'center',
        'color' : 'black'
    }
    ),
    dcc.Upload(id='upload-data',
        children=html.Div([
            'Drag and Drop Single Patient Data (.txt or .csv) or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'backgroundColor' : '#FFDFD3',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }),
    html.Div([
       dcc.Input(placeholder='Enter Current Medications...', type="text", id='my-id', value='Lipitor'),
       html.Button('Submit', id='button'),
       html.Div(id='my-div2')
],
       style={
           'width': '100%',
           'height': '130px',
           'lineHeight': '60px',
           'borderWidth': '1px',
           'borderStyle': 'dashed',
           'backgroundColor' : 'pink',
           'borderRadius': '5px',
           'textAlign': 'center',
           'margin': '10px'
       }),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        sorting=True,
        sorting_type="multi",
        style_table={
            'maxHeight' : '300',
            'overflowY' : 'scroll',
            'border':0,
            'align' : 'center'},
        style_cell_conditional=[{
        'if': {'row_index': 'odd'},
        'backgroundColor': '#FFDFD3'
    }],
    ),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'BRCA1', 'value': 'BRCA1'},
            {'label': 'BRCA2', 'value': 'BRCA2'},
            {'label': 'CHEK2', 'value': 'CHEK2'},
            {'label': 'PTEN', 'value': 'PTEN'},
            {'label': 'TP53', 'value': 'TP53'}
        ],
        value=list_name,
        multi=True
    ),
    html.Div(id='my-div'),
    dash_table.DataTable(
        id='medtable',
        columns=[{"name": i, "id": i} for i in df2.columns[1:]],
        data=df2.to_dict("rows"),
        style_table={
            'padding' : '20px',
            'align' : 'center'
            },
    ),
        html.P('We would like to provide you with an interactive map of available cancer care providers to consult as you navigate through your medical journey.'
        ),
    html.Iframe(
      width="600",
      height="450",
      style={
        'border':0,
        'padding' : '50px',
       },
      src="https://www.google.com/maps/embed/v1/search?key=AIzaSyACU8QODHAUXs0igLHiqeFgUQaiNPNUGQ0&q=oncology+center"
      )
    ])



@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value')]
)
def update_output_div(input_value):
    return "Patient {}, we\'ve detected the following mutated genes: {}. The chemotherapy options formulated to work best with the mutations are below, as well as their relative efficacy score based on drug-drug and gene interactions. Please discontinue the following medications based on counterindications from your current medications: {}".format(id1,input_value,df2.to_string(index=False))

@app.callback(Output(component_id='my-div2', component_property='children'),
   [Input('button', 'n_clicks')],
   state=[State(component_id='my-id', component_property='value')]
)

def update_meds(n_clicks, input_val):
   return 'You are currently taking "{}"'.format(input_val)# @app.callback(Output(component_id='medtable', component_property='data'), [Input(component_id='my-dropdown', component_property='value')])
# def update_rows(input_value):
#     calc_col(input_value)
#     drug_suggested= out.nsmallest(5,('sum'[:4]))
#     drug_harm = out.nlargest(5,'sum')
#     drug_suggested[['Drug','sum']].to_csv(path+"suggested.csv")
#     drug_harm[['Drug','sum']].to_csv(path+"harm.csv")
#     columns=[{"name": i, "id": i} for i in df2.columns[1:]],
#     pd.read_csv(path+'suggested.csv'),
#     df_1 = mut_fil[['Drug', 'Effect size']]
#     data = df_1.to_dict('rows')
#     return data,columns

# # callback table creation
# @app.callback(Output('table', 'data'),
#               [Input('upload-data', 'contents'),
#                Input('upload-data', 'filename')])
# def update_output(contents, filename):
#     if contents is not None:
#         print("contents is None")
#         df = pd.read_csv(io.StringIO(base64.b64decode(filename).decode('utf-8')), sep='\t', names=('Common', 'BRCA1', 'BRCA2', 'CHEK2', 'PTEN', 'TP53'))
#         df=df[2:]
#         df=df.,reset_index()
#         print(df,contents)
#         if df is not None:
#             print("df is not None")
#             df.append(data)
#             return df.to_dict('rows')
#         else:
#             print("df is None")
#             return [{}]
#     else:
#         print("contents is not None")
#         return [{}]

if __name__ == '__main__':
    app.run_server(debug=True)
