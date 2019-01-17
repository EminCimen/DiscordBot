import discord
import youtube_dl
from discord.ext import commands
import asyncio
from itertools import cycle


TOKEN= 'NTM1MDc2NDU4NjQ1OTQ2Mzc5.DyC4kg.57Ttl3KDjGa-TwX3G1BVBCw3tCA'
client = commands.Bot(command_prefix='.')
client.remove_command('help')

players = {}
queues = {}

def check_queue(id):
    if queses[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

#BOTUN DURUMUNU DEĞİŞTİREN KOD
status = ['YERLI VE MILLI BOT','GORUNDUGU GIBI OLAN','GUCUNU MILLETTEN ALAN']
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(3)

#BOT ÇALIŞMAYA BAŞLADIĞINDA EKRAN ÇIKTISI
@client.event
async def on_ready():
    print('Bot calismaya basladi reis.')

#KANALA YENİ BİR ÜYE KATILDIĞINDA ONU SELAMLAYAN VE "UYE" RUTBESINI VEREN KOD
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='UYE')
    await client.add_roles(member, role)
    server = member.server
    fmt = 'Aramiza hos geldin {0.mention} !'
    await client.send_message(server, fmt.format(member, server))

#TEKRAR ET KOMUTU
@client.command()
async def tekrar(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

#MESAJLARI TEMİZLEME KOMUTU
@client.command(pass_context=True)
async def temizle(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Mesajlar temizlendi!')


#KOMUT LISTESI
@client.command(pass_context=True)
async def yardim(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.red()
    )
    embed.set_author(name='KOMUT LISTEM')
    embed.add_field(name='.yardim' , value='Bu ekranı görmenizi sağlar' , inline=False)
    embed.add_field(name='.tekrar' , value='Koddan sonra yazdiginiz mesaji tekrar etmenizi sağlar' , inline=False)
    embed.add_field(name='.temizle SAYI' , value='SAYI kadar mesajı temizler, limit 100 mesaj' , inline=False)
    embed.add_field(name='.katil' , value='Sizin bulunduğunuz kanala ışınlanmmızı sağlar' , inline=False)
    embed.add_field(name='.play URL' , value='URLde belirttiğiniz youtube linkini çalar' , inline=False)
    embed.add_field(name='.pause' , value='Çalan sarkıyı duraklatır' , inline=False)
    embed.add_field(name='.resume' , value='Duraklatılan şarkıyı devam ettirir' , inline=False)
    embed.add_field(name='.stop' , value='Çalan şarkıyı tamamen durdurur' , inline=False)

    await client.send_message(author, embed=embed)

#MÜZİK BOTU KISMI
@client.command(pass_context=True)
async def katil(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say('Kostum, geldim yanina...')

@client.command(pass_context=True)
async def kapat(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def  sira(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Sıraya ekledim...')



#BOTUN CIKIS KOMUTU
@client.command()
async def cikis():
    await client.say('BEHLUL KACAR...')
    await client.logout()


client.loop.create_task(change_status())
client.run(TOKEN)
