import streamlit as st
import pandas as pd
import plotly.express as px

from src.analysis import get_channel_data, get_video_and_channel_id, get_video_comments, get_video_data
API_KEY = "AIzaSyCvK1NgmC04lkoMMXS7dYDjCSlLM1Ymb38"
# link = st.text_input("Enter your link")
link = st.session_state['url']
# btn = st.button("Analyze")


if link:
    # if btn and link:
    video_id, channel_id = get_video_and_channel_id(link,API_KEY)

    st.markdown("## 📢 Channel Information")
    # st.markdown("## 📺 Channel Information")

    channel_data = get_channel_data(channel_id,API_KEY)

    # Extract channel information
    channel_name = channel_data['snippet']['title']
    channel_description = channel_data['snippet']['description']

    # Display channel information
    st.markdown(f"#### Channel Name : {channel_name}")

    desc = st.checkbox("View Channel Description")

    if desc:
        st.markdown(channel_description)

    data = {
        # 'Metric': ['Subscribers', 'Video Count'],
        'Metric': ['Channel Name','Subscribers', 'Total Views','Video Count'],
        'Count': [
            channel_data['snippet']['title'],
            int(channel_data['statistics']['subscriberCount']),
            int(channel_data['statistics']['viewCount']),
            int(channel_data['statistics']['videoCount'])
        ]
    }
    df = pd.DataFrame(data)

    st.markdown(f"#### Other Statistical Information")
    st.dataframe(df)


    # Create pie chart

    filtered_df = df[~df['Metric'].isin(['Channel Name', 'Video Count'])]
    filtered_df = filtered_df.reset_index(drop=True)

    fig = px.pie(filtered_df, values='Count', names='Metric', title='Channel Statistics', hole=0.3)
    st.plotly_chart(fig)



    st.markdown("## 🎥 Video Statistics")


    video_data = get_video_data(video_id,API_KEY)


    st.markdown(f"#### **Video Title :** {video_data['snippet']['title']}")

    st.video(link)

    vid_desc = st.checkbox("Show Video Description")
    if vid_desc:
        st.markdown(video_data['snippet']['description'])

    # st.write(video_data)
    data = {
        'Metric': [
            'Video Title',
            'Published Date',  # Add a comma here
            'Total Views',
            'Likes',
            'Comments Count'
        ],
        'Count': [
            video_data['snippet']['title'],
            video_data['snippet']['publishedAt'],
            int(video_data['statistics']['viewCount']),
            int(video_data['statistics'].get('likeCount', 0)), 
            int(video_data['statistics']['commentCount'])
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame in the Streamlit app
    st.markdown(f"#### Other Statistical Information")
    st.write(df)

    filtered_df = df[~df['Metric'].isin(['Comments Count'])]
    filtered_df = filtered_df.reset_index(drop=True)

    fig = px.pie(filtered_df, values='Count', names='Metric', title='Video Statistics', hole=0.3)
    st.plotly_chart(fig)

    max_comments = st.slider("Select the number of comments to fetch", min_value=10, max_value=500, step=10, value=50)
    comments_df = get_video_comments(video_id, API_KEY, max_comments)
    st.dataframe(comments_df)

else:
    st.info("Please enter a YouTube URL and click 'Submit and Load Data' to start chatting.")






