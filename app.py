import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode(encoding="utf-8")
    df = preprocessor.preprocess(data)


    # fetch unique users
    users_list = df["user"].unique().tolist()
    users_list.remove("group notification")
    users_list = sorted(users_list)
    users_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",users_list)

    if st.sidebar.button("Show Analysis"):
        
        st.title("Top Statistics")
        num_messages, words, media_elements, links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Elements")
            st.title(media_elements)

        with col4:
            st.header("Links Shared")
            st.title(links)


        # timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline["time"],timeline["message"],color="m")
        plt.ylabel("No. of messages")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)


        # active days
        st.title("Activity Map")
        
        col1, col2 = st.columns(2)
        with col1:
            day_series = helper.active_days(selected_user,df)
            fig,ax = plt.subplots()
            ax.barh(day_series.index,day_series.values.tolist(),color="g")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        with col2:
            month_series = helper.active_days(selected_user,df)
            fig,ax = plt.subplots()
            ax.barh(month_series.index,month_series.values.tolist(),color="g")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        # Most busy users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df= helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        
        # wordcloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words 
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = "vertical")
        st.title("Most Common Words")
        st.pyplot(fig)


        # popuar emoji

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head().tolist(),shadow=True,explode=[0.1 for i in range(emoji_df.head().shape[0])],autopct="%0.2f")
            st.pyplot(fig)

        # activity heatmap
        st.title("Activity Heatmap")
        mat_heatmap = helper.activity_heatmap(selected_user,df)

        fig,ax = plt.subplots()
        ax = sns.heatmap(mat_heatmap,cmap="Blues")
        st.pyplot(fig)
