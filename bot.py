from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7149352904:AAHMeIQ2yV8Spop0RobOW19B_c_Cc97l_KQ"
OWNER_ID = 8153631464  # ← Вставь сюда свой Telegram ID

perfumes = [
    "🏝️ Le Beau Le Parfum",
    "🍦 Le Male Elixir",
    "🚽 Dior Sauvage",
    "🍋‍🟩 Bleu De Chanel",
    "🖤 Black Afgano",
    "❤️‍🔥 Creed Aventus",
    "🍋 Versace Eros",
    "🪵 Tom Ford Ombré Leather",
    "💪 Stronger With You Absolutely",
    "🚬 Tom Ford Tobacco Vanille"
]

user_choice = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[p] for p in perfumes]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите парфюм:", reply_markup=markup)

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🧾 *Прайс-лист:*

"
        "🏝️ Le Beau Le Parfum — 5мл: 1600₸ | 10мл: 2500₸
"
        "🍦 Le Male Elixir — 5мл: 1500₸ | 10мл: 2400₸
"
        "🚽 Dior Sauvage — 5мл: 1200₸ | 10мл: 2000₸
"
        "🍋‍🟩 Bleu De Chanel — 5мл: 1300₸ | 10мл: 2200₸
"
        "🖤 Black Afgano — 5мл: 1500₸ | 10мл: 2500₸
"
        "❤️‍🔥 Creed Aventus — 5мл: 1600₸ | 10мл: 2700₸
"
        "🍋 Versace Eros — 5мл: 1000₸ | 10мл: 1800₸
"
        "🪵 Ombré Leather — 5мл: 1400₸ | 10мл: 2300₸
"
        "💪 Stronger With You — 5мл: 1100₸ | 10мл: 1900₸
"
        "🚬 Tobacco Vanille — 5мл: 1500₸ | 10мл: 2500₸"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if text == "🔙 Назад":
        await start(update, context)
        return

    if text in perfumes:
        user_choice[chat_id] = text
        markup = ReplyKeyboardMarkup([["5МЛ", "10МЛ"], ["🔙 Назад"]], resize_keyboard=True)
        await update.message.reply_text("Выберите объём:", reply_markup=markup)

    elif text in ["5МЛ", "10МЛ"] and chat_id in user_choice:
        perfume = user_choice[chat_id]
        await update.message.reply_text("✅ Спасибо! Ваш заказ принят.")

        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"📦 Новый заказ!\n👤 Пользователь: @{update.effective_user.username}\n✨ Парфюм: {perfume}\n📏 Объём: {text}"
        )
        del user_choice[chat_id]

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("прайс", price))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
