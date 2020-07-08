import discord
import requests
import socket
import json
from discord.ext import commands, tasks
from clientMessage import ClientMessage
from protocol import Protocol
from serverMessage import ServerMessage
import asyncio

client = discord.Client()

file = open("config.json", "r").read()
d = json.loads(file)
print(d)
CHANNEL_IDS = d.get("ids")
PORT = d.get("port")
IP = d.get("ip")
TOKEN = d.get("token")

writer = None

print("connected to server on " + f"{IP}:{PORT}")

bot = commands.Bot(command_prefix="!")


chars = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]


async def open_connection(ip, port):
    global writer
    reader, writer = await asyncio.open_connection(ip, port)
    bot.loop.create_task(coro=handle_server_message(reader), name="msg-handle")


def handle(msg):
    message = ServerMessage(msg)

    if message.header == Protocol.SYNC_SUCCESS:
        user = bot.get_user(int(message.value))
        user.send("success")

    if message.header == Protocol.ALREADY_SYNCED:
        user = bot.get_user(int(message.value))
        user.send("fail 1")

    if message.header == Protocol.WRONG_CODE:
        user = bot.get_user(int(message.value))
        user.send("fail 2")


async def handle_server_message(reader):
    msg = await reader.read(100)
    print("received: " + msg.decode())
    handle(msg.decode())
    bot.loop.create_task(handle_server_message(reader))


async def send(client_message):
    print("sending to server: " + client_message.format())
    writer.write(client_message.format().encode())
    await writer.drain()


# @bot.event
# async def on_command_error(error, ctx):
#     print("command failed")


@bot.command(name='live')
async def confirm(ctx):
    await ctx.channel.send("live!")


@bot.command(name='confirm')
async def confirm(ctx, arg):
        print("com", ctx, arg)
        out = ""
        for c in arg:
            if c in chars:
                out += c
        # print(f"http://{IP}:{PORT}/test/?confirm_player_code={str(ctx.author.id)}:{out}")
        await send(ClientMessage(Protocol.USER_SEND_CODE, ctx.author.id, out))


@bot.event
async def on_voice_state_update(member, before, after):
    print(before, after)
    # if not before.mute and after.mute:
    #     send(ClientMessage(Protocol.USER_MUTED_MIC, member.id))
    #
    # if :
    #     send(ClientMessage(Protocol.USER_UNMUTED_MIC, member.id))
    #
    # if:
    #     send(ClientMessage(Protocol.USER_MUTED_HEADPHONES, member.id))
    #
    # if:
    #     send(ClientMessage(Protocol.USER_UNMUTED_HEADPHONES, member.id))
    #
    # if:
    #     send(ClientMessage(Protocol.USER_START_STREAM, member.id))
    #
    # if:
    #     send(ClientMessage(Protocol.USER_END_STREAM, member.id))

    if before.channel is None and after.channel is not None and after.channel.id in CHANNEL_IDS:
        print("user", member.id, "joined us")
        send(ClientMessage(Protocol.USER_JOINED_VOICE, member.id))

    elif before.channel.id in CHANNEL_IDS:
        print("user", member.id, "left us")
        send(ClientMessage(Protocol.USER_LEFT_VOICE, member.id))

bot.loop.create_task(coro=open_connection(IP, PORT), name="open-con")

bot.run(TOKEN)
