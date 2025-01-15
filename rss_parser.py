import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from io import StringIO

def clean_html_content(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Handle lists separately for better formatting
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            li.insert_before("\n- ")
        ul.insert_before("\n")
        ul.unwrap()

    for ol in soup.find_all("ol"):
        for i, li in enumerate(ol.find_all("li"), start=1):
            li.insert_before(f"\n{i}. ")
        ol.insert_before("\n")
        ol.unwrap()

    # Extract and clean text
    text = soup.get_text(separator="\n").strip()
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)

    return text

def parse_rss_feed(rss_content):
    # Parse the RSS feed from string content
    tree = ET.parse(StringIO(rss_content))
    root = tree.getroot()

    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/"
    }

    data = []

    # Extract publication info from channel
    channel = root.find("channel")
    publication_info = {
        "title": channel.find("title").text if channel.find("title") is not None else "",
        "description": channel.find("description").text if channel.find("description") is not None else "",
        "link": channel.find("link").text if channel.find("link") is not None else ""
    }

    # Extract posts
    for item in root.findall(".//item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        description = item.find("description").text if item.find("description") is not None else ""
        content = item.find("content:encoded", namespaces)
        raw_html = content.text if content is not None else ""

        clean_content = clean_html_content(raw_html)

        data.append({
            "title": title.strip(),
            "link": link.strip(),
            "description": description.strip(),
            "content": clean_content
        })

    return {
        "publication_info": publication_info,
        "posts": data
    } 