# 📅 Agente de Agendamento no Telegram

Bot para gerenciar agendamentos no Google Calendar direto pelo Telegram. Consulte eventos, veja horários livres em comum entre membros e agende reuniões sem sair do chat.

---

## ✨ Funcionalidades

- **/agenda** — veja os eventos de qualquer membro em um dia
- **/disponivel** — encontre horários livres em comum entre múltiplos membros
- **/agendar** — crie eventos no Google Calendar com participantes

---

## 🚀 Como configurar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/agente-telegram.git
cd agente-telegram
```

### 2. Instale as dependências

```bash
pip install python-telegram-bot python-dotenv google-auth google-auth-oauthlib google-api-python-client openpyxl
```

### 3. Crie o bot no Telegram

1. Abra o Telegram e fale com o [@BotFather](https://t.me/BotFather)
2. Mande `/newbot` e siga as instruções
3. Copie o token gerado

### 4. Configure o Google Calendar API

1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto
3. Ative a **Google Calendar API**
4. Vá em **Credenciais** → **Criar credenciais** → **ID do cliente OAuth**
5. Tipo: **Aplicativo de computador**
6. Baixe o arquivo e renomeie para `credentials.json`
7. Coloque na raiz do projeto

### 5. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```
TOKEN=seu_token_do_telegram_aqui
```

### 6. Configure o `config.py`

Edite o arquivo `config.py` com suas configurações:

```python
CAMINHO_EXCEL = "membros.xlsx"       # caminho pro arquivo de membros
CAMINHO_CREDENTIALS = "credentials.json"
CAMINHO_TOKEN = "token.json"
FUSO_HORAS = -3                      # UTC-3 para Brasília
```

### 7. Monte o arquivo de membros

Um arquivo de exemplo `Membros_exemplo.xlsx` já está incluído no repositório com o formato correto.

> ⚠️ **Renomeie `Membros_exemplo.xlsx` para `Membros.xlsx` e substitua pelos dados reais antes de rodar o bot.**

O arquivo deve ter duas colunas:

| Nome Completo | E-mail |
|---|---|
| João Silva | joao.silva@empresa.com |
| Maria Santos | maria.santos@empresa.com |

### 8. Rode o bot

```bash
python main.py
```

Na primeira execução vai abrir o navegador para você autenticar com sua conta Google. Após isso o `token.json` é salvo automaticamente.

---

## 📱 Como usar

### Ver eventos de um membro
```
/agenda 12/06 Marcus
```

### Ver horários livres em comum
```
/disponivel 12/06 Marcus Ana Nicollas
```

### Agendar uma reunião
```
/agendar 12/06 15:00 2 Marcus Ana @reunião de feedback
```
> Os nomes vêm antes do `@`, o título vem depois do `@`

---

## 📁 Estrutura do projeto

```
agente-telegram/
├── main.py                  # comandos do bot
├── config.py                # configurações editáveis
├── Membros_exemplo.xlsx     # modelo da planilha de membros
├── credentials.json         # credenciais do Google (não sobe pro GitHub)
├── token.json               # token gerado na autenticação (não sobe pro GitHub)
├── .env                     # token do Telegram (não sobe pro GitHub)
├── .gitignore
└── tools/
    ├── google_calendar.py   # integração com Google Calendar
    └── excel.py             # busca de membros na planilha
```

---

## 🔒 Segurança

Nunca suba os arquivos abaixo pro GitHub. Eles já estão no `.gitignore`:

```
.env
credentials.json
token.json
Membros.xlsx
```

---

## 🛠️ Hospedagem

Para deixar o bot rodando 24h gratuitamente, recomendamos o [Railway](https://railway.app):

1. Suba o código no GitHub
2. Conecte o repositório no Railway
3. Configure as variáveis de ambiente no painel
4. Deploy automático

---

## 📋 Requisitos

- Python 3.10+
- Conta Google com acesso ao Google Calendar
- Bot criado no Telegram via BotFather
