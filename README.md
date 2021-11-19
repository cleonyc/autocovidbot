# Auto Covid Bot

Automatically fill out the NYC DOE health screening form and trigger an email with the success verification.

To use, create a `data.json` file in the same directory as `main.py` with the format:
```json
{
    "firstName":"X",
    "lastName":"X",
    "email":"X@X.X",
    "stateCode":"XX",
    "schoolCode":"XXXX",
    "sendHour":0
}
```

* School code is the 4 character code specific to your NYC school. You can find the school code (here)[https://schoolsearch.schools.nyc/]. For example, "Q300."
* State code is the 2 character state abbreviation. For example, "NY".
* Send hour is the hour in which the bot should submit the form. This is in 24 hour time. For example, 8 = 8AM, and 13 = 1PM.
* If you get a `ModuleNotFound` error, type `pip install <name of the module that wasn't found>` into console. You may need to close and reopen console after it is installed.

Note: you should not need to modify `main.py` to get the bot working.

To use, simply run `main.py` by typing `python main.py` into your console, from the same directory the file is in.
