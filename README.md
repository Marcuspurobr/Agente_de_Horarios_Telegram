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
4. Se for usar Google Sheets, ative também a **Google Sheets API**
5. Vá em **Credenciais** → **Criar credenciais** → **ID do cliente OAuth**
6. Tipo: **Aplicativo de computador**
7. Baixe o arquivo e renomeie para `credentials.json`
8. Coloque na raiz do projeto

### 5. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```
TOKEN=seu_token_do_telegram_aqui
SHEETS_ID=id_da_sua_planilha  # só necessário se usar Google Sheets
```

### 6. Configure o `config.py`

Edite o arquivo `config.py` com suas configurações:

```python
CAMINHO_CREDENTIALS = "credentials.json"
CAMINHO_TOKEN = "token.json"
FUSO_HORAS = -3         # UTC-3 para Brasília
FONTE_MEMBROS = "sheets" # "sheets" ou "excel"
CAMINHO_EXCEL = "Membros.xlsx"
```

### 7. Configure a lista de membros

O bot suporta duas fontes de dados para os membros — escolha a que preferir no `config.py`:

**Opção 1 — Google Sheets:**
- Crie uma planilha no Google Sheets com duas colunas: **Nome Completo** e **E-mail**
- Compartilhe a planilha com sua conta Google
- Copie o ID da planilha da URL e coloque no `.env` como `SHEETS_ID`
- No `config.py` defina `FONTE_MEMBROS = "sheets"`

**Opção 2 — Excel local:**
- Renomeie `Membros_exemplo.xlsx` para `Membros.xlsx`
- Substitua pelos dados reais
- No `config.py` defina `FONTE_MEMBROS = "excel"`

> ⚠️ O arquivo `Membros.xlsx` não sobe pro GitHub — ele está no `.gitignore` para proteger os dados.

### 8. Rode o bot

```bash
python main.py
```

Na primeira execução vai abrir o navegador para você autenticar com sua conta Google. Após isso o `token.json` é salvo automaticamente.

> ⚠️ Se mudar de `excel` para `sheets` ou vice-versa, delete o `token.json` e autentique novamente.

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
    ├── google_calendar.py   # integração com Google Calendar e Sheets
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
