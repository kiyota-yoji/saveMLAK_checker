#!/usr/bin/env python
# -*- coding: utf-8 -*-

### 熊本地震ページからのリンク抽出テスト

import urllib, urllib2, lxml.html, chardet
from html2text import html2text
from urlparse import urlparse, urlunparse

def get_html(url):
    html_original = urllib2.urlopen(url).read()
    encoding = chardet.detect(html_original)['encoding']
    html = html_original.decode(encoding)
    return html

def extract_links(html):
    # parse HTML
    root = lxml.html.fromstring(html)

    link_nodes = root.xpath('//a[@class="external free"]')
    links = []
    for n in link_nodes:
        original_url = n.attrib['href']
        (protocol, domain, path, params, query, fragment) = urlparse(original_url.encode('utf-8'))
        domain = unicode(domain, 'utf-8', 'ignore')
        domain = domain.encode('idna')
        path = urllib.quote(path, '/')
        query = urllib.quote(query, '/=&')
        url = urlunparse((protocol, domain, path, params, query, ''))
        links.append(url)
    return links


if __name__ == '__main__':
    links = extract_links(get_html('http://savemlak.jp/wiki/2016%E5%B9%B44%E6%9C%88%E7%86%8A%E6%9C%AC%E5%9C%B0%E9%9C%87'))
    for l in links:
        try:
            html = get_html(l)
            print 'ZZZ(%d): %s' % (len(html), l)
            print html2text(html)
        except urllib2.HTTPError:
            pass
