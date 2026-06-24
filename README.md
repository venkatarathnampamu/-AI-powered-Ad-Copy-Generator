# AI Ad Copy Generator

An AI-powered advertisement copy generator that creates engaging, platform-specific ad content using Generative AI.

## Features

- Input product/service details, target audience, and preferences
- Select ad tone (Professional, Casual, Urgent, Humorous, Luxury)
- Select platform (Facebook, Instagram, Google Search, X/Twitter, LinkedIn)
- Set authenticity level (Low — promotional, Medium — balanced, High — transparent)
- AI-generated ad headlines, descriptions, CTAs, and hashtags
- Regenerate and save favorite ad copies (persisted in localStorage)
- Fallback ad generation when no API key is configured
- Responsive, mobile-friendly UI

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Backend:** Python (Flask with CORS)
- **AI:** OpenAI API (GPT-3.5/GPT-4) — pluggable, any LLM API supported
- **Deployment:** Ready for cloud deployment (Render, Railway, Vercel, etc.)

## Project Structure

```
project/
├── frontend/
│   ├── index.html          # Main UI
│   ├── css/style.css       # Gradient-themed responsive styles
│   └── js/script.js        # Form handling, API calls, saved ads
├── backend/
│   ├── app.py              # Flask entry point, CORS config
│   ├── routes.py           # API routes, AI call, fallback generation
│   └── utils.py            # Prompt builder, input validation, config
├── .env                    # API key & model config (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Running

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API key in `.env`:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   > The app works without an API key — built-in fallback templates generate sample ad copy.

3. **Run the backend:**
   ```bash
   python backend/app.py
   ```
   Server starts at `http://localhost:5000`.

4. **Open the frontend:**
   Open `frontend/index.html` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/api/tones` | List available tones |
| GET | `/api/platforms` | List available platforms |
| GET | `/api/authenticity` | List authenticity levels |
| POST | `/api/generate` | Generate ad copy |

### POST `/api/generate` — Request Body

```json
{
  "product_name": "EcoBottle",
  "product_desc": "Reusable stainless steel water bottle, keeps drinks cold 24hrs",
  "target_audience": "Environmentally conscious consumers aged 20-40",
  "tone": "casual",
  "platform": "instagram",
  "authenticity": "high"
}
```

### POST `/api/generate` — Response

```json
{
  "success": true,
  "ad": {
    "headline": "Sip Sustainably with EcoBottle",
    "description": "Ditch single-use plastic. Our stainless steel bottle keeps your water ice-cold for 24 hours — and the planet happy.",
    "cta": "Get Your EcoBottle Now",
    "hashtags": ["#EcoBottle", "#SustainableLiving", "#PlasticFree", "#Hydration", "#EcoFriendly"]
  }
}
```

## Branches

- `main` — Final working code
- `dev` — Development work

## Optional Configuration (`.env`)

```
OPENAI_API_KEY=sk-...          # Your OpenAI API key
API_URL=https://api.openai.com/v1/chat/completions  # API endpoint (change for other LLMs)
MODEL=gpt-3.5-turbo            # Model name
```
