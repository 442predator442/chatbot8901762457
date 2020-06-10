import discord
import asyncio
import os
from discord.ext import commands
import time
from random import randint
import requests
from discord import Webhook, RequestsWebhookAdapter
import wikipedia
import nekos

word = ['сраннич', 'сранный', 'сранич', 'сраный', 'сраный кот', 'даун', 'лох', 'пидарас', 'пидор', 'пидорас']

commandd = ['.clear', '.avatar', '.ping', '.serverinfo', '.say', '.bug', '.kick']

red = ['red', 'r']

green = ['green', 'gr']

purple = ['purple', 'prp']

gold = ['gold', 'yellow']

blue = ['blue', 'bl']

black = ['black', 'blk']

magenta = ['magenta', 'mgn']

bot = commands.Bot(command_prefix = ".")
bot.remove_command('help')


@bot.event
async def on_command_error(ctx, error):
	pass


@bot.event
async def on_member_join(member):
	guild = member.guild
	channel = discord.utils.find (lambda c: c.id ==670666494182555662, guild.text_channels)
	emb = discord.Embed(title = f'{guild.name}', description = f'У нас новенький(-ая), {member.mention} \n\n\n**[📋] Узнать все доступные команды сервера** - ``.commands``\n\n\n**[📜] Ознакомится с правилами ты сможешь сдесь** - \n<#690315259944501519>', colour = discord.Colour.green())
	emb.set_author(name = f'{member.name}', icon_url = member.avatar_url)
	emb.set_image (url = 'https://i.gifer.com/8CPR.gif')
	await channel.send(embed = emb)
	print ('На сервер', guild.name, 'приесоденился', member.name)

	new_role = discord.utils.get(member.guild.roles, name = '〘🔑〙Verific')
	await member.add_roles(new_role)


@bot.event
async def on_message_delete(message):
	if message.author == bot.user:
		return
	guild = message.guild
	channel = discord.utils.find (lambda c: c.id ==670712805061820477, guild.text_channels)
	emb = discord.Embed(title = '🚮Message Deleted', description = f'**User:** {message.author.mention}\n**Channel: {message.channel}**\n**Message**: {message.content}', colour = discord.Colour.red())
	emb.set_footer(text = f'Message ID: {message.id} | User ID: {message.author.id}')
	await channel.send(embed = emb)

	for attachment in message.attachments:
		if attachment.filename.endswith(('.bmp', '.jpeg', '.jpg', '.png', '.gif')):
			embed = discord.Embed(
				title = '🚮Message Deleted', 
				description = f'**User:** {message.author.mention}\n**Channel: {message.channel}**\n**Message**: {message}', 
				colour = discord.Colour.red()
				)

			await channel.send(embed = embed)


@bot.event
async def on_message_edit(msg_b, msg_a):
    if msg_b.author == bot.user:
        return
    if msg_b.content is None:
        return;
    elif msg_a.content is None:
        return;
    if msg_b in commandd:
    	return
    guild = msg_b.guild
    channel = discord.utils.find(lambda c: c.id ==670712805061820477, guild.text_channels)
    emb = discord.Embed(title = '📝Edit Message', description = f'**User:** {msg_b.author.mention}\n**Channel:** {msg_b.channel}\n\n**Before message:** {msg_b.content}\n\n**After message:** {msg_a.content}', colour = discord.Colour.gold())
    emb.set_footer(text = f'Message ID: {msg_b.id} | User ID: {msg_b.author.id}')
    await channel.send(embed = emb)
    return


@bot.event
async def on_member_remove(member):
	guild = member.guild
	channel = discord.utils.find (lambda c: c.id ==670666605440794654, guild.text_channels)
	emb = discord.Embed(title = f'**{member.name}** покинул наш сервер👋', colour = discord.Colour.red())
	emb.set_image(url = 'https://media.giphy.com/media/9eM1SWnqjrc40/giphy.gif')
	await channel.send(embed = emb)
	print (member.name, 'покинул сервер', guild.name)


@bot.event
async def on_ready():
    print ("Странный Бот подключился!")
    await bot.change_presence( status = discord.Status.online, activity = discord.Game( 'СТРАННЫЙ SQUAD [.help]' ) )


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.id == 614424106242277416:
    	return

    if 'discord.gg' in message.content.lower():
        await message.delete()
        emb = discord.Embed(description = f'{message.author.mention}, **сдесь пиар запрещен.**\n**Вы можете написать администрации, если хотите уложить партнерство!**')
        emb.set_footer(text = f'Server: {message.guild.name}')
        await message.channel.send(embed = emb, delete_after = 10.0) 
        return

    for attachment in message.attachments:
    	if attachment.filename.endwith(('.bmp', '.jpeg', '.jpg', '.png', '.gif')):
    		await message.add_reaction('👍')
    		return


@bot.command()
async def help(ctx):

	msg = await ctx.send('**Подождите...**')

	await msg.add_reaction('📁')
	await msg.add_reaction('🔧')
	await msg.add_reaction('📃')
	await msg.add_reaction('🖱')

	await asyncio.sleep(1)

	await msg.edit(content = '***Выбери категорию:***\n\n📁 - **General**\n🔧 - **Moderation**\n📃 - **Info**\n🖱 - **Games and fun**')

	r_list = ['📁', '🔧', '📃', '🖱',]

	try:
		reaction, user = await bot.wait_for('reaction_add', timeout = 60.0, check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in r_list)

	except asyncio.TimeoutError:
		await msg.edit(content = 'Time is over :/', delete_after = 5.0)

	else:
		if str(reaction.emoji) == '📁':
			emb = discord.Embed(
				title = 'Обычные команды:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``.avatar (@участник)`` \n**Вывод твоей аватарки или упомянутого участника.**\n\n``.suggest [идея]``\n**Отправка твоей идеи для сервера.**\n\n``.bug [текст]``\n**Сообщить создателю бота об ошибке или недороботке.**\n\n``.ping``\n**Пинг бота.**', 
				colour = discord.Colour.dark_blue()
				)

			emb.set_footer(
				text = f'Bot created by Странный Кот#9099'
				)
			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('📁')

			await msg.add_reaction('✅')
			e_list = ['✅']

			try:
				reaction, user = await bot.wait_for('reaction_add', timeout = 300.0, check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send('**Time is over :/**', delete_after = 5.0)

			else:
				if str(reaction.emoji) == '✅':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


		elif str(reaction.emoji) == '🔧':
			emb = discord.Embed(
				title = 'Команды для модерации:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``.clear [к-во]``\n**Очищает указанное к-во сообщений.**\n\n``.ban [@участник] [причина]``\n**Бан указаного участника (в розроботке...).**\n\n``.unban [@участник] (причина)``\n**Розбан указанного участника (в розроботке...).**\n\n``.kick [@участник] (причина)``\n**Выгнать указанного участника.**\n\n``.warn``\n**Выдать предуприждение нарушителю.**\n\n``.say [текст]``\n**Отправить сообщение от имени бота.**', 
				colour = discord.Colour.dark_blue()
				)

			emb.set_footer(
				text = f'Bot created by Странный Кот#9099'
				)
			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('📁')

			await msg.add_reaction('✅')
			e_list = ['✅']

			try:
				reaction, user = await bot.wait_for('reaction_add', timeout = 300.0, check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send('**Time is over :/**', delete_after = 5.0)

			else:
				if str(reaction.emoji) == '✅':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


		elif str(reaction.emoji) == '📃':
			emb = discord.Embed(
				title = 'Инфо:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``.help``\n**Помощь по коммандам.**\n\n``.serverinfo``\n**Информация о сервере.**\n\n``.user (@участник)``\n**Информация о тебе или об указанном участнике.**', 
				colour = discord.Colour.dark_blue()
				)

			emb.set_footer(text = f'Bot created by Странный Кот#9099')
			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('📁')

			await msg.add_reaction('✅')
			e_list = ['✅']

			try:
				reaction, user = await bot.wait_for('reaction_add', timeout = 300.0, check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send('**Time is over :/**', delete_after = 5.0)

			else:
				if str(reaction.emoji) == '✅':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


		elif str(reaction.emoji) == '🖱':
			emb = discord.Embed(
				title = 'Игры и веселье:', 
				description = '```() - Необязательный аргумент.\n[] - Обязательный аргумент.```\n\n``.hug``\n**Обнять упомянутого участника.**\n\n``.slap``\n**Ударить упомянутого участника.**\n\n``.pat``\n**Погладить упомянутого участника.**\n\n``.kiss``\n**Поцеловать упомянутого участника.**', 
				colour = discord.Colour.dark_blue()
				)

			emb.set_footer(text = f'Bot created by Странный Кот#9099')
			await msg.edit(content = None, embed = emb)

			await msg.clear_reaction('🖱')
			await msg.clear_reaction('📃')
			await msg.clear_reaction('🔧')
			await msg.clear_reaction('📁')

			await msg.add_reaction('✅')
			e_list = ['✅']

			try:
				reaction, user = await bot.wait_for('reaction_add', timeout = 300.0, check=lambda reaction, user: user == ctx.author and reaction.message.channel == ctx.channel and reaction.emoji in e_list)

			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send('**Спасибо!**', delete_after = 5.0)

			else:
				if str(reaction.emoji) == '✅':
					await msg.clear_reactions()
					await asyncio.sleep(1)
					await msg.edit(content = '**Спасибо!**', embed = None, delete_after = 5.0)


@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear (ctx, amount: int):
	await ctx.message.delete()
	await ctx.channel.purge( limit =  amount)
	emb = discord.Embed(description = f'Delete {amount} messages', colour = discord.Colour.red())
	await ctx.send(embed = emb, delete_after= 5.0)


@bot.command()
async def avatar (ctx, member: discord.Member = None):
	user = ctx.message.author if member == None else member
	emb = discord.Embed (title = f'Avatar "{user.name}":', colour = discord.Colour.green())
	emb.set_image(url = user.avatar_url)
	await ctx.send (embed = emb)


@bot.command()
async def hug(ctx, member : discord.Member):
    if member == ctx.message.author:
        await ctx.send('Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(
        description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.'
        )
        emb.set_image(url=nekos.img('hug'))
 
        await ctx.send(embed=emb)

@bot.command()
async def slap(ctx, member : discord.Member):
    if member == ctx.message.author:
        await ctx.send('Вы не можете ударить сами себя.')
    else:
        emb = discord.Embed(
        description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.'
        )
        
        emb.set_image(url=nekos.img('slap'))
 
        await ctx.send(embed=emb)


@bot.command()
async def pat(ctx, member : discord.Member):
    if member == ctx.message.author:
        await ctx.send('Вы не можете погладить сами себя.')
    else:
        emb = discord.Embed(
        description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.'
        )

        emb.set_image(url=nekos.img('pat'))
 
        await ctx.send(embed=emb)


@bot.command()
async def kiss(ctx, member : discord.Member):
    if member == ctx.message.author:
        await ctx.send('Вы не можете поцеловать сами себя.')
    else:
        emb = discord.Embed(
        description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.'
        )
        
        emb.set_image(url=nekos.img('kiss'))

        await ctx.send(embed=emb)


@bot.command()
async def tickle(ctx, member : discord.Member):
    if member == ctx.message.author:
        await ctx.send('Вы не можете пощекотать самого себя.')
    else:
        emb = discord.Embed(
        description= f'{member.mention}, Вас пощекотал(а) {ctx.message.author.mention}.'
        )
        
        emb.set_image(url=nekos.img('tickle'))

        await ctx.send(embed=emb)
	

@bot.command()
@commands.has_permissions(administrator = True)
async def say(ctx,* , agr: str):
    await ctx.send (f'{agr}')
    await ctx.message.delete()


@bot.command()
async def suggest( ctx , * , agr: str ):
    suggest_chanell = bot.get_channel( 665166873272516629 )
    emb = discord.Embed(title=f'Suggest:', description= f'{agr} \n\n', colour = discord.Colour.purple())

    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_footer(text = f'Suggest ID: {ctx.message.id} | User ID: {ctx.author.id}')
    message = await suggest_chanell.send(embed=emb)
    await message.add_reaction('🟩')
    await message.add_reaction('🟨')
    await message.add_reaction('🟥')

    embed = discord.Embed(description = '***Твоя идея успешно отправлена! ✅***', colour = discord.Colour.green())
    await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
	guild = ctx.guild
	channel = discord.utils.find (lambda c: c.id ==690088643003547653, guild.text_channels)
	await member.ban(reason = reason)


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
	await ctx.message.delete()
	emb = discord.Embed(description = f'**{member}** has been kicked by {ctx.author.mention}.\n\n**Reason:** {reason}', colour = discord.Colour.red())
	emb.set_footer(text = f'Kicked User ID: {member.id}\nAdministrator ID: {ctx.author.id}')
	await member.kick(reason = reason)
	await ctx.send(embed = emb, delete_after = 10.0)


@bot.command()
@commands.has_permissions(manage_nicknames = True)
async def warn(ctx, member: discord.Member, *, reason = None):

	await ctx.message.delete()
	await ctx.send(f'✅{member.mention} has been warned.')
	guild = ctx.guild
	channel = discord.utils.find (lambda c: c.id ==670717697155399700, guild.text_channels)

	emb = discord.Embed(description = f'**Member:** {member.mention}\n**Member ID:** ``{member.id}``\n**Action:** ``Warn``\n**Reason:** {reason}', colour = discord.Colour.gold())
	emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
	await channel.send(embed = emb)

	embed = discord.Embed(description = f'**Server:** {ctx.guild.name}\n**Actioned by:** {ctx.author.mention}\n**Action:** ``Warn``\n**Reason:** ``{reason}``')
	embed.set_footer(text = f'Server: {ctx.guild.name}')
	await member.send(embed = embed)


@bot.command()
async def serverinfo(ctx):
	roles = len(ctx.guild.roles)
	members = len(ctx.guild.members)
	channels = len(ctx.guild.channels)
	text_channels = len(ctx.guild.text_channels)
	voice_channels = len(ctx.guild.voice_channels)
	categories = len(ctx.guild.categories)
	emojis = len(ctx.guild.emojis)

	emb = discord.Embed(title = 'Информация о сервере:', description = f'**Имя:** ``{ctx.guild.name}``\n**ID:** ``{ctx.guild.id}``\n**Регион:** ``{ctx.guild.region}``\n**Язык:** ``{ctx.guild.preferred_locale}``\n**AFK канал:** ``{ctx.guild.afk_channel}``\n**Время AFK:** ``{ctx.guild.afk_timeout}с``\n**Создатель:** ``Странный Кот#9099``\n**Ролей:** ``{roles}``\n**Всех участников:** ``{members}``\n**Все каналы и категории:** ``{channels}``\n**Текстовых каналов:** ``{text_channels}``\n**Голосовых каналов:** ``{voice_channels}``\n**Категорий:** ``{categories}``\n**Эмодзи:** ``{emojis}``', colour = discord.Colour.purple())
	emb.set_footer(text = f'{ctx.author.name} ID: {ctx.author.id}')
	await ctx.send(embed = emb)


@bot.command()
async def bug(ctx, *, agr):
	guild = ctx.guild
	member = discord.utils.find (lambda m: m.id ==614424106242277416, guild.members)
	emb = discord.Embed(
		title = 'Неполадки бота:', 
		description = f'**От:** {ctx.author.mention}\n**Баг:** *{agr}*', 
		colour = discord.Colour.blurple()
		)

	await member.send(embed = emb)
	embed = discord.Embed(
		description = '✅ ***Ваше сообщение успешно отправлено!***', 
		colour = discord.Colour.green()
		)

	await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(administrator = True)
async def bug_answer(ctx, member:discord.Member, *, arg):
	await ctx.message.delete()
	emb = discord.Embed(description = f'**Ответ от:** {ctx.author.mention}\n**Кому:** {member.mention}\n\n**Ответ:** ``{arg}``',colour = discord.Colour.green())
	emb.set_footer(text = f'Server: {ctx.guild.name}')
	await member.send(embed = emb)
	await ctx.send(embed = emb)


@bot.command()
async def ping(ctx): 
    emb = discord.Embed(description= f'**Пинг:** ``{bot.ws.latency * 1000:.0f} ms``',colour = discord.Colour.blue())
    emb.set_footer(text = f'Your ID: {ctx.author.id}')
    await ctx.send(embed=emb)


@bot.command()
async def user(ctx, member: discord.Member = None):
	user = ctx.message.author if member == None else member
	emb = discord.Embed(title = 'User Info:', description = f'**User:** ``{user.name}#{user.discriminator}``\n**Nickname:** ``{user.display_name}``\n**User ID:** ``{user.id}``\n**Status:** ``{user.status}``\n**User colour:** ``{user.colour}``\n**Account creation date:** ``{user.created_at.strftime("%d.%m.%Y")}``\n**Joined to server:** ``{user.joined_at.strftime("%d.%m.%Y")}``\n**Top role:** ``{user.top_role}``', colour = user.colour)
	emb.set_footer(text = f'Server: {ctx.guild.name} | Server ID: {ctx.guild.id}')
	await ctx.send(embed = emb)


@bot.command()
@commands.has_permissions(administrator = True)
async def embed(ctx, text, title, *, arg):
	if text in green:
		await ctx.message.delete()
		emb = discord.Embed(title = title, description = arg, colour = discord.Colour.green())
		emb.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = emb)

	if text in red:
		await ctx.message.delete()
		embed = discord.Embed(title = title, description = arg, colour = discord.Colour.red())
		embed.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = embed)

	if text in black:
		await ctx.message.delete()
		embed = discord.Embed(title = title, description = arg, colour = discord.Colour.default())
		embed.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = embed)

	if text in gold:
		await ctx.message.delete()
		embed = discord.Embed(title = title, description = arg, colour = discord.Colour.gold())
		embed.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = embed)

	if text in magenta:
		await ctx.message.delete()
		embed = discord.Embed(title = title, description = arg, colour = discord.Colour.magenta())
		embed.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = embed)

	if text in blue:
		await ctx.message.delete()
		embed = discord.Embed(title = title, description = arg, colour = discord.Colour.blue())
		embed.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = embed)

	if text in purple:
		await ctx.message.delete()
		embed = discord.Embed(title = title, description = arg, colour = discord.Colour.purple())
		embed.set_footer(text = f'Embed by {ctx.author.name}#{ctx.author.discriminator}')
		await ctx.send(embed = embed)

# cd C:/python/ChatBot

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**Введите количество сообщений для очистки!**', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)

	if isinstance(error, commands.MissingPermissions):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**У тебя недостаточно прав для использования данной команды!**', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)


@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**Введите все аргуметы!**\n**Использовать:** ``.ban [@user] [reason]``', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)

	if isinstance(error, commands.MissingPermissions):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**У тебя недостаточно прав для использования данной команды!**', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)


@suggest.error
async def suggest_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**Введите все аргуметы!**\n**Использовать:** ``.suggest [идея]``', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)


@say.error
async def say_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**Введите все аргуметы!**\n**Использовать:** ``.say [текст]``', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)

	if isinstance(error, commands.MissingPermissions):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**У тебя недостаточно прав для использования данной команды!**', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)


@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(
			title = 'Error:',
			 description = '**Введите все аргуметы!**\n**Использовать:** ``.kick [@участник] (причина)``', 
			 colour = discord.Colour.red()
			 )

		await ctx.send(embed = emb)

	if isinstance(error, commands.MissingPermissions):
		emb = discord.Embed(
			title = 'Error:', 
			description = '**У тебя недостаточно прав для использования данной команды!**', 
			colour = discord.Colour.red()
			)

		await ctx.send(embed = emb)


@wiki.error
async def wiki_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(
			title = 'Error:',
			 description = '**Введите все аргуметы!**\n**Использовать:** ``.wiki [текст]``', 
			 colour = discord.Colour.red()
			 )

		await ctx.send(embed = emb)

token = os.environ.get('BOT_TOKEN')
bot.run(str(token))
