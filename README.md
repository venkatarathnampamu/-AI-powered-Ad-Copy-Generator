# AI Ad Copy Generator

An AI-powered advertisement copy generator that creates engaging, platform-specific ad content using Generative AI.

## Features

- Input product/service details, target audience, and preferences
- Select ad tone (Professional, Casual, Urgent, Humorous, Luxury)
- Select platform (Facebook, Instagram, Google Search, X/Twitter, LinkedIn)
- AI-generated ad headlines, descriptions, CTAs, and hashtags
- Regenerate and save favorite ad copies
- Fallback ad generation when API key is not configured

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **AI:** OpenAI API (GPT-3.5/GPT-4)
- **Deployment:** Ready for cloud deployment

## Project Structure

```
project/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/script.js
├── backend/
│   ├── app.py
│   ├── routes.py
│   └── utils.py
├── .env
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
   > The app works without an API key using built-in fallback templates.

3. **Run the backend:**
   ```bash
   python backend/app.py
   ```

4. **Open the frontend:**
   Open `frontend/index.html` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/api/tones` | List available tones |
| GET | `/api/platforms` | List available platforms |
| POST | `/api/generate` | Generate ad copy |

### POST `/api/generate` - Request Body

```json
{
  "product_name": "FreshBite Meal Delivery",
  "product_desc": "Healthy meals delivered to your door",
  "target_audience": "Health-conscious professionals",
  "tone": "professional",
  "platform": "facebook"
}
```

## Branches

- `main` - Final working code
- `dev` - Development work
