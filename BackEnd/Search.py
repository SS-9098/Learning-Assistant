import requests


# Define the function to search articles
def search_query(query):
    # Set up API endpoint and headers with your RapidAPI details
    url = "https://real-time-web-search.p.rapidapi.com/search"

    querystring = {"q": query, "limit": "2"}  # Using the passed query as input

    headers = {
        "x-rapidapi-key": "129f14a6famsh22282ee9f5122a2p14e6bcjsn6f2761a1d1b3",  # Replace with your actual API key
        "x-rapidapi-host": "real-time-web-search.p.rapidapi.com"
    }

    # Send GET request to the API
    response = requests.get(url, headers=headers, params=querystring)

    # Print the full response for debugging
    print("Full Response:", response.text)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:  # Access the correct 'data' key
            articles = []
            for article in data['data']:
                articles.append({
                    "title": article['title'],
                    "snippet": article['snippet'],
                    "url": article['url']
                })
            return articles  # Return list of articles with title, snippet, and url
        else:
            print("No articles found.")
            return None  # No articles found
    else:
        print(f"Error: {response.status_code}, {response.text}")  # Print error details
        return {"error": response.status_code, "message": response.text}  # Return error if API call fails


if __name__ == "__main__":
    # Take input from the user for the search query
    search_query_input = input("Enter the topic you want to search for: ")

    # Run the search query and store the results
    result = search_query(search_query_input)

    # Check if results are found and print them
    if result:
        for article in result:
            print(f"\nTitle: {article['title']}")
            print(f"Snippet: {article['snippet']}")
            print(f"Link: {article['url']}")
    else:
        print("No articles found or an error occurred.")
