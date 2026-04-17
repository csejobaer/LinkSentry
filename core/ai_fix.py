def suggest_fix(url):

    suggestions = []

    if "http://" in url:
        suggestions.append(url.replace("http://", "https://"))

    if "//" in url and not url.startswith("http"):
        suggestions.append("https:" + url)

    if " " in url:
        suggestions.append(url.replace(" ", "%20"))

    # fallback
    if not suggestions:
        suggestions.append("Check domain or endpoint manually")

    return suggestions
