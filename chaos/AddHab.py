import csv
from datetime import datetime

def file_name(name):
    return name + ".csv"

def init_file(filename):
     with open("chaos/" + filename, "a") as file:
        writer = csv.writer(file)
        writer.writerow(["Carimbo de Data/Hora","Nome","Descrição"])
        
def add_hab(filename, nome, descricao):
    with open("chaos/" + filename, "a") as file:
        writer = csv.writer(file)
        now = datetime.now()
        date_string = now.strftime('%d/%m/%y %H:%M:%S')  
        writer.writerow([date_string,nome,descricao])

