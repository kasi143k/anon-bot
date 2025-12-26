import os
import logging
from aiogram import Bot, Dispatcher, executor, types

# Токен берётся из переменных окружения (безопасно)
API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    args = message.get_args()

    # Если /start без параметров — даём личную ссылку
    if not args:
        user_id = message.from_user.id
        bot_username = (await bot.get_me()).username
        link = f"https://t.me/{bot_username}?start={user_id}"

        await message.answer(
            "🔐 Анонимные сообщения\n\n"
            "Вот твоя личная ссылка:\n"
            f"{link}\n\n"
            "Отправь её кому угодно — тебе смогут написать анонимно."
        )

    # Если /start с параметром — отправка анонимного сообщения
    else:
        await message.answer("✍️ Напиши сообщение. Отправитель будет анонимным.")

        @dp.message_handler()
        async def send_anon(msg: types.Message):
            try:
                target_id = int(args)
                await bot.send_message(
                    target_id,
                    f"📩 Новое анонимное сообщение:\n\n{msg.text}"
                )
                await msg.answer("✅ Сообщение отправлено анонимно.")
            except:
                await msg.answer("❌ Не удалось отправить сообщение.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
