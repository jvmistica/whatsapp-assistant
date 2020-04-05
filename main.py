import logging
import pytz
import random
from datetime import datetime, timezone
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from cloud_sql import search_table, insert_record, show_record, update_record, delete_record


app = Flask(__name__)
local_tz = pytz.timezone("Singapore")
logging.basicConfig(level=logging.INFO)
msg_samples = ["Gotcha.", "Okay, I saved it.", "Consider it done.", "Saved it.", "All good.", "Got it."]


@app.route("/sms", methods=["POST"])
def sms_reply():
    resp = MessagingResponse()
    text = request.values.get("Body").lower()
    action = text.split(":")[0]
    text = text.replace(action, "")[2:].strip().capitalize()
    logging.info("Received a message with action '%s' and text '%s'", action, text)

    if action[:3] == "new":
        x_new_record(text, action)
    elif action[:4] == "show":
        txt = x_show_record(text, action)
        msg = resp.message(txt)
        return str(resp)
    elif action[:4] == "edit":
        x_edit_record(text, action)
    elif action[:6] == "delete":
        x_delete_record(text, action)
    else:
        pass

    resp.message(random.choice(msg_samples))
    return resp


def x_new_record(text, action):
    logging.info("Creating new record for '%s' and text '%s'", action, text)
    if "note" in action:
        timestamp = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%m/%d/%y %H:%M")
        title = timestamp
        insert_record("Notes", title=title, details=text.capitalize())
    elif "recipe" in action:
        title = text.split(";")[0].capitalize()
        details = text.split(";")[1].strip().capitalize()
        insert_record("Recipes", title=title, details=details)
    elif "item" in action:
        title = text.capitalize()
        insert_record("Items", title=title, details="")
    else:
        pass


def x_edit_record(text, action):
    logging.info("Editing '%s' record with text '%s'.", action, text)
    if "note" in action:
        title = text.split("->")[0].strip()
        updated_details = text.split("->")[1].strip().capitalize()
        rid = show_record("Notes", title=title)[0]
        update_record("Notes", title=title, details=updated_details, id=rid)
    elif "recipe" in action:
        title = text.split("->")[0].strip()
        updated_details = text.split("->")[1].strip().capitalize()
        rid = show_record("Recipes", title=title)[0]
        update_record("Recipes", title=title, details=updated_details, id=rid)
    elif "item" in action:
        title = text.split("->")[0].strip()
        updated_title = text.split("->")[1].strip().capitalize()
        rid = show_record("Items", title=title)[0]
        update_record("Items", title=updated_title, details="", id=rid)
    else:
        pass


def x_show_record(text, action):
    logging.info("Showing '%s' records.", action)
    table_name = action.replace("show ", "").replace(".", "").capitalize()
    if table_name == "Notes":
        result = [": ".join(i) for i in search_table(table_name, "title", "details")]
        result = "\n".join(result)
    elif table_name in ["Items", "Recipes"]:
        result = "\n".join([i[0] for i in search_table(table_name, "title")])
    else:
        result = x_show_details(text, action)
    return result


def x_delete_record(text, action):
    logging.info("Deleting '%s' record '%s'.", action, text)
    table_name = action.replace("delete ", "").replace(":", "").capitalize() + "s"
    delete_record(table_name, text)


def x_show_details(text, action):
    logging.info("Showing details for '%s' record '%s'.", action, text)
    table_name = action.replace("show ", "").replace(".", "").capitalize()
    if table_name == "Notes":
        result = [": ".join(i) for i in search_table(table_name, "title", "details")]
        result = "\n".join(result)
    elif table_name in ["Items", "Recipes"]:
        result = "\n".join([i[0] for i in search_table(table_name, "title")])
    else:
        table_name = (action.replace("show ", "").split()[0] + "s").capitalize()
        result = show_record(table_name, title=text)
        result = f"*{result[1]}*\n{result[2]}"
    return result


if __name__ == "__main__":
    app.run(debug=True)
