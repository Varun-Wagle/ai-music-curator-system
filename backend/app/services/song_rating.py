import json
import re
from groq import Groq
from backend.app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def rate_song(features: dict):

    prompt = f"""
    You are an AI music evaluation engine.

    Analyze the provided audio features and produce a rating.

    Rules:
    - Respond ONLY with valid JSON.
    - Do NOT include explanations.
    - Do NOT include markdown.
    - Do NOT include code.
    - Do NOT include text outside the JSON object.

    JSON format:

    {{
        "quality_score": number,
        "energy_score": number,
        "virality_score": number,
        "recommended_playlist": "playlist name"
    }}

    Audio Features:
    tempo: {features['tempo']}
    rms_energy: {features['rms_energy']}
    spectral_centroid: {features['spectral_centroid']}
    spectral_bandwidth: {features['spectral_bandwidth']}
    chroma_mean: {features['chroma_mean']}
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an AI music evaluation engine. Analyze audio features and produce a rating in strict JSON format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    raw_output = completion.choices[0].message.content or ""

    # Extract JSON block from response
    match = re.search(r"\{[\s\S]*\}", raw_output)

    if not match:
        return {
            "error": "AI response parsing failed",
            "raw_output": raw_output
        }
    
    json_str = match.group(0)

    # Remove code block markers if present
    json_str = json_str.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(json_str)

    except json.JSONDecodeError:
        # Attempt basic cleanup
        json_str = json_str.replace("'", '"')

        try:
            return json.loads(json_str)
        except Exception:
            return {
                "error": "Invalid AI JSON format",
                "raw_output": raw_output
            }