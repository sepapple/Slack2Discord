import discord
import os
import json
import datetime
import requests

token = "My-token" # 自身で作成したBotのtoken
dir_path = "/Users/sepa/Downloads/infolab Slack export Nov 2 2017 - Aug 21 2022/" # エクスポートディレクトリのパス
dir_name = sorted([directory for directory in os.listdir(dir_path) if os.path.isdir(dir_path+directory)])

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# user.jsonの読み込み
users = {}
users_open = open(dir_path+'users.json')
for u in json.load(users_open):
    if not u['deleted']:
        users[u['id']] = u['real_name']

# channles.jsonの読み込み
channels = {}
channles_open = open(dir_path+'channels.json', encoding="utf-8")
for channel in json.load(channles_open):
    channels[channel['id']] = channel['name']

# IDから名前への置換
def replaceID2Name(message):
    for uid, name in users.items():
        message = message.replace(f"<@{uid}>", f"@{name}")
    for cid, name in channels.items():
        message = message.replace(f"<#{cid}>", f"#{name}")
    return message

# 表示形式の整形
def format_message(msg):
    """Format the given message in Markdown, suitable for posting on Discord."""
    if(msg.get('files')):
        url=msg.get('files')[0].get('url_private')
        dl_name = url.split('/')[5].split('?')[0]
        data = requests.get(url).content
        with open(dl_name,'wb') as f:
            f.write(data)
    else:
        url=""
        dl_name=""
        data=""

    return "{timestamp} **{user}**: {text} ".format(
        timestamp = datetime.datetime.fromtimestamp(float(msg['ts'])).strftime('%Y-%m-%d %H:%M'),
        user=users.get(msg.get('user'), 'Unknown'),
        text=replaceID2Name(msg['text']),
        ), url, dl_name, data

# メッセージが書き込まれた時に発火するイベント関数
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # :importを打った時のimport処理部分
    if message.content.startswith(':import'):
        guild = await client.fetch_guild(message.author.guild.id)
        category = await guild.create_category("過去のログ")
        for channel_name in dir_name:
            created_channel = await guild.create_text_channel(channel_name,category=category)
            json_file_path = dir_path + channel_name + '/'
            json_full_path = sorted([json_file_path + directory for directory in os.listdir(json_file_path) if os.path.isfile(json_file_path+directory) and 'json' in directory])
            for full_path in json_full_path:
                with open(full_path, "rb") as f:
                    for msg in json.load(f):
                        text, url, dl_name, data = format_message(msg)
                        # ファイルの有無で場合分け
                        if data:
                            if len(data) >= 8000000:
                                await created_channel.send(content=text+url)
                                await created_channel.send("8MB以上のファイルのため、アップロード不可")
                            else:
                                await created_channel.send(content=text,file=discord.File(dl_name))
                            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/"+dl_name):
                                os.remove(os.path.dirname(os.path.abspath(__file__))+"/"+dl_name)
                        else:
                            # Discordの文字数制限回避
                            if(len(text) < 1900):
                                await created_channel.send(content=text)
                            else:
                                if(len(text) > 1900):
                                    await created_channel.send(content=text[0:1900])
                                if(len(text) >= 1900 and len(text) < 3800):
                                    await created_channel.send(content=text[1900:])
                                if(len(text) >= 3800 and len(text) < 5700):
                                    await created_channel.send(content=text[3800:])
    
    # 初期のチャンネル以外を消去(:delte)
    if message.content.startswith(':delete'):
        guild = await client.fetch_guild(message.author.guild.id)
        print(guild.id)
        target_channels = await guild.fetch_channels()
        for channel in target_channels:
            if not (channel.name == 'テキストチャンネル' or channel.name == 'ボイスチャンネル' or channel.name == '一般'):
                await channel.delete()

client.run(token)
