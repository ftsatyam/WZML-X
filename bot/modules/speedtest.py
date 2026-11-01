from speedtest import ConfigRetrievalError, Speedtest

from bot import LOGGER
from bot.helper.ext_utils.bot_utils import new_task, sync_to_async
from bot.helper.ext_utils.status_utils import get_readable_file_size
from bot.helper.telegram_helper.message_utils import (
    delete_message,
    edit_message,
    send_message,
)


def format_result(result):
    server = result.get("server") or {}
    return f"""
➲ <b><i>SPEEDTEST INFO</i></b>
┠ <b>Upload:</b> <code>{get_readable_file_size(result["upload"] / 8)}/s</code>
┠ <b>Download:</b>  <code>{get_readable_file_size(result["download"] / 8)}/s</code>
┠ <b>Ping:</b> <code>{result["ping"]} ms</code>
┠ <b>Time:</b> <code>{result["timestamp"]}</code>
┠ <b>Data Sent:</b> <code>{get_readable_file_size(int(result["bytes_sent"]))}</code>
┖ <b>Data Received:</b> <code>{get_readable_file_size(int(result["bytes_received"]))}</code>

➲ <b><i>SPEEDTEST SERVER</i></b>
┠ <b>Name:</b> <code>{server.get("name")}</code>
┠ <b>Country:</b> <code>{server.get("country")}, {server.get("cc")}</code>
┠ <b>Sponsor:</b> <code>{server.get("sponsor")}</code>
┠ <b>Latency:</b> <code>{server.get("latency")}</code>
┠ <b>Latitude:</b> <code>{server.get("lat")}</code>
┖ <b>Longitude:</b> <code>{server.get("lon")}</code>
"""


@new_task
async def speedtest_command(_, message):
    status = await send_message(message, "<i>Initiating Speedtest...</i>")
    try:
        results = await sync_to_async(Speedtest)
        await sync_to_async(results.get_best_server)
        await sync_to_async(results.download)
        await sync_to_async(results.upload)
    except ConfigRetrievalError:
        await edit_message(
            status,
            "<b>ERROR:</b> <i>Can't connect to Server at the Moment, Try Again Later !</i>",
        )
        return
    except Exception as error:
        LOGGER.error(f"speedtest failed: {error}")
        await edit_message(status, f"<b>ERROR:</b> <i>{error}</i>")
        return

    try:
        await sync_to_async(results.results.share)
    except Exception:
        pass

    result = results.results.dict()
    text = format_result(result)
    try:
        await send_message(message, text, photo=result.get("share"))
        await delete_message(status)
    except Exception as error:
        LOGGER.error(str(error))
        await edit_message(status, text)
