import requests
import json
import os

from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader

class WebTools:

    @tool('search internet')
    def search_internet(query:str) -> str:
        """
        Use this tool to search internet for information. This tool returns 5 results from Google search engine.
        """
        return WebTools.search(query)

    def search(query, limit=5):
        url = "https://google.serper.dev/search"

        payload = json.dumps({
        "q": query,
        "num": limit
        })
        headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']

        string =[]
        for result in results:
            string.append(f"{result['title']}\n{result['snippet']}\n{result['link']}\n\n")
        return f"Search results for '{query}':\n\n" + "\n".join(string)
    

# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     load_dotenv()
#     product_url="https://www.nike.com/w/white-air-force-1-shoes-4g797z5sj3yzy7ok"
#     product_info = WebTools.get_product_info(product_url)
#     # Check if data is retrieved successfully
#     # Check if data is retrieved successfully
#     if product_info:
#         print("Product Information:")
#         # Try to access all potential data fields using a loop
#         for key, value in product_info.items():
#             print(f"  {key}: {value}")  # Print key-value pairs
#         else:
#             print("Failed to retrieve product information.")