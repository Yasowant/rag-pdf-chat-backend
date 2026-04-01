# app/ats.py
import re
from collections import Counter

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def calculate_ats_score(resume_text, job_description):
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(job_description)

    match_count = 0
    total_keywords = len(jd_words)

    missing_keywords = []

    for word in jd_words:
        if word in resume_words:
            match_count += 1
        else:
            missing_keywords.append(word)

    score = (match_count / total_keywords) * 100 if total_keywords else 0

    return {
        "ats_score": round(score, 2),
        "matched_keywords": match_count,
        "total_keywords": total_keywords,
        "missing_keywords": missing_keywords[:20]
    }