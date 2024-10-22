import os

from googleapiclient.discovery import build

# Replace with your YouTube Data API key
API_KEY = os.getenv('GOOGLE_API_KEY')


def youtube_search(query, max_results=5):
    # Build a resource object for interacting with the YouTube API
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    # Perform the search
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',  # Only return video results
        order='relevance',
        maxResults=max_results
    )
    response = request.execute()
    # Extract video details from the response\
    c = 0
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        print(f"Title: {title}")
        print(f"Video ID: {video_id}")
        print(f"Description: {description}")
        print(f"Watch Link: https://www.youtube.com/watch?v={video_id}")
        print("=" * 50)
        l = [title, f"https://www.youtube.com/watch?v={video_id}"]
        return l


# Example usage:
if __name__ == "__main__":
    search_term = input("Enter search keyword: ")
    print(youtube_search(search_term))
