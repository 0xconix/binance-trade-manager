import os
import asyncio
import telegram
import dotenv

dotenv.load_dotenv()

class Jarvis(object):
    def __init__(self) -> None:
        self.__bot = telegram.Bot(os.getenv('TELEGRAM_API_KEY'))
        self.__chat_id = os.getenv('CHAT_ID')
        
    async def get_updates(self):
        async with self.bot:
            print(await self.bot.get_updates()[0])

    async def send_message(self, message:str):
        async with self.bot:
            await self.bot.send_message(text=message, chat_id=self.__chat_id)

    @property
    def bot(self):
        return self.__bot


if __name__ == '__main__':
    jarvis = Jarvis()
    asyncio.run(jarvis.send_message('miam miam'))