# Auto Covid Bot

Automatically fill out the NYC DOE health screening form and trigger an email with the success verification.

To use, create a `data.json` file with the format:
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

Then run main.py, and hit enter to start.
Note that sendhour is in 24 hour time, based on your pc's/server's clock