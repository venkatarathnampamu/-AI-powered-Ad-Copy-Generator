import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = os.getenv("API_URL", "https://api.openai.com/v1/chat/completions")
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")

TONES = {
    "professional": "Use a formal, trustworthy, and authoritative tone.",
    "casual": "Use a friendly, conversational, and relaxed tone.",
    "urgent": "Use an urgent, action-driven tone with scarcity language.",
    "humorous": "Use a funny, witty, and entertaining tone.",
    "luxury": "Use an elegant, exclusive, and premium tone.",
}

PLATFORMS = {
    "facebook": "Facebook ad (max 40 characters headline, 125 characters description).",
    "instagram": "Instagram caption (concise, visual-focused, with hashtags).",
    "google": "Google Search ad (max 30 characters headline, 90 characters description).",
    "twitter": "X/Twitter ad (max 280 characters including hashtags).",
    "linkedin": "LinkedIn ad (professional tone, B2B-focused, max 150 characters).",
}


def build_prompt(product_name, product_desc, target_audience, tone, platform):
    tone_guide = TONES.get(tone, TONES["professional"])
    platform_guide = PLATFORMS.get(platform, PLATFORMS["facebook"])

    prompt = f"""You are an expert advertising copywriter. Generate a high-converting advertisement for the following product or service.

Product/Service Name: {product_name}
Description: {product_desc}
Target Audience: {target_audience}
Tone: {tone_guide}
Platform: {platform_guide}

Generate the ad copy in the following structured format:

Headline: (one powerful headline)
Description: (short engaging description)
Call To Action: (compelling CTA line)
Hashtags: (3-5 relevant hashtags if applicable for social media)

Keep the content persuasive, engaging, and platform-appropriate."""
    return prompt


def validate_input(data):
    errors = []
    if not data.get("product_name") or not data["product_name"].strip():
        errors.append("Product/Service name is required.")
    if not data.get("product_desc") or not data["product_desc"].strip():
        errors.append("Product/Service description is required.")
    if not data.get("target_audience") or not data["target_audience"].strip():
        errors.append("Target audience is required.")
    if data.get("tone") and data["tone"] not in TONES:
        errors.append(f"Invalid tone. Choose from: {', '.join(TONES.keys())}")
    if data.get("platform") and data["platform"] not in PLATFORMS:
        errors.append(f"Invalid platform. Choose from: {', '.join(PLATFORMS.keys())}")
    return errors
