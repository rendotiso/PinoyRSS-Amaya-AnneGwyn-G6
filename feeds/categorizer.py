"""Keyword-based category assignment for incoming articles."""
import re

DEFAULT_CATEGORIES = {
    'Politics':      'Government, elections, Congress and public policy',
    'Business':      'Economy, markets, jobs and money',
    'Sports':        'Local and international sports',
    'Entertainment': 'Showbiz, film, music and pop culture',
    'Technology':    'Gadgets, internet, science and innovation',
    'Health':        'Medicine, wellness and public health',
    'Weather':       'Typhoons, weather and disasters',
    'Crime':         'Crime, courts and justice',
    'World':         'News from outside the Philippines',
    'Lifestyle':     'Food, travel, culture and living',
    'General':       'Everything else',
}

KEYWORDS = {
    'Politics': ['senate', 'senator', 'congress', 'house of representatives', 'president', 'marcos', 'duterte',
                 'comelec', 'election', 'malacañang', 'malacanang', 'lawmaker', 'bill', 'ombudsman', 'impeach',
                 'mayor', 'governor', 'barangay', 'palace', 'dilg', 'politic'],
    'Business': ['peso', 'economy', 'stock', 'psei', 'inflation', 'bsp', 'bangko sentral', 'investment', 'bank',
                 'business', 'gdp', 'tax', 'jobs', 'price', 'trade', 'company', 'earnings', 'fuel'],
    'Sports':   ['nba', 'pba', 'gilas', 'uaap', 'ncaa', 'volleyball', 'basketball', 'boxing', 'pacquiao',
                 'olympic', 'sea games', 'football', 'tennis', 'championship', 'tournament', 'coach', 'league'],
    'Entertainment': ['showbiz', 'celebrity', 'actor', 'actress', 'movie', 'film', 'concert', 'kapamilya',
                      'kapuso', 'pbb', 'album', 'singer', 'netflix', 'k-pop', 'mmff', 'teleserye'],
    'Technology': ['technology', 'tech', 'ai ', 'artificial intelligence', 'smartphone', 'app ', 'internet',
                   'cyber', 'software', 'startup', 'google', 'meta ', 'openai', 'dost', 'satellite'],
    'Health':   ['health', 'doh', 'hospital', 'disease', 'vaccine', 'dengue', 'covid', 'doctor', 'medical',
                 'philhealth', 'cancer', 'mental health'],
    'Weather':  ['typhoon', 'pagasa', 'storm', 'flood', 'earthquake', 'phivolcs', 'landslide', 'rain', 'weather',
                 'volcano', 'signal no'],
    'Crime':    ['police', 'pnp', 'nbi', 'arrest', 'murder', 'suspect', 'court', 'sandiganbayan', 'drugs',
                 'killed', 'shooting', 'convicted', 'scam'],
    'World':    ['china', 'u.s.', 'united states', 'ukraine', 'russia', 'gaza', 'israel', 'asean', 'un ',
                 'united nations', 'japan', 'korea', 'europe', 'taiwan', 'trump', 'global'],
    'Lifestyle': ['food', 'recipe', 'travel', 'fashion', 'restaurant', 'wellness', 'culture', 'festival',
                  'tourism', 'lifestyle', 'home', 'pets'],
}

TAG_ALIASES = {
    'nation': 'Politics', 'politics': 'Politics', 'government': 'Politics', 'news': None,
    'business': 'Business', 'money': 'Business', 'economy': 'Business',
    'sports': 'Sports', 'sport': 'Sports',
    'entertainment': 'Entertainment', 'showbiz': 'Entertainment',
    'technology': 'Technology', 'tech': 'Technology', 'sci-tech': 'Technology',
    'health': 'Health', 'weather': 'Weather', 'crime': 'Crime',
    'world': 'World', 'global nation': 'World', 'lifestyle': 'Lifestyle', 'life': 'Lifestyle',
}


def guess_category(title, summary='', tags=()):
    """Return a category name from feed tags first, then keyword scoring, else 'General'."""
    for t in tags:
        mapped = TAG_ALIASES.get((t or '').strip().lower())
        if mapped:
            return mapped
    text = ' %s %s ' % (title or '', summary or '')
    text = text.lower()
    scores = {}
    for cat, words in KEYWORDS.items():
        n = 0
        for w in words:
            if re.search(r'(?<![a-z])' + re.escape(w.strip()) + (r'' if w.endswith(' ') else r'(?![a-z])'), text):
                n += 2 if w.strip() in (title or '').lower() else 1
        if n:
            scores[cat] = n
    return max(scores, key=scores.get) if scores else 'General'
