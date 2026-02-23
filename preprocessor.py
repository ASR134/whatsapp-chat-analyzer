import re
import pandas as pd
def preprocess(data):

    # unusual space b/w time and am/pm
    data = data.replace("\u202f", " ") 

    # Separating Date/time and User/message
    pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s"

    # list of strings
    messages = re.split(pattern,data)[1:] 
    dates = re.findall(pattern,data)

    dates = pd.Series(dates)
    dates = pd.to_datetime(dates.str.replace(" - ","",regex=False),format="%m/%d/%y, %I:%M %p")
    df = pd.DataFrame({
    "user_message" : messages,
    "message_date" : dates
    })

    user = []
    message = []

    for text in df["user_message"]:
        entry = re.split(r"([\w\W]+?):\s", text)
        if len(entry)>1:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("group notification")
            message.append(entry[0])

    df["user"] = user
    df["message"] = message
    df.drop(columns="user_message",inplace=True)

    df["year"] = df["message_date"].dt.year
    df["month"] = df["message_date"].dt.month_name()
    df["month_name"] = df["message_date"].dt.month
    df["day"] = df["message_date"].dt.day
    df["day_name"] = df["message_date"].dt.day_name()
    df["hour"] = df["message_date"].dt.hour
    df["minute"] = df["message_date"].dt.minute

    df = df.sort_values(by="hour",ascending=True)
    period = []
    for hour in df["hour"]:
        if hour==23:
            period.append(str(hour)+" - "+'00')
        elif hour==0:
            period.append(str(00)+" - "+'1')
        else:
            period.append(str(hour)+" - "+str(hour+1))
    df["period"] = period
    df.drop(columns="message_date",inplace=True)
    df.reset_index(inplace=True)

    return df