from telebot import TeleBot #Clase para instanciar Bot
from telebot.types import Message #Clase que representa un Mensaje
from telebot.types import ReplyKeyboardMarkup #Clase que modela un boton en teclado
from tgbot.utils.database import Database #Clase de Conexion a BD Posgresql
from tgbot.models.registro import Registro #Clase que modela un registro
import tgbot.config as config #constantes
import csv #Para manejo de csv
import psycopg2 #Libreria para manejo de conexion a BD Posgresql


registro_dict = {}

def any_user(message: Message, bot: TeleBot):
    """Mensaje enviado a cualquier usuario."""
    bot.send_message(message.chat.id, "Hello, user!")

def registrar_evento(message: Message, bot: TeleBot):
    """Solicitar hora."""
    msg = bot.reply_to(message, "Introduzca la hora de ingreso Formato hh:mm")
    bot.register_next_step_handler(msg, process_hour_step, bot)

def process_hour_step(message: Message, bot: TeleBot):
    """Registrar hora."""
    chat_id = message.chat.id
    hora = message.text
    ingreso = Registro(hora)
    registro_dict[chat_id] = ingreso

    msg = bot.reply_to(message, "Introduzca Site: Sitio RBS o Nodo/Tamper")
    bot.register_next_step_handler(msg, process_site_step, bot)

def process_site_step(message: Message, bot: TeleBot):
    """Registrar site."""
    chat_id = message.chat.id
    ingreso = registro_dict[chat_id]
    site = message.text
    ingreso.site = site

    msg = bot.reply_to(message, "Introduzca Provisioner: Empresa") 
    bot.register_next_step_handler(msg, process_provisioner_step, bot)

def process_provisioner_step(message: Message, bot: TeleBot):
    """Registrar empresa."""
    chat_id = message.chat.id
    prov = message.text
    ingreso = registro_dict[chat_id]
    ingreso.prov = prov

    msg = bot.reply_to(message, "Introduzca Responsible: Responsable")
    bot.register_next_step_handler(msg, process_responsible_step, bot)

def process_responsible_step(message: Message, bot: TeleBot):
    """Registrar Responsable."""
    chat_id = message.chat.id
    ingreso = registro_dict[chat_id]
    resp = message.text
    ingreso.resp = resp

    msg = bot.reply_to(message, "Introduzca Work: Trabajo a Realizar") 
    bot.register_next_step_handler(msg, process_work_step, bot)

def process_work_step(message: Message, bot: TeleBot):
    """Registrar trabajo."""
    chat_id = message.chat.id
    ingreso = registro_dict[chat_id]
    work = message.text
    ingreso.work = work

    msg = bot.reply_to(message, "Introduzca CP Number: Telefono para contacto") 
    bot.register_next_step_handler(msg, process_telephone_step, bot)

def process_telephone_step(message: Message, bot: TeleBot):
    """Registrar telefono."""
    chat_id = message.chat.id
    ingreso = registro_dict[chat_id]
    telef = message.text
    ingreso.telef = telef

    msg = bot.reply_to(message, "Introduzca Obs.: Observaciones") 
    bot.register_next_step_handler(msg, process_obs_step, bot)

def process_obs_step(message: Message, bot: TeleBot):
    """Registrar observaciones y guardar datos"""
    chat_id = message.chat.id
    ingreso = registro_dict[chat_id]
    obs = message.text
    ingreso.obs = obs
    bot.send_message(chat_id, f"Confirmar si desea registrar sus datos:\nhora: {ingreso.hora}\
        \nsite:{ingreso.site}\
        \nProvisioner: {ingreso.prov}\
        \nResponsible: {ingreso.resp}\
        \nWork: {ingreso.work}\
        \nTelefono: {ingreso.telef}\
        \nObservaciones: {ingreso.obs}\
        ")

    #markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Si', 'No')
    msg = bot.send_message(chat_id, '¿Guardar Datos?', reply_markup=markup)
    msg = bot.register_next_step_handler(msg, process_save_step, bot)

def process_save_step(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    ingreso = registro_dict[chat_id]
    resp = message.text
    if resp != '' and resp == 'Si':
        lista_reg = [ingreso.hora, ingreso.site, ingreso.prov, ingreso.resp, ingreso.work, ingreso.telef, ingreso.obs]
        escribir_csv(lista_reg, config.DOC_CSV)
        msg = bot.send_message(chat_id, 'Sus datos fueron registrados con exitos.!!')
    else:
        bot.send_message(chat_id,"Registro Cancelado")

def escribir_db(db: Database, reg: Registro):
    try:
        db = Database()
        with db.get_conn().cursor() as cursor:
            query = "INSERT INTO red_entrada (hora, sitio, empresa, responsable, trabajo, telef, observ) \
            VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(query,(reg.hora, reg.site, reg.prov, reg.resp, reg.work, reg.telef, reg.obs))
        db.get_conn.commit()
    except psycopg2.Error as e:
        print("Ocurrió un error al insertar: ", e)
    finally:
        del db

def escribir_csv(lista, file_out):
    """Guardar datos en formato csv."""
    with open(file_out,'a', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(lista)