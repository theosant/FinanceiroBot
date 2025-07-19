import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configuração básica de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Estados para a conversa
DATA, NOME, PARCELA, VALOR, DESCONTOS, CATEGORIA, DESCRICAO, PAGO, FIXO = range(9)

# Começa a conversa
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Use /add para adicionar um gasto.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qual a data do gasto? (ex: 14/07)")
    return DATA

async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['data'] = update.message.text
    await update.message.reply_text("Nome do gasto?")
    return NOME

# ... (repita o processo para os outros campos)

# Finaliza a conversa
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cadastro cancelado.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_data)],
            # Adicione os outros estados (NOME, PARCELA, etc.) aqui
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
