import random
import csv
import requests
import discord
from discord import app_commands
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
OM = ['大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶']
tokumei = "匿名ちゃねら"
TOKEN = os.getenv("DISCORD_TOKEN")
API = os.getenv("API_KEY")
AGENT = os.getenv("AGENT_KEY")

#起動確認
@client.event
async def on_ready():
 print(f'{client.user}でログインしました')
  # スラッシュコマンドを同期 
 await tree.sync()
#ちょっとテスト用
@client.event
async def on_message(message: discord.Message):
 if message.author.bot:
  return
 if type(message.channel) == discord.DMChannel :
  date=[
 [message.content, message.author]
]

  with open('data.csv', 'a', newline='') as csvfile:
   writer = csv.writer(csvfile)
   writer.writerows(date)
 if message.content == "テスト":
  await message.reply("成功")
#DMを匿名化して匿名ちゃねらで叫ぶ
 if type(message.channel) == discord.DMChannel : 
#dmかどうか
  if message.author.bot: #BOTの場合は何もせず終了
   return
        #メッセージ送信部
  for channel in client.get_all_channels(): #BOTが所属する全てのチャンネルをループ
   if channel.name == tokumei: #匿名チャンネルが見つかったとき                
    embed=discord.Embed(description=message.content, color=0x9B95C9) 
    #埋め込みの説明に、メッセージを挿入し、埋め込みのカラーを紫`#9B95C9`に設定
    if message.attachments != []: #添付ファイルが存在するとき
     embed.set_image(url=message.attachments[0].url)
    await channel.send(embed=embed) #メッセージを送信
  await message.add_reaction('✅') #リアクションを送信

#おみくじコマンド
@tree.command(name="omikuji", description="おみくじを引きます")
async def omikuji(interaction: discord.Interaction):
 await interaction.response.send_message(f'今日の運勢は{OM[random.randrange(len(OM))]}です')

@tree.command(name="gpd",description="chatgptとお話し")
async def gpd(interaction: discord.Interaction,text:str=None):
    await interaction.response.defer()
    url = "https://api-mebo.dev/api"
    headers = {'content-type': 'application/json'}
    item_data = {
            "api_key": API,
            "agent_id": AGENT,
            "utterance": text
  }
    r = requests.post(url,json=item_data,headers=headers)
    print(r)
    print(r.json()["utterance"])
    print(r.json()["bestResponse"]["utterance"])
    e=r,r.json()["utterance"],r.json()["bestResponse"]["utterance"]
    await interaction.followup.send(e)

client.run(TOKEN)
