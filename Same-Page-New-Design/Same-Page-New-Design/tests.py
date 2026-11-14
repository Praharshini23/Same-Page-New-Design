from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).parent
class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('style','script','head'): self.hidden += 1
    def handle_endtag(self, tag):
        if tag in ('style','script','head') and self.hidden: self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden and data.strip(): self.parts.append(data.strip())

def visible(path):
    p=VisibleText(); p.feed(path.read_text(encoding='utf-8'))
    return re.sub(r'\s+',' ',' '.join(p.parts)).strip()

before=visible(ROOT/'before.html')
after=visible(ROOT/'after.html')
assert before == after, f'Visible copy mismatch:\nBEFORE={before}\nAFTER={after}'
assert 'viewport' in (ROOT/'before.html').read_text()
css=(ROOT/'after.html').read_text()
assert '@media (max-width:700px)' in css
assert 'prefers-reduced-motion' in css
assert 'TECHNOVA 2026' in after and 'Chai and Co.' in after and 'Bright Path Classes' in after
print('PASS: visible copy matches exactly')
print('PASS: mobile responsive breakpoint exists')
print('PASS: reduced-motion support exists')
print('PASS: all three content sections exist')
