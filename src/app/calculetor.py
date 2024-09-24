import telebot

# Token for the bot (replace with your actual token)
Token = "7516525615:AAG48QidN5-ZlN295o2oLRXSLr4FnkBHFzw"

bot = telebot.TeleBot(Token)

# Dictionary to hold questions and correct answers
questions = {
    1: {"question": "What is 5 + 3?", "answer": "8"},
    2: {"question": "What is 9 - 4?", "answer": "5"},
    3: {"question": "What is 6 * 7?", "answer": "42"},
    4: {"question": "What is 12 / 4?", "answer": "3"},
    5: {"question": "What is 10 % 3?", "answer": "1"},
}

# Track the current question for each user
user_data = {}

# Welcome message
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hi! Welcome to Math_360 🎉\nLet's test your math skills. I'll ask you 5 questions. Get ready! ✏️")
    user_data[message.chat.id] = {"question_index": 1}  # Initialize the user's data
    ask_question(message)

# Help command
@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, '''
    /start -> Start the quiz
    /help -> Show available commands
    /cancel -> Cancel the quiz
    ''')

# Function to ask the next question
def ask_question(message):
    user_id = message.chat.id
    question_index = user_data[user_id]["question_index"]

    if question_index <= len(questions):
        bot.send_message(user_id, questions[question_index]["question"])
    else:
        bot.send_message(user_id, "You've completed the quiz! 🎉 Great job! 🚀\nYou can start over with /start or end the session with /cancel.")
        user_data[user_id]["completed"] = True  # Mark the quiz as completed

# Handle text responses (answers to the questions)
@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.chat.id

    # If the user has completed the quiz, don't check answers
    # if user_id in user_data and "completed" in user_data[user_id] and user_data[user_id]["completed"]:
    #     bot.reply_to(message, "You've already completed the quiz! Use /start to begin again.")
    #     return

    # Check if the user has started the quiz
    if user_id not in user_data:
        bot.reply_to(message, "Please start quiz with /start.")
        return

    question_index = user_data[user_id]["question_index"]
    correct_answer = questions[question_index]["answer"]

    # Check the answer
    if message.text.strip() == correct_answer:
        bot.reply_to(message, "Correct! 🎉")
    else:
        bot.reply_to(message, f"Oops! The correct answer was {correct_answer}. ❌")

    # Move to the next question
    user_data[user_id]["question_index"] += 1
    ask_question(message)

# Cancel the quiz
@bot.message_handler(commands=["cancel"])
def cancel(message):
    if message.chat.id in user_data:
        del user_data[message.chat.id]
        bot.reply_to(message, "Quiz cancelled. You can restart anytime with /start.")
    else:
        bot.reply_to(message, "No quiz in progress. Start one with /start.")

# Start the bot
bot.polling()
