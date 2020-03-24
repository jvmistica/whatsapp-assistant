import random
import pytz
from datetime import datetime, timezone
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from cloud_sql import search_table, insert_record


app = Flask(__name__)
local_tz = pytz.timezone("Singapore")


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    resp = MessagingResponse()
    text = request.values.get("Body")
    msg_samples = ["Gotcha.", "Okay, I saved it.", "Consider it done.", "Saved it.", "All good.", "Got it."]

    if text.lower()[:9] == "new note:":
        timestamp = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%m/%d/%y %H:%M")
        title = timestamp + " " + text[9:].strip().capitalize()
        try:
            insert_record("Notes", title=title, description="")
            msg = resp.message(random.choice(msg_samples))
        except Exception as err:
            msg = resp.message(str(err))
    else:
        result = [i[0] for i in search_table("Notes", "title")]
        msg = resp.message(f"\n".join(result))

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
