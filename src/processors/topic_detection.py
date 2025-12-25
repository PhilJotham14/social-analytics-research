import re
from collections import Counter
from typing import Iterable, Dict, Any, Tuple

STOPWORDS = set("""
a an the and or of for to in is are was were be been being on with as by from that this it its at into about over after before during while not but if then than so such very can will just more most other some any each every
""".split())


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords_from_titles(titles: Iterable[str], top_k: int = 50) -> Tuple[str, Counter]:
    counts = Counter()
    for t in titles:
        t_norm = normalize(t)
        tokens = [tok for tok in t_norm.split() if tok not in STOPWORDS and len(tok) > 2]
        # Build unigrams; simple approach for Step 2 skeleton
        for tok in tokens:
            counts[tok] += 1
    top = counts.most_common(top_k)
    top_topic = top[0][0] if top else ""
    return top_topic, counts
