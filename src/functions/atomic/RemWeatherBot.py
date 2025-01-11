import os
import logging
from typing import List
import telebot
from telebot import types
from telebot.callback_data import CallbackData
import requests
from bot_func_abc import AtomicBotFunctionABC

class AtomicExampleBotFunction(AtomicBotFunctionABC):
    """Example of implementation of atomic function"""

    commands: List[str] = ["quote"]
    authors: List[str] = ["FeyBM"]
    about: str = "Получение цитат из Breaking Bad!"
    description: str = """Этот бот позволяет получать случайные цитаты из сериала Breaking Bad.
    Для получения цитат используйте команду /quote <количество>"""
    state: bool = True

    bot: telebot.TeleBot
    example_keyboard_factory: CallbackData

    def set_handlers(self, bot: telebot.TeleBot):

        self.bot = bot
        self.example_keyboard_factory = CallbackData('t_key_button', prefix=self.commands[0])

        @bot.message_handler(commands=self.commands)
        def send_quote(message: types.Message):
            # Извлечение количества цитат из сообщения
            try:
                num_quotes = int(message.text.split()[1])  # Получаем число после команды /quote
            except (IndexError, ValueError):
                bot.send_message(message.chat.id, "Пожалуйста, укажите количество цитат. Пример: /quote 3")
                return

            # Получение цитат с API
            quotes = []
            for _ in range(num_quotes):
                response = requests.get("https://api.breakingbadquotes.xyz/v1/quotes")
                if response.status_code == 200:
                    data = response.json()[0]
                    quote = data['quote']
                    author = data['author']
                    quotes.append(f"Цитата: {quote}\nАвтор: {author}")
                else:
                    bot.send_message(message.chat.id, "Не удалось получить цитату.")
                    return

            # Отправка полученных цитат
            for quote in quotes:
                bot.send_message(message.chat.id, quote)
