# filters
from tgbot.filters.admin_filter import AdminFilter

# handlers
from tgbot.handlers.admin import admin_user
from tgbot.handlers.spam_command import anti_spam
from tgbot.handlers.user import any_user, registrar_evento

# middlewares
from tgbot.middlewares.antiflood_middleware import antispam_func

# states
#from tgbot.states.register_state import Register

# telebot
from telebot import TeleBot #Clase para instanciar Bot
from telebot.types import BotCommand 

# Constantes
from tgbot import config

# remove this if you won't use middlewares:
from telebot import apihelper
apihelper.ENABLE_MIDDLEWARE = True

# I recommend increasing num_threads
bot = TeleBot(config.TOKEN, num_threads=5)

def register_handlers():
    #bot.register_message_handler(admin_user, commands=['start'], admin=True, pass_bot=True)
    bot.register_message_handler(registrar_evento, commands=['register'], admin=False, pass_bot=True)
    #bot.register_message_handler(anti_spam, commands=['spam'], pass_bot=True)
    #bot.register_message_handler(registrar_entrada, commands=['start'], admin=True, pass_bot=True)

register_handlers()

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=['message'])


# custom filters
bot.add_custom_filter(AdminFilter())
# add menu commands
bot.set_my_commands(commands=[\
        BotCommand('/register', 'Realizar registro')\
    ])

def run():
    bot.infinity_polling(skip_pending=True) #kip_pending: omite antiguos (mensajes)updates


run()