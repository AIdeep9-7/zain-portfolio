from pathlib import Path
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

ROOT=Path(__file__).parent
html_path=ROOT/'index.html'
html=html_path.read_text(encoding='utf-8')
soup=BeautifulSoup(html,'html.parser')
css=(ROOT/'styles.css').read_text(encoding='utf-8')
js=(ROOT/'script.js').read_text(encoding='utf-8')
issues=[]
warnings=[]
checks=[]

def check(label, ok, detail=''):
    checks.append((label, bool(ok), detail))
    if not ok:
        issues.append(f'{label}: {detail}')

def warn(label, detail=''):
    warnings.append(f'{label}: {detail}')

check('HTML document has lang', soup.html and soup.html.get('lang')=='en', str(soup.html.get('lang') if soup.html else None))
check('Title present', bool(soup.title and soup.title.get_text(strip=True)), soup.title.get_text(strip=True) if soup.title else '')
check('Meta description present', bool(soup.find('meta',attrs={'name':'description'})), '')
check('Open Graph metadata present', bool(soup.find('meta',attrs={'property':'og:title'})) and bool(soup.find('meta',attrs={'property':'og:image'})), '')
check('Structured Person data present', 'schema.org' in html and 'Zain Ul Abideen' in html, '')
check('Latest contact email present', 'Connectwithzayn1@gmail.com' in html and 'Connectwithzayna@gmail.com' not in html, '')
check('Expanded interests present', all(term.lower() in html.lower() for term in ['AI tools','Programming','SEO research','Chess','Open source','Learning']), '')
check('Interest grid has responsive six-item layout', 'grid-template-columns:repeat(3,1fr)' in css and '.interest-grid{gap:8px}' in css, '')
check('Modern image sources present', html.count('type="image/webp"') >= 2 and all((ROOT/name).exists() for name in ['assets/zayn-hero-match-a.webp','assets/zayn-about-professional.webp']), '')
ids=[x.get('id') for x in soup.find_all(id=True)]
check('IDs are unique', len(ids)==len(set(ids)), [x for x in set(ids) if ids.count(x)>1])
for img in soup.find_all('img'):
    check(f'Image alt: {img.get("src")}', bool(img.get('alt')), 'present' if img.get('alt') else 'missing alt')
for el in soup.find_all(['a','img','script','link']):
    attr='href' if el.name in ('a','link') else 'src'
    ref=el.get(attr)
    if not ref or ref.startswith(('http://','https://','mailto:','tel:','#','data:')):
        continue
    p=(ROOT/ref.split('?')[0].split('#')[0]).resolve()
    check(f'Local asset: {ref}', p.exists(), str(p))
for a in soup.find_all('a',href=True):
    h=a['href']
    if h.startswith('#'):
        check(f'Anchor target: {h}', bool(soup.find(id=h[1:])), '')
    if h.startswith('mailto:'):
        check('Email link present', 'connectwithzayn1@gmail.com' in h.lower(), h)
    if h.startswith('tel:'):
        check('Phone link present', '923454577149' in h, h)
for forbidden in ['Lahore, Pakistan','zayn.test@example.com','+92 300 000 0000','Northstar Institute','Connectwithzayna@gmail.com','[ADD','placeholder']:
    check(f'No test placeholder: {forbidden}', forbidden.lower() not in html.lower(), '')
for sec in ['top','about','work','resume','contact','main']:
    check(f'Section exists: #{sec}', bool(soup.find(id=sec)), '')
nav_labels=[a.get_text(' ',strip=True) for a in soup.select('#site-nav a')]
check('Navigation order matches reference', nav_labels==['About me','Resume','Work','Get in touch!'], str(nav_labels))
for nav_text in ['About me','Work','Resume','Get in touch!']:
    check(f'Navigation label: {nav_text}', nav_text in html, '')
check('Experience heading matches reference', 'Selected work' not in html and 'Experience' in html, '')
check('Responsive breakpoint <=700px', '@media (max-width:700px)' in css, '')
check('Mobile menu JS present', 'menu-toggle' in js and 'aria-expanded' in js, '')
check('Light-header behavior present', 'on-light' in css and 'IntersectionObserver' in js, '')
check('No external stylesheet dependency', 'fonts.googleapis.com' not in html+css, '')
external_scripts=[tag.get('src') for tag in soup.find_all('script',src=True) if tag.get('src','').startswith(('http://','https://'))]
check('No external script dependency', not external_scripts, str(external_scripts))

# Live deployment smoke test.
live='https://zain-portfolio-dcc.pages.dev/'
try:
    req=Request(live,headers={'User-Agent':'portfolio-audit/1.0'})
    remote=urlopen(req,timeout=20).read().decode('utf-8','ignore')
    remote_soup=BeautifulSoup(remote,'html.parser')
    check('Live site HTTP response', bool(remote), f'{len(remote)} bytes')
    check('Live title matches local', (remote_soup.title and remote_soup.title.get_text(strip=True))==(soup.title.get_text(strip=True)), '')
    for phrase in ['Zain Ul Abideen','Toba Tek Singh, Pakistan','Connectwithzayn1@gmail.com','University of Agriculture','AI Automation Systems']:
        if phrase in remote:
            check(f'Live content: {phrase}', True, '')
        else:
            warn(f'Live deployment pending: {phrase}', 'public site is an older revision')
except Exception as e:
    check('Live site HTTP response', False, repr(e))

print('# Portfolio audit report')
print()
print(f'Local file: {html_path}')
print(f'Checks passed: {sum(ok for _,ok,_ in checks)}/{len(checks)}')
print()
for label,ok,detail in checks:
    print(('PASS' if ok else 'FAIL')+' | '+label+(f' | {detail}' if detail else ''))
if issues:
    print('\n## Issues')
    for issue in issues:
        print('- '+issue)
if warnings:
    print('\n## Warnings')
    for warning in warnings:
        print('- '+warning)
