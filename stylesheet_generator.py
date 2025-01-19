from openai import OpenAI
import streamlit as st
import json
import anthropic

def generate_stylesheet(publication_data, ai_choice):
    """Generate a writer's stylesheet based on the publication's content"""
    
    # Initialize OpenAI client with Streamlit secret
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=st.secrets["ANTHROPIC_API_KEY"]
    )

    
    # Extract publication info and posts
    pub_info = publication_data["publication_info"]
    posts = publication_data["posts"]
    
    # Combine content from all posts into a single text corpus
    content_samples = "\n\n".join([
        f"Title: {post['title']}\n{post['content']}" 
        for post in posts[:5]  # Limit to first 5 posts to stay within token limits
    ])
    
    # Prompt for GPT-4
    prompt = """You are an expert ghostwriter who manages a team of junior ghostwriters. 
    I am going to give you a bunch of sample content from a client you are working with, 
    and I want you to extract a stylesheet. It should be something you can give to your 
    junior ghostwriters so they can reliably produce content that sounds exactly like 
    the client's voice. Pay attention to tone, style, and sentence construction. 
    Avoid giving overly specific examples from one piece, as those might be over-applied. 
    Instead, provide multiple examples that highlight a clear style or tone.

    Here is the sample content:

    {content}"""
    
    # Create messages array
    messages = [
        {"role": "system", "content": "You are an expert writing style analyst."},
        {"role": "user", "content": prompt.format(content=content_samples)}
    ]
    
    try:
        if ai_choice == "gpt":
            # Existing GPT API call
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        elif ai_choice == "claude":
            # Claude API call
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt.format(content=content_samples)}
                ]
            )
            return response.content[0].text
    except Exception as e:
        raise Exception(f"Error generating stylesheet: {str(e)}")
        
    