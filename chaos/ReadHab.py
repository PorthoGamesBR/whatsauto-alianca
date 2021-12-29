import csv, random

def get_keyset(filename):
   with open("chaos/" + filename, "r") as file:
        reader = csv.DictReader(file)
        
        return reader.fieldnames
     
def get_hab_dict(filename):
     dict_from_csv = {}
     with open("chaos/" + filename, "r") as file:
        reader = csv.DictReader(file)
        nome_key = get_nome_key(filename)
        desc_key = get_desc_key(filename)
        for row in reader:
           dict_from_csv[row[nome_key]] = row[desc_key]
        
        return dict_from_csv
     
def get_hab_desc(filename,hab_name):
   desc = "empty"
   name_key = get_nome_key(filename)
   desc_key = get_desc_key(filename)
   with open("chaos/" + filename, "r") as file:
      reader = csv.DictReader(file)
      for row in reader:
         if row[name_key].lower() == hab_name.lower():
            desc = row[desc_key] 
   return desc
      
def get_hab(filename):
    with open("chaos/" + filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)
        return random.choice(rows)

def get_nome_key(filename):
    nome_ind = get_nome_ind(filename)
    keyset = get_keyset(filename) 
    name_key = keyset[nome_ind] 
    return name_key

def get_desc_key(filename):
    nome_ind = get_nome_ind(filename)
    keyset = get_keyset(filename) 
    desc_key = keyset[nome_ind + 1]
    return desc_key

def get_nome_ind(filename):
    nome_ind = 0
    keyset = get_keyset(filename) 
    for k in keyset:
        if k.lower() == 'nome':
            break
        nome_ind += 1
    return nome_ind
