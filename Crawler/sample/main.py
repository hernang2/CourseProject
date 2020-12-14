from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib
import urllib.request
import validators
import json
from nltk import tokenize


# uses webdriver object to execute javascript code and get dynamically loaded webcontent
def get_js_soup(url, driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
    return soup


# tidies extracted text
def process_bio(bio):
    bio = bio.encode('ascii', errors='ignore').decode('utf-8')  # removes non-ascii characters
    bio = re.sub('\s+', ' ', bio)  # replaces repeated whitespace characters with single space
    return bio


''' More tidying
Sometimes the text extracted HTML webpage may contain javascript code and some style elements. 
This function removes script and style tags from HTML so that extracted text does not contain them.
'''


def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


# Checks if bio_url is a valid faculty homepage
def is_valid_homepage(bio_url, dir_url):
    if bio_url.endswith('.pdf'):  # we're not parsing pdfs
        return False
    try:
        # sometimes the homepage url points to the same page as the faculty profile page
        # which should be treated differently from an actual homepage
        ret_url = urllib.request.urlopen(bio_url).geturl()
    except:
        return False  # unable to access bio_url
    urls = [re.sub('((https?://)|(www.))', '', url) for url in
            [ret_url, dir_url]]  # removes url scheme (https,http or www)
    return not (urls[0] == urls[1])


# extracts all Faculty Profile page urls from the Directory Listing Page
def scrape_dir_page(faculty_base_url, dir_url, driver):
    print('-' * 20, 'Scraping directory page', '-' * 20)
    faculty_professors = []
    nameRegex = '^([A-Za-z]{2,25}(\s\([A-Za-z]{2,25}\))?(,)?(\s[A-Za-z]{2,25}))$'
    name = ''
    try:
        soup = get_js_soup(dir_url, driver)
        professor_hyperlinks = soup.find_all('a')
        for hyperlink in professor_hyperlinks:  # get list of all <div> of class 'name'
            if hyperlink.string and re.match(nameRegex, hyperlink.string) is not None:
                rel_link = hyperlink['href']  # get url
                if validators.url(rel_link):
                    name = hyperlink.string.strip()
                    bio, email, faculty, location = scrape_faculty_page(rel_link, driver)
                    faculty_professors.append({
                        'name': name,
                        'bio': bio,
                        'email': email,
                        'faculty': faculty,
                        'location': location,
                        'url': rel_link
                    })
        print('-' * 20, 'Found {} faculty profile urls'.format(len(faculty_professors)), '-' * 20)
    except:
        pass
    return faculty_professors


def scrape_faculty_page(fac_url, driver):
    email = ''
    faculty = ''
    location = ''
    bio = ''

    try:
        soup = get_js_soup(fac_url, driver)
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        faculty_keywords = ['department', 'Department', 'faculty', 'Faculty', 'institute', 'Institute']
        bio = visible_text.strip()
        tags = soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'td', 'span'])
        strippy = ''
        for tag in tags:
            try:
                if tag and (tag.string or tag.contents):
                    if tag.string:
                        strippy = tag.string.strip()
                        if re.match(email_regex, strippy):
                            reg_result = re.findall(email_regex, strippy)
                            if reg_result:
                                email = reg_result[0]

                        elif any(ext in strippy for ext in faculty_keywords):
                            for sentence in tokenize.sent_tokenize(strippy):
                                strippy = ''.join(sentence[:6]).strip()
                                if any(ext in strippy for ext in faculty_keywords):
                                    faculty = sentence
                                    break
                    elif tag.contents:
                        for content in tag.contents:
                            if content.string:
                                if isinstance(content, str):
                                    strippy = content.strip()
                                else:
                                    strippy = content
                                try:
                                    if any(ext in strippy for ext in faculty_keywords):
                                        for sentence in tokenize.sent_tokenize(strippy):
                                            strippy = ''.join(sentence[:6]).strip()
                                            if any(ext in strippy for ext in faculty_keywords):
                                                faculty = strippy
                                                break
                                    elif re.match(email_regex, strippy):
                                        reg_result = re.findall(email_regex, strippy)
                                        if reg_result:
                                            email = reg_result[0]
                                    else:
                                        for sentence in tokenize.sent_tokenize(strippy):
                                            strippy = sentence.strip()
                                            if re.match(email_regex, strippy):
                                                reg_result = re.findall(email_regex, strippy)
                                                if reg_result:
                                                    email = reg_result[0]
                                                    break
                                except:
                                    pass
            except:
                pass
    except:
        pass
    return bio, email, faculty, location


def write_lst(lst, file_):
    with open(file_, 'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')


def write_json(data, file_):
    with open(file_, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    # driver = webdriver.Edge(executable_path="D:/Projects/410/MP2.1_private/sample/edgedriver_win64/msedgedriver.exe")
    driver = webdriver.Firefox(
        executable_path=r"D:\Projects\410\MP2.1_private\scraper_code\geckodriver-v0.28.0-win64/geckodriver.exe")

    # Scrape homepages of all urls
    bios = []
    dir_url = [
        'https://www.csd.cs.cmu.edu/directory/faculty',
        'https://www.cs.stanford.edu/directory/faculty',
        'https://cs.vt.edu/People/Faculty.html',
        'https://www.cs.washington.edu',
        'https://www.eecs.mit.edu/people/faculty-advisors',
        'https://www.scs.gatech.edu/people/faculty',
        'https://www.cs.ucla.edu/faculty/',
        'https://www.cs.utexas.edu/faculty',
        'https://www.cs.wisc.edu/people/faculty/',
        'https://www2.eecs.berkeley.edu/Faculty/Lists/CS/faculty.html',
        'http://www.cms.caltech.edu/people',
        'https://www.cs.cornell.edu/people/faculty',
        'https://www.colorado.edu/cs/faculty',
        'http://www.cis.upenn.edu/about-people/index.php',
        'http://www.eecs.umich.edu/eecs/faculty/csefaculty.html',
        'http://cs.ua.edu/people/',
        'https://csweb.rice.edu/faculty',
        'https://www.seas.harvard.edu/computer-science/people',
        'https://www.isye.gatech.edu/academics/bachelors/industrial-engineering/faculty',
        'https://www.math.toronto.edu/cms/people/',
        'https://bioengineering.rice.edu/people',
        'https://www.biology.washington.edu/people/faculty'
    ]
    for faculty_url in dir_url:
        faculty_links = scrape_dir_page('', faculty_url, driver)

        tot_urls = len(faculty_links)
        for i, professor in enumerate(faculty_links):
            print('-' * 20, 'Scraping faculty url {}/{}'.format(i + 1, tot_urls), '-' * 20)
            # professors_array = scrape_faculty_page(link, driver)
            bios.append(professor)

    driver.close()
    # bio_urls_file = 'bio_urls.txt'
    # bios_file = 'bios.txt'
    # write_lst(bio_urls, bio_urls_file)
    # write_lst(bios, bios_file)
    write_json(bios, 'bios_json.txt')
