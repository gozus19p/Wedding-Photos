"""
CLIP-based image classifier for wedding moments.

Uses OpenAI CLIP (via open-clip-torch) to classify each photo into one of the
predefined wedding moment categories using zero-shot inference — no training needed.
"""

import io
import os
from pathlib import Path
from PIL import Image
import torch
import open_clip

from pipeline.storage import get_unclassified_photos, update_moment

MOMENT_LABELS = ["cerimonia", "cena", "ricevimento", "balli", "altro"]

MOMENT_PROMPTS = {
    "cerimonia": [
        "a wedding ceremony in a church or outdoor venue",
        "bride and groom exchanging vows at the altar",
        "wedding ceremony with guests seated in rows",
    ],
    "cena": [
        "a wedding dinner with guests seated at tables",
        "people eating at a decorated wedding reception table",
        "wedding banquet with food and candles on the table",
    ],
    "ricevimento": [
        "wedding cocktail reception with guests drinking and socializing",
        "people mingling and celebrating at a wedding party",
        "wedding aperitivo with champagne and appetizers",
    ],
    "balli": [
        "people dancing at a wedding party",
        "first dance of the bride and groom",
        "wedding dance floor with guests dancing",
    ],
    "altro": [
        "a candid wedding photo",
        "wedding guests taking photos together",
        "behind the scenes wedding moment",
    ],
}

_model = None
_preprocess = None
_tokenizer = None
_text_features = None

def _load_model():
    global _model, _preprocess, _tokenizer, _text_features

    if _model is not None:
        return

    model_name = os.getenv("CLIP_MODEL", "ViT-B-32")
    pretrained = os.getenv("CLIP_PRETRAINED", "openai")

    _model, _, _preprocess = open_clip.create_model_and_transforms(
        model_name,
        pretrained=pretrained
    )
    _tokenizer = open_clip.get_tokenizer(model_name)
    _model.eval()

    all_prompts = []
    prompt_to_moment = []
    for moment, prompts in MOMENT_PROMPTS.items():
        for p in prompts:
            all_prompts.append(p)
            prompt_to_moment.append(moment)

    with torch.no_grad():
        tokens = _tokenizer(all_prompts)
        text_feats = _model.encode_text(tokens)
        text_feats = text_feats / text_feats.norm(dim=-1, keepdim=True)

    _text_features = (text_feats, prompt_to_moment)


def classify_image_bytes(image_bytes: bytes) -> tuple[str, float]:
    """
    Classify a single image given its raw bytes.
    Returns (moment_label, confidence_score).
    """
    _load_model()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_tensor = _preprocess(image).unsqueeze(0)

    with torch.no_grad():
        image_feats = _model.encode_image(image_tensor)
        image_feats = image_feats / image_feats.norm(dim=-1, keepdim=True)

    text_feats, prompt_to_moment = _text_features
    similarities = (image_feats @ text_feats.T).squeeze(0)

    moment_scores = {m: 0.0 for m in MOMENT_LABELS}
    moment_counts = {m: 0 for m in MOMENT_LABELS}

    for score, moment in zip(similarities.tolist(), prompt_to_moment):
        moment_scores[moment] += score
        moment_counts[moment] += 1

    for m in moment_scores:
        if moment_counts[m] > 0:
            moment_scores[m] /= moment_counts[m]

    best_moment = max(moment_scores, key=lambda m: moment_scores[m])
    confidence = float(moment_scores[best_moment])

    return best_moment, confidence


def classify_image_from_local(path: str) -> tuple[str, float]:
    """Read image from local filesystem and classify it."""
    return classify_image_bytes(Path(path).read_bytes())


def classify_all_photos() -> dict:
    """
    Classify all unclassified photos in the database.
    Reads each from the local filesystem, runs CLIP, updates the DB.
    Returns a summary dict with 'classified' and 'errors' counts.
    """
    photos = get_unclassified_photos()
    classified = 0
    errors = 0

    for photo in photos:
        try:
            path = photo.get("public_url")
            if not path or not Path(path).exists():
                errors += 1
                continue

            moment, confidence = classify_image_from_local(path)
            update_moment(
                object_key=photo["object_key"],
                moment=moment,
                confidence=round(confidence, 4)
            )
            classified += 1

        except Exception as e:
            print(f"Error classifying {photo.get('object_key')}: {e}")
            errors += 1

    return {"classified": classified, "errors": errors}
