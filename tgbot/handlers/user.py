from telebot import TeleBot
from telebot.types import Message

class Reg_Entrada:
    def __init__(self, hora):
        self.hora = hora
        self.site = None
        self.prov = None
        self.resp = None
        self.work = None
        self.telef = None
        self.obs = None

ingreso_dict = {}

def any_user(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    bot.send_message(message.chat.id, "Hello, user!")

def _extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None

def _get_username_from_storage(code):
    return True

def registrar_entrada(message: Message, bot: TeleBot):
    """
    Registrar entrada.
    """
    unique_code = _extract_unique_code(message.text)
    if unique_code:  # if the '/start' command contains a unique_code
        username = _get_username_from_storage(unique_code)
        if username:  # if the username exists in our database
            
            msg = bot.reply_to(message, "Introduzca la hora de ingreso Formato hh:mm")
            bot.register_next_step_handler(msg, process_hour_step, bot)
        else:
            bot.reply_to(message, "No se encontro usuario...")
    else:
        reply = "Solicitar a su Superv. su acceso"
        bot.send_message(message.chat.id,reply)

def process_hour_step(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    hora = message.text
    ingreso = Reg_Entrada(hora)
    ingreso_dict[chat_id] = ingreso

    msg = bot.reply_to(message, "Introduzca Site: Sitio RBS o Nodo/Tamper")
    bot.register_next_step_handler(msg, process_site_step, bot)

def process_site_step(message: Message, bot: TeleBot):
    """
    Registrar site.
    """
    chat_id = message.chat.id
    ingreso = ingreso_dict[chat_id]
    site = message.text
    ingreso.site = site

    msg = bot.reply_to(message, "Introduzca Provisioner: Empresa") 
    bot.register_next_step_handler(msg, process_provisioner_step, bot)

def process_provisioner_step(message: Message, bot: TeleBot):
    """
    Registrar provisioner.
    """
    chat_id = message.chat.id
    prov = message.text
    ingreso = ingreso_dict[chat_id]
    ingreso.prov = prov

    msg = bot.reply_to(message, "Introduzca Responsible: Responsable")
    bot.register_next_step_handler(msg, process_responsible_step, bot)

def process_responsible_step(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    ingreso = ingreso_dict[chat_id]
    resp = message.text
    ingreso.resp = resp

    msg = bot.reply_to(message, "Introduzca Work: Trabajo a Realizar") 
    bot.register_next_step_handler(msg, process_work_step, bot)

def process_work_step(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    ingreso = ingreso_dict[chat_id]
    work = message.text
    ingreso.work = work

    msg = bot.reply_to(message, "Introduzca CP Number: Telefono para contacto") 
    bot.register_next_step_handler(msg, process_telephone_step, bot)

def process_telephone_step(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    ingreso = ingreso_dict[chat_id]
    telef = message.text
    ingreso.telef = telef

    msg = bot.reply_to(message, "Introduzca Obs.: Observaciones") 
    bot.register_next_step_handler(msg, process_obs_step, bot)

def process_obs_step(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    ingreso = ingreso_dict[chat_id]
    obs = message.text
    ingreso.obs = obs
    bot.send_message(chat_id, f"Datos:\nhora: {ingreso.hora}\
        \nsite:{ingreso.site}\
        \nProvisioner: {ingreso.prov}\
        \nResponsible: {ingreso.resp}\
        \nWork: {ingreso.work}\
        \nTelefono: {ingreso.telef}\
        \nObservaciones: {ingreso.obs}\
        ")