from getpass import getpass
from mysql.connector.constants import ClientFlag
from mysql.connector import connect, Error

connection_data = open('.connectiondata', 'r')
password = connection_data.readline().replace('\n','')
host = connection_data.readline().replace('\n','')
database_name = connection_data.readline().replace('\n','')

config = {
    'user' : 'root',
    'password' : password,
    'host' : host,
    'client_flags' : [ClientFlag.SSL],
    'ssl_ca' : 'server-ca.pem',
    'ssl_cert' : 'client-cert.pem',
    'ssl_key' : 'client-key.pem',
    'database' : database_name
} 


    
#Classe personagem, que contem os dados a adicionar na lista   
class Personagem:
    def __init__(self,nome="New Character",nivel=1,xp=0,gold=20000,id=0):
        self.nome = nome
        self.nivel = int(nivel)
        self.xp = int(xp)
        self.gold = int(gold)
        self.id = int(id)
        
    def generate_list_str(pp_tuple,id = 0):
        if isinstance(pp_tuple, Personagem):
            list_str = f"{id} - {pp_tuple.nome}/{pp_tuple.nivel}/{pp_tuple.xp:,} XP/{pp_tuple.gold:,} G$"
            return list_str
        else:
            list_str = f"{pp_tuple[0]} - {pp_tuple[1]}/{pp_tuple[2]}/{int(pp_tuple[3]):,} XP/{int(pp_tuple[4]):,} G$"
            return list_str
        
    def add_xp(self,ammount):
        lista_de_up ={
            15 : 19000,
            16 : 26000,
            17 : 27000,
            18 : 28000,
            19 : 29000,
            20 : 30000          
         }
        total_xp = self.xp + ammount
        xp_to_up = lista_de_up[self.nivel]
        while total_xp > xp_to_up:
            total_xp -= xp_to_up
            self.nivel += 1
            xp_to_up = lista_de_up[self.nivel]
            
        self.xp = total_xp
        
    def __repr__(self):
        return f"{self.nome}/{self.nivel}/{self.xp:,} XP/{self.gold:,} G$"
        
db_table_name = "listona"

def init_table():
    cnxn = connect(**config)
    cursor = cnxn.cursor()
    cursor.execute("SHOW TABLES LIKE '" + db_table_name + "'")
    result = cursor.fetchone()

    #Create first table. Should only be done one time
    if not result:
        create_table = """
        CREATE TABLE """ + db_table_name + """(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            nivel INT,
            xp INT,
            gold INT
        )

        """
        cursor.execute(create_table)
        cnxn.commit()
        
    cursor.close()

init_table()

#Função que adiciona os dados no banco de dados
def add_personagem(pp):
    insert_pp_query = """
    INSERT INTO """ + db_table_name + """ (nome, nivel, xp, gold)
    VALUES
        ("%s", %i, %i, %i)"""
    if isinstance(pp, Personagem):
       complete_query = insert_pp_query % (pp.nome, pp.nivel, pp.xp, pp.gold) 
         
       try:
            with connect(**config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(complete_query)
                    connection.commit()
                    print(f'"{pp.nome}" Adicionado com sucesso!')
       except Error as e:
            print(e)
    else:
       print("Não é um personagem, não pode ser adicionado.")

#Função para ler os personagens da lista
def get_listona():
    select_personagens_query = "SELECT * FROM " + db_table_name
    pp_list = ""
    
    try:
        with connect(**config) as connection:
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(select_personagens_query)
                result = cursor.fetchall()
                print("Listona lida com sucesso!")
                for row in result:
                    pp_list += Personagem.generate_list_str(row) + '\n'               
    except Error as e:
        print(e)
        
    return pp_list
        
#Função para pegar personagem especifico da lista
def get_personagem_by_name(pp_name):
    select_personagens_query = f"""
    SELECT * 
    FROM {db_table_name}
    WHERE nome = %s
    %s
    """
    val_tuple = (pp_name,"")
    
    pp = Personagem()
    
    try:
        with connect(**config) as connection:
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(select_personagens_query,val_tuple)
                result = cursor.fetchone()
                if result:
                    print(Personagem.generate_list_str(result))               
                    pp = Personagem(result[1],result[2],result[3],result[4],result[0])
                else:
                    pp = ""   
                cursor.fetchall()            
    except Error as e:
        print(e)
        
    return pp
        
#Função para pegar personagem especifico da lista pelo número
def get_personagem_by_id(pp_id):
    select_personagens_query = f"""
    SELECT * 
    FROM {db_table_name}
    WHERE id = %s
    %s
    """
    val_tuple = (str(pp_id), "")

    
    try:
        with connect(**config) as connection:
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(select_personagens_query,val_tuple)
                result = cursor.fetchone()
                #print(Personagem.generate_list_str(result))
                if result:                
                    pp = Personagem(result[1],result[2],result[3],result[4],result[0])
                else:
                    pp = ""
                cursor.fetchall()            
    except Error as e:
        print(e)   
    return pp

#Mudar alguma coisa em um personagem da listona
def change_pp_listona(pp_id, pp_char, value):
    if pp_char.lower() == 'lvl':
        pp_char = 'nivel'
        
    #nivel, xp, gold
    change_pp_query = f"""
    UPDATE
        {db_table_name}
    SET
        {pp_char} = %s
    WHERE
        id = %s
    """
    
    val_tuple = (str(value),str(pp_id))
    
    select_personagens_query = f"""
    SELECT * 
    FROM {db_table_name}
    WHERE id = %s
    %s
    """
    select_tuple = (str(pp_id), "")
    
    try:
        with connect(**config) as connection:
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(select_personagens_query,select_tuple)
                result = cursor.fetchone()
                if result:
                    cursor.fetchall()
                    cursor.execute(change_pp_query,val_tuple)
                    connection.commit()
                    cursor.execute(select_personagens_query,select_tuple)
                    result = cursor.fetchone()
                    cursor.fetchall()
                    return Personagem(result[1],result[2],result[3],result[4],result[0])             
                else:
                    cursor.fetchall()
                    return "Erro: personagem não encontrado"                             
    except Error as e:
        print(e)

#Limpar tabela inteira (Para carregar a listona de uma vez só)
def clear_table():
    clear_query = "TRUNCATE TABLE " + db_table_name
    awnser = input("Are you sure that you want to delete all from '" + db_table_name + "' ?(y/n)")
    if awnser.lower()[0] == 'y':
        try:
            with connect(**config) as connection:
                with connection.cursor(buffered = True) as cursor:
                    cursor.execute(clear_query)
                    connection.commit()
                    print("Tabela limpa com sucesso!")             
        except Error as e:
            print(e)
 
def add_gold_pp(pp_id, value):
    add_value_query = f"""
    UPDATE 
        {db_table_name} 
    SET 
        gold = gold + %s 
    WHERE 
        id = %s;
    
    SELECT * 
    FROM {db_table_name}
    WHERE 
        id = %s
    """
    val_tuple = (str(value),str(pp_id),str(pp_id))
    
    try:
        with connect(**config) as connection:
            with connection.cursor(buffered = True) as cursor:
                for result in cursor.execute(add_value_query,val_tuple,multi=True):
                    if result.with_rows:
                        result = cursor.fetchone()
                        if result:                
                            pp = Personagem(result[1],result[2],result[3],result[4],result[0])
                        else:
                            pp = ""
                        cursor.fetchall() 
                connection.commit()          
             
    except Error as e:
        print(e)
    
    return pp

def add_xp_pp(pp_id, value):
    select_personagens_query = f"""
    SELECT * 
    FROM {db_table_name}
    WHERE id = %s
    %s
    """
    val_tuple = (str(pp_id), "")
        
    change_pp_query = f"""
    UPDATE
        {db_table_name}
    SET
        nivel = %s,
        xp = %s     
    WHERE
        id = %s
    """

    try:
        with connect(**config) as connection:
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(select_personagens_query,val_tuple)
                result = cursor.fetchone()
                if result:             
                    pp = Personagem(result[1],result[2],result[3],result[4],result[0])
                    pp.add_xp(value)
                    cursor.fetchall()
                else:
                    cursor.fetchall()
                    return ""
                
                
                change_tuple = (str(pp.nivel), str(pp.xp),str(pp_id))
                cursor.execute(change_pp_query,change_tuple)
                connection.commit()             
                              
    except Error as e:
        print(e)
    return pp  
    