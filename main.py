from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from cloud_sql import search_table


app = Flask(__name__)


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming calls with a MMS message."""

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a text message
    notes = search_table("Notes", "title")
    msg = resp.message(str(notes))

    # Add a picture message
    # msg.media("https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
