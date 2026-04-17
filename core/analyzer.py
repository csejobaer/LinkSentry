def analyze(results):
    broken = [r for r in results if r['status'] != 200]
    return {
        "total": len(results),
        "broken": len(broken)
    }
