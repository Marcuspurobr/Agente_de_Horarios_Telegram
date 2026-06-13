from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
import os
from config import CAMINHO_CREDENTIALS, FUSO_HORAS, CAMINHO_TOKEN

# Fuso horário de Brasília (UTC-3)
# Usamos timedelta ao invés do pytz pra não precisar instalar biblioteca extra
# Desvantagem: não lida automaticamente com horário de verão
FUSO_BRASILIA = timezone(timedelta(hours=FUSO_HORAS))

# Escopo de permissão — o que o app pode fazer na conta do Google
# "calendar" = leitura e escrita na agenda
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def autenticar_google():
    """
    Autentica com o Google Calendar.
    - Na primeira vez: abre o navegador pra fazer login
    - Nas próximas vezes: usa o token.json salvo automaticamente
    """
    creds = None

    # Verifica se já tem um token salvo de uma autenticação anterior
    if os.path.exists(CAMINHO_TOKEN):
        creds = Credentials.from_authorized_user_file(CAMINHO_TOKEN, SCOPES)

    # Se não tem credenciais válidas, precisa autenticar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Token expirado mas tem refresh token — renova automaticamente
            creds.refresh(Request())
        else:
            # Primeira vez — abre o navegador pra fazer login
            flow = InstalledAppFlow.from_client_secrets_file(CAMINHO_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva o token pra não precisar logar de novo
        with open(CAMINHO_TOKEN, "w") as token:
            token.write(creds.to_json())

    # Retorna o serviço autenticado do Google Calendar
    return build("calendar", "v3", credentials=creds)


def buscar_eventos(service, data, calendarioId="primary"):
    """
    Busca todos os eventos de um dia específico no Google Calendar.
    Recebe a data no formato brasileiro: "12/06/2026"
    """

    # Converte de "12/06/2026" para objeto de data do Python
    # %d = dia, %m = mês, %Y = ano com 4 dígitos
    data_obj = datetime.strptime(data, "%d/%m/%Y")

    # Define o início e fim do dia com fuso horário de Brasília
    # O Google Calendar precisa do formato: 2026-06-12T00:00:00-03:00
    inicio = data_obj.replace(hour=0, minute=0, second=0, tzinfo=FUSO_BRASILIA).isoformat()
    fim_dia = data_obj.replace(hour=23, minute=59, second=59, tzinfo=FUSO_BRASILIA).isoformat()

    # Consulta a API do Google Calendar
    # É como perguntar: "me dá todos os eventos entre X e Y"
    eventos = service.events().list(
        calendarId=calendarioId,   # "primary" = seu calendário principal
        timeMin=inicio,         # a partir de quando buscar
        timeMax=fim_dia,        # até quando buscar
        singleEvents=True,      # mostra eventos repetidos separados (não agrupados)
        orderBy="startTime"     # ordena por horário de início
    ).execute()

    # A resposta vem assim:
    # {
    #   "items": [evento1, evento2, ...],
    #   "summary": "...",
    # }
    # O .get("items", []) pega a lista de eventos
    # O [] é o valor padrão caso não tenha nenhum evento — evita erro
    return eventos.get("items", [])


def formatar_eventos(items, data):
    """
    Formata a lista de eventos em uma mensagem legível pro Telegram.
    Recebe a lista de eventos do Google e a data no formato "12/06/2026"
    """

    if not items:
        return f"Nenhum evento no dia {data}!"

    resposta = f"Eventos do dia {data}:\n\n"

    for evento in items:
        # .get("summary", "Sem título") — pega o título
        # Se o evento não tiver título, usa "Sem título" como padrão
        titulo = evento.get("summary", "Sem título")

        # Pega o horário de início e fim do evento
        # Se for evento de dia inteiro, não tem "dateTime", só "date"
        horario = evento["start"].get("dateTime", "Dia todo")
        fim_evento = evento["end"].get("dateTime", "Dia todo")

        if horario != "Dia todo":
            # Converte de "2026-06-12T15:00:00-03:00" pra "15:00"
            horario = datetime.fromisoformat(horario).strftime("%H:%M")
            fim_evento = datetime.fromisoformat(fim_evento).strftime("%H:%M")
            resposta += f"🕐 || {horario} - {fim_evento} || {titulo}\n"
        else:
            resposta += f"🗓️ || Dia todo || {titulo}\n"

    return resposta

def agendar_evento(service, data, horario_inicio, duracao, titulo, email=None):
    

    horario_inicio_obj = datetime.strptime(f"{data} {horario_inicio}", "%d/%m/%Y %H:%M")
    horario_fim_obj = horario_inicio_obj + timedelta(hours=int(duracao))

    body ={
            "summary": titulo,        
            "start": {"dateTime": horario_inicio_obj.replace(tzinfo=FUSO_BRASILIA).isoformat()},  
            "end": {"dateTime": horario_fim_obj.replace(tzinfo=FUSO_BRASILIA).isoformat()},    
        }
    
    if email:
        body["attendees"] = [{"email":e} for e in email]

    evento = service.events().insert(
        calendarId="primary",
        body=body
    ).execute()

    return evento

def horarios_livres(service, data, disponibilidade_membros):
    horarios_ocupados = []
    for agenda in disponibilidade_membros:
        for evento in agenda:
            inicio = evento["start"].get("dateTime")
            fim = evento["end"].get("dateTime")
            horarios_ocupados.append((inicio,fim))

    data_obj = datetime.strptime(data, "%d/%m/%Y")
    inicio_dia = data_obj.replace(hour=0, minute=0, tzinfo=FUSO_BRASILIA)
    fim_dia = data_obj.replace(hour=23, minute=59, tzinfo=FUSO_BRASILIA)
    
    horario_livre = []
    horario_atual = inicio_dia
    inicio_bloco = None

    while horario_atual < fim_dia:
        ocupado = False
        for inicio, fim in horarios_ocupados:
            if inicio and fim:
                inicio_dt = datetime.fromisoformat(inicio)
                fim_dt = datetime.fromisoformat(fim)
                if inicio_dt <= horario_atual < fim_dt:
                    ocupado = True
                    break

        if not ocupado:
            if inicio_bloco is None:
                inicio_bloco = horario_atual
        else:
            if inicio_bloco is not None:
                horario_livre.append((inicio_bloco, horario_atual))
                inicio_bloco = None

        horario_atual += timedelta(minutes=15)

    if inicio_bloco is not None:
            horario_livre.append((inicio_bloco, fim_dia))
    
    resultado = ""
    for inicio, fim in horario_livre:
            resultado += inicio.strftime("%H:%M") + " - " + fim.strftime("%H:%M") + "\n"

    return resultado


def completar_data(data):
    # se já tem ano, usa como está
    if len(data.split("/")) == 3:
        return data
    
    # senão adiciona o ano atual
    ano_atual = datetime.now().year
    return f"{data}/{ano_atual}"