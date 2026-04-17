"""
Storage layer for wedding photo app.
- Cloudflare R2 (S3-compatible) for image files
"""

import os
from functools import lru_cache
import boto3
from botocore.config import Config


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


def _public_url(object_key: str) -> str:
    if R2_PUBLIC_BASE:
        return f"{R2_PUBLIC_BASE}/{object_key}"
    return f"https://{R2_BUCKET}.r2.cloudflarestorage.com/{object_key}"


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
    return _public_url(object_key)


def get_all_photos() -> list[dict]:
    """List all objects under photos/ prefix, newest first."""
    paginator = _r2().get_paginator("list_objects_v2")
    photos = []
    for page in paginator.paginate(Bucket=R2_BUCKET, Prefix="photos/"):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            photos.append(
                {
                    "object_key": key,
                    "public_url": _public_url(key),
                    "uploaded_at": obj["LastModified"].isoformat(),
                    "filename": key.split("/")[-1],
                }
            )
    photos.sort(key=lambda x: x["uploaded_at"], reverse=True)
    return photos


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
