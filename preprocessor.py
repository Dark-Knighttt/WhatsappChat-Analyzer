import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({"user_message":messages,"message_dates":dates})
# converting message data type
    df['message_dates'] = pd.to_datetime(df['message_dates'],format = '%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_dates' : 'dates'} , inplace=True)
        
    user = []
    message = []
    for m in df['user_message']:
        entry = re.split('([\w\W]+?):\s',m)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('group_notification')
            message.append(entry[0])

        df['users'] = pd.Series(user)
        df['messages'] = pd.Series(message)
        df.drop(columns = ['user_message'])
    df['year']=df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['month_num'] = df['dates'].dt.month
    df['date_wise'] = df['dates'].dt.date
    df['active_month'] = df['month']
    df['day_name'] = df['dates'].dt.day_name()
    
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    df['period'] = period

    return df