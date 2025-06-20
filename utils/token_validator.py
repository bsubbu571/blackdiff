import requests
import re

# ----------------------------
# AWS STS API Key Validation
# ----------------------------
def is_valid_aws_key(access_key, secret_key):
    try:
        import boto3
        from botocore.exceptions import ClientError
        client = boto3.client(
            'sts',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        identity = client.get_caller_identity()
        return identity.get("Arn", "Unknown")
    except Exception:
        return False

# ----------------------------
# Firebase DB Live Check
# ----------------------------
def is_valid_firebase_url(firebase_url):
    try:
        if not firebase_url.startswith("http"):
            firebase_url = "https://" + firebase_url
        if not firebase_url.endswith(".json"):
            firebase_url += "/.json"
        response = requests.get(firebase_url, timeout=5)
        return response.status_code == 200
    except:
        return False

# ----------------------------
# Slack Token Validation
# ----------------------------
def is_valid_slack_token(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://slack.com/api/auth.test", headers=headers, timeout=5)
        return response.status_code == 200 and response.json().get("ok", False)
    except:
        return False

# ----------------------------
# GitHub PAT Token Validation
# ----------------------------
def is_valid_github_pat(token):
    try:
        headers = {"Authorization": f"token {token}"}
        res = requests.get("https://api.github.com/user", headers=headers, timeout=5)
        return res.status_code == 200
    except:
        return False

# ----------------------------
# Discord Bot/User Token Check
# ----------------------------
def is_valid_discord_token(token):
    try:
        headers = {"Authorization": token}
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        return res.status_code == 200
    except:
        return False

# ----------------------------
# Pattern Checkers (light filters)
# ----------------------------
def is_aws_access_key(token):
    return token.startswith("AKIA") or token.startswith("ASIA")

def is_github_token(token):
    return bool(re.match(r"gh[pousr]_[A-Za-z0-9_]{30,}", token))

