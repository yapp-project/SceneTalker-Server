from drama.models import Drama
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import requests


class NaverCrawler:
    @staticmethod
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

    @staticmethod
    def get_live_drama_list():
        drama_list = []
        count = 1
        while True:
            params = (
                ('where', 'nexearch'),
                ('pkid', '57'),
                ('key', 'BroadcastListAPI'),
                ('u1', count),
                ('u2', '6'),
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
                    drama_list.append(drama_name)
                count += 6
            else:
                break

        return drama_list

    def get_detail(self, keyword):
        html = self.search_keyword(keyword)
        soup = bs(html, 'html.parser')

        detail = soup.find(id='brcs_detail')
        if not detail:
            return None
        summary = detail.find(id='layer_sy').text.strip() if hasattr(detail.find(id='layer_sy'), 'text') \
            else detail.find('dd', class_='intro _multiLayerContainer').text.strip()
        rating = float(detail.select_one('.fred').text.replace('%', '')) if hasattr(detail.select_one('.fred'), 'text') \
            else 0.0
        broadcasting_station = detail.find('dd').find('span').find('a').text
        is_broadcasiting = True if detail.find('dd').find('span').select_one('.broad_txt').text == '방영중' else False
        poster_url = soup.select_one('.brcs_thumb').find('img').attrs['src']

        datetime_info = detail.find('span', class_='inline').text.split('|')[1].strip().split(' [')[0]
        print(datetime_info[:-9])
        broadcasting_day = ''
        time_info = datetime_info.split(') ')[1]
        broadcasting_start_time = datetime.strptime(time_info[3:], "%H:%M") if time_info[:2] == '오전' \
            else datetime.strptime(f'{int(time_info[3:5]) + 12}{time_info[5:]}', "%H:%M")
        broadcasting_end_time = broadcasting_start_time + timedelta(hours=1, minutes=20)

        return {'title': keyword,
                'rating': rating,
                'summary': summary,
                'broadcasting_station': broadcasting_station,
                'is_broadcasiting': is_broadcasiting,
                'broadcasting_start_time': broadcasting_start_time,
                'broadcasting_end_time': broadcasting_end_time,
                'broadcasting_day': broadcasting_day,
                'poster_url': poster_url}

    def get_genre(self, keyword):
        html_for_genre = self.search_keyword(f'{keyword} 장르')
        soup = bs(html_for_genre, 'html.parser')
        genre = soup.select_one('.v').text if hasattr(soup.select_one('.v'), 'text') else '드라마'
        return genre


def update_drama():
    crawler = NaverCrawler()
    qs = Drama.objects.filter(is_broadcasiting=True)
    title_list = [drama.title for drama in qs]

    for title in title_list:
        detail = crawler.get_detail(title)
        Drama.objects.filter(title=title).update(rating=detail['rating'], is_broadcasiting=detail['is_broadcasiting'])

    for live_drama in crawler.get_live_drama_list():
        if live_drama not in title_list:
            drama = Drama.objects.create(**crawler.get_detail(live_drama))
            for genre in crawler.get_genre(live_drama).replace(' ', '').split(','):
                drama.genre.add(genre)
