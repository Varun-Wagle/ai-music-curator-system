import json
import re
from groq import Groq
from backend.app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def rate_song(features: dict):

    prompt = f"""
    Evaluate the following music features and rate the song.

    Tempo: {features['tempo']}
    RMS Energy: {features['rms_energy']}
    Spectral Centroid: {features['spectral_centroid']}
    Spectral Bandwidth: {features['spectral_bandwidth']}
    Chroma Mean: {features['chroma_mean']}

    Return ONLY valid JSON in this format:

    {{
      "quality_score": number,
      "energy_score": number,
      "virality_score": number,
      "recommended_playlist": "playlist name"
    }}
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw_output = completion.choices[0].message.content or ""

    # Extract JSON block from response
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)

    if match:
        json_str = match.group(0)
        return json.loads(json_str)
    else:
        return {"error": "AI response parsing failed", "raw_output": raw_output}