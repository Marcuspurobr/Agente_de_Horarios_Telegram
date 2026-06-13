import openpyxl
from config import CAMINHO_EXCEL, FONTE_MEMBROS, SHEETS_ID

def buscar_email(nome,sheets_service=None):
    if FONTE_MEMBROS == "sheets":
        return buscar_email_sheets(sheets_service,nome)
    else:
        return buscar_email_excel(nome)

def buscar_email_sheets(sheets_service, nome):
    resultado = sheets_service.spreadsheets().values().get(
        spreadsheetId=SHEETS_ID,
        range="A2:B"  # A = nomes, B = emails, pula cabeçalho
    ).execute()
    
    rows = resultado.get("values", [])
    
    encontrados = []
    for row in rows:
        if row[0] and nome.lower() in row[0].lower():
            encontrados.append(row)
    
    if len(encontrados) == 0:
        return None
    
    if len(encontrados) > 1:
        nomes = []
        for pessoa in encontrados:
            nomes.append(pessoa[0])
        resposta = "Foi encontrado mais de uma pessoa com esse nome: " + ", ".join(nomes)
        return resposta
    
    return encontrados[0][1]


def buscar_email_excel(nome):
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