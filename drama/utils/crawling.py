import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import quote


class Crawler:
    def __init__(self):
        pass

    def get_detail_in_naver(self, keyword):
        def search_keyword(keyword):
            headers = {
                'authority': 'search.naver.com',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'sec-fetch-site': 'same-origin',
                'referer': 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%B0%B0%EA%B0%80%EB%B3%B8%EB%93%9C',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'cookie': 'NNB=P5SLKNMWRQ4F2; nx_open_so=1; ASID=7db134b80000016cc3de939f0000005e; _ga_4BKHBFKFK0=GS1.1.1568988287.1.1.1568989819.60; nx_ssl=2; _ga=GA1.2.1718670836.1568988288; BMR=s=1570176040457&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dhsetsh%26logNo%3D221166630296%26proxyReferer%3Dhttps%253A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=UiEUCsprvh8ssMe+mBKssssstb8-461137; _naver_usersession_=qLyt7RAkfpVyH9nVoCmWjg==',
            }

            params = (
                ('sm', 'tab_hty.top'),
                ('where', 'nexearch'),
                ('query', keyword),
                ('oquery', ''),
                ('tqi', 'UiEUCsprvh8ssMe+mBKssssstb8-461137'),
            )
            response = requests.get('https://search.naver.com/search.naver', headers=headers, params=params)
            assert response.ok, response.reason
            return response.text

        html = search_keyword(keyword)
        soup = bs(html, 'html.parser')
        detail = soup.find(id='brcs_detail')
        try:
            rating = detail.select_one('.fred').text
        except AttributeError:
            rating = '알수없음'
        summary = detail.find(id='layer_sy').text.strip()

        return {'rating': rating, 'summary': summary}

    def get_detail_in_wiki(self, keyword):
        def search_keyword(keyword):
            response = requests.get(f'https://ko.wikipedia.org/wiki/{keyword}')
            assert response.ok, response.reason
            return response.text

        try:
            html = search_keyword(quote(keyword))
            assert '장르' in html and '방송 채널' in html, 'keyword 뒤에 (드라마)를 붙여야 한다.'
        except AssertionError:
            html = search_keyword(f'{quote(keyword)}_({quote("드라마")})')

        soup = bs(html, 'html.parser')
        table = soup.select_one('.infobox')
        info = {}
        for tr in table.select_one('tbody').find_all('tr')[2:]:
            info.update({
                tr.select_one('th').text.strip(): tr.select_one('td').text.strip()
            })

        return info


if __name__ == "__main__":
    crawler = Crawler()
    naver_info = crawler.get_detail_in_naver('배가본드')
    wiki_info = crawler.get_detail_in_wiki('배가본드')

    drama_info = {**naver_info, **wiki_info}
    from pprint import pprint
    pprint(drama_info)
