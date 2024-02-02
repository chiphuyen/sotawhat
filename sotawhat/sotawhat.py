import os
import re
import sys
import PyPDF2
import urllib.error
import urllib.request
import warnings
import requests
from io import BytesIO
import openai
from getpass import getpass


import nltk
from nltk.tokenize import word_tokenize
from six.moves.html_parser import HTMLParser
from spellchecker import SpellChecker

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

h = HTMLParser()

AUTHOR_TAG = '<a href="/search/?searchtype=author'
TITLE_TAG = '<p class="title is-5 mathjax">'
ABSTRACT_TAG = '<span class="abstract-full has-text-grey-dark mathjax"'
DATE_TAG = '<p class="is-size-7"><span class="has-text-black-bis has-text-weight-semibold">Submitted</span>'


def get_authors(lines, i):
    authors = []
    while True:
        if not lines[i].startswith(AUTHOR_TAG):
            break
        idx = lines[i].find('>')
        if lines[i].endswith(','):
            authors.append(lines[i][idx + 1: -5])
        else:
            authors.append(lines[i][idx + 1: -4])
        i += 1
    return authors, i

# Source: https://github.com/chiphuyen/sotawhat/pull/33/files
def extract_first_arxiv_url(html_string):
    pattern = r'https://[^"]+arxiv\.org/[^"]+' # Regular expression to match URLs from the arxiv.org domain
    match = re.search(pattern, html_string)
    return match.group(0) if match else None

def get_next_result(lines, start):
    """
    Extract paper from the xml file obtained from arxiv search.

    Each paper is a dict that contains:
    + 'title': str
    + 'pdf_link': str
    + 'main_page': str
    + 'authors': []
    + 'abstract': str
    """

    result = {}
    idx = lines[start + 3][10:].find('"')
    result['main_page'] = extract_first_arxiv_url(lines[start + 3])
    idx = lines[start + 4][23:].find('"')
    result['pdf'] = lines[start + 4][22: 23 + idx] + '.pdf'

    start += 4

    while lines[start].strip() != TITLE_TAG:
        start += 1

    title = lines[start + 1].strip()
    title = title.replace('<span class="search-hit mathjax">', '')
    title = title.replace('</span>', '')
    result['title'] = title

    authors, start = get_authors(lines, start + 5)  # orig: add 8

    while not lines[start].strip().startswith(ABSTRACT_TAG):
        start += 1
    abstract = lines[start + 1]
    abstract = abstract.replace('<span class="search-hit mathjax">', '')
    abstract = abstract.replace('</span>', '')
    result['abstract'] = abstract

    result['authors'] = authors

    while not lines[start].strip().startswith(DATE_TAG):
        start += 1

    idx = lines[start].find('</span> ')
    end = lines[start][idx:].find(';')

    result['date'] = lines[start][idx + 8: idx + end]

    return result, start


def clean_empty_lines(lines):
    cleaned = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned.append(line)
    return cleaned


def is_float(token):
    return re.match("^\d+?\.\d+?$", token) is not None


def is_citation_year(tokens, i):
    if len(tokens[i]) != 4:
        return False
    if re.match(r'[12][0-9]{3}', tokens[i]) is None:
        return False
    if i == 0 or i == len(tokens) - 1:
        return False
    if (tokens[i - 1] == ',' or tokens[i - 1] == '(') and tokens[i + 1] == ')':
        return True
    return False


def is_list_numer(tokens, i, value):
    if value < 1 or value > 4:
        return False
    if i == len(tokens) - 1:
        return False

    if (i == 0 or tokens[i - 1] in set(['(', '.', ':'])) and tokens[i + 1] == ')':
        return True
    return False


def has_number(sent):
    tokens = word_tokenize(sent)
    for i, token in enumerate(tokens):
        if token.endswith('\\'):
            token = token[:-2]
        if token.endswith('x'):  # sometimes people write numbers as 1.7x
            token = token[:-1]
        if token.startswith('x'):  # sometimes people write numbers as x1.7
            token = token[1:]
        if token.startswith('$') and token.endswith('$'):
            token = token[1:-1]
        if is_float(token):
            return True
        try:
            value = int(token)
        except:
            continue
        if (not is_citation_year(tokens, i)) and (not is_list_numer(tokens, i, value)):
            return True

    return False


def contains_sota(sent):
    return 'state-of-the-art' in sent or 'state of the art' in sent or 'SOTA' in sent


def extract_line(abstract, keyword, limit):
    lines = []
    numbered_lines = []
    kw_mentioned = False
    abstract = abstract.replace("et. al", "et al.")
    sentences = abstract.split('. ')
    kw_sentences = []
    for i, sent in enumerate(sentences):
        if keyword in sent.lower():
            kw_mentioned = True
            if has_number(sent):
                numbered_lines.append(sent)
            elif contains_sota(sent):
                numbered_lines.append(sent)
            else:
                kw_sentences.append(sent)
                lines.append(sent)
            continue

        if kw_mentioned and has_number(sent):
            if not numbered_lines:
                numbered_lines.append(kw_sentences[-1])
            numbered_lines.append(sent)
        if kw_mentioned and contains_sota(sent):
            lines.append(sent)

    if len(numbered_lines) > 0:
        return '. '.join(numbered_lines), True
    return '. '.join(lines[-2:]), False


def get_report(paper, keyword):
    if keyword in paper['abstract'].lower():
        title = h.unescape(paper['title'])
        headline = '{} ({} - {})\n'.format(title, paper['authors'][0], paper['date'])
        abstract = h.unescape(paper['abstract'])
        extract, has_number = extract_line(abstract, keyword, 280 - len(headline))
        if extract:
            report = headline + extract + '\nLink: {}'.format(paper['main_page'])
            return report, has_number
    return '', False


def txt2reports(txt, keyword, num_to_show):
    found = False
    txt = ''.join(chr(c) for c in txt)
    lines = txt.split('\n')
    lines = clean_empty_lines(lines)
    unshown = []

    for i in range(len(lines)):
        if num_to_show <= 0:
            return unshown, num_to_show, found

        line = lines[i].strip()
        if len(line) == 0:
            continue
        if line == '<li class="arxiv-result">':
            found = True
            paper, i = get_next_result(lines, i)
            report, has_number = get_report(paper, keyword)

            if has_number:
                print(report)
                print('====================================================')
                num_to_show -= 1
            elif report:
                unshown.append(report)
        if line == '</ol>':
            break
    return unshown, num_to_show, found


def get_papers(keyword, num_results=5):
    """
    If keyword is an English word, then search in CS category only to avoid papers from other categories, resulted from the ambiguity
    """

    if keyword in set(['GAN', 'bpc']):
        query_temp = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={}&terms-0-field=all&classification-computer_science=y&classification-physics_archives=all&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size={}&order=-announced_date_first&start={}'
        keyword = keyword.lower()
    else:
        keyword = keyword.lower()
        words = keyword.split()
        d = SpellChecker()
        if not d.unknown(words):
            query_temp = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={}&terms-0-field=all&classification-computer_science=y&classification-physics_archives=all&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size={}&order=-announced_date_first&start={}'
        else:
            query_temp = 'https://arxiv.org/search/?searchtype=all&query={}&abstracts=show&size={}&order=-announced_date_first&start={}'
    keyword_q = keyword.replace(' ', '+')
    page = 0
    per_page = 200
    num_to_show = num_results
    all_unshown = []

    while num_to_show > 0:
        query = query_temp.format(keyword_q, str(per_page), str(per_page * page))

        req = urllib.request.Request(query)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print('Error {}: problem accessing the server'.format(e.code))
            return

        txt = response.read()
        unshown, num_to_show, found = txt2reports(txt, keyword, num_to_show)
        if not found and not all_unshown and num_to_show == num_results:
            print('Sorry, we were unable to find any abstract with the word {}'.format(keyword))
            return

        if num_to_show < num_results / 2 or not found:
            for report in all_unshown[:num_to_show]:
                print(report)
                print('====================================================')
            if not found:
                return
            num_to_show -= len(all_unshown)
        else:
            all_unshown.extend(unshown)
        page += 1

def get_paper_content(pdf_url):
    """
    Gets the content of the paper from the pdf url
    """
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_content = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_content)

    all_text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        all_text += text

    return all_text

def summarise_paper(paper_content, model="gpt-3.5-turbo-0125", role="user"):
    """
    Summarises the paper content using the OpenAI GPT-3.5 16k model
    """
    if len(paper_content) > 45000:
        warnings.warn(f'Paper content is too long - {len(paper_content)} characters. Using only first 45000 characters.')
        paper_content = paper_content[:45000]    
    response = openai_client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a text summarising system that provides easy to understand summaries of research papers."
        },
        {"role": role, 
         "content": "Summarise paper text in 150 words: " + paper_content
         }])

    return response.choices[0].message.content

def key_findings(paper_content, model="gpt-3.5-turbo-0125", role="user"):
    """
    Retrieves Key Findings from a paper using OpenAI GPT-3.5 16k model
    """
    if len(paper_content) > 45000:
        warnings.warn(f'Paper content is too long - {len(paper_content)} characters. Using only first 45000 characters.')
        paper_content = paper_content[:45000]

    openai_client = openai.OpenAI()
    
    response = openai_client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a academic paper parsing system that provides key findings/learnings of research papers."
        },
        {"role": role, 
         "content": "List down the key findings of the paper: " + paper_content
         }])

    return response.choices[0].message.content


def main():
    if 'nt' in os.name:
        try:
            import win_unicode_console
            win_unicode_console.enable()
        except ImportError:
            warnings.warn('On Windows, encoding errors may arise when displaying the data.\n'
                          'If such errors occur, please install `win_unicode_consolde` via \n'
                          'the command `pip install win-unicode-console`.')

    if len(sys.argv) > 1 and sys.argv[1] == 'summarize':
        
        # Check for OpenAI API key only when 'summarize' is the argument
        if 'OPENAI_API_KEY' not in os.environ:
            openai_api_key = getpass('Please enter your OpenAI API Key: ')
        
        os.environ['OPENAI_API_KEY'] = openai_api_key

        if len(sys.argv) < 3:
            raise ValueError('You must specify a paper url')
        paper_url = sys.argv[2]
        paper_content = get_paper_content(paper_url)
        paper_summary = summarise_paper(paper_content)
        print("Paper Summary: \n", paper_summary)
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == 'keyfindings':
    
        # Check for OpenAI API key only when 'keyfindings' is the argument
        if 'OPENAI_API_KEY' not in os.environ:
            openai_api_key = getpass('Please enter your OpenAI API Key: ')
        
        os.environ['OPENAI_API_KEY'] = openai_api_key

        if len(sys.argv) < 3:
            raise ValueError('You must specify a paper url')
        paper_url = sys.argv[2]
        paper_content = get_paper_content(paper_url)
        paper_summary = key_findings(paper_content)
        print("Key Findings: \n", paper_summary)
        return

    if len(sys.argv) < 2:
        raise ValueError('You must specify a keyword')

    try:
        num_results = int(sys.argv[-1])
        assert num_results > 0, 'You must choose to show a positive number of results'
        keyword = ' '.join(sys.argv[1:-1])

    except ValueError:
        keyword = ' '.join(sys.argv[1:])
        num_results = 5


    get_papers(keyword, num_results)


if __name__ == '__main__':
    main()
