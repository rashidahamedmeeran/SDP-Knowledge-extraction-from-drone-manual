import re
import textract
from pyinflect import getAllInflections
from nltk.tokenize import word_tokenize
from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://3.84.148.75:7687",auth=basic_auth("neo4j", "bytes-bridge-markets"))

files = ['Freefly ALTA 8 Specifications - Dimensions, Weight & Payload.pdf',
         'alta-8-pro-manual.pdf',
         'Matrice_600_User_Manual_v1_EN_1208.pdf',
         'anafi_user_guide_v6.7.0.1.pdf',
         'Elios 2 - Brochure EN LW.pdf']

def extract_text(file_name):
    text = textract.process(file_name).decode("utf-8")
    page_pattern = re.compile(r'(^\x0c)\x0c')
    text = re.split("\x0c",text)[0:-1]
    for page_num,page_text in enumerate(text):
        text[page_num] = re.split("\n\n",page_text)[0:-1]
        for sent_num, sent_text in enumerate(text[page_num]):
            text[page_num][sent_num] = re.sub("\n"," ",sent_text)
    return text

def find_dim(text,file_name):
    
    with driver.session(database="neo4j") as session:
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name}) MERGE (m)-[p:Prop]-(f:Features{name: 'Dimension'})", name=file_name).data())

    dim_words = ['dimension','diameter','height','width']
    type_words = ['fold','unfold']
    dim_syn = [i[0] for j in dim_words for i in list(getAllInflections(j).values())]
    type_syn = [i[0] for j in type_words for i in list(getAllInflections(j).values())]
    
    result = {}
    dim_pattern = re.compile(r'\d+[.]?\d*[ ]?mm|\d+[.]?\d*[ ]?cm')
    
    for page_num,page_text in enumerate(text):
        for sent_num, sent_text in enumerate(text[page_num]):

            matches = dim_pattern.findall(sent_text)
            sent_text = sent_text.lower()
            temp_sent = sent_text
            
            for num,match in enumerate(matches):
                dim3_pattern = re.compile(r'\d+[ ]?[xX][ ]?\d+[ ]?[xX][ ]?%s'%match)
                dim3_match = re.findall(dim3_pattern,temp_sent)
                if (len(dim3_match)!=0):
                    matches[num] = dim3_match[0]
                    temp_sent = re.sub(r'%s'%dim3_match[0],' ',temp_sent)
                    
            for match in matches:
                splitted = re.split(r'%s'%match,sent_text)
                tokens = word_tokenize(splitted[0])
                dim_flag = 0
                type_flag = 0
                prop = ''
                for wd in tokens:
                    if wd in dim_syn:
                        prop = wd
                        dim_flag = 1
                        break
                if (dim_flag==0):
                    prev_sent = text[page_num][sent_num-1].lower()
                    tks = word_tokenize(prev_sent)
                    for wd in tks:
                        if wd in dim_syn:
                            prop = wd
                            dim_flag = 1
                            break
                for wd in tokens:
                    if wd in type_syn:
                        prop = wd + ' ' + prop
                        type_flag = 1
                        break
                if (type_flag==0):
                    prev_sent = text[page_num][sent_num-1].lower()
                    tks = word_tokenize(prev_sent)
                    for wd in tks:
                        if wd in type_syn:
                            prop = wd + ' ' + prop
                            type_flag = 1
                            break
                if prop!='':
                    result[prop] = match
                sent_text = splitted[1]
    print('\n')
    print('----------')
    print('Dimensions:')
    print('----------')
    
    if (len(result)!=0):
        for i in result.keys():
            print('\t'+i+':',result[i])
            with driver.session(database="neo4j") as session:
                results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Dimension'}) MERGE (f)-[t:Type]-(dt: dim_type {name:$dim_type})-[v:Value]-(dim: dim_value {name:$dim})", name=file_name,dim_type=i,dim=result[i]).data())
    else:
        print('\t'+'not specified')
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Dimension'}) MERGE (f)-[v:Value]-(dim: dim_value {name:$dim})", name=file_name,dim='not specified').data())

def find_weight(text,file_name):
    
    with driver.session(database="neo4j") as session:
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name}) MERGE (m)-[p:Prop]-(f:Features{name: 'Weight'})", name=file_name).data())

    weight_words = ['weight']
    weight_syn = [i[0] for j in weight_words for i in list(getAllInflections(j).values())]
    
    result = {}
    weight_patterns = [re.compile(r'\d+[.]?\d*[ ]?kg'),re.compile(r'\d+[.]?\d*[ ]?g')]
    
    for weight_pattern in weight_patterns:
        for page_num,page_text in enumerate(text):
            for sent_num, sent_text in enumerate(text[page_num]):

                matches = weight_pattern.findall(sent_text)
                sent_text = sent_text.lower()
                temp_sent = sent_text
                
                for match in matches:
                    splitted = re.split(r'%s'%match,sent_text)
                    tokens = word_tokenize(splitted[0])
                    weight_flag = 0
                    type_flag = 0
                    prop = ''
                    for wd in tokens:
                        if wd in weight_syn:
                            prop = wd
                            weight_flag = 1
                            break
                    if (weight_flag==0):
                        prev_sent = text[page_num][sent_num-1].lower()
                        tks = word_tokenize(prev_sent)
                        for wd in tks:
                            if wd in weight_syn:
                                prop = wd
                                weight_flag = 1
                                break
                    if prop!='':
                        result[prop] = match
                    sent_text = splitted[1]
                    
        if result!={}:
            break
            
    print('\n')
    print('------')
    print('Weight:')
    print('------')
    
    if (len(result)!=0):
        for i in result.keys():
            print('\t'+result[i])
            with driver.session(database="neo4j") as session:
                results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Weight'}) MERGE (f)-[v:Value]-(wt: weight_value {name:$weight})", name=file_name,weight=result[i]).data()) 
    else:
        print('\t'+'not specified')
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Weight'}) MERGE (f)-[v:Value]-(wt: weight_value {name:$weight})", name=file_name,weight='not specified').data())

def find_payload(text,file_name):
    
    with driver.session(database="neo4j") as session:
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name}) MERGE (m)-[p:Prop]-(f:Features{name: 'Payload'})", name=file_name).data())
            
    payload_words = ['payload']
    payload_syn = [i[0] for j in payload_words for i in list(getAllInflections(j).values())]
    
    result = {}
    payload_patterns = [re.compile(r'\d+[.]?\d*[ ]?kg'),re.compile(r'\d+[.]?\d*[ ]?g'),re.compile(r'\d+[.]?\d*[ ]?lbs')]
    
    for payload_pattern in payload_patterns:
        for page_num,page_text in enumerate(text):
            for sent_num, sent_text in enumerate(text[page_num]):

                matches = payload_pattern.findall(sent_text)
                sent_text = sent_text.lower()
                temp_sent = sent_text
                
                for match in matches:
                    splitted = re.split(r'%s'%match,sent_text)
                    tokens = word_tokenize(sent_text)
                    payload_flag = 0
                    type_flag = 0
                    prop = ''
                    for wd in tokens:
                        if wd in payload_syn:
                            prop = wd
                            payload_flag = 1
                            break
                    if (payload_flag==0):
                        prev_sent = text[page_num][sent_num-1].lower()
                        tks = word_tokenize(prev_sent)
                        for wd in tks:
                            if wd in payload_syn:
                                prop = wd
                                payload_flag = 1
                                break
                    if prop!='':
                        result[prop] = match
                    sent_text = splitted[1]
                    
        if result!={}:
            break
    
    print('\n')
    print('-------')
    print('Payload:')
    print('-------')
    
    if (len(result)!=0):
        for i in result.keys():
            print('\t'+result[i])
            with driver.session(database="neo4j") as session:            
                results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Payload'}) MERGE (f)-[v:Value]-(pl: payload_value {name:$payload})", name=file_name,payload=result[i]).data())
    else:
        print('\t'+'not specified')
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Payload'}) MERGE (f)-[v:Value]-(pl: payload_value {name:$payload})", name=file_name,payload='not specified').data())

def find_limitation(text,file_name):
    
    with driver.session(database="neo4j") as session:
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name}) MERGE (m)-[p:Prop]-(f:Features{name: 'Limitation'})", name=file_name).data())

    lim_words = ['limitation']
    lim_syn = [i[0] for j in lim_words for i in list(getAllInflections(j).values())]
    
    result = []
    
    for page_num,page_text in enumerate(text):
        for sent_num, sent_text in enumerate(text[page_num]):
            sent_text = sent_text.lower()
            tokens = word_tokenize(sent_text)
            for wd in tokens:
                if wd in lim_syn:
                    if '.' in sent_text:
                        result.append(sent_text)
                    elif(len(page_text)>sent_num+1):
                        result.append(sent_text + page_text[sent_num+1])
    print('\n')
    print('-----------')
    print('Limitations:')
    print('-----------')
    
    if (len(result)!=0):
        for i in list(set(result)):
            print('\t'+i)
            with driver.session(database="neo4j") as session:
                results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Limitation'}) MERGE (f)-[t:Text]-(lim: limitations {name:$limitation})", name=file_name,limitation=i).data())
    else:
        print('\t'+'not specified')
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Limitation'}) MERGE (f)-[t:Text]-(lim: limitations {name:$limitation})", name=file_name,limitation='not specified').data())

def find_emergency_procedure(text,file_name):
    
    with driver.session(database="neo4j") as session:
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name}) MERGE (m)-[p:Prop]-(f:Features{name: 'Emergency_procedure'})", name=file_name).data())
            
    emergency_words = ['emergency']
    emergency_syn = [i[0] for j in emergency_words for i in list(getAllInflections(j).values())]
    procedure_words = ['procedure']
    procedure_syn = [i[0] for j in procedure_words for i in list(getAllInflections(j).values())]
    
    result = []
    emergency_patterns = [re.compile(r'\d+[.]?\d*[ ]?kg'),re.compile(r'\d+[.]?\d*[ ]?g')]
    
    for page_num,page_text in enumerate(text):
        for sent_num, sent_text in enumerate(text[page_num]):
            sent_text = sent_text.lower()
            tokens = word_tokenize(sent_text)
            for wd in tokens:
                if wd in emergency_syn:
                    for WD in tokens:
                        if WD in procedure_syn:
                            result_text = sent_text
                            sn = sent_num
                            flag=True
                            pg_txt = page_text
                            while(flag==True):
                                if(len(pg_txt)>sn+1):
                                    sn=sn+1
                                    next_sent_text = pg_txt[sn].lower()
                                    tokens1 = word_tokenize(next_sent_text)
                                    flag=False
                                    for wd1 in tokens1:
                                        if wd1 in emergency_syn:
                                            flag=True
                                            result_text += next_sent_text
                                            break
                                else:
                                    pg_txt = text[page_num+1]
                                    sn=-1
                            result.append(result_text)
                            
    print('\n')
    print('--------------------')
    print('Emergency procedures:')
    print('--------------------')
    
    if (len(result)!=0):
        for i in list(set(result)):
            print('\t'+i)
            with driver.session(database="neo4j") as session:
                results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Emergency_procedure'}) MERGE (f)-[t:Text]-(emergency: emergency_procedures {name:$emergency_procedure})", name=file_name,emergency_procedure=i).data())
    else:
        print('\t'+'not specified')
        results = session.write_transaction(lambda tx: tx.run("MATCH (m:Drone_Manual {name: $name})-[p:Prop]-(f:Features{name: 'Emergency_procedure'}) MERGE (f)-[t:Text]-(emergency: emergency_procedures {name:$emergency_procedure})", name=file_name,emergency_procedure='not specified').data())


for file_name in files:
    
    print('\n')
    print('='*len(file_name))
    print(file_name)
    print('='*len(file_name))
    
    with driver.session(database="neo4j") as session:
        results = session.write_transaction(lambda tx: tx.run("MERGE (m:Drone_Manual {name: $name})", name=file_name).data())
    
    text = extract_text(file_name)
    
    find_dim(text,file_name)
    find_weight(text,file_name)
    find_payload(text,file_name)
    find_limitation(text,file_name)
    find_emergency_procedure(text,file_name)
    
driver.close()