def analyze_ticket(user_input):
    if "password" in user_input.lower():
        return {
            "category": "Access",
            "summary": "User needs password reset",
            "severity": "Low",
            "resolution": "Auto-resolve",
            "sentiment": "Neutral",
            "department": "IT",
            "confidence": 95,
            "estimated_time": "5 minutes"
        }
    
    return {
        "category": "Bug",
        "summary": "User cannot login",
        "severity": "High",
        "resolution": "Assign",
        "sentiment": "Frustrated",
        "department": "IT",
        "confidence": 90,
        "estimated_time": "2 hours"
    }