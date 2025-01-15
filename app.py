import streamlit as st
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from rss_parser import parse_rss_feed
from stylesheet_generator import generate_stylesheet
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_rss_feed(publication_url):
    """Fetch RSS feed from a Substack publication URL"""
    # Clean the URL
    publication_url = publication_url.rstrip('/')
    
    # Try different RSS feed URL patterns
    feed_urls = [
        f"{publication_url}/feed",  # Standard pattern
        f"{publication_url}/rss",   # Alternative pattern
        f"https://{publication_url.split('/')[-1]}.substack.com/feed"  # Convert custom domain to substack.com
    ]
    
    last_error = None
    for feed_url in feed_urls:
        try:
            response = requests.get(feed_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            last_error = e
            continue
    
    # If we get here, none of the URLs worked
    raise Exception(f"Could not fetch RSS feed. Please ensure this is a valid Substack publication URL. Last error: {last_error}")

def main():
    st.title("Substack Stylesheet Generator")
    
    # User input for Substack URL
    publication_url = st.text_input(
        "Enter Substack Publication URL",
        placeholder="https://example.substack.com"
    )
    
    if st.button("Generate Stylesheet") and publication_url:
        try:
            with st.spinner("Fetching RSS feed..."):
                rss_content = get_rss_feed(publication_url)
            
            with st.spinner("Parsing content..."):
                publication_data = parse_rss_feed(rss_content)
            
            with st.spinner("Generating stylesheet..."):
                stylesheet = generate_stylesheet(publication_data)
            
            # Display the generated stylesheet
            st.code(stylesheet, language='css')
            
            # Add download button
            st.download_button(
                label="Download Stylesheet",
                data=stylesheet,
                file_name="publication_style.css",
                mime="text/css"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 