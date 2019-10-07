import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import quote, unquote


class Crawler:
    def __init__(self):
        pass

    def get_live_drama_list(self):
        drama_list = []
        u1 = 1
        while True:
            params = (
                ('where', 'nexearch'),
                ('pkid', '57'),
                ('key', 'BroadcastListAPI'),
                ('u1', u1),
                ('u2', '8'),
                ('u3', 's3.asc'),
                ('u4', 'KR'),
                ('u5', 'drama'),
                ('u6', 'ing'),
                ('u7', ''),
                ('u8', ''),
                ('u9', ''),
                ('_callback', 'jQuery1124014662727284181387_1570449645314'),
            )
            response = requests.get('https://search.naver.com/p/csearch/content/nqapirender.nhn', params=params)

            html = response.text.split('sHtml" : " ')[1]
            soup = bs(html, 'html.parser')

            dt_tags = soup.find_all('dt')
            if dt_tags:
                for dt in dt_tags:
                    drama_name = dt.find('a').text.split('<')[0]
                    if 'KBS' in drama_name:
                        continue
                    drama_list.append(drama_name)
                u1 += 6
            else:
                break

        return drama_list

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
        html_for_genre = search_keyword(f'{keyword} 장르')
        soup = bs(html, 'html.parser')
        soup_genre = bs(html_for_genre, 'html.parser')

        detail = soup.find(id='brcs_detail')
        summary = detail.find(id='layer_sy').text.strip()
        broadcasting_station = detail.find('dd').find('span').find('a').text
        is_broadcasiting = detail.find('dd').find('span').select_one('.broad_txt').text

        try:
            rating = detail.select_one('.fred').text
        except AttributeError:
            rating = '알수없음'

        try:
            genre = soup_genre.select_one('.v').text
        except AttributeError:
            genre = '드라마'

        return {'rating': rating, 'summary': summary, 'genre': genre, 'broadcasting_station': broadcasting_station,
                'is_broadcasiting': is_broadcasiting}


if __name__ == "__main__":
    crawler = Crawler()

    live_drama_list = crawler.get_live_drama_list()
    for drama in live_drama_list:
        print(drama)
        print(crawler.get_detail_in_naver(drama))
