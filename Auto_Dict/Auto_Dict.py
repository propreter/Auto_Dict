# 基于requests-bs4路线，自动爬取指定词条释义
import re
import time
import traceback

import requests
from bs4 import BeautifulSoup

import File_Process

# 网页编码规则
code = 'utf-8'
# 判断文本字符
regexp_pron = r'\[(.*?)\]'


# 获取cookie，并将其由字典类型转换成字符串
def get_html_cookie():
    cookies = ''
    # 获取cookie
    init_url = 'https://www.bing.com/?FORM=Z9FD1&mkt=zh-CN'
    for item in requests.get(init_url).cookies:
        cookies += item.name + '=' + item.value + ';'
    return cookies


# 获取网页源代码
def get_html_text(word):
    cookie = get_html_cookie()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64    ; x64)  ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/79.0.3945.88 Safari/537.36'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,  ' \
             'image/webp,image/apng,*/*;' \
             'q=0.8,application/signed-exchange;v=b3;q=0.9'
    accept_encoding = 'gzip, deflate, br'
    accept_language = 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7'
    head = {
        'user-agent': user_agent,
        'cookie': cookie,
        'accept': accept,
        'accept_encoding': accept_encoding,
        'accept-language': accept_language,
    }
    kv = {'q': word}
    url = 'https://cn.bing.com/dict/search'

    try:
        r = requests.get(url, params=kv, headers=head, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except Exception:
        traceback.print_exc()
        return '未找到该词！'


# 词汇重定向
def get_entry_redir(headword):
    word_dict_redir = get_entry(headword)
    return word_dict_redir


# 获取词条释义
def get_entry(word):
    word_dict = {}
    temp = ''
    entry = ''
    item_list = []

    html = get_html_text(word)
    soup = BeautifulSoup(html, 'html.parser')
    redirect_identifier = soup.find('div', attrs={'class': 'in_tip'})
    if redirect_identifier is not None:
        redirect_word = soup.find('div', attrs={'class': 'hd_div'}).text
        word_dict = get_entry_redir(redirect_word)
    else:
        if char_identifier:
            pron = soup.find('div', attrs={'lang': r'en'})
        else:
            pron = soup.find('div', attrs={'class': r'hd_pr'})
        if pron is not None:
            pattern = re.compile(regexp_pron)
            pron_list = pattern.search(pron.text)
            if pron_list:
                symbol = pron_list.group(1)
            # 例外1：源文为英文词组，无音标，有音频
            else:
                symbol = '未找到音标'
        # 例外2：源文为英文词组，无音标，无音频
        else:
            symbol = '未找到音标'
        item_list.append(symbol + '\\')
        if soup.find_all('a', attrs={'id': 'authtabid'}):
            for authid in soup.find_all('div', attrs={'id': 'authid'}):
                for seg in authid.find_all('div', attrs={'class': 'each_seg'}):
                    li_pos = seg.find_all('div', attrs={'class': 'li_pos'})
                    if len(li_pos):
                        for li in seg.find_all('div',
                                               attrs={'class': 'li_pos'}):
                            pos_list = li.find_all('div',
                                                   attrs={'class': 'pos'})
                            for i in range(len(pos_list)):
                                key = '[' + pos_list[i].text + ']' + '\n'
                                item_list.append(key)
                            for lis in li.find_all('div',
                                                   attrs={'class': 'se_lis'}):
                                idx = lis.find_all('div',
                                                   attrs={'class': 'se_d'})
                                if idx is not None:
                                    for pa in lis.find_all(
                                            'div', attrs={'class': 'def_pa'}):
                                        bil_list = pa.find_all(
                                            'span', attrs={'class': 'bil'})
                                        val_list = pa.find_all(
                                            'span', attrs={'class': 'val'})
                                        if len(val_list) > 1:
                                            for v in val_list:
                                                temp += v.text
                                            val = ''.join(idx[0].text +
                                                          bil_list[0].text +
                                                          '\\' + temp + '\n')
                                        else:
                                            val = ''.join(idx[0].text +
                                                          bil_list[0].text +
                                                          '\\' +
                                                          val_list[0].text +
                                                          '\n')
                                        item_list.append(val)
                                else:
                                    # 该词性下没有释义条目
                                    item_list.append('未找到单词词性释义条目')
                    else:
                        # 该词汇没有词性条目
                        item_list.append('未找到单词词性条目')
        elif soup.find_all('a', attrs={'id': 'crosstabid'}):
            for crossid in soup.find_all('div', attrs={'id': 'crossid'}):
                for seg in crossid.find_all('tr',
                                            attrs={'class':
                                                   'def_row df_div1'}):
                    pos_list = seg.find_all('div', attrs={'class': 'pos pos1'})
                    for f1 in seg.find_all('div', attrs={'class': 'def_fl'}):
                        idx_list = f1.find_all('div', attrs={'class': 'se_d'})
                        val_list = f1.find_all('div',
                                               attrs={'class': 'df_cr_w'})
                        for i in range(len(pos_list)):
                            key = '[' + pos_list[i].text + ']' + '\n'
                            item_list.append(key)
                            for j in range(len(val_list)):
                                val = ''.join(idx_list[j].text +
                                              val_list[j].text + '\n')
                                item_list.append(val)
        elif soup.find_all('a', attrs={'id': 'hometabid'}):
            for homoid in soup.find_all('div', attrs={'id': 'homoid'}):
                for seg in homoid.find_all('tr',
                                           attrs={'class': 'def_row df_div1'}):
                    pos_list = seg.find_all('div', attrs={'class': 'pos pos1'})
                    for f1 in seg.find_all('div', attrs={'class': 'def_fl'}):
                        idx_list = f1.find_all('div', attrs={'class': 'se_d'})
                        val_list = f1.find_all('div',
                                               attrs={'class': 'df_cr_w'})
                        for i in range(len(pos_list)):
                            key = '[' + pos_list[i].text + ']' + '\n'
                            item_list.append(key)
                            for j in range(len(val_list)):
                                val = ''.join(idx_list[j].text +
                                              val_list[j].text + '\n')
                                item_list.append(val)
        elif soup.find_all('a', attrs={'id': 'webtabid'}):
            for webid in soup.find_all('div', attrs={'id': 'webid'}):
                for seg in webid.find_all(
                        'tr', attrs={'class': 'def_row de_li1 de_li4'}):
                    pos_list = seg.find_all('div', attrs={'class': 'se_d'})
                    val_list = seg.find_all('div', attrs={'class': 'p1-1'})
                    for i in range(len(pos_list)):
                        key = pos_list[i].text
                        item_list.append(key)
                        val = ''.join(val_list[i].text + '\n')
                        item_list.append(val)
        else:
            item_list.append('未找到单词释义')
        for item in item_list:
            entry += item
        word_dict[word] = entry.rstrip('\n')
    return word_dict


# 获取中文释义
def get_entry_english(eng_wd):
    # global pr
    eng_dict = {}
    try:
        # 获取音标
        # pr = get_phonetic_symbol(eng_wd)
        # 获取词条
        eng_dict = get_entry(eng_wd)
    except Exception:
        traceback.print_exc()
    return eng_dict


# 获取英文释义
def get_entry_chinese(chn_wd):
    chn_dict = {}
    try:
        # 获取词条
        chn_dict = get_entry(chn_wd)
    except Exception:
        traceback.print_exc()
    return chn_dict


# 获取单词释义
def get_meaning_entry(wlist):
    cnt = 0
    info_dict = {}
    # 字符语言标志
    global char_identifier
    for w in wlist:
        # 利用正则识别中英文文本
        # print(w)
        char_identifier = File_Process.char_discriminator(w)
        time.sleep(1)
        if char_identifier:
            info_dict.update(get_entry_chinese(w))
        else:
            info_dict.update(get_entry_english(w))
        cnt += 1
        print('\r查询进度： {:.2f}%'.format(cnt * 100 / len(wlist)), end='')
        # print('\n')
    return info_dict


# 自动查词入口
def auto_dict(word_list):
    entry_dict = get_meaning_entry(word_list)
    return entry_dict
