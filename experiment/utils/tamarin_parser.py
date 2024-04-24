import re
from bs4 import BeautifulSoup


def parse_theory_link(html: str, file: str):
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if tds[2].text == 'Original' and \
                tds[3].text.split('/')[-1] == file:
            return tds[0].find('a', href=True)['href']
    return None


def parse_trace_links(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    trace_spans = soup.find_all('span', text='// trace found')
    trace_links = [s.parent['href'] for s in trace_spans]
    return trace_links


def parse_img_link(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img')
    if img is None:
        return None
    else:
        return img['src'].strip()


def parse_lemma_results(text: str):
    lemmas = []
    pattern = r'(.+?) \((.+?)\): (.+?) \((.+?) steps\)'
    matches = re.findall(pattern, text)
    for m in matches:
        lemmas.append({
            "name": m[0].strip(),
            "type": m[1].strip(),
            "result": m[2].strip(),
            "steps": m[3].strip()
        })
    return lemmas


def parse_hardware_info(text: str):
    return {
        "CPU Model": re.findall(r'CPU Model: (.+)', text)[0].strip(),
        "CPU Phycial Cores": re.findall(r'CPU Phycial Cores: (.+)', text)[0].strip(),
        "CPU Logical Cores": re.findall(r'CPU Logical Cores: (.+)', text)[0].strip(),
        "CPU Frequency": re.findall(r'CPU Frequency: (.+)', text)[0].strip(),
        "Total Memory": re.findall(r'Total Memory: (.+)', text)[0].strip()
    }

def parse_time_info(text: str):
    return re.findall(r'processing time: (.+)', text)[0].strip()