import asyncio
import re

from discord.commands import Option

import json
import discord
import os
import sqlite3
from threading import Thread

bot = discord.Bot()


con = sqlite3.connect('users.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users( 
    discord_id      ID PRIMARY KEY NOT NULL,
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT,
    school_code     TEXT
    );""")
con.commit()
con.close()
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


def add_student(first, last, email, school):
    users.append({
        "firstName": first,
        "lastName": last,
        "email": email,
        "stateCode": "NY",
        "schoolCode": school
    })
    with open("users.json", "w") as file_object:
        json.dump(users, file_object)


@bot.slash_command(guild_ids=[916896832737648710], description="Automatically fills out health screenings")
async def screening(
        ctx,
        first: Option(str, "First Name"),
        last: Option(str, "Last Name"),
        email: Option(str, "Email"),
        school_code: Option(str, "School Code (NOT NAME, CHECK #info)"),
):
    if not re.match(r"\D[0-9]{3}", school_code):
        await ctx.respond("Find your school code on https://schoolsearch.schools.nyc/, it should be something like ("
                          "Letter)(3 numbers)", ephemeral=True)
        return
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);", (ctx.author.id, first, last, email, school_code))
    con.commit()
    con.close()
    embed = discord.Embed(title="New user signed up", description=f"${ctx.author.name}#${ctx.author.discriminator}")
    embed.add_field(name="First Name", value=f"`${first}`")
    embed.add_field(name="Last Name", value=f"`${last}`")
    embed.add_field(name="Email", value=f"`${email}`")
    embed.add_field(name="School Code", value=f"`${school_code}`")

    await bot.get_guild(919057346238509066).get_channel(919057346238509066).send(embed=embed)
    await ctx.respond(f"A health screening will now be sent every day at 6 am to your email!", ephemeral=True)

@bot.slash_command(guild_ids=[916896832737648710], description="Modify your info stored in db")
async def modifyscreening(
        ctx,
        first: Option(str, "First Name", required=False),
        last: Option(str, "Last Name", required=False),
        email: Option(str, "Email", required=False),
        school_code: Option(str, "School Code (NOT NAME, CHECK #info)",  required=False),
):
    
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    embed = discord.Embed(title="User updated screening info", description=f"${ctx.author.name}#${ctx.author.discriminator}")

    if first is not None:
        cur.execute("UPDATE users SET first_name = ? WHERE discord_id = ?;", (first, ctx.author.id))
        embed.add_field(name="First Name", value=f"`${first}`")

    if last is not None:
        cur.execute("UPDATE users SET last_name = ? WHERE discord_id = ?;", (last, ctx.author.id))
        embed.add_field(name="Last Name", value=f"`${last}`")

    if email is not None:
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"):
            await ctx.respond("The email adress provided is invalid, please double check the command being sent", ephemeral=True)
            return
        cur.execute("UPDATE users SET email = ? WHERE discord_id = ?;", (email, ctx.author.id))
        embed.add_field(name="Email", value=f"`${email}`")

    if school_code is not None:
        if not re.match(r"\D[0-9]{3}", school_code):
            await ctx.respond("Find your school code on https://schoolsearch.schools.nyc/, it should be something like ("
                            "Letter)(3 numbers)", ephemeral=True)
            return
        cur.execute("UPDATE users SET school_code = ? WHERE discord_id = ?;", (school_code, ctx.author.id))
        embed.add_field(name="School Code", value=f"`${school_code}`")

    con.commit()
    con.close()

    await bot.get_guild(919057346238509066).get_channel(919057346238509066).send(embed=embed)
    add_student(first, last, email, school_code)
    await ctx.respond(f"A health screening will now be sent every day at 6 am to your email!", ephemeral=True)


bot.run(os.getenv("TOKEN"))
con.close()