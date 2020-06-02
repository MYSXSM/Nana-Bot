
import requests
from time import sleep
import asyncio

from pyrogram import Filters, Message, User
from pyrogram.api import functions
from pyrogram.errors import PeerIdInvalid

from nana import app, Command
from nana.helpers.PyroHelpers import ReplyCheck

__MODULE__ = "CAS Scanner"
__HELP__ = """
──「 **Combot Anti Spam Check** 」──
-> `cas` @username
-> `cas` (reply to a text) To find information about a person.

"""

def replace_text(text):
        return text.replace("[", "").replace("]", "").replace("\"", "").replace("\\r", "").replace("\\n", "\n").replace(
            "\\", "")

@app.on_message(Filters.me & Filters.command(["cas"], Command))
async def cas(client, message):
    cmd = message.command

    user = ""
    if len(cmd) > 1:
        user = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        user = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Usage: cas user_id`")
        await asyncio.sleep(2)
        await message.delete()
        return
    results = requests.get(f'https://api.cas.chat/check?user_id={user}').json()
    try:
        reply_text = f'`User ID: `{user}\n`Offenses: `{results["result"]["offenses"]}\n`Messages: `\n{results["result"]["messages"]}\n`Time Added: `{results["result"]["time_added"]}'
    except:
        reply_text = "`Record not found.`"
    await message.edit(replace_text(reply_text))