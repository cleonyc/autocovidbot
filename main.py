import aiohttp
import asyncio
import sys
from datetime import datetime
from discord.commands import Option
from apscheduler.schedulers.background import BackgroundScheduler
import json
import atexit
import discord
import os
from threading import Thread


bot = discord.Bot()
# import data file with info on how to fill out form
with open("users.json") as data:
    users = json.load(data)
async def screen(
    # see lines 32-45 to see purposes of args
    firstName,
    lastName,
    email,
    stateCode,
    schoolCode,
    session,
    answer1=0,
    answer2=0,
    answer3=3,
    floor="",
):
    """
    Function to fill out doe health screening.
    Variables are all as their name implies.
    """

    data = {
        "Type": "G",  # G = guest filling out form (aka students/parents)
        "IsOther": "False",  # for non guests and non teachers
        "IsStudent": "1",  # 0 for teacher, 1 for student
        "FirstName": firstName,  # first name of responder
        "LastName": lastName,  # last name of responder
        "Email": email,  # email to send success form to
        "State": stateCode,  # state code (2 letters)
        "Location": schoolCode,  # school code (4 characters)
        "Floor": floor,  # floor of school (optional)
        "Answer1": str(answer1),  # answer to question 1 (0 = non-covid answer)
        "Answer2": str(answer2),  # answer to question 2 (0 = non-covid answer)
        "Answer3": str(answer3),  # answer to question 3 (0 = non-covid answer)
        "ConsentType": "",  # not needed
    }
    async with session.post(
        "https://healthscreening.schools.nyc/home/submit", data=data
    ) as resp:  # make request to doe endpoint to submit the form
        return await resp.json()  # gather response json

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
async def req(student):
    async with aiohttp.ClientSession() as session:  # create aiohttp session object for sending requests
        # while True:  # continue forever
        screening = (  # fill out screening
            await screen(
                student["firstName"],
                student["lastName"],
                student["email"],
                student["stateCode"],
                student["schoolCode"],
                session,
            )
        )["success"]

        if screening:
            print("Successfully screened!","-",datetime.now())
        else:
            print("Error screening.")
                
    
async def main():
    """
    Main function, awaits the time to fill out form, and then fills out form.
    """

    print("Auto covid-form bot ready to boot.")
    print("Users:")
    print(json.dumps(users, indent=3))
    input("Press [ENTER] to start")
    print()
    # TODO:  use a better scheduling method than this
    while True: 
        if datetime.now().hour == "6" and datetime.datetime.today().weekday() < 5:
            for s in users:
                await req(s)
                await asyncio.sleep(1)
            await asyncio.sleep(82800)
            continue
        await asyncio.sleep(500)
        


    
            
def addstudent(first, last, email, school):
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
    schoolcode: Option(str, "School Code (NOT NAME, CHECK #info)"),
    ):
    addstudent(first, last, email, schoolcode)
    await ctx.respond(f"A health screening will now be sent every day at 6 am to your email!")
def runmain():
    asyncio.run(main())

Thread(target=runmain).start()

bot.run(os.getenv("TOKEN"))
