import os

def retorna_float_valor(val):
    if ',' in val:
        return str(val.replace(',','.'))
    elif '.' in val:
        return str(val.replace('.','.'))
    else:
        return str(val)
def caminho_imagem(folder_principal,nome_arq):
    return os.path.join(folder_principal,nome_arq)