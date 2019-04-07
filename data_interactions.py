import urllib.request
import xml.etree.ElementTree as ET

# drug_name="lipitor"
def drug_rxcui(drug_name):
     path_rx="https://rxnav.nlm.nih.gov/REST/rxcui?name="
     with urllib.request.urlopen(path_rx+drug_name) as response:
        html = response.read()
        root = ET.fromstring(html)
        for ID  in root.findall('idGroup'):
             RxCUI = ID.find('rxnormId').text
     return RxCUI
# rxcui=drug_rxcui(drug_name)

def list_drugs(RxCUI):
     path_in="https://rxnav.nlm.nih.gov/REST/interaction/interaction.xml?rxcui="
     list_d=[]
     with urllib.request.urlopen(path_in+RxCUI) as response:
        list_htm = response.read()
        root = ET.fromstring(list_htm)
        # Top-level elements
        root.findall(".")

        # child and grandchild extraction
        for reac in root.findall("./interactionTypeGroup/interactionType/interactionPair"):
          for x in reac.findall("interactionConcept/minConceptItem"):
            list_d.append(x.find('name').text)

     from collections import Counter
     val = Counter(list_d).most_common()[0][0]
     list_d[:] = filter(lambda a: a != val, list_d)
     return list_d
# list = list_drugs(rxcui)
