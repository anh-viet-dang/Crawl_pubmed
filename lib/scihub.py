from .config import PMID2DOI_FILE_PATH
from .one_paper import find_DOI
from .utils import pmid2Url, send_request

# doi = r'10.1016/j.semcancer.2020.02.016'

# -*- coding: utf-8 -*-

"""
Sci-API Unofficial API
[Search|Download] research papers from [scholar.google.com|sci-hub.io].

@author zaytoun
https://github.com/zaytoun/scihub.py/blob/master/scihub/scihub.py
"""

import hashlib
import logging
import os
import re

import requests
import urllib3
from bs4 import BeautifulSoup
from colorama import Fore
from retrying import retry

# log config
logging.basicConfig()
logger = logging.getLogger('Sci-Hub')
logger.setLevel(logging.DEBUG)

#
urllib3.disable_warnings()

# constants
SCHOLARS_BASE_URL = 'https://scholar.google.com/scholar'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}

class SciHub(object):
    """
    SciHub class can search for papers on Google Scholars 
    and fetch/download papers from sci-hub.io
    """
    @staticmethod
    def pmid2doi(pmid:str, is_save:bool = True, path_save:str= PMID2DOI_FILE_PATH) -> str:
        """
        sent request to pubmed để tìm doi
        """
        full_url = pmid2Url(pmid)
        body = send_request(full_url)
        doi = find_DOI(body)
        if is_save:
            with open(path_save, 'a', encoding= 'utf-8') as f:
                f.write(pmid + ',' + doi + '\n')

        return doi

    @staticmethod
    def rewrite_pmid2doi():
        with open(PMID2DOI_FILE_PATH, 'r', encoding= 'utf-8') as f:
            lines = f.read().strip().split('\n')

        newline = []
        pmids = []
        for line in lines:
            pmid = line.split(',')[0].strip()
            if pmid not in pmids:
                pmids.append(pmid)
                newline.append(line)
        
        with open(PMID2DOI_FILE_PATH, 'w', encoding= 'utf-8') as f:
            f.write('\n'.join(newline) + '\n')

    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers = HEADERS
        self.available_base_url_list = self.get_available_scihub_urls()
        for scihub_url in self.available_base_url_list:
            print(scihub_url)
        self.base_url = self.available_base_url_list[0] + '/'

    @staticmethod
    def get_available_scihub_urls():
        # @author watson21 imnova1212@gmail.com
        # Finds available scihub urls via https://sci-hub.now.sh/
        resp = send_request('https://sci-hub.now.sh/')
        scihub_tag = resp.find_all('a', href=True)
        urls = []
        for sci in scihub_tag:
            url = sci.__getitem__(key= "href").strip().strip(r'/')
            if url.startswith(r"https://sci-hub.") or url.startswith(r"http://sci-hub."):
                # NOTE get url scihub from below url
                # https://creativecommons.org/choose/results-one?q_1=2&q_1=1&field_commercial=yes&field_derivatives=n&field_jurisdiction=&field_format=Text&field_worktitle=sci-hub&field_attribute_to_name=&field_attribute_to_url=https://sci-hub.41610.org&lang=en_EN&language=en_EN&n_questions=3
                
                if url not in urls:
                    urls.append(url)

        return urls

    # def _get_available_scihub_urls(self):
    #     '''
    #     Finds available scihub urls via https://sci-hub.now.sh/
    #     '''
    #     urls = []
    #     res = requests.get('https://sci-hub.now.sh/')
    #     s = self._get_soup(res.content)
    #     for a in s.find_all('a', href=True):
    #         if 'sci-hub.' in a['href']:
    #             urls.append(a['href'])
    #     return urls

    # def set_proxy(self, proxy):
    #     '''
    #     set proxy for session
    #     :param proxy_dict:
    #     :return:
    #     '''
    #     if proxy:
    #         self.sess.proxies = { "http": proxy, 
    #                               "https": proxy,}

    def _change_base_url(self):
        if not self.available_base_url_list:
            raise Exception('Ran out of valid sci-hub urls')
        del self.available_base_url_list[0]
        self.base_url = self.available_base_url_list[0] + '/'
        logger.info("I'm changing to {}".format(self.available_base_url_list[0]))

    def search(self, query, limit=10, download=False):
        """
        Performs a query on scholar.google.com, and returns a dictionary
        of results in the form {'papers': ...}. Unfortunately, as of now,
        captchas can potentially prevent searches after a certain limit.
        """
        start = 0
        results = {'papers': []}

        while True:
            try:
                res = self.sess.get(SCHOLARS_BASE_URL, params={'q': query, 'start': start})
            except requests.exceptions.RequestException as e:
                results['err'] = 'Failed to complete search with query %s (connection error)' % query
                return results

            s = self._get_soup(res.content)
            papers = s.find_all('div', class_="gs_r")

            if not papers:
                if 'CAPTCHA' in str(res.content):
                    results['err'] = 'Failed to complete search with query %s (captcha)' % query
                return results

            for paper in papers:
                if not paper.find('table'):
                    source = None
                    pdf = paper.find('div', class_='gs_ggs gs_fl')
                    link = paper.find('h3', class_='gs_rt')

                    if pdf:
                        source = pdf.find('a')['href']
                    elif link.find('a'):
                        source = link.find('a')['href']
                    else:
                        continue

                    results['papers'].append({
                        'name': link.text,
                        'url': source
                    })

                    if len(results['papers']) >= limit:
                        return results

            start += 10

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    def download(self, identifier, destination='', path=None) -> int:
        """
        Downloads a paper from sci-hub given an indentifier (DOI, PMID, URL).
        Currently, this can potentially be blocked by a captcha if a certain
        limit has been reached.
        >>> return size of downloaded pdf file : int
        """
        data = self.fetch(identifier)

        if not 'err' in data:
            # self._save(data['pdf'],
            #            os.path.join(destination, path if path else data['name']))
            # path = os.path.join(destination, path if path else data['name'])
            path = path if path else os.path.join(destination, data['name'])
            with open(path, 'wb') as f:
                f.write(data['pdf'])

            return os.path.getsize(path)
        else:
            return 0

    # def _save(self, data, path):
    #     """
    #     Save a file give data and a path.
    #     """
    #     with open(path, 'wb') as f:
    #         f.write(data)

    def fetch(self, identifier):
        """
        Fetches the paper by first retrieving the direct link to the pdf.
        If the indentifier is a DOI, PMID, or URL pay-wall, then use Sci-Hub
        to access and download paper. Otherwise, just download paper directly.
        """

        try:
            url = self._get_direct_url(identifier)

            # verify=False is dangerous but sci-hub.io 
            # requires intermediate certificates to verify
            # and requests doesn't know how to download them.
            # as a hacky fix, you can add them to your store
            # and verifying would work. will fix this later.
            res = self.sess.get(url, verify=False)

            if res.headers['Content-Type'] != 'application/pdf':
                self._change_base_url()
                logger.info('Failed to fetch pdf with identifier %s '
                                           '(resolved url %s) due to captcha' % (identifier, url))
                raise CaptchaNeedException(Fore.LIGHTRED_EX + 'Failed to fetch pdf with identifier %s '
                                           '(resolved url %s) due to captcha' % (identifier, url))
                # return {
                #     'err': 'Failed to fetch pdf with identifier %s (resolved url %s) due to captcha'
                #            % (identifier, url)
                # }
            else:
                return {
                    'pdf': res.content,
                    'url': url,
                    'name': self._generate_name(res)
                }

        except requests.exceptions.ConnectionError:
            logger.info('Cannot access {}, changing url'.format(self.available_base_url_list[0]))
            self._change_base_url()

        except requests.exceptions.RequestException as e:
            logger.info('Failed to fetch pdf with identifier %s (resolved url %s) due to request exception.'
                       % (identifier, url))
            return {
                'err': 'Failed to fetch pdf with identifier %s (resolved url %s) due to request exception.'
                       % (identifier, url)
            }

    def _get_direct_url(self, identifier):
        """
        Finds the direct source url for a given identifier.
        """
        id_type = self._classify(identifier)

        return identifier if id_type == 'url-direct' \
            else self._search_direct_url(identifier)

    def _search_direct_url(self, identifier):
        """
        Sci-Hub embeds papers in an iframe. This function finds the actual
        source url which looks something like https://moscow.sci-hub.io/.../....pdf.
        """
        res = self.sess.get(self.base_url + identifier, verify=False)
        s = self._get_soup(res.content)
        iframe = s.find('iframe')
        if iframe:
            return iframe.get('src') if not iframe.get('src').startswith('//') \
                else 'http:' + iframe.get('src')

    def _classify(self, identifier):
        """
        Classify the type of identifier:
        url-direct - openly accessible paper
        url-non-direct - pay-walled paper
        pmid - PubMed ID
        doi - digital object identifier
        """
        if (identifier.startswith('http') or identifier.startswith('https')):
            if identifier.endswith('pdf'):
                return 'url-direct'
            else:
                return 'url-non-direct'
        elif identifier.isdigit():
            return 'pmid'
        else:
            return 'doi'

    def _get_soup(self, html):
        """
        Return html soup.
        """
        return BeautifulSoup(html, 'html.parser')

    def _generate_name(self, res):
        """
        Generate unique filename for paper. Returns a name by calcuating 
        md5 hash of file contents, then appending the last 20 characters
        of the url which typically provides a good paper identifier.
        """
        name = res.url.split('/')[-1]
        name = re.sub('#view=(.+)', '', name)
        pdf_hash = hashlib.md5(res.content).hexdigest()
        return '%s-%s' % (pdf_hash, name[-20:])

class CaptchaNeedException(Exception): ...
