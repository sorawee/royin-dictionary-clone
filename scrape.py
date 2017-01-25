import grequests
import requests
import re
import os

alphabets = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮ"
lookup_domain = "http://www.royin.go.th/dictionary/Lookup/lookupDomain.php"
lookup_word = "http://www.royin.go.th/dictionary/func_lookup.php"

session = requests.Session()

for alphabet in alphabets:
    if not os.path.exists('words/' + alphabet):
        os.makedirs('words/' + alphabet)
    page = requests.get(lookup_domain, params={'page': 1, 'domain': alphabet})
    num_words, all_words = eval(page.content)
    num_words //= 10
    pages = grequests.imap((grequests.get(lookup_domain, params={'page': i, 'domain': alphabet})
                            for i in range(2, num_words + 1)), size=10)
    for i, page in enumerate(pages):
        print("fetching index {}/{}".format(i + 1, num_words))
        _, words = eval(page.content)
        all_words.extend(words)

    pages = grequests.imap((grequests.post(lookup_word, data={'funcName': "lookupWord", 'status': "domain", "word": w}) for w in all_words), size=10)
    for i, word in enumerate(pages):
        print("fetching word {}/{}".format(i + 1, len(all_words)))
        content = word.content.decode('utf-8')
        title = re.search('ผลการค้นหา "(.*?)"', content).group(1)
        with open('words/' + alphabet + '/file-' + title, 'w') as f:
            f.write(content)
