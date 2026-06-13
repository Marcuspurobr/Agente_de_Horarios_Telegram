import openpyxl
from config import CAMINHO_EXCEL
def buscar_email(nome):
    wb = openpyxl.load_workbook(CAMINHO_EXCEL)
    ws = wb.active
    
    encontrados = []
    for row in ws.iter_rows(values_only=True, min_row=2):
        if row[0] and nome.lower() in row[0].lower():
            encontrados.append(row)  # salva todos que bateram
    
    if len(encontrados) == 0:
        return None  # não achou ninguém
    
    if len(encontrados) > 1:
        # retorna lista de nomes pra avisar o usuário
        nomes = []
        for pessoa in encontrados:
            nomes.append(pessoa[0])
        resposta = "Foi encontrado mais de uma pessoa com esse nome: " + ", ".join(nomes)
        return resposta

    
    return encontrados[0][1]  # achou só um, retorna o email