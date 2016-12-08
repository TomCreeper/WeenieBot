import discord
import asyncio
import random
import json
import time
import cleverbot
import requests
import git
import subprocess
import sys
import os
from google import search

#changes! testing updates heehee

with open("prefix.json", "r") as infile:
    prefix = json.loads(infile.read())

with open("quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))
    
with open("adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))
    
with open("prefix.json", "w+") as outfile:
    outfile.write(json.dumps(prefix))
    
status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}

x33 = '%m-%d-%Y'
counter1 = len(Quotes_All)
counter2 = len(Quotes_All) - 1
timer = 0
cb1 = cleverbot.Cleverbot()
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)
pfix = prefix["prefix"]
BASE_URL = 'http://pokeapi.co'


async def cleverbot_logic(message, client):
    global cb1
    question = str(message.content.strip('weeniebot '))
    answer = cb1.ask(question)
    await client.send_message(message.channel, message.author.mention + ' ' + answer)
    
async def add_admin_logic(message, client):
    if message.author.name in admin:
        await client.send_message(message.channel, 'Type the ID you want to make admin.')
        msg3 = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel, 'Admin Added')
        admin.append(msg3.content)
        with open("adminweenie.json", "w+") as outfile:
            outfile.write(json.dumps(admin))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'ERROR You are not Admin')


async def getPokemonData(message, client):
    url = '{0}{1}'.format(BASE_URL, resource_url)
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    return None


async def randPokemon(message, client):
    parsedPokemon = random.randint(0, 709)
    try:
        pokemon = await getPokemonData('/api/v1/pokemon/' + str(parsedPokemon), message)

        sprite_uri = pokemon['sprites'][0]['resource_uri']
        description_uri = pokemon['descriptions'][0]['resource_uri']
        type_uri = pokemon['types'][0]['resource_uri']


        sprite = await getPokemonData(sprite_uri, message)
        description = await getPokemonData(description_uri, message)
        ptype = await getPokemonData(type_uri, message)

        p_details = discord.Embed(title='', description='', colour=0x1f3A44)
        p_details.add_field(name='Pokemon:', value=pokemon['name'], inline=True)
        p_details.add_field(name='National Pokedex ID:', value=pokemon['national_id'], inline=True)
        p_details.add_field(name='Desc:', value=description['description'], inline=True)
        p_details.add_field(name='Type:', value=ptype['name'], inline=True)
        p_details.add_field(name='Defense:', value=pokemon['defense'], inline=True)
        p_details.add_field(name='Health Points:', value=pokemon['hp'], inline=True)
        p_details.add_field(name='Attack:', value=pokemon['attack'], inline=True)
        p_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
        p_details.set_image(url=BASE_URL + sprite['image'])
        p_details.set_author(name=pokemon['name'], icon_url=BASE_URL + sprite['image'])
        await client.send_message(message.channel, embed=p_details)
        print(pokemon['name'])
        print(description['description'])
        print(ptype['name'])
        print(pokemon['hp'])
        print(pokemon['defense'])
        print(pokemon['attack'])
        print(pokemon['national_id'])
        print(BASE_URL + sprite['image'])
    except TypeError:
        await client.send_message(message.channel, 'ERROR {} is not in the Pokedex! Try using all lowercase!'.format(parsedPokemon))
       
async def getPokemon(message, client):
    try:
        parsedPokemon = message.content.replace(pfix + 'pokedex ','')

        pokemon = await getPokemonData('/api/v1/pokemon/' + parsedPokemon, message)

        sprite_uri = pokemon['sprites'][0]['resource_uri']
        description_uri = pokemon['descriptions'][0]['resource_uri']
        type_uri = pokemon['types'][0]['resource_uri']

        sprite = await getPokemonData(sprite_uri, message)
        description = await getPokemonData(description_uri, message)
        ptype = await getPokemonData(type_uri, message)
        #print(pokemon['evolutions'])
        p_details = discord.Embed(title='', description='', colour=0x1f3A44)
        p_details.add_field(name='Pokemon:', value=pokemon['name'], inline=True)
        p_details.add_field(name='National Pokedex ID:', value=pokemon['national_id'], inline=True)
        p_details.add_field(name='Desc:', value=description['description'], inline=True)
        p_details.add_field(name='Type:', value=ptype['name'], inline=True)
        p_details.add_field(name='Defense:', value=pokemon['defense'], inline=True)
        p_details.add_field(name='Health Points:', value=pokemon['hp'], inline=True)
        p_details.add_field(name='Attack:', value=pokemon['attack'], inline=True)
        p_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
        p_details.set_image(url=BASE_URL + sprite['image'])
        p_details.set_author(name=pokemon['name'], icon_url=BASE_URL + sprite['image'])
        await client.send_message(message.channel, embed=p_details)
        print(pokemon['name'])
        print(description['description'])
        print(ptype['name'])
        print(pokemon['hp'])
        print(pokemon['defense'])
        print(pokemon['attack'])
        print(pokemon['national_id'])
        print(BASE_URL + sprite['image'])
    except TypeError:
        await client.send_message(message.channel, 'ERROR {} is not in the Pokedex!'.format(parsedPokemon))        

async def google_Fight(message, client):
    if message.author.name in admin:
        fight = message.content.replace(pfix + 'googlefight','')
        result = fight.split(' ')
        await client.send_message(message.channel, 'http://www.googlefight.com/{}-vs-{}.php'.format(result[1], result[2]))
        print(result[1])
        print(result[2])        
        
async def purge(message, client):
    if message.author.name in admin:
        deleted = await client.purge_from(message.channel, limit=500, check=None)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Purge channels!')

async def sleep(message, client):
    tmp = await client.send_message(message.channel, 'ZzzzzzzZZzzzz...')
    await asyncio.sleep(5)
    await client.edit_message(tmp, 'Done sleeping')

async def cooldown(message, client):
    await client.send_message(message.author, '10 second Command Cooldown please be patient and don\'t spam commands! :)')
    await asyncio.sleep(8)
    timer = 0

async def rand_quote(message, client):
    random_quote = random.randint(0, len(Quotes_All) - 1)
    await client.send_message(message.channel, (Quotes_All[random_quote]))
    timer = 1

async def quoteadd_logic(message, client):
    if message.author.name in admin:
            await client.send_message(message.channel, 'Type quote to add.')
            test = await client.wait_for_message(author=message.author)
            global counter1
            counter1 = len(Quotes_All)
            await client.send_message(message.channel, 'Quote {} Added!'.format(counter1))
            counter1
            counter1 = len(Quotes_All)
            Quotes_All.append(test.content)
            with open("quoteweenie.json", "w+") as outfile:
                outfile.write(json.dumps(Quotes_All))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Add Quotes!')

async def user_messages(message, client):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=500):
        if log.author == message.author:
            counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
            print(counter)

async def google_search(message, client):
    search_google = message.content.replace(pfix + 'google ', '')
    if message.author.name in admin:
        for url in search(search_google, stop=5):
            await client.send_message(message.channel, url)
            break

async def quote_amount(message, client):
    global counter2
    counter2 = len(Quotes_All) - 1
    await client.send_message(message.channel, message.author.mention + ' ' + 'There Are {} Quotes!'.format(counter2))

async def admin_amount(message, client):
    open("quoteweenie.json","r")
    await client.send_message(message.channel, message.author.mention + ' ' + 'Admins {}'.format(', '.join(admin)))

async def user(message, client):
    if message.content.startswith(pfix + 'user'):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        try:
            username = message.content.replace(pfix + 'user ', '')
            print(username)
            roles_member = message.server.get_member_named(username).roles
            user_details = discord.Embed(title='', description='', colour=int(rr, 16))
            user_details.add_field(name='Username:', value=message.server.get_member_named(username).name, inline=True)
            user_details.add_field(name='Nick:', value=message.server.get_member_named(username).nick, inline =True)
            user_details.add_field(name='Current Status:', value=status[str(message.server.get_member_named(username).status)], inline=True)
            user_details.add_field(name='Playing:', value=message.server.get_member_named(username).game, inline =True)
            user_details.add_field(name='Joined Server:', value=message.server.get_member_named(username).joined_at.strftime(x33), inline =True)
            user_details.add_field(name='User Roles:', value= ', '.join([i.name.replace('@', '') for i in roles_member]), inline=True)
            user_details.add_field(name='Account Created:', value=message.server.get_member_named(username).created_at.strftime(x33), inline=True)
            user_details.set_author(name=message.server.get_member_named(username).display_name, icon_url=message.server.get_member_named(username).avatar_url)
            await client.send_message(message.channel, embed=user_details)

        except AttributeError:
            if message.content == pfix + 'user':
                roles_member = message.author.roles
                user_details = discord.Embed(title='', description='', colour=int(rr, 16))
                user_details.add_field(name='Username:', value=message.author.name, inline=True)
                user_details.add_field(name='Nick:', value=message.author.nick, inline =True)
                user_details.add_field(name='Current Status:', value=status[str(message.author.status)], inline=True)
                user_details.add_field(name='Playing:', value=message.author.game, inline =True)
                user_details.add_field(name='Joined Server:', value=message.author.joined_at.strftime(x33), inline =True)
                user_details.add_field(name='User Roles:', value= ', '.join([i.name.replace('@', '') for i in roles_member]), inline=True)
                user_details.add_field(name='Account Created:', value=message.author.created_at.strftime(x33), inline=True)
                user_details.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                await client.send_message(message.channel, embed=user_details)
            else:
                print(username)
                await client.send_message(message.channel, 'Invalid User Name')

