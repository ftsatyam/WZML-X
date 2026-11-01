from os import getcwd
from os import path as ospath
from urllib.parse import unquote, urlsplit
from uuid import uuid4

from aiofiles import open as aiopen
from aiofiles.os import mkdir
from aiofiles.os import path as aiopath
from aiofiles.os import remove as aioremove
from aiohttp import ClientSession
from pyrogram.types import LinkPreviewOptions

from bot import LOGGER
from bot.core.config_manager import Config
from bot.core.tg_client import TgClient
from bot.helper.ext_utils.bot_utils import cmd_exec, new_task
from bot.helper.ext_utils.telegraph_helper import telegraph
from bot.helper.telegram_helper.message_utils import edit_message, send_message


async def gen_mediainfo(message, link=None, media=None, mmsg=None):
    temp_send = await send_message(message, "<i>Generating MediaInfo...</i>")
    des_path = None
    try:
        directory = "mediainfo"
        if not await aiopath.isdir(directory):
            await mkdir(directory)

        file_size = 0
        if link:
            filename = ospath.basename(unquote(urlsplit(link).path)) or "media"
            des_path = ospath.join(directory, f"{uuid4().hex}_{filename}")
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 12; 2201116PI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
            }
            async with ClientSession() as session:
                async with session.get(link, headers=headers) as response:
                    response.raise_for_status()
                    file_size = int(response.headers.get("Content-Length", 0))
                    async with aiopen(des_path, "wb") as file:
                        async for chunk in response.content.iter_chunked(10_000_000):
                            await file.write(chunk)
                            break
        elif media:
            filename = ospath.basename((media.file_name or "media").replace("\\", "/"))
            des_path = ospath.join(directory, f"{uuid4().hex}_{filename}")
            file_size = media.file_size
            if file_size <= 50_000_000:
                await mmsg.download(ospath.join(getcwd(), des_path))
            else:
                async for chunk in TgClient.bot.stream_media(media, limit=5):
                    async with aiopen(des_path, "ab") as file:
                        await file.write(chunk)
        else:
            raise ValueError("No media or download link was provided")

        stdout, _, _ = await cmd_exec(["mediainfo", des_path])
        if not stdout:
            raise RuntimeError("MediaInfo returned no information for this file")
        content = f"<h4>📌 {ospath.basename(des_path)}</h4><br><br>"
        content += parseinfo(stdout, file_size)
    except Exception as error:
        LOGGER.error(f"MediaInfo failed: {error}", exc_info=True)
        await edit_message(temp_send, f"MediaInfo stopped due to {error}")
        return
    finally:
        if des_path and await aiopath.exists(des_path):
            await aioremove(des_path)

    link_id = (await telegraph.create_page(title="MediaInfo X", content=content))[
        "path"
    ]
    await temp_send.edit(
        f"<b>MediaInfo:</b>\n\n➲ <b>Link :</b> https://graph.org/{link_id}",
        link_preview_options=LinkPreviewOptions(is_disabled=False),
    )


section_dict = {"General": "🗒", "Video": "🎞", "Audio": "🔊", "Text": "🔠", "Menu": "🗃"}


def parseinfo(out, size):
    content, trigger = "", False
    size_line = (
        f"File size                                 : {size / (1024 * 1024):.2f} MiB"
    )
    for line in out.split("\n"):
        for section, emoji in section_dict.items():
            if line.startswith(section):
                trigger = True
                if not line.startswith("General"):
                    content += "</pre><br>"
                content += f"<h4>{emoji} {line.replace('Text', 'Subtitle')}</h4>"
                break
        if line.startswith("File size"):
            line = size_line
        if trigger:
            content += "<br><pre>"
            trigger = False
        else:
            content += line + "\n"
    content += "</pre><br>"
    return content


@new_task
async def mediainfo(_, message):
    reply = message.reply_to_message
    command = f"mediainfo{Config.CMD_SUFFIX}"
    alias = f"mi{Config.CMD_SUFFIX}"
    help_message = f"""
<b>By replying to media:</b>
<code>/{command} or /{alias} [media]</code>

<b>By reply/sending download link:</b>
<code>/{command} or /{alias} [link]</code>
"""
    if len(message.command) > 1 or (reply and reply.text):
        link = reply.text if reply else message.command[1]
        return await gen_mediainfo(message, link)
    if reply:
        media = next(
            (
                item
                for item in (
                    reply.document,
                    reply.video,
                    reply.audio,
                    reply.voice,
                    reply.animation,
                    reply.video_note,
                )
                if item is not None
            ),
            None,
        )
        if media:
            return await gen_mediainfo(message, media=media, mmsg=reply)
    return await send_message(message, help_message)
