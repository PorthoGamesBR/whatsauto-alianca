from chaos import chaosGenerator as chaos
import random as rand
import listona as ls_pp


def main():
    while(True):
        message = input("m - digitar mensagem\nh - ver comandos\ne - sair\n")
        if message.lower()[0] == 'm':            
            message = input("Coloque sua mensagem:")
            print(process_message(message))
        elif message.lower()[0] == 'h':
            print(
            """Commands: 
 !listona, !ppnome (nome do pp), !ppnum (numero do pp),
 !addgs (numero do pp) (GS), !addxp (numero do pp) (xp)
 !chaos_hab, !dice (numero de dados + d + tipo), !chaos_effect,
 !setpp (numero do pp) (lvl ou level,gold,xp) (quantia) 
 !newpp (nome do pp)
            """)
        elif message.lower()[0] == 'e':
            exit()
    
def dice(ammount, dice_type):
    dice_result = rand.randrange(1,dice_type + 1)
    result = dice_result
    result_str = str(dice_result)
    for i in range(ammount - 1):
        dice_result = rand.randrange(1,dice_type + 1)
        result += dice_result
        result_str += f'+ {dice_result}'
    return result_str + ' = ' + str(result)

def process_message(message):
    if message == 'Mensagem de teste':
        return 'oi!'
    
    # Commands: !listona, !ppnome (nome do pp), !ppnum (numero do pp),
    # !addgs (numero do pp) (GS), !addxp (numero do pp) (xp)
    # !chaos_hab, !dice (numero de dados + d + tipo), !chaos_effect,
    # !setpp (numero do pp) (lvl ou level,gold,xp) (quantia)
    # !newpp (nome do pp)
    
    mes = message.strip('!')
    mes_ls = mes.split(' ')
    mes_ls[0] = mes_ls[0].lower()
    #TOFIX: Check if two arguments exist in messages that need more than 1 argument
        
    if mes_ls[0] == 'chaos_hab':
        return chaos.read_hab('r')  
    
    elif mes_ls[0] == 'dice':
        if len(mes_ls) > 1:
            dice_opt = mes_ls[1].split('d')
            if len(dice_opt) > 1:
                print("Dado 1:" + dice_opt[0])
                print("Dado 2:" + dice_opt[1])
            else:
                return "Formatação errada. Argumento deve ser (numero de dados + d + tipo de dado)"
            try:
                return dice(int(dice_opt[0]), int(dice_opt[1]))
            except ValueError:
                return "Valor não numérico inserido."
        else:
            return "Faltam os seguintes argumentos: Quantidade e tipo de dados"
    
    elif mes_ls[0] == 'listona':
        return ls_pp.get_listona()
    
    elif mes_ls[0] == 'ppnome':
        if len(mes_ls) > 1:
            nome = mes_ls[1]
            for string in mes_ls[2:]:
                nome += " " + string
            pp = ls_pp.get_personagem_by_name(nome)
            if pp:
                if isinstance(pp, ls_pp.Personagem):
                    return ls_pp.Personagem.generate_list_str(pp,pp.id)
                else:
                    return pp
            else:
                return "ERRO: Personagem não encontrado"
        else:
            return "ERRO: Faltam os seguintes argumentos: Nome do Personagem"
        
    elif mes_ls[0] == 'ppnum':
        if len(mes_ls) > 1:
            try:
                pp_id = int(mes_ls[1])
            except ValueError:
                return "ERRO: Valor não numérico inserido no argumento 1: " + mes_ls[1]
            pp = ls_pp.get_personagem_by_id(pp_id=pp_id)
            if pp:
                if isinstance(pp, ls_pp.Personagem):
                    return ls_pp.Personagem.generate_list_str(pp,pp.id)
                else:
                    return pp
            else:
                return "ERRO: Personagem não encontrado"
        else:
            return "ERRO: Faltam os seguintes argumentos: ID do Personagem"
    
    elif mes_ls[0] == 'addgs':
        if len(mes_ls) > 2:
            try:
                pp_id = int(mes_ls[1])
            except ValueError:
                return "ERRO: Valor não numérico inserido no argumento 1: " + mes_ls[1]
            try:
                gold_add = int(mes_ls[2])
            except ValueError:
                return "ERRO: Valor não numérico inserido no argumento 2: " + mes_ls[2]
            
            pp = ls_pp.add_gold_pp(pp_id=pp_id,value=gold_add)
            if pp:
                if isinstance(pp, ls_pp.Personagem):
                    return ls_pp.Personagem.generate_list_str(pp,pp.id)
                else:
                    return pp
            else:
                return "ERRO: Personagem não encontrado"
        else:
            return "ERRO: Menos argumentos do que esperado. São necessários: ID Do personagem, Quantidade de G$"
        
    elif mes_ls[0] == 'addxp':
        if len(mes_ls) > 2:
            try:
                pp_id = int(mes_ls[1])
            except ValueError:
                return "ERRO: Valor não numérico inserido no argumento 1: " + mes_ls[1]
            try:
                xp_add = int(mes_ls[2])
            except ValueError:
                return "ERRO: Valor não numérico inserido no argumento 2: " + mes_ls[2]
            
            addxp_list = ls_pp.add_xp_pp(pp_id=pp_id,value=xp_add)
            if addxp_list:
                if isinstance(addxp_list[0], ls_pp.Personagem):
                    return ls_pp.Personagem.generate_list_str(addxp_list[0],addxp_list[0].id) + "\n" + addxp_list[1]
                else:
                    return addxp_list
            else:
                return "ERRO: Personagem não encontrado"
        else:
             return "ERRO: Menos argumentos do que esperado. São necessários: ID Do personagem, Quantidade de XP"
    
    elif mes_ls[0] == 'setpp':
        #PARA USO APENAS DA ADMNISTRAÇÂO DIRETAMENTE PELO CONSOLE.
        #NÃO DEVE SER ADICIONADO COMO COMANDO
        try:
            pp_id = int(mes_ls[1])
        except ValueError:
            return "ERRO: Valor não numérico inserido no argumento 1: " + mes_ls[1]
        try:
            xp_add = int(mes_ls[3])
        except ValueError:
            return "ERRO: Valor não numérico inserido no argumento 3: " + mes_ls[3]
        
        pp = ls_pp.change_pp_listona(pp_id=pp_id,
                                     value=xp_add,
                                     pp_char=mes_ls[2])
        if pp:
            if isinstance(pp, ls_pp.Personagem):
                return ls_pp.Personagem.generate_list_str(pp,pp.id)
            else:
                return pp
        else:
            return "ERRO: Personagem não encontrado"
    
    elif mes_ls[0] == 'newpp':
        if len(mes_ls) > 1:
            nome = ""
            for i in mes_ls[1:]:
                nome += f"{i} "
            nome = nome.lstrip(' ')
            nome = nome.rstrip(' ')
                
            ls_pp.add_personagem(ls_pp.Personagem(nome=nome))
            
            pp = ls_pp.get_personagem_by_name(nome)
            if pp:
                if isinstance(pp, ls_pp.Personagem):
                    return ls_pp.Personagem.generate_list_str(pp,pp.id)
                else:
                    return pp
            else:
                return "Personagem não foi criado."
        else: 
            return "ERRO: Faltam os seguintes argumentos: Nome do Personagem"

if __name__ == '__main__':
    main()