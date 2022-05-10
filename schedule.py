from flask import request, Blueprint

schedule_api = Blueprint('schedule_api', __name__)

@schedule_api.route("/api/schedule")
def scheduletest():
    return "schedule"