from flask import Blueprint, request, jsonify
from utils import build_prompt, validate_input, API_KEY, API_URL, MODEL
import requests
import json

api_bp = Blueprint("api", __name__)


def call_ai_api(prompt):
    if not API_KEY:
        return generate_fallback_ad(prompt)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional advertising copywriter generating engaging ad content.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return parse_ad_content(content)
    except requests.exceptions.RequestException as e:
        return {
            "error": f"API request failed: {str(e)}",
            "fallback": generate_fallback_ad(prompt),
        }


def generate_fallback_ad(prompt):
    lines = prompt.split("\n")
    product_name = "your product"
    for line in lines:
        if line.startswith("Product/Service Name:"):
            product_name = line.split(":", 1)[1].strip()
            break

    return {
        "headline": f"Discover the Best {product_name} Today!",
        "description": f"Experience {product_name} like never before. Quality you can trust, value you deserve. Don't miss out on this incredible opportunity.",
        "cta": "Shop Now and Save!",
        "hashtags": [f"#{product_name.replace(' ', '')}", "#Quality", "#BestDeals", "#ShopNow", "#MustHave"],
    }


def parse_ad_content(content):
    result = {}
    lines = content.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.lower().startswith("headline:"):
            result["headline"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("description:"):
            result["description"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("call to action:"):
            result["cta"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("hashtags:"):
            tags = line.split(":", 1)[1].strip()
            result["hashtags"] = [t.strip() for t in tags.split(",") if t.strip()]

    if not result.get("headline"):
        result["headline"] = lines[0] if lines else "Great Product, Great Deal!"
    if not result.get("description"):
        result["description"] = "Check out this amazing offer today!"
    if not result.get("cta"):
        result["cta"] = "Get Yours Now!"
    if not result.get("hashtags"):
        result["hashtags"] = ["#Ad", "#Offer", "#Deal"]

    return result


@api_bp.route("/generate", methods=["POST"])
def generate_ad():
    data = request.get_json()
    errors = validate_input(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    prompt = build_prompt(
        data["product_name"],
        data["product_desc"],
        data["target_audience"],
        data.get("tone", "professional"),
        data.get("platform", "facebook"),
        data.get("authenticity", "medium"),
    )

    ad_content = call_ai_api(prompt)

    if isinstance(ad_content, dict) and "error" in ad_content:
        return jsonify({"success": True, "ad": ad_content["fallback"], "warning": ad_content["error"]})

    return jsonify({"success": True, "ad": ad_content})


@api_bp.route("/tones", methods=["GET"])
def get_tones():
    from utils import TONES
    return jsonify({"success": True, "tones": list(TONES.keys())})


@api_bp.route("/platforms", methods=["GET"])
def get_platforms():
    from utils import PLATFORMS
    return jsonify({"success": True, "platforms": list(PLATFORMS.keys())})


@api_bp.route("/authenticity", methods=["GET"])
def get_authenticity():
    from utils import AUTHENTICITY
    return jsonify({"success": True, "authenticity": list(AUTHENTICITY.keys())})
