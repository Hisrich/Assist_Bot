import telebot
import os
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
PRIVATE_CHANNEL = os.getenv("PRIVATE_CHANNEL")

bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands=["start"])
def begin(message):
    user_id = message.chat.id

    assist_keyboard = InlineKeyboardMarkup()

    faq_button = InlineKeyboardButton("Read FAQs\U0001f4d6", callback_data="faq")
    issue_button = InlineKeyboardButton("Report an Issue\u26a0\ufe0f", callback_data="issue")
    ques_button = InlineKeyboardButton("Add Questions to Game\U0001f64b\u200d\u2640\ufe0f\U0001f64b\u200d\u2642\ufe0f", callback_data="ques")

    assist_keyboard.add(faq_button)
    assist_keyboard.add(issue_button) 
    assist_keyboard.add(ques_button)

    bot.send_message(user_id, "What would you like to do?", reply_markup=assist_keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["faq", "issue", "ques"])
def handle_button(call: CallbackQuery):
    user_id= call.message.chat.id
    if call.data == "faq":
        bot.send_message(user_id, "*Frequently Asked Questions*\n\n_1. What is the Quizy Genius Bot?_\nThe Quizy-G Bot is a fun and interactive game on Telegram where you can test your knowledge on various topics through trivia questions. Challenge yourself or compete with friends to see who knows more!\n\n_2. How do I start playing?_\nTo start playing, simply send the command /start to the bot. Follow the prompts to connect to your other game player, then you're ready to begin!\n\n_3. What types of questions can I expect?_\nThe Quizy-G Bot features a wide range of questions across multiple categories, including history, science, entertainment, sports, and general knowledge.\n\n_4. Can I play with friends?_\nYes! You can invite friends to join the game by sharing the bot link. Everyone can play simultaneously, and the bot keeps track of each player's score.\n\n_5.What do I do if I mistakenly generate a Session ID?_\nGo to the menu and tap on the command /reset to cancel your current game session. You can start a new game by using the /start command.\n\n_6.Why do some of the questions repeat?_\nCurrently, the bot does not keep track of all questions given out, hence the repetition of questions. The support team is working on resolving this issue.\n\n_7. What should I do if I encounter a problem?_\nIf you experience any issues while playing, please contact the bot's support team by using the command /help. This will take you to the help bot where you can send a message with your problem description. We'll get back to you as soon as possible!\n\n_8. How often are new questions added?_\nThe bot is regularly updated with new questions to keep the game fresh and exciting. Be sure to check back often for new content!\n\n_9.How do I suggest questions to be added to the game?_\nYou can use the /help command which will take you to the Help Bot. The Help Bot has a button for suggesting questions to be added to the questions database. The suggested question(s) is then reviewed and added to the database if it is accurate.\n\n_10. How do I leave the game?_\nTo exit the current game session, simply send the command /reset. You can start a new game anytime by sending /start again.", parse_mode="Markdown")

    elif call.data == "issue":
        bot.send_message(user_id, "Type your issue or suggestion")

    elif call.data == "ques":
        bot.send_message(user_id, "Send your question in this format\n\nQ - 'question here'\nA - 'answer here'")

    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: "-" in message.text)
def handle_ques_suggestion(message):
    user_id = message.chat.id
    message_text = message.text
    bot.send_message(PRIVATE_CHANNEL, f"{user_id}\n{message_text}")
    bot.send_message(user_id, f"Your question will be verified and added to the game. Thank you for your suggestion")


@bot.message_handler(func=lambda message: "-" not in message.text)
def handle_issues(message):
    user_id = message.chat.id
    message_text = message.text
    bot.send_message(PRIVATE_CHANNEL, f"{user_id}\n{message_text}")
    bot.send_message(user_id, "Report received. We will work on it and get back to you ASAP\nThank you" )



if __name__ == "__main__":
    bot.infinity_polling()