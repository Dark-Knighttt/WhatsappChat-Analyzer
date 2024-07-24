import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # to read file as bytes
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    
    selected = st.sidebar.selectbox("Show analysis wrt", user_list)

    # stats area
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media,links = helper.fetch_stats(selected,df)
        st.title('Top Statistics')

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("Links shared")
            st.title(links)

    # month wise timeline
    st.title('Monthly Timeline')
    timeline = helper.monthly_timeline(selected,df)
        # st.dataframe(timeline)
    
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['messages'], color = 'green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline
    st.title("Daily Activity")
    
    daily_timeline = helper.daily_timeline(selected,df)
        # st.dataframe(daily_timeline)

    fig,ax = plt.subplots()
    # plt.figure(figsize = (18,10))
    ax.plot(daily_timeline['date_wise'],daily_timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # busiest month
    col1, col2 = st.columns(2)
    with col1:
        st.title('Weekly activity Map')
        active_month = helper.most_active_month(selected,df)
        # st.dataframe(active_month)
        active_day = helper.most_active_day(selected,df)
        fig,ax = plt.subplots()
        ax.bar(active_day['day_name'],active_day['messages'], color = 'pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.title('Monthly activity map')
        fig,ax = plt.subplots()
        ax.bar(active_month['active_month'],active_month['messages'], color = 'orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # most active day of week
    # col1, col2 = st.columns(2)
    # with col1:
    #     active_day = helper.most_active_day(selected,df)
    #     st.dataframe(active_day)
    # with col2:
    #     fig,ax = plt.subplots()
    #     ax.bar(active_day['day_name'],active_day['messages'], color = 'green')
    #     plt.xticks(rotation='vertical')
    #     st.pyplot(fig)

    # finding busiest users in group
    if selected == 'Overall':
        st.title('Most Busy Users')
        x,new_df = helper.most_busy_user(df)
        fig, ax = plt.subplots()
        
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values,  color = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # wordcloud
    df_wc = helper.create_wordcloud(selected,df)
    st.title('Wordcloud')
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most common words
    most_common_df = helper.most_common_words(selected, df)
    st.title('Most Common Words')

    col1,col2 = st.columns(2)
    with col1:
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
    with col2:
        st.dataframe(most_common_df)

    #most common emoji
    emoji_helper = helper.emoji_helper(selected,df)
    st.title('Analyzing Emojis')
    
    col1,col2 = st.columns(2)
    with col1:
        fig,ax = plt.subplots()
        ax.pie(emoji_helper[1],labels = emoji_helper[0],autopct = "%0.2f")

        st.pyplot(fig)
    with col2:
        st.dataframe(emoji_helper)

    # activity heatmap
    activity_heatmap = helper.activity_heatmap(selected,df)
    st.title('Activity Heatmap')
    fig,ax = plt.subplots()
    ax = sns.heatmap(activity_heatmap)
    st.pyplot(fig)
    plt.yticks(rotation='horizontal')
    # plt.show()

    