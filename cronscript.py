from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import aiohttp
import json
import asyncio

with open("users.json") as d:
    users = json.load(d)


async def main():
    """
    Main function, awaits the time to fill out form, and then fills out form.
    """

    print("Sending covid screenings!")
    print("Users:")
    print(json.dumps(users, indent=3))
    for s in users:
        await req(s)
        await asyncio.sleep(1)


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
            print("Successfully screened!", "-", datetime.now())
        else:
            print("Error screening.")


async def screen(
        # see lines 32-45 to see purposes of args
        first_name,
        last_name,
        email,
        state_code,
        school_code,
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
        "FirstName": first_name,  # first name of responder
        "LastName": last_name,  # last name of responder
        "Email": email,  # email to send success form to
        "State": state_code,  # state code (2 letters)
        "Location": school_code,  # school code (4 characters)
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
