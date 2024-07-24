# import pyplot as plt
from wordcloud import WordCloud
from urlextract import URLExtract
extract = URLExtract()
import pandas as pd
import emoji
from collections import Counter
def fetch_stats(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    
    # no. of messages
    num_messages = df.shape[0]
    # no.of words
    words = []
    for m in df['messages']:
        words.extend(m.split())
    # no. of media messages
    num_media = df[df['messages'] == '<Media Omitted>/n'].shape[0]

    # number of links
    links = []
    for m in df['messages']:
        links.extend(extract.find_urls(m))
    return num_messages,len(words),num_media,len(links)


    # if selected == 'Overall':
    #     num_messages = df.shape[0]
    #     words = []
    #     for m in df['messages']:
    #         words.extend(m.split())
    #     return num_messages,len(words)
    # else:
    #     new_df = df[df['users'] == selected]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for m in new_df['messages']:
    #         words.extend(m.split())
    #     return num_messages,len(words)

def most_busy_user(df):
    x = df['users'].value_counts().head()
    # name = x.index
    # count = x.values
    # plt.bar(name,count)
    # plt.xticks(rotation = 'vertical')
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name','users':'percent'})
    # plt.show()
    return x,df

def create_wordcloud(selected , df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected != 'Overall':
        df = df[df['users'] == selected]
    temp = df[df['users']!= 'group_notification']
    temp = temp[temp['messages'] != '<Media Omitted>\n']
    
    def remove_stop_words(messages):
        y = []
        for w in messages.lower().split():
            if w not in stop_words:
                y.append(w)
        return " ".join(y)

    wc = WordCloud(width = 500, height = 500 , min_font_size = 10, background_color = 'white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected != 'Overall':
        df = df[df['users'] == selected]
    temp = df[df['users']!= 'group_notification']
    temp = temp[temp['messages'] != '<Media Omitted>\n']
    words = []
    for m in temp['messages']:
        for word in m.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    num_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return num_emoji

def monthly_timeline(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    
    return timeline

def daily_timeline(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    daily_timeline = df.groupby('date_wise').count()['messages'].reset_index()
    return daily_timeline

def most_active_month(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    active_month = df.groupby('active_month').count()['messages'].reset_index() 
    return active_month

def most_active_day(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    active_day = df.groupby('day_name').count()['messages'].reset_index()
    return active_day

def activity_heatmap(selected,df):
    if selected != 'Overall':
        df = df[df['users'] == selected]
    activity_heatmap = df.pivot_table(index='day_name', columns = 'period',values='messages',aggfunc='count').fillna(0) 
    return activity_heatmap
