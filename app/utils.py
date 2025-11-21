import re

def normalize(text: str) -> str:
    if not text:
        return ""
    return text.strip().lower()

def contains_partial(text: str, query: str) -> bool:
    if not text:
        return False
    return query.lower() in text.lower()

def extract_language(lang_list):
    if not lang_list:
        return None
    return lang_list[0]

def clean_url(url: str) -> str:
    if not url:
        return ""
    return url.replace(" ", "%20")

def safe_int(value):
    try:
        return int(value)
    except:
        return None
