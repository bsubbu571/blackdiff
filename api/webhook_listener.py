import os
import hmac
import hashlib
import logging
from fastapi import APIRouter, Request, Header, HTTPException
from core.scanners.scanner_runner import run_scanners_on_repo

router = APIRouter()

# Load webhook secret securely
GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "changeme")  # Set this in your env

def verify_signature(signature_header: str, body: bytes) -> bool:
    if not signature_header:
        logging.warning("Missing signature header.")
        return False
    try:
        sha_name, signature = signature_header.split('=')
        if sha_name != 'sha256':
            logging.warning("Unsupported hash type: %s", sha_name)
            return False
        mac = hmac.new(GITHUB_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
        return hmac.compare_digest(mac.hexdigest(), signature)
    except Exception as e:
        logging.error(f"Signature verification failed: {e}")
        return False

@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    body = await request.body()

    if not verify_signature(x_hub_signature_256, body):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()

    # Handle ping (test delivery)
    if x_github_event == "ping":
        return {"status": "Ping received", "zen": payload.get("zen", "🤙")}

    repo_url = payload.get("repository", {}).get("clone_url")
    if repo_url:
        logging.info(f"[Webhook Triggered] Scanning repo: {repo_url}")
        run_scanners_on_repo(repo_url)
        return {"status": "Scan started", "repo": repo_url}

    raise HTTPException(status_code=400, detail="Repository URL missing in payload")

