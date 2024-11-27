import spacy

# Load the NER model
nlp = spacy.load('en_ner_bc5cdr_md')
# Increase the max_length to avoid the error "ValueError: [E088] Text of length 1200001 exceeds maximum of 1000000."
nlp.max_length = 1200000

text = """Aspirin is a nonsteroidal antiinflammatory drug and this drug is used as an analgesic, antipyretic, and in the treatment of rheumatoid arthritis and acute rheumatic fever.

Aspirin at high dosages may increase vitamin C excretion in the urine and decrease vitamin C absorption in the small intestine. 
Vitamin C may protect the stomach mucosa from aspirin-induced injury, presumably by inhibiting inducible nitric oxide synthase expression(Konturek et al., 2006). 
Further, supplemental vitamin E in high amounts may enhance aspirin’s antiplatelet effects"
"""

doc = nlp(text)

chemicals = []
diseases = []

for ent in doc.ents:
    ent_label = ent.label_

    #convert to lowercase to avoid case sensitive duplication
    ent_text = ent.text.lower()

    #remove extended ascii characters
    ent_text = ent_text.encode('ascii', 'ignore').decode('ascii')
    
    #remove special characters except - and /
    ent_text = ''.join(e for e in ent_text if e.isalnum() or e == ' ' or e == '-' or e == '/')
    ent_text = ent_text.strip()
    
    #if starts with - or /, remove it
    if ent_text.startswith('-') or ent_text.startswith('/'):
        ent_text = ent_text[1:].strip()
    
    if ent_label == 'CHEMICAL' and ent_text not in chemicals:
        chemicals.append(ent_text)

    if ent_label == 'DISEASE' and ent_text not in diseases:
        diseases.append(ent_text)

print('Chemicals', chemicals)
print('Diseases', diseases)
        