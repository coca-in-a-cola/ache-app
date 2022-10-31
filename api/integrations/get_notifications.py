from datetime import datetime, timedelta
from email import message
from api.model.event import Event

def get_notifications(user):
    userEvents = user.events
    result = []
    for event in userEvents:
        eventDetail = Event.query.get(event.eventUUID)
        
        if (datetime.utcnow() < eventDetail.datetimeEnd and event.status == 1
            or (datetime.utcnow() - eventDetail.datetimeStart < timedelta(minutes=30) and event.status != 0)):
            result.append(eventDetail)
    
    return sorted(result, key=lambda e: e.datetimeStart, reverse=True)


def notify(event, participant):
    pass