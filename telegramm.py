from pyexpat.errors import messages
import telebot
from telebot.types import Message
from telebot.types import InlineKeyboardButton as IB
import time
import datetime
import random
import base

bot = telebot.TeleBot("7687102007:AAGPyYihvTq_5faJ1DaLVTZIgpiAmZ6pDyY")

reg = ("Привет, %s. В этой игре ты отринешь свою сущность и станешь настоящим магом 🧙‍♂️. Мир на пороге уничтожения: " 
    "народ огня 🔥 развязал войну и теперь все пытаются помешать им. Именно ты станешь тем, " 
    "кто спасёт человечество ⚔️!\n" 
    "Я верю в тебя!\n\nКак твоё имя, ученик?")


temp = {}

tren = "Отлично, теперь ты должен стать сильнее! Ты можешь прийти на площадь чтобы потренироваться или отдохнуть в лагере!"

powers = {
    "Земля🌍": (120, 20),
    "Вода💦": (100, 30),
    "Воздух🌬️": (90, 35),
    "свет💡": (80, 40),
    "камень💎": (130, 15),
    "Огонь🔥": (0, 0)
}

enemies = {
    "Огненный элементаль 🪬": (30, 5),
    "Огненный проказник 🤪": (35, 8),
    "Стена Огня 🔥": (40, 15),
    "камекадзе💣": (25, 5),
    "Ученик Огня 🧑‍🎓": (80, 20),
    "Студент Огня 👨‍🎓": (100, 25),
    "воин огня🗡🔥": (110, 30),
    "Заклинатель Огня 🧙": (120, 30),
    "Маг Огня 🧙‍♂️": (135, 35),
    "убийца Огня️ 🥷": (150, 50),
    "ассасин огня🥷🔥": (170, 60),
    "ОГНЕННЫЙ СМЕРЧ 🔥🌪️": (200, 80),
    "орда огненых магов🧙‍♂️🧙‍♂️🧙‍": (400, 100),
    "ОГНЕНЫЙ ТОРНАДО🔥🌪️🔥🌪️": (500, 150),
    "КОРОЛЬ ОГНЯ🔥👑": (10000, 1000)
}


@bot.message_handler(['start'])
def start(msg: Message):
    if base.is_new_player(msg):
        reg1(msg)
        temp[msg.chat.id] = {"name": None}
    else:
        menu(msg)

def reg1(msg: Message):
    bot.send_message(msg.chat.id, reg % msg.from_user.first_name)
    bot.register_next_step_handler(msg, reg2)


def reg2(msg: Message):
    if not temp[msg.chat.id]["name"]:
        temp[msg.chat.id]["name"] = msg.text
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.row("Земля🌍", "Вода💦")
    kb.row("Огонь🔥", "Воздух🌬️")
    kb.row("свет💡", "камень💎")
    bot.send_message(msg.chat.id, "Выбери свою стихию", reply_markup=kb)
    bot.register_next_step_handler(msg, reg_3)

def reg_3(msg: Message):
    clear = telebot.types.ReplyKeyboardRemove()
    if msg.text == "Огонь🔥":
        bot.send_message(msg.chat.id, "Магия Огня под запретом!🔥❌")
        reg2(msg)
        return
    if msg.text not in tuple(powers.keys()):
        bot.send_message(msg.chat.id, "не шути")
        reg2(msg)
        return
    temp[msg.chat.id]["power"] = msg.text
    base.users.write([msg.chat.id, temp[msg.chat.id]["name"], msg.text, powers[msg.text][0], powers[msg.text][1],1, 0,
                      {"хлеб🥖":[3, 20], "пойло🍺":[1, 100]}, 0])
    print("Игрок добавлен в БД")
    bot.send_message(msg.chat.id, tren, reply_markup=clear)
    time.sleep(2)
    menu(msg)

@bot.message_handler(["menu"])
def menu(msg: Message):
    text = 'Что будешь делать?\n' \
      '/square — площадь\n' \
      '/home — лагерь🏕\n' \
      '/stats — статистика📊\n'\
      '/menu — меню'
    if base.users.read("user", msg.chat.id)[8]:
        text += "\n/defend - защита города🛡"
    bot.send_message(msg.chat.id, text)

@bot.message_handler(['square'])
def square(msg: Message):
   kb = telebot.types.ReplyKeyboardMarkup(True, True)
   kb.row("Тренироваться🥵")
   kb.row("Проверить силы⚔")
   bot.send_message(msg.chat.id, "Ты на площади тренировок", reply_markup=kb)
   bot.register_next_step_handler(msg, sqhand)

def workout(msg: Message):
    kb = telebot.types.InlineKeyboardMarkup()
    kb.row(IB("тренероваться", callback_data="workout"))
    kb.row(IB("назад", callback_data="menu"))
    bot.send_message(msg.chat.id, "жми чтобы тренероваться", reply_markup=kb)



def sqhand(msg: Message):
   if msg.text == "Тренироваться🥵":
       workout(msg)
   if msg.text == "Проверить силы⚔":
       exam(msg)

@bot.message_handler(['home'])
def home(msg: Message):
   kb = telebot.types.ReplyKeyboardMarkup(False, True)
   kb.row("Пожрать🍽")
   kb.row("Поспать💤")
   bot.send_message(msg.chat.id, "ты в лагере🏕", reply_markup=kb)
   bot.register_next_step_handler(msg, homehand)


def homehand(msg: Message):
   if msg.text == "Пожрать🍽":
       eat(msg)
   if msg.text == "Поспать💤":
       sleep(msg)

def eat(msg: Message):
   kb = telebot.types.InlineKeyboardMarkup()
   _, _, _, _, _, _, _, food, _ = base.users.read("user", msg.chat.id)
   if len(food) != 0:
       for key in food:
           kb.row(IB(f"{key} {food[key][1]}❤️ -- {food[key][0]}шт.",
                     callback_data=f"food_{key}_{food[key][1]}"))
       bot.send_message(msg.chat.id, "Что будешь жрать😋?", reply_markup=kb)
   else:
       bot.send_message(msg.chat.id, "у тебя нет еды😭")
       time.sleep(2)
       menu(msg)

def eating(msg, ft, hp):
    player = base.users.read("user", msg.chat.id)
    if player[7][ft][0] == 1:
        del player[7][ft]
    else:
        player[7][ft][0] -= 1
    player[3] += int(hp)
    base.users.write(player)
    print("игрок поел")

def sleep(msg: Message):
    player = base.users.read("user", msg.chat.id)
    low = int(powers[player[2]][0] * player[5]) / 2 - player[3]
    high = int(powers[player[2]][0] * player[5]) - player[3]
    kb = telebot.types.InlineKeyboardMarkup()
    if low > 0:
        kb.row(IB(f"Вздремнуть — +{low}❤️", callback_data=f"sleep_{low}"))
    if high > 0:
        kb.row(IB(f"Поспать — +{high}❤️", callback_data=f"sleep_{high}"))
        bot.send_message(msg.chat.id, "Выбери, сколько будешь отдыхать🛏:", reply_markup=kb)
    else:
        bot.send_message(msg.chat.id, "ты не хочешь  спать")
        menu(msg)

def sleeping(msg, hp):
    player = base.users.read("user", msg.chat.id)
    player[3] += int(round(float(hp), 0))
    base.users.write(player)
    print("Игрок поспал.")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
   print(call.data)
   if call.data.startswith("food_"):
       a = call.data.split("_")
       eating(call.message, a[1], a[2])
       kb = telebot.types.InlineKeyboardMarkup()
       _, _, _, _, _, _, _, food, _ = base.users.read("user", call.message.chat.id)
       for key in food:
           kb.row(IB(f"{key} {food[key][1]}❤️ -- {food[key][0]}шт.", callback_data=f"food_{key}_{food[key][1]}"))
       bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb)

   if call.data.startswith("menu"):
       bot.delete_message(call.message.chat.id, call.message.message_id)
       menu(call.message)

   if call.data == "workout":
       player = base.users.read("user", call.message.chat.id)
       player[4] += player[5] / 10
       player[4] = round(player[4], 4)
       base.users.write(player)
       bot.answer_callback_query(call.id,f"Ты тренируешься и твоя сила увеличивается! Теперь ты наносишь {player[4]}⚔️", True)

   if call.data.startswith("sleep_"):
       b = call.data.split("_")
       t = float(b[1]) / 2
       bot.send_message(call.message.chat.id, f"ты будеш спать {t} минут😴")
       bot.delete_message(call.message.chat.id, call.message.message_id)
       time.sleep(t * 60)
       sleeping(call.message, b[1])
       menu(call.message)

@bot.message_handler(['stats'])
def stats(msg: Message):
    player = base.users.read("user", msg.chat.id)
    t = f"{player[2]} {player[1]}:\n" \
        f"Здоровье: {player[3]}❤️\n" \
        f"Урон: {player[4]}⚔️\n" \
        f"LVL: {player[5]}.{player[6]}⚜️\n\n" \
        f"Еда:\n"
    _, _, _, _, _, _, _, food, _ = base.users.read("user", msg.chat.id)
    for f in food:
        t += f"{f} ❤️{food[f][1]} — {food[f][0]}шт.\n"
    bot.send_message(msg.chat.id, t)
    time.sleep(3)
    menu(msg)

def exam(msg: Message):
    try:
        print(temp[msg.chat.id])
    except KeyError:
        temp[msg.chat.id] = {}
    clear = telebot.types.ReplyKeyboardRemove()
    player = base.users.read("user", msg.chat.id)
    bot.send_message(msg.chat.id, f"Приготовься к испытанию, {player[1]}!", reply_markup=clear)
    time.sleep(2)
    start_exam(msg)

def start_exam(msg: Message):
    random.choice((block, attack))(msg)

def block(msg: Message):
    sides = ["слева", "справо", "сверху", "снизу"]
    random.shuffle(sides)
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.row(sides[0], sides[1])
    kb.row(sides[2], sides[3])
    side = random.choice(sides)
    bot.send_message(msg.chat.id, f"тебя атакуют {side}", reply_markup=kb)
    temp[msg.chat.id]["block_start"] = datetime.datetime.now().timestamp()
    bot.register_next_step_handler(msg, block_hand, side)

def block_hand(msg: Message, side:str):
    final = datetime.datetime.now().timestamp()
    player = base.users.read("user", msg.chat.id)
    if final - temp[msg.chat.id]["block_start"] > player[4] / 10 or side != msg.text:
        bot.send_message(msg.chat.id, "ты провалил😭")
        time.sleep(1)
        menu(msg)
        return
    bot.send_message(msg.chat.id, "ты отразил удар")
    start_exam(msg)

def attack(msg: Message):
    sides = ["слева", "справо", "сверху", "снизу"]
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.row(sides[0], sides[1])
    kb.row(sides[2], sides[3])
    side = random.choice(sides)
    bot.send_message(msg.chat.id, f"выбери сторону атаки👊", reply_markup=kb)
    bot.register_next_step_handler(msg, attack_hand, side)

def attack_hand(msg: Message, side:str):
    player = base.users.read("user", msg.chat.id)
    if side != msg:
        bot.send_message(msg.chat.id, "молодец ты смог ударить тренера😵")
        try:
            temp[msg.chat.id]["point"] += 1
        except KeyError:
            temp[msg.chat.id]["point"] = 1
        if temp[msg.chat.id]["point"] == 10:
            bot.send_message(msg.chat.id, "молодец ты убил тренера☠️")
            player[8] = True
            base.users.write(player)
            menu(msg)
        else:
            start_exam(msg)
    else:
        bot.send_message(msg.chat.id, "ты промазал")
        start_exam(msg)

@bot.message_handler(['defend'])
def defend(msg: Message):
    player = base.users.read("user", msg.chat.id)
    if player[8]:
        bot.send_message(msg.chat.id, "ты вышел за ворота города🌃")
        deffend_hand(msg)
    else:
        bot.send_message(msg.chat.id, "ты ещё не готов👎")
        menu(msg)

def deffend_pass(msg):
    deffend_hand(msg)

def deffend_hand(msg: Message):
    player = base.users.read("user", msg.chat.id)
    enemy = random.choice(list(enemies.keys()))
    if enemy == "ОГНЕНЫЙ ТОРНАДО🔥🌪️🔥🌪️" or "орда огненых магов🧙‍♂️🧙‍♂️🧙‍" and player[5] <= 30:
        deffend_pass(msg)
        return
    if enemy == "КОРОЛЬ ОГНЯ🔥👑" and player[5] <= 200:
        deffend_pass(msg)
        return
    if enemy == "камекадзе💣":
        bot.send_message(msg.chat.id, f"о нет на тебя летит бешеная бомба которая вот вот готова взорваться!!!!"
                                      f"на тебя напал {enemy}")
        firht2(msg, enemy)
        return

    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.row("атака⚔")
    kb.row("бежать🏃", "набратся сил")
    bot.send_message(msg.chat.id, f"тебе встретился {enemy},\n"
                                  f" его hp = {enemies[enemy][0]}❤️, его dmg = {enemies[enemy][1]}⚔\n"
                                  f"что будеш делатъ? атака/ бежать/ отскок", reply_markup=kb)
    bot.register_next_step_handler(msg, fight, enemy)

def fight2(msg:Message, enemy):
    player = base.users.read("user", msg.chat.id)
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.row("атака⚔")
    kb.row("бежать🏃")
    bot.send_message(msg.chat.id, "атака, бежать", reply_markup=kb)
    answer = msg.text
    if answer == "атака⚔":
        eh = enemies[enemy][0]
        ed = enemies[enemy][1]
        t = True
        while t:
            a = random.randint(1, 3)
            if a == 1:
                player[3] //= 2
                base.users.write(player)
                bot.send_message(msg.chat.id, f"{enemy} взорвался и оставил тебе половину жизни у тебя {player[3]} hp")
                defeated(msg)

            eh -= player[4]
            bot.send_message(msg.chat.id, f"ты отбил {enemy} {player[4]} hp у него осталось {eh} hp❤️")
            if eh <= 0:
                t = False
                win(msg, enemy)
                return
            player[3] -= ed
            bot.send_message(msg.chat.id, f"{enemy} отбил тебе {ed}, у тебя осталось {player[3]} hp❤️")
            base.users.write(player)
            if player[3] <= 0:
                t = False
                print("ended")
                defeated(msg)


def fight(msg: Message, enemy):
    player = base.users.read("user", msg.chat.id)
    answer = msg.text
    if answer == "атака⚔":
        fight_hand(msg, enemy)

    if answer == "бежать🏃":
        a = random.randint(1, 5)
        if a == 1:
            bot.send_message(msg.chat.id, "ты сбежал")
            menu(msg)
            return
        else:
            bot.send_message(msg.chat.id, f"у тебя отбили {enemies[enemy][1]} hp❤️")
            player[3] -= enemies[enemy][1]
            base.users.write(player)
            menu(msg)
            defeated(msg)

    if answer == "набратся сил":
        bot.send_message(msg.chat.id, "ты успесшно отпрыгнул и отошел в сторону")
        if msg.text == "набратся сил":
            bot.send_message(msg.chat.id, f"hp = {player[3]}")
            player[3] += 1
            base.users.write(player)
            fight_hand(msg, enemy)
        else:
            fight_hand(msg, enemy)

def fight_hand(msg: Message, enemy):
    player = base.users.read("user", msg.chat.id)
    eh = enemies[enemy][0]
    ed = enemies[enemy][1]
    t = True
    while t:
        eh -= player[4]
        bot.send_message(msg.chat.id, f"ты отбил {enemy} {player[4]} hp у него осталось {eh} hp❤️")
        if eh <= 0:
            t = False
            win(msg, enemy)
            return
        player[3] -= ed
        bot.send_message(msg.chat.id, f"{enemy} отбил тебе {ed}, у тебя осталось {player[3]} hp❤️")
        base.users.write(player)
        if player[3] <= 0:
            t = False
            print("ended")
            defeated(msg)



def win(msg: Message, enemy):
    player = base.users.read("user", msg.chat.id)
    player[6] += enemies[enemy][0] // 1.2
    base.users.write(player)
    level(msg, enemy)


def level(msg: Message, enemy):
    player = base.users.read("user", msg.chat.id)
    if player[6] >= 150:
        player[5] += 1
        player[6] -= 150
        print("xp=lvl")
        base.users.write(player)
        bot.send_message(msg.chat.id,f"ты победил {enemy}, у тебя {player[3]} hp, {player[4]} dmg, {player[5]} lvl, {player[6]} xp")
        level(msg, enemy)
    else:
        bot.send_message(msg.chat.id,f"ты победил {enemy}, у тебя {player[3]} hp, {player[4]} dmg, {player[5]} lvl, {player[6]} xp")
        deffend_hand(msg)


def defeated(msg: Message):
    player = base.users.read("user", msg.chat.id)
    if player[3] <= 0:
        a = random.randint(1, 30)
        if a == 1:
            bot.send_message(msg.chat.id, "ты получил силные ранения и не смог дальше жить, ты умер☠️!!!!!!!!!")
            base.users.delete(player)
        else:
            bot.send_message(msg.chat.id, "ты получил силные ранения но смог выжить у тебя 10 хп!!!")
            player[3] = 10
            base.users.write(player)
            menu(msg)

bot.infinity_polling()
