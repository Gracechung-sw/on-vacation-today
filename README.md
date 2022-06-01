# on-vacation-today

Gcal ➔ Slack: Automatically update member's Slack status according to the current Google Calendar event. No Contact During Vacation!

---

This Desktop App automatically changes product team members status in certine Slack workspace, depending on the current event in your Google Calendar.

It is designed to run periodically from a cron job and, during each execution, it checks whether the current event Title in Google Calendar contains the match-text defined in the set of status rules.

```ini
status = {
    "연차": {'status_text': '[연차] Paid Time Off', 'status_emoji': ':shushing_face:'},
    "보상휴가": {'status_text': '[보상휴가] Paid Time Off', 'status_emoji': ':shushing_face:'},
    "재택근무": {'status_text': '[재택] Work From Home', 'status_emoji': ':house:'}
}
```

| Configurations | Description                                       | Maps to…                         |
| -------------- | ------------------------------------------------- | -------------------------------- |
| `key`          | key status value that product team set to use     | **Google Calendar**: Event Title |
| `status-emoji` | The symbol to display as the status               | **Slack**: Status Emoji          |
| `status-text`  | The status’ description (can also contain emojis) | **Slack**: Status Text           |

For more information, see this document.

---

## Credentials

### 1. Authorizing Requests to the Google Calendar API

Place credentials.json file in root directory of this project.
To generate this file, see https://developers.google.com/calendar/api/guides/auth

### 2. Slack users token

If you use free plan of Slack,  
Each users need user token that allowed `users.profile:write` scope.  
To generate this file, see https://api.slack.com/methods/users.profile.set, https://youtu.be/z9PD7-UXSbA  
and check src/app/slack_client.py how to use it.

---

## How to run

Git clone this repo and cd into the directory

```bash
python3 -m venv venv && source ./venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python3 src/app/main.py
```
