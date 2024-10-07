import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def extract_transcript_and_metadata(youtube_video_url):
    try:
        # Extract video ID from the URL using regex
        video_id_match = re.search(r'(v=|be/|embed/|v/|watch\?v=|watch\?.+&v=)([^#&?]*)(.*)?', youtube_video_url)
        if video_id_match:
            video_id = video_id_match.group(2)
        else:
            raise ValueError("Invalid YouTube URL")
        
        # Fetch the transcript
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['mr', 'en'])

        # Concatenate transcript into a single string
        transcript = " ".join([entry["text"] for entry in transcript_text])

        # Fetch video metadata using pytube
        yt = YouTube(youtube_video_url)
        metadata = {
            "title": yt.title,
            "description": yt.description,
            "publish_date": yt.publish_date.strftime("%Y-%m-%d") if yt.publish_date else "N/A",
            "views": yt.views,
            "length": yt.length,
            "author": yt.author
        }

        return {
            "transcript": transcript,
            "metadata": metadata
        }

    except Exception as e:
        raise e

# Example usage
# video_url = "https://youtu.be/GPuOMDIEcNo?si=6e9Ok6P4di3Vb2Jg"
# details = extract_transcript_and_metadata(video_url)

# Display the details
# print("Title:", details["metadata"]["title"])
# # print("Description:", details["metadata"]["description"])
# print("Publish Date:", details["metadata"]["publish_date"])
# print("Views:", details["metadata"]["views"])
# print("Length (seconds):", details["metadata"]["length"])
# print("Author:", details["metadata"]["author"])
# print("\n")
# print("Transcript:", details["transcript"])
