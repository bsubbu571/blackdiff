def rank_severity(token: str, file_path: str) -> str:
    token = token.lower()

    # High severity patterns
    if "aws_access_key_id" in token or "aws" in token or "AKIA" in token:
        return "High"
    if "-----begin rsa private key-----" in token:
        return "High"
    if "slack" in token or token.startswith("xoxb-"):
        return "High"
    if token.startswith("ghp_") or token.startswith("ghs_"):
        return "High"

    # Medium severity
    if "apikey" in token or "api_key" in token or "token" in token:
        return "Medium"
    if "auth" in file_path.lower() or "login" in file_path.lower():
        return "Medium"

    # Low severity (maybe FP or not directly exploitable)
    if token.endswith(".json") or token.endswith(".env"):
        return "Low"

    return "Unknown"

