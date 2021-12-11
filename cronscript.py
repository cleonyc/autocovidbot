from datetime import datetime
import aiohttp
import json
import asyncio
import sqlite3


con = sqlite3.connect('users.db')
cur = con.cursor()


async def main():
    """
    Main function, awaits the time to fill out form, and then fills out form.
    """
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    # print(users)
    con.commit()
    con.close()

    print("Sending covid screenings!")
    print("Users:")
    print(users)
    
    for s in users:
        await req(s)
        await asyncio.sleep(1)


async def req(student):
    async with aiohttp.ClientSession() as session:  

        screening = (
            await screen(
                student[1],
                student[2],
                student[3],
                "NY",
                student[4],
                session,
            )
        )["success"]

        if screening:
            print("Successfully screened!", "-", datetime.now())
        else:
            print("Error screening.")


async def screen(
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

asyncio.run(main())
con.close()
