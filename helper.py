from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(selected_user,df):

    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]
    
    # no. of messages
    num_messages = df.shape[0]
    # no. of words
    words = 0
    for m in df["message"]:
        words += len(m.split())
    
    # no. of media elements
    media_elements = df[df["message"]=="<Media omitted>\n"].shape[0]

    # no. of links
    extractor = URLExtract()
    links = 0
    for m in df["message"]:
        l = extractor.find_urls(m)
        links += len(l)

    return num_messages, words, media_elements, links

def most_busy_users(df):

    x = df[df["user"]!="group notification"]
    x = x["user"].value_counts().head()

    new_series = round(x/df.shape[0]*100,2)
    new_df = pd.DataFrame({
        "Name": new_series.index,
        "Percent" : new_series.values
    })
    return x, new_df



def create_wordcloud(selected_user,df):

    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]

    with open("stop_hinglish.txt","r") as f:
        stop_hinglish = f.read()

    temp = df[df["user"]!="group notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    temp = temp[temp["message"] != "<Video note omitted>\n"]
    temp = temp[temp["message"] != "<message deleted>\n"]
    temp = temp[temp["message"] != "<message edited>\n"]

    def remove_stop_words(message):
        l = []
        for word in message.lower().split():
            if word not in stop_hinglish:
                l.append(word)
        return " ".join(l)
    
    temp["message"] = temp["message"].apply(remove_stop_words)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user,df):
    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]

    temp = df[df["user"]!="group notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    temp = temp[temp["message"] != "<Video note omitted>\n"]

    with open("stop_hinglish.txt","r") as f:
        stop_hinglish = f.read()

    words = []
    for m in temp["message"]:
        for word in m.lower().split(" "):
            if word not in stop_hinglish:
                words.append(word)
        
    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user,df):
    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]
    
    emojis = []

    for m in df["message"]:
        emojis.extend([c for c in m if emoji.is_emoji(c)])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    

def monthly_timeline(selected_user,df):

    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]

    timeline = df.groupby(["year","month_num","month"]).count()["message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + " - " + str(timeline["year"][i]))

    timeline["time"] = time
    return timeline

def active_days(selected_user,df):

    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]
    
    return df["day_name"].value_counts()

def active_months(selected_user,df):

    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]
    
    return df["month"].value_counts()

def activity_heatmap(selected_user,df):
    if (selected_user != "Overall"):
        df = df[df["user"]==selected_user]

    mat =df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)

    return mat