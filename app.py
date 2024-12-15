#--------------------------------------
#импортируем зависимости
from aiohttp import web
import asyncio
import telegram
import re

#-------------------------------------
#эти параметры пока оставим пустыми
bot_token = "8052297012:AAHN_U_mL41eUM0Qg9bRy95qzsBwDfKPAvM"
bot_user_name = "Aio_Http_bot"
URL = ""

#-----------------------------------
TOKEN = bot_token
# создаём экземпляр API для Telegram
bot = telegram.Bot(token=TOKEN)

#-----------------------------------
#этот обработчик мы будем использовать только для проверки работоспособности приложения
async def index(request):
    return web.Response(text='Ok')


# об этом обработчике чуть позже
async def set_webhook(request):
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return web.Response(text='webhook set')
    else:
        return web.Response(text = 'failed to set hook')


#основной обработчик, который обменивается сообщениями с серверами Telegram
async def respond(request):
#получаем JSON из запроса и превращаем его в объект API Telegram
   update = telegram.Update.de_json(await request.json(), bot)
   #получаем id чата и сообщения
   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # получаем текст сообщения с учётом кодировки
   text = update.message.text.encode('utf-8').decode()
   # Самой первой командой, которую направляют боту, обычно является /start
   if text == "/start":
       # возвращаем приветствие ответом на запрос
       bot_welcome = """
       Hello! Im work!       """
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
   else:
       try:
           # убираем из сообщения все небуквенные символы (пробелы и прочее)
           text = re.sub(r"\W", "_", text)
           # в качестве ответа мы будем возвращать ссылку на картинку от сервиса adorable.io
           url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # возвращаем наш ответ
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
       except Exception:
           # Если произошла ошибка, то можем вернуть сообщение об ошибке
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)


# aiohttp предполагает возврат какого-то ответа, однако в данном случае все ответы идут через API Telegram, поэтому тут мы можем вернуть пустой ответ
   return web.Response(text = '')


# метод "фабрика приложения" создаёт и настраивает наше приложение
async def my_web_app(*args):
    app = web.Application()
    #прописываем роуты
    app.add_routes([web.get('/setwebhook', set_webhook)
                ,web.post(f'/{TOKEN}', respond)
                ,web.get('/',index)
                ,web.get('/favicon.ico', favicon)])
    return app