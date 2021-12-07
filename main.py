import asyncio
import re

from discord.commands import Option

import json
import discord
import os
from threading import Thread

bot = discord.Bot()
# import data file with info on how to fill out form
with open("users.json") as data:
    users = json.load(data)


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
    add_student(first, last, email, school_code)
    await ctx.respond(f"A health screening will now be sent every day at 6 am to your email!", ephemeral=True)


bot.run(os.getenv("TOKEN"))
