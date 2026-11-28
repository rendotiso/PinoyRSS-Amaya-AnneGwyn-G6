"""Helpers for turning raw feed / page HTML into clean, safe reading text.

Standard library only. The output is a small whitelist of tags with every
attribute dropped (except a safe href on links), so it can be rendered with |safe.
"""
import re
from html import escape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ALLOWED = {'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'blockquote', 'strong', 'b',
           'em', 'i', 'a', 'br'}
HEADINGS = {'h1': 'h2', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h4', 'h6': 'h4'}
SKIP = {'script', 'style', 'noscript', 'iframe', 'svg', 'form', 'nav', 'footer',
        'header', 'aside', 'figure', 'figcaption', 'img', 'picture', 'video',
        'audio', 'button', 'select', 'template'}
VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'source', 'wbr'}
JUNK_HINT = re.compile(r'(share|social|related|comment|promo|advert|\bads?\b|newsletter|'
                       r'subscribe|sidebar|breadcrumb|widget|banner|taboola|outbrain)', re.I)


class _Sanitizer(HTMLParser):
    def __init__(self, base_url=''):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.out = []
        self.skip_depth = 0
        self.stack = []  # (tag, skipped?)

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if tag == 'br' and not self.skip_depth:
                self.out.append('<br>')
            return
        d = dict(attrs)
        junk = tag in SKIP or bool(JUNK_HINT.search((d.get('class') or '') + ' ' + (d.get('id') or '')))
        if junk or self.skip_depth:
            self.skip_depth += 1
            self.stack.append((tag, True))
            return
        self.stack.append((tag, False))
        tag = HEADINGS.get(tag, tag)
        if tag == 'div':
            return
        if tag not in ALLOWED:
            return
        if tag == 'a':
            href = urljoin(self.base_url, d.get('href') or '')
            if urlparse(href).scheme in ('http', 'https'):
                self.out.append('<a href="%s" target="_blank" rel="noopener noreferrer">' % escape(href, quote=True))
            else:
                self.out.append('<a>')
        else:
            self.out.append('<%s>' % tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # pop to matching tag (tolerates sloppy HTML)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                popped = self.stack[i:]
                del self.stack[i:]
                for t, skipped in reversed(popped):
                    if skipped:
                        self.skip_depth -= 1
                    elif HEADINGS.get(t, t) in ALLOWED:
                        self.out.append('</%s>' % HEADINGS.get(t, t))
                return

    def handle_data(self, data):
        if not self.skip_depth:
            self.out.append(escape(data, quote=False))

    def result(self):
        for t, skipped in reversed(self.stack):
            if not skipped and HEADINGS.get(t, t) in ALLOWED:
                self.out.append('</%s>' % HEADINGS.get(t, t))
        return ''.join(self.out)


def sanitize_html(html, base_url=''):
    p = _Sanitizer(base_url)
    p.feed(html or '')
    p.close()
    return _tidy(p.result())


def _tidy(html):
    # Bare text blocks (from <div>s) become paragraphs; drop empties.
    html = re.sub(r'<(p|li|blockquote|h2|h3|h4)>\s*</\1>', '', html)
    if '<p>' not in html and html.strip():
        parts = [s.strip() for s in re.split(r'\n\s*\n|<br>\s*<br>', html) if s.strip()]
        html = ''.join('<p>%s</p>' % s for s in parts)
    return html.strip()


def strip_tags(html):
    """Plain text (for summaries / search)."""
    class T(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.t = []
        def handle_data(self, d):
            self.t.append(d)
    t = T()
    t.feed(html or '')
    t.close()
    return re.sub(r'\s+', ' ', ''.join(t.t)).strip()


# ---- main-content extraction from a full page ---------------------------------

def extract_article_html(page_html, base_url=''):
    """Best-effort 'reader mode'. Returns sanitised HTML or '' if nothing usable."""
    page_html = re.sub(r'(?is)<!--.*?-->', '', page_html or '')
    # 1) prefer the first <article> or a well-known body container
    m = re.search(r'(?is)<article\b[^>]*>(.*)</article>', page_html)
    chunk = m.group(1) if m else None
    if not chunk:
        m = re.search(r'(?is)<(div|section|main)\b[^>]*(?:class|id)="[^"]*(?:article-body|article-content|'
                      r'entry-content|post-content|story-body|article__body|td-post-content|content-body)'
                      r'[^"]*"[^>]*>(.*)', page_html)
        chunk = m.group(2) if m else page_html
    clean = sanitize_html(chunk, base_url)
    # keep only if it looks like prose
    if len(strip_tags(clean)) < 400 and chunk is not page_html:
        clean = sanitize_html(page_html, base_url)
    return clean if len(strip_tags(clean)) >= 300 else ''


def fetch_article_html(url, timeout=10):
    if urlparse(url).scheme not in ('http', 'https'):
        return ''
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; PinoyRSS/1.0; reader)',
                                'Accept': 'text/html,application/xhtml+xml'})
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read(3_000_000)
        charset = resp.headers.get_content_charset() or 'utf-8'
    html = raw.decode(charset, errors='replace')
    return extract_article_html(html, url)
