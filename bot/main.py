import os
from enum import Enum
from urllib.parse import quote

from aiotg import Bot, aiohttp

from utils import html_decode

bot = Bot(api_token=os.environ['BOT_TOKEN'])
advice_api_url = "http://fucking-great-advice.ru/api/{}"
sound_url = 'http://fucking-great-advice.ru/files/sounds/{}'  # sound_9.MP3
dummy_image = 'https://dummyimage.com/1200x200/000000/ff0000.png&text={}'


class Advice:
    def __init__(self, id, text, sound, stat=0):
        self._id = id
        self.text = text
        self.sound = sound
        self.stat = stat


class Method(Enum):
    random = 'random'
    latest = 'latest'


async def get_random_advice():
    async with aiohttp.ClientSession() as session:
        async with session.get(advice_api_url.format('random')) as resp:
            return Advice(**(await resp.json()))


async def get_latest_advices(n=1):
    async with aiohttp.ClientSession() as session:
        async with session.get(advice_api_url.format('latest')) as resp:
            body = (await resp.json())
            return map(lambda a: Advice(**a), body)


@bot.command(r"/advice")
@bot.command(r"/random")
@bot.command(r"совет")
async def random(chat, match):
    advice = await get_random_advice()
    return await chat.send_text(html_decode(advice.text))


@bot.command(r'/latest')
async def latest(chat, match):
    advices = list(await get_latest_advices())
    return await chat.send_text(html_decode(advices[0].text))


@bot.command(r'/image')
async def image(chat, match):
    advice = await get_random_advice()
    return await chat.send_text(dummy_image.format(quote(advice.text)))


@bot.command(r'/sound')
async def sound(chat, match):
    await chat.send_chat_action('record_audio')
    advice = await get_random_advice()
    await chat.send_text(sound_url.format(advice.sound))


bot.run()
