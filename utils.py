import os

def retorna_float_valor(val):
    if ',' in val:
        return str(val.replace(',','.'))
def caminho_imagem(folder_principal,nome_arq):
    return os.path.join(folder_principal,nome_arq)