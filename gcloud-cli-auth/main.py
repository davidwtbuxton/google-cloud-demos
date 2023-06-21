import logging

import flask
import google.cloud.logging
import googleapiclient.discovery


google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)
app = flask.Flask(__name__)


@app.route("/<sheet_id>")
def home(sheet_id):
    service = googleapiclient.discovery.build("sheets", "v4")
    request = service.spreadsheets().get(spreadsheetId=sheet_id)
    response = request.execute()

    return response
