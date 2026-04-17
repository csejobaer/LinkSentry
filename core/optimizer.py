def suggest_fix(url):
    if "http://" in url:
        return url.replace("http://", "https://")
    return None
