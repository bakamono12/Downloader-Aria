import os
import logging
import asyncio
import random

from pyrogram import Client, idle, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from downloader import Aria2Downloader
from utils import is_download_link, extract_gid, PATH, EMOJI

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"
baka_dl_bot = Client("baka-dl-bot")

# intialize downloader
downloader = Aria2Downloader()


@baka_dl_bot.on_message(filters.command("start"))
async def start_handler(_, message):
    await message.reply_text("Hi, I'm Downloader Bot. Send me a link to download.")


@baka_dl_bot.on_message(filters.command("help"))
async def help_handler(_, message):
    await message.reply_text("Hi, this is Downloader Bot. Send me a Direct DL link to download and upload here.")


@baka_dl_bot.on_message(filters.command("about"))
async def about_handler(_, message):
    await message.reply_text("Hola, this is Downloader Bot. Created By [Baka](t.me/DTMK_C).")


@baka_dl_bot.on_message(filters.command("download_this"))
def link_handler(_, message):
    if message.text.split()[1]:
        url = message.text.split()[1]
    buttons = [
        InlineKeyboardButton("Download", callback_data="download"),
        InlineKeyboardButton("Cancel", callback_data="cancel"),
    ]
    message.reply_text("Press the download button to start downloading.", reply_markup=InlineKeyboardMarkup([buttons]))


@baka_dl_bot.on_callback_query(filters.regex(r"download"))
async def download_handler(client, callback_data):
    url = callback_data.message.reply_to_message.text
    # check if the link sender and the button clicker are the same
    if callback_data.from_user.id != callback_data.message.reply_to_message.from_user.id:
        await callback_data.answer("You didn't send this link.", show_alert=True)
        return
    cancel_buttons = [
        InlineKeyboardButton("Cancel", callback_data="cancel"),
    ]
    # initialize the download
    files = downloader.start_download(url)
    response_text = "Starting download..."
    for file_update in files:
        try:
            response_text = (
                f"Status: `{file_update['status']}`\n"
                f"Name: `{file_update['name']}`\n"
                f"Downloaded: `{file_update['downloaded']}`\n"
                f"Speed: `{file_update['download_speed']}`\n"
                f"ETA: `{file_update['eta']}`\n"
                f"GID: `{file_update['gid']}`"
            )
            await callback_data.edit_message_text(response_text, reply_markup=InlineKeyboardMarkup([cancel_buttons]))
            if file_update['is_complete']:
                response_text = (
                    f"Status: `{file_update['status']}`\n"
                    f"Name: `{file_update['name']}`\n"
                    f"Downloaded: `{file_update['downloaded']}\n`"
                    f"GID: `{file_update['gid']}`"
                )
                await callback_data.edit_message_text(response_text)
                break
            await asyncio.sleep(3.5)
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(2.5)
            await callback_data.edit_message_text(f"Some Error Occurred: {e}\n\n {random.choice(EMOJI)}")


@baka_dl_bot.on_callback_query(filters.regex(r"cancel"))
async def cancel_download_handler(client, callback_data):
    # Handle cancel button click
    name, gid = await extract_gid(callback_data.message.text)
    if gid:
        try:
            downloader.cancel_download(gid)
            os.remove(PATH + "/" + name)
            await callback_data.message.edit_text("Download cancelled and removed.")
            return
        except Exception as e:
            logger.error(e)
            await callback_data.message.edit_text(f"Some Error Occurred: {e}\n\n {random.choice(EMOJI)}")
            return
    await callback_data.message.edit_text("Download already completed/Cancelled/Removed.")


# start the bot
baka_dl_bot.run()
