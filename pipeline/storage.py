"""
Storage layer for wedding photo app.
- Cloudflare R2 (S3-compatible) for image files
- Supabase (PostgreSQL) for metadata
"""

import os
from functools import lru_cache
import boto3
from botocore.config import Config
from supabase import create_client, Client

# --- Supabase Configuration ---
SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "")


@lru_cache(maxsize=1)
def _supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# --- R2 Configuration ---
@lru_cache(maxsize=1)
def _r2():
    return boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT_URL"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


R2_BUCKET = os.getenv("R2_BUCKET_NAME", "wedding-photos")
R2_PUBLIC_BASE = os.getenv("R2_PUBLIC_BASE_URL", "").rstrip("/")

# --- Image Operations ---


def upload_photo(
    file_bytes: bytes, object_key: str, content_type: str = "image/jpeg"
) -> str:
    """Upload to R2, return public URL."""
    _r2().put_object(
        Bucket=R2_BUCKET,
        Key=object_key,
        Body=file_bytes,
        ContentType=content_type,
    )
    if R2_PUBLIC_BASE:
        return f"{R2_PUBLIC_BASE}/{object_key}"
    return f"https://{R2_BUCKET}.r2.cloudflarestorage.com/{object_key}"


# --- Metadata Operations (Supabase) ---


def save_metadata(
    object_key: str,
    public_url: str,
    filename: str,
    file_size: int,
    uploaded_at: str,
) -> None:
    data = {
        "object_key": object_key,
        "public_url": public_url,
        "guest_name": "web_upload",  # Placeholder since guest tracking is removed
        "filename": filename,
        "file_size": file_size,
        "uploaded_at": uploaded_at,
        "moment": None,
        "confidence": None,
    }
    _supabase().table("photos").insert(data).execute()


def get_all_photos() -> list[dict]:
    response = (
        _supabase()
        .table("photos")
        .select("*")
        .order("uploaded_at", desc=True)
        .execute()
    )
    return response.data


def get_unclassified_photos() -> list[dict]:
    response = (
        _supabase()
        .table("photos")
        .select("object_key, public_url")
        .is_("moment", "null")
        .execute()
    )
    return response.data


def get_photos_by_moment(moment: str) -> list[dict]:
    response = (
        _supabase()
        .table("photos")
        .select("*")
        .eq("moment", moment)
        .order("uploaded_at", desc=True)
        .execute()
    )
    return response.data


def update_moment(object_key: str, moment: str, confidence: float) -> None:
    _supabase().table("photos").update({"moment": moment, "confidence": confidence}).eq(
        "object_key", object_key
    ).execute()
