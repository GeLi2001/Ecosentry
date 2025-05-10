from mcp.server.fastmcp import FastMCP
import base64
from openai import OpenAI
from typing import Optional
import os
from models import EnvironmentalIssue, EnvironmentalIssueType
from supabase_client import upload_image
import json



# Create an MCP server
mcp = FastMCP("Demo")

# Initialize OpenAI client
client = OpenAI()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add image analysis tool
@mcp.tool()
def analyze_image(image_path: str) -> str:
    """Analyze an image using OpenAI's Vision model
    
    Args:
        image_path: Path to the image file
        query: Question to ask about the image
    
    Returns:
        Analysis of the image content
    """
    try:
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Call OpenAI API
        response = client.responses.parse(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
            text_format=EnvironmentalIssue
        )
        
        # Parse the output text (string) into a dictionary
        print(response.output_text)
        image_response = json.loads(response.output_text)
        #return image_response
        # Check if the issue_type is not NONE before uploading to Supabase
        if image_response["issue_type"] != EnvironmentalIssueType.NOT_QUALIFIED:
            # Upload image to Supabase and get public URL
            public_url = upload_image(image_path)
            image_response["image_url"] = public_url
        
        return json.dumps(image_response)
    except Exception as e:
        return f"Error analyzing image: {str(e)}"