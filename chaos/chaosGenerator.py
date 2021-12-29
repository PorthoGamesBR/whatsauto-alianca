from . import AddHab as addh
from . import ReadHab as readh

filename = "chaos_hab"
csv_filename =  addh.file_name(filename)

def main():
    if not readh.get_keyset(csv_filename):
        addh.init_file(csv_filename)
    
def read_hab(opt):
    if opt == 'a':
        hab_block = ''
        hab_dict = readh.get_hab_dict(csv_filename)
        print(len(hab_dict))
        for key in hab_dict:
            hab_block += f"\n-{key}- \nDescription: {hab_dict[key]}\n"
        return hab_block
        
    elif opt == 'r':        
        hab_rand = readh.get_hab(csv_filename)
        name_ind = readh.get_nome_ind(csv_filename)
        hab_name = hab_rand[name_ind]
        hab_desc = hab_rand[name_ind + 1]
        found_hab = True
    
    elif opt == 's':
        hab_name = input("Please tipe the name of the ability: ")
        hab_desc = readh.get_hab_desc(csv_filename, hab_name)
        if hab_desc != 'empty':
            found_hab = True
        else:
            print("This ability isnt on the list")
            
    if found_hab:
        hab_block = f"\n-{hab_name}- \nDescription: {hab_desc}\n"
        return hab_block
        
       
def choose_option(opt_name):
    main()
    chosen_opt = opt_name.lower()
    if chosen_opt == '!chaos_hab':
        return read_hab('r',csv_filename)
    if chosen_opt == 'mensagem de teste':
        return read_hab('a',csv_filename)
        
        