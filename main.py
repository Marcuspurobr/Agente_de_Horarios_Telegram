from telegram.ext import Application, CommandHandler
from telegram import Update
from tools.google_calendar import autenticar_google, buscar_eventos, formatar_eventos, agendar_evento, horarios_livres, completar_data
from tools.excel import buscar_email
import os
import asyncio
from dotenv import load_dotenv



# Implementação para caso o usuário digite /help /ajuda /start
async def start(update, context):
    await update.message.reply_text(
        "Ola! Comigo aqui vc pode realizar os seguintes comandos:\n\n"
        "/agenda <data> <nome> para ver os eventos do dia da pessoa\n\n"
        "/agendar <data> <horário de inicio> <tempo em horas> <nome do participante 1> <nome do participante 2> <nome do participante X> <@titulo> para agendar um horario\n\n"
        "/disponivel <data> <nome do membro 1> <nome do membro 2> <nome do membro X>"
    )

    # **Comando**
    await asyncio.sleep(2)
    await update.message.reply_text("Aqui alguns exemplos de como tu deve fazer:")
    await asyncio.sleep(2)
    await update.message.reply_text("Para ver os eventos do dia 12 de junho do marcus: \n/agenda 12/06/2026 Marcus")
    await asyncio.sleep(2)
    await update.message.reply_text("Para marcar uma reuniao chamada 'feedback' de duas horas entre o Nicollas e o Marcus: \n/agendar 12/06/2026 15:00 2 Marcus Nicollas @feedback")
    await asyncio.sleep(2)
    await update.message.reply_text("Para ver os eventos do dia 12 de junho do marcus: \n/agenda 12/06/2026 Marcus")


# Implementação para caso o usuário digite /agenda
# Retorna todos os eventos do dia informado
async def agenda(update, context):
    try:
        # args[0] é o primeiro texto depois do comando
        # ex: /agenda 12/06/2026 → args[0] = "12/06/2026"
        data = completar_data(context.args[0])
        nome = context.args[1]

        resultado = buscar_email(nome)

        if resultado is None:
            await update.message.reply_text(f"Nenhum membro encontrado com o nome '{nome}'!")
            return

        if "@" not in resultado:
            await update.message.reply_text(resultado)
            return

        # Busca os eventos no Google Calendar (está em tools/google_calendar.py)
        items = buscar_eventos(service, data, buscar_email(nome))

        # Formata os eventos em uma mensagem legível
        resposta = formatar_eventos(items, data)

        await update.message.reply_text(resposta)

    except IndexError:
        # **Comando** Usuário mandou /agenda sem data 
        await update.message.reply_text("Use nesse formato: /agenda 12/06/2026 Marcus")

    except ValueError:
        # **Comando** Usuário mandou a data em formato errado
        await update.message.reply_text("Data inválida! Use o formato: 12/06/2026")


# Implementação para caso o usuário digite /agendar
# Cria um novo evento no Google Calendar
async def agendar(update, context):
    try:
        data = completar_data(context.args[0])
        horario_inicio = context.args[1]
        duracao = context.args[2]

        # pega os nomes até encontrar o @ do título
        nomes = []
        i = 3
        while i < len(context.args) and "@" not in context.args[i]:
            nomes.append(context.args[i])
            i += 1

        # resto vira título, remove o @
        titulo = " ".join(context.args[i:]).replace("@", "", 1)

        # busca os emails dos nomes
        emails = []
        for nome in nomes:
            resultado = buscar_email(nome)

            if resultado is None:
                await update.message.reply_text(f"Nenhum membro encontrado com o nome '{nome}'!")
                return

            if "@" not in resultado:
                await update.message.reply_text(resultado)
                return

            emails.append(resultado)

        evento = agendar_evento(service, data, horario_inicio, duracao, titulo, emails)
        await update.message.reply_text(f"O Evento '{evento['summary']}' com duração de {duracao}h foi agendado!")

    except IndexError:
        await update.message.reply_text("Use nesse formato: /agendar 12/06/2026 15:00 2 Marcus Nicollas @reunião de feedback")

    except ValueError:
        await update.message.reply_text("Data inválida! Use o formato: 12/06/2026")

async def disponivel(update, context):
    try:
        
        data = completar_data(context.args[0])
        nomes = []
        i=1
        while i < len(context.args):
            nomes.append(context.args[i])
            i += 1
        emails = []
        for nome in nomes:
            resultado = buscar_email(nome)
            
            if resultado is None:
                await update.message.reply_text(f"Nenhum membro encontrado com o nome '{nome}'!")
                return
            
            if "@" not in resultado:
                await update.message.reply_text(resultado)
                return
            
            emails.append(resultado)

        disponibilidade_membros = []
        for email in emails:
            disponibilidade_membros.append(buscar_eventos(service, data, email))

        resultado = horarios_livres(service, data, disponibilidade_membros)
        if resultado:
            await update.message.reply_text(resultado)
        else:
            await update.message.reply_text("Nenhum horário livre em comum no dia!")

    except IndexError:
        # **Comando** Usuário mandou /disponivel sem os emails
        await update.message.reply_text("Use nesse formato: /disponivel <email1> <email2>")

    except ValueError:
        await update.message.reply_text("Data inválida! Use o formato: 12/06/2026")
        




# Carrega as variáveis do .env (TOKEN do Telegram, etc)
load_dotenv()

# Autentica com o Google Calendar
# Na primeira vez abre o navegador, depois usa o token.json salvo
service = autenticar_google()

# Cria o bot com o token do .env
app = Application.builder().token(os.getenv("TOKEN")).build()

# **Comando** Registra os comandos — cada CommandHandler escuta um /comando diferente
app.add_handler(CommandHandler(["start", "help", "ajuda"], start))
app.add_handler(CommandHandler("agenda", agenda))
app.add_handler(CommandHandler("agendar", agendar))
app.add_handler(CommandHandler("disponivel", disponivel))

# Fica em loop esperando mensagens
# Ctrl+C no terminal para encerrar
app.run_polling(allowed_updates=Update.ALL_TYPES)
