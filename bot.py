# pip install python-telegram-bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from secret import bot_token

logged_user=[] #lista di utenti che possono accedere al bot
#voglio avere un bot che risponde solo agli utenti che hanno la password segreta:
#-nella funzione "welcome" --> chiedo la password
#-se il messaggio seguente contiene la password --> aggiungo l'utente alla lista "logged_user"
#altrimenti manda "welcome"
#controllo che l'utente sia in "logged_user"

def welcome(update, context):
    msg = '''Welcome in <b>My Bot</b>'''
    update.message.reply_text(msg, parse_mode='HTML')

def process_chat(update, context):
    print(context)
    if update.message.text.lower() == 'avvisi': #se scrivi "avvisi" ti dico che non ci sono nuovi avvisi
        msg = 'Non ci sono nuovi avvisi'
        update.message.reply_text(msg, parse_mode='HTML')
    elif update.message.text.lower() == 'graph':
        chat_id = update.message.chat.id
        context.bot.send_document(chat_id=chat_id, document=open('photo.jpg', 'rb'))
    else:
        welcome(update, context)

def process_location(update, context):

    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    user_location = message.location

    user = message.from_user
    print(user)
    print(f"You talk with user {user['first_name']} and his user ID: {user['id']}")

    msg = f'Ti trovi presso lat={user_location.latitude}&lon={user_location.longitude}'
    print(msg)
    message.reply_text(msg)

def photo_handler(update, context):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('photo.jpg')
    update.message.reply_text('photo received')

def main():
   print('bot started')
   #queste due righe di codice (fanno parte della libreria telegram) fanno partire il chatbot
   upd= Updater(bot_token, use_context=True)
   disp=upd.dispatcher
   # quando qualcuno scrive al bot, queste linee ci dicono cosa dare
   disp.add_handler(CommandHandler("start", welcome))# cosa fa il bot quando si inzia chat
   disp.add_handler(MessageHandler(Filters.regex('^.*$'), process_chat)) #cosa fa il bot quando qualcuno scrive un messaggio di testo
   disp.add_handler(MessageHandler(Filters.location, process_location))# cosa fa il bot quando qualcuno condivide posizione
   disp.add_handler(MessageHandler(Filters.photo, photo_handler))# cosa fa il bot quando qualcuno condivide foto


   upd.start_polling()
   upd.idle()


#questa linea di codice ci dice "se faccio il run di questo file allora esegui la funzione main (vedi sopra)"
if __name__=='__main__':
   main()
