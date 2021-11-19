"""
By using you agree to https://github.com/bread/autoCovid/blob/main/LICENSE
"""

import aiohttp
import asyncio
import sys
from datetime import datetime
import json

# import data file with info on how to fill out form
with open("data.json") as data:
    data = json.load(data)


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


async def main():
    """
    Main function, awaits the time to fill out form, and then fills out form.
    """

    print("Auto covid-form bot ready to boot.")
    print("Settings:")
    print(json.dumps(data, indent=3))
    input("Press [ENTER] to start")
    print()

    async with aiohttp.ClientSession() as session:  # create aiohttp session object for sending requests
        while True:  # continue forever
            if datetime.now().hour == data["sendHour"]:  # when it's the hour to send
                screening = (  # fill out screening
                    await screen(
                        data["firstName"],
                        data["lastName"],
                        data["email"],
                        data["stateCode"],
                        data["schoolCode"],
                        session,
                    )
                )["success"]

                # break on fail; wait an hour on success
                if screening:
                    print("Successfully screened!","-",datetime.now())
                    await asyncio.sleep(60 * 61)
                else:
                    print("Error screening.")
                    break
            else:
                # don't overload cpu by running datetime.now() every microsecond; instead sleep every lapse
                await asyncio.sleep(1)


if sys.platform == "win32":
    # prevent "Event loop is closed" error on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
