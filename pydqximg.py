# -*- coding: utf-8 -*-
#
# ドラクエ10の冒険者の広場画像の一括ダウンロード
#

import os
import re
import sys
import cookielib
import mechanize
from bs4 import BeautifulSoup as bs

def do_login(b, us, pw, ci):
    # ログイン画面
    r = b.open('http://hiroba.dqx.jp/sc/login')
    print(b.geturl())
    print(b.title())
    b.select_form(name='mainForm')
    for f in b.form.controls:
        f.readonly = False
    b.form['_pr_confData_sqexid'] = us
    b.form['_pr_confData_passwd'] = pw
    b.form['_pr_confData_otppw'] = ''
    b.form['_event'] = 'Submit'
    b.submit()
    # 中間画面
    print(b.geturl())
    print(b.title())
    b.select_form(name='mainForm')
    b.submit()
    # キャラクターセレクト
    r = b.open('http://hiroba.dqx.jp/sc/login/characterselect/')
    print(b.geturl())
    print(b.title())
    b.select_form(nr=0)
    for f in b.form.controls:
        f.readonly = False
    b.form['cid'] = ci
    b.submit()

def test_login(b):
    r = b.open('http://hiroba.dqx.jp/sc/home')
    s = bs(r)
    p = s.find_all('h1', {'id': 'cttTitle'})
    if len(p) == 0:
        raise Exception()

def get_browser(filename, proxy=None):
    # username, character_id, directory
    f = open(filename, 'r')
    us = f.readline().strip()
    ci = f.readline().strip()
    dr = f.readline().strip()
    f.close()
    # ask for password
    pw = raw_input('Password? ')
    # setup browser
    b = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    b.set_cookiejar(cj)
    b.set_handle_equiv(True)
    b.set_handle_redirect(True)
    b.set_handle_referer(True)
    b.set_handle_robots(False)
    if proxy:
        b.set_proxies({'http': proxy, 'https': proxy})
    # check cookie
    try:
        cj.load(filename+'cookie', ignore_discard=True, ignore_expires=True)
        test_login(b)
        print('Successfully opened a cookie.')
    except:
        do_login(b, us, pw, ci)
        cj.save(filename+'cookie', ignore_discard=True, ignore_expires=True)
        print('Successfully logged in as {0}, Char#{1}'.format(us, ci))
    return (b, ci, dr)

def download_pics(b, ci, dr):
    urllist = ['http://hiroba.dqx.jp/sc/character/{0}/picture'.format(ci)]
    r = b.open(urllist[0])
    s = bs(r)
    pages = s.find_all('a', {'href': re.compile('picture\/page')})
    for page in pages:
        # ignore next/prev
        if page.string:
            urllist.append('http://hiroba.dqx.jp'+page['href'])
    for url in urllist:
        r = b.open(url)
        s = bs(r)
        imgs = s.find_all('img', {'src': re.compile('img.dqx.jp')})
        for img in imgs:
            url = img['src'].replace('thum2', 'original')
            # use image id as a filename
            name = '{0}.jpg'.format(url.split('/')[-2])
            try:
                open(os.path.join(dr, name), 'r')
                print('File {0} already exists.'.format(name))
            except IOError:
                b.retrieve(url, os.path.join(dr, name))
                print('File {0} saved successfully.'.format(name))

if __name__ == '__main__':
    proxy = None
    if len(sys.argv) > 2:
        proxy = sys.argv[2]
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        (b, ci, dr) = get_browser(filename, proxy)
        download_pics(b, ci, dr)
    else:
        print('Please specify a filename.')
