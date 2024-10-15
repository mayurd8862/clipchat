import streamlit as st
import requests
import re
import pandas as pd
from googleapiclient.discovery import build


def get_video_and_channel_id(youtube_url, api_key):
    # Regular expression patterns for different YouTube link formats
    patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
    ]
    
    # Extract video ID
    video_id = None
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            video_id = match.group(1)  # Return the video ID
            break
    
    if not video_id:
        return None, None  # Return None if video ID is not found

    # Get channel ID from video ID
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet'
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        channel_id = data['items'][0]['snippet']['channelId']
        return video_id, channel_id
    else:
        return video_id, None  # Return None for channel ID if not found



# Function to get channel data (same as before)
def get_channel_data(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]
    except Exception as e:
        st.error(f'Error fetching channel data: {e}')
    return None



# Function to get video data
def get_video_data(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]
    except Exception as e:
        st.error(f'Error fetching video data: {e}')
    return None



def get_video_comments(video_id, api_key, max_comments):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None
    comments_fetched = 0

    while comments_fetched < max_comments:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=min(100, max_comments - comments_fetched),
            pageToken=next_page_token
        ).execute()

        for item in response.get('items', []):
            comment_info = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment_info['authorDisplayName'],
                'text': comment_info['textDisplay'],
                'published_at': comment_info['publishedAt']
            })
            comments_fetched += 1
            if comments_fetched >= max_comments:
                break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return pd.DataFrame(comments)


# # Streamlit app layout
# st.title("YouTube Video and Channel Analysis")

# # Input for API key
# API_KEY = st.text_input("Enter Your YouTube API Key", type="password")

# # Input for Channel ID
# channel_id = st.text_input("Enter Channel ID", value="UC_x5XG1OV2P6uZZ5FSM9Ttw")  # Example Channel ID (Google Developers)

# if st.button("Get Channel Data"):
#     if API_KEY:
#         channel_info = get_channel_data(channel_id, API_KEY)
#         if channel_info:
#             st.subheader('Channel Data:')
#             st.write(f"**Title:** {channel_info['snippet']['title']}")
#             st.write(f"**Description:** {channel_info['snippet']['description']}")
#             st.write(f"**Subscribers:** {channel_info['statistics']['subscriberCount']}")
#             st.write(f"**Total Views:** {channel_info['statistics']['viewCount']}")
#             st.write(f"**Video Count:** {channel_info['statistics']['videoCount']}")
#         else:
#             st.error('Channel data not found.')
#     else:
#         st.error('Please enter a valid API key.')

# # Input for Video ID
# video_id = st.text_input("Enter Video ID", value="dQw4w9WgXcQ")  # Example Video ID

# max_comments = st.slider("Select the number of comments to fetch", min_value=10, max_value=1000, step=10, value=50)

# if st.button("Get Video Comments"):
#     if API_KEY:
#         comments_df = get_video_comments(video_id, API_KEY, max_comments)
#         if not comments_df.empty:
#             st.subheader('Video Comments:')
#             st.dataframe(comments_df)
#         else:
#             st.error('No comments found or comments are disabled for this video.')
#     else:
#         st.error('Please enter a valid API key.')

#     video_info = get_video_data(video_id, API_KEY)
#     if video_info:
#             st.subheader('Video Data:')
#             st.write(f"**Title:** {video_info['snippet']['title']}")
#             st.write(f"**Description:** {video_info['snippet']['description']}")
#             st.write(f"**Published At:** {video_info['snippet']['publishedAt']}")
#             st.write(f"**Views:** {video_info['statistics']['viewCount']}")
#             st.write(f"**Likes:** {video_info['statistics'].get('likeCount', 'N/A')}")
#             st.write(f"**Comments Count:** {video_info['statistics']['commentCount']}")

# # Optional: Add more features such as visualizations or additional data analysis
