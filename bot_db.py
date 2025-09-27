import s_taper
from s_taper.consts import *
import telebot

user_scheme = {"ID":INT+KEY,
               "NAME":TEXT,
               "POWER":TEXT,
               "HP":INT,
               "DMG":INT,
               "LVL":INT,
               "EXP":INT
               "FOOD":TEXT}
users = s_taper.Taper("Users", "TgRPGBotUsers.db").create_table(user_scheme)
def check(msg: telebot.types.Message):
    resualt = users.read_all()
    for x in resualt:
        if x[0] == msg.chat.id:
            return False
    return True