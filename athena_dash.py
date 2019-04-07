# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Her2_Her
import requests, sys
from ensemblrest import EnsemblRest
import random
import pandas as pd

def rand_pt_genes(standards,mutations,pt_genes):
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

#standard sequence API data
standards = []
brca1_seq = ensRest.getSequenceById(id='ENSG00000012048')
brca2_seq = ensRest.getSequenceById(id='ENSG00000139618')
chek2_seq = ensRest.getSequenceById(id='ENSG00000183765')
pten_seq = ensRest.getSequenceById(id='ENSG00000171862')
tp53_seq = ensRest.getSequenceById(id='ENSG00000141510')

#assign sequence data
#brca1_seq1 = standards.append(brca1_seq['seq'])
#brca2_seq1 = standards.append(brca2_seq['seq'])
#chek2_seq1 = standards.append(chek2_seq['seq'])
#pten_seq1 = standards.append(pten_seq['seq'])
#tp53_seq1 = standards.append(tp53_seq['seq'])

for i in (brca1_seq,brca2_seq,chek2_seq,pten_seq,tp53_seq):
    standards.append(i['seq'])

#mutation dash_table
mutations = []
brca1_mut = ensRest.getSequenceById(id= 'ENST00000357654?content-type=text/x-fasta;type=cdna')
brca2_mut = ensRest.getSequenceById(id='ENST00000380152?content-type=text/x-fasta;type=cdna')
chek2_mut = ensRest.getSequenceById(id='ENST00000382580?content-type=text/x-fasta;type=cdna')
pten_mut = ensRest.getSequenceById(id='ENST00000371953?content-type=text/x-fasta;type=cdna')
tp53_mut = ensRest.getSequenceById(id='ENST00000269305?content-type=text/x-fasta;type=cdna')

for i in (brca1_mut,brca2_mut,chek2_mut,pten_mut,tp53_mut):
    mutations.append(i['seq'])

random.randint(1,20)
brca1 = [standards[0],mutations[0]]
brca2 = [standards[1],mutations[1]]
chek2 = [standards[2],mutations[2]]
pten = [standards[3], mutations[3]]
tp53 = [standards[4],mutations[4]]


pt_genes = []
pt_genes = rand_pt_genes(standards, mutations, pt_genes)
pt_genes_NaN = []


for i in range(len(pt_genes)):
    x = random.randint(1, 10)
    print(x)
    if x < 7:
        pt_genes_NaN.append('NaN')
    else:
        pt_genes_NaN.append('MUT')


df = pd.read_table('C:\\Users\\Helen Flynn\\Documents\\GitHub\\Her2_ToHer\\cBioPortal_data (1).txt',delim_whitespace=True,names=('Common','BRCA1','BRCA2','CHEK2','PTEN','TP53'))
df=df[2:]
df = df.reset_index()

#TODO 
def return_muts(id):
    return(df.loc[id].notnull())

print(return_muts('MB-0008'))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Upload Mutation Data Here (.csv,.txt) or ',
            html.A('Launch Browser')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'maxHeight' : '300',
            'overflowY' : 'scroll'
        },
    )
])




if __name__ == '__main__':
    app.run_server(debug=True)
