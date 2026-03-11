from pyrogram import Client, filters
import config
import datetime
import keyboard
import random
import json
from FusionBrain_AI import generate

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name= "Kinich201Bot"
)

def button_filter(button):
   async def func(_, __, msg):
       return msg.text == button.text
   return filters.create(func, "ButtonFilter", button=button)

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Nice to meet you!", reply_markup=keyboard.kb_main)
    #await bot.send_sticker(message.chat.id,"CAACAgQAAxkBAAEOsmloTVCUL_ZkUssNAXK-pj6Bvqw38QACORgAAtjnaVLBBlzvJoXxRDYE")

    with open("users.json", "r") as file:
      users = json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open("users.json", "w") as file:
            json.dump(users,file)

@bot.on_message(filters.command("info") | button_filter(keyboard.btn_info))
async def info(bot, message):
    await message.reply(
        "Here are the available commands:"
        "/start - Start the bot and get a welcome message"
        "/sticker - Send a fun sticker"
        "/info - Get information about all commands")

@bot.on_message(filters.command("time"))
async def time(bot, message):
    await message.reply(f"The current date and time: {datetime.datetime.now()}")

@bot.on_message(filters.command("games") | button_filter(keyboard.btn_games))
async def games(bot, message):
    await message.reply("Choose the game you want to play", reply_markup=keyboard.kb_games)

@bot.on_message(filters.command("game") | button_filter(keyboard.btn_rps))
async def game(bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)
        if str(message.from_user.id) in users:

         if users[str(message.from_user.id)] >= 10:
            await message.reply("Choose between rock, paper, and scissor", reply_markup=keyboard.kb_rps)
         else:
            await message.reply(f"You don't have enough coins. You have {users[str(message.from_user.id)]}.The minimum amount to play is 10")

@bot.on_message(filters.command("quest") | button_filter(keyboard.btn_quest))
async def quest(bot,message):
    await message.reply_text("Would you like to start a new adventure full of wonderful discoveries and exciting mysteries and friendships ?",
                             reply_markup=keyboard.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot,query):
    if query.data == "start_quest":
        await bot.answer_callback_query(query.id,
            text="Welcome to the quest called the Legend of Teyvat",
            show_alert=True)
        await query.message.reply_text("You are now standing in front of two doors. Which one will you choose Traveler ?", reply_markup=keyboard.inline_kb_choice_door)
    elif query.data =="left_door":
        await query.message.reply_text("You see a young lady who needs help. You can help her or continue your adventure.", reply_markup=keyboard.inline_kb_left_door)
    elif query.data =="right_door":
        await query.message.reply_text("You see a treasure with gold and jewels and some people in need. You can help the people in need or go take the treasure.", reply_markup=keyboard.inline_kb_right_door)

    elif query.data == "lady":
        await bot.answer_callback_query(query.id, text="You help the young lady who is a witch. To thank you she offers you 3 wishes",
                                        show_alert=True)
    elif query.data == "leave":
        await bot.answer_callback_query(query.id, text="You decide to leave the lady who is a with. She decide to take revenge by giving you a curse.",
                                        show_alert=True)
    elif query.data == "people":
        await bot.answer_callback_query(query.id, text="You decide to help the people who are in reality an king and a queen. to thank you they offer you a palace full of gold and jewels",
                                        show_alert=True)
    elif query.data == "treasure":
        await bot.answer_callback_query(query.id, text="You decide to take the treasure and discovers that it was only an illusion and that thay are stones in reality",
                                        show_alert=True)
    elif query.data == "start_quiz":
       await query.message.reply_text(
            "Who is this character ? He is an Hokage, and a ninja who helped everyone during the war.",
            reply_markup=keyboard.inline_kb_quiz_question1)
    elif query.data == "Naruto":
        await bot.answer_callback_query(query.id, text= "Good guess !", show_alert=True)
    elif query.data == "Sasuke":
        await bot.answer_callback_query(query.id, text= "Wrong guess.", show_alert=True)

@bot.on_message(filters.command("quiz")| button_filter(keyboard.btn_quiz))
async def start_quiz(bot, message):
    await message.reply_text("Discovers which characters is hidden behind which description", reply_markup=keyboard.inline_kb_start_quiz)

quiz = {
    "q1":{"question":"Who is this character ? He is an Hokage, and a ninja who helped everyone during the war.",
          "correct_answer":"Naruto",
          "options":["Sasuke","Naruto","Shikamaru","Obito"]},
    "q2":{"question":"Who is this character ? He has a scar on his forehead, wear glasses, and is known as a wizard.",
          "correct_answer":"Harry Potter",
          "options":["Harry Potter","Goku","Saitama","Drago Malfoy"]},
    "q3":{"question":"Who is this character ? He is a dendro character from genshin impact, a saurien hunter, and a five star",
          "correct_answer":"Kinich",
          "options":["Gaming, Lyney, Kinich, Xiao"]}
}

@bot.on_message(filters.command("back") | button_filter(keyboard.btn_back))
async def back(bot, message):
    await message.reply("Return to the menu", reply_markup=keyboard.kb_main)

@bot.on_message(button_filter(keyboard.btn_rock) |
                button_filter(keyboard.btn_scissor) |
                button_filter(keyboard.btn_paper))
async def choice_rps(bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)

    rock = keyboard.btn_rock.text
    scissor = keyboard.btn_scissor.text
    paper = keyboard.btn_paper.text
    user = message.text
    bot = random.choice([rock, paper, scissor])

    if user == bot:
        await message.reply("It's a draw.")
    elif (user == scissor and bot == paper) or (user == paper and bot == rock) or (user == rock and bot == scissor):
        await message.reply(f'Congratulation! You won! The bot choose {bot}', reply_markup=keyboard.kb_main)
        users[str(message.from_user.id)]+= 10
    else :
        await message.reply(f'Loser! You lost! Try again. The bot choose {bot}', reply_markup=keyboard.kb_main)
        users[str(message.from_user.id)] -= 10

    with open("users.json", "w") as file:
        json.dump(users,file)

@bot.on_message(filters.command("image"))
async def image(bot,message):
    if len(message.text.split()) > 1:
        query = message.text.replace('/image','')
        await message.reply_text(f"Generating an image upon prompt '{query}', wait a bit...")
        images = await generate(query)
    else:
        await message.reply_text("Enter your prompt")


# async def echo(bot, message):
#     if message.text.lower() == "hello":
#         await message.reply("Welcome")
#     elif message.text.lower() == "bye":
#         await message.reply("Goodbye")
#     else:
#         await message.reply(f'You wrote:{message. text}')


bot.run()

