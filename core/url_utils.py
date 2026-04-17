from urllib.parse import urlparse


# =========================
# 🔥 SMART URL NORMALIZER
# =========================
def normalize_url(url: str):

    url = url.strip()

    # ❌ empty check
    if not url:
        return None, "URL is empty"

    # ❌ invalid format check
    if " " in url:
        return None, "Wrong URL format (contains spaces)"

    # 🔥 auto add https if missing
    if not url.startswith("http"):
        url = "https://" + url

    try:
        parsed = urlparse(url)

        # ❌ invalid domain
        if not parsed.netloc:
            return None, "Wrong URL (no valid domain)"

        # 🔥 remove duplicate www normalization
        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain.replace("www.", "")

        clean_url = f"{parsed.scheme}://{domain}{parsed.path}"

        return clean_url, None

    except Exception:
        return None, "Invalid URL format"
