import discord
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = 1483715317283684426        # 認証ロールID
VERIFY_CHANNEL_ID = 1483713236619624539  # 認証チャンネルID
LOG_CHANNEL_ID = 1483727437660553226     # ログチャンネルID


def is_x_profile(url):
    return re.match(r"https?://(www\.)?(x\.com|twitter\.com)/[A-Za-z0-9_]+/?$", url)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ✅ 特定チャンネル以外は無視
    if message.channel.id != VERIFY_CHANNEL_ID:
        return

    urls = re.findall(r"https?://[^\s]+", message.content)

    for url in urls:
        if is_x_profile(url):
            role = message.guild.get_role(ROLE_ID)
            log_channel = bot.get_channel(LOG_CHANNEL_ID)

            # すでに持ってる場合
            if role in message.author.roles:
                await message.reply("すでに認証済み！")
                return

            # ロール付与
            await message.author.add_roles(role)
            await message.reply("認証完了🎉")

            # ✅ ログ送信
            if log_channel:
                await log_channel.send(
                    f"📜 認証ログ\n"
                    f"ユーザー: {message.author} ({message.author.id})\n"
                    f"リンク: {url}"
                )

    await bot.process_commands(message)

import os
bot.run(os.getenv("DISCORD_TOKEN"))