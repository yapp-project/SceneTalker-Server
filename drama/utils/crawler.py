from drama.models import Drama
from feed.models import Feed
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from time import sleep
from random import randint
import requests


class NaverCrawler:
    @staticmethod
    def search_keyword(keyword):
        sleep(randint(0, 2))
        params = (
            ('sm', 'tab_hty.top'),
            ('where', 'nexearch'),
            ('query', keyword),
            ('oquery', ''),
            ('tqi', 'UiEUCsprvh8ssMe+mBKssssstb8-461137'),
        )

        response = requests.get('https://search.naver.com/search.naver', params=params)
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

        detail = soup.select_one('.detail_info')
        if detail is None:
            return None

        if hasattr(detail.find('p', class_='episode_txt _text'), 'text'):
            summary = detail.find('p', class_='episode_txt _text').text.strip()
        else:
            summary = '알수없음'

        try:
            rating = float(detail.find('em').text)
        except AttributeError:
            rating = 0.0

        try:
            if detail.find('span', class_='broad_txt').text == '방영중':
                is_broadcasting = True
            else:
                is_broadcasting = False
        except AttributeError:
            is_broadcasting = False

        try:
            broadcasting_station = detail.find('dd').find('a').text
        except AttributeError:
            broadcasting_station = '알수없음'

        try:
            poster_url = soup.find('div', class_='main_thumb').find('img').attrs['src']
        except AttributeError:
            poster_url = 'https://webhostingmedia.net/wp-content/uploads/2018/01/http-error-404-not-found.png'

        try:
            episode = soup.find('dl', class_='turn_info_desc').find('strong').text
        except AttributeError:
            episode = '알수없음'

        try:
            datetime_info = detail.find('span').text.strip()
            broadcasting_day = parse_day(datetime_info.split('(')[1].split(')')[0])
            time_info = datetime_info.split(') ')[1]
            if time_info[:2] == '오전':
                broadcasting_start_time = datetime.strptime(time_info[3:], "%H:%M") - timedelta(minutes=10)
            else:
                broadcasting_start_time = datetime.strptime(f'{int(time_info[3:5]) + 12}{time_info[5:]}',
                                                            "%H:%M") - timedelta(minutes=10)
            broadcasting_end_time = broadcasting_start_time + timedelta(hours=1, minutes=30)
        except Exception as e:
            print(e)
            return None

        return {'title': keyword,
                'rating': rating,
                'summary': summary,
                'broadcasting_station': broadcasting_station,
                'is_broadcasting': is_broadcasting,
                'broadcasting_start_time': broadcasting_start_time,
                'broadcasting_end_time': broadcasting_end_time,
                'broadcasting_day': broadcasting_day,
                'poster_url': poster_url,
                'episode': episode}

    def get_genre(self, keyword):
        html_for_genre = self.search_keyword(f'{keyword} 장르')
        soup = bs(html_for_genre, 'html.parser')
        try:
            genre = soup.select_one('.v').text
        except AttributeError:
            genre = '드라마'

        return genre


def parse_day(day):
    days = ['월', '화', '수', '목', '금', '토', '일']
    result = []
    if '~' in day:
        day_range = day.split('~')
        for i in days[days.index(day_range[0]): days.index(day_range[1]) + 1]:
            result.append(i)
    elif ',' in day:
        for i in day.replace(' ', '').split(','):
            result.append(i)
    else:
        result.append(day)
    return result


def update_drama():
    crawler = NaverCrawler()
    qs = Drama.objects.filter(is_broadcasting=True)
    title_list = [drama.title for drama in qs]
    for title in title_list:
        detail = crawler.get_detail(title)
        if detail:
            Drama.objects.filter(title=title).update(rating=detail['rating'],
                                                     is_broadcasting=detail['is_broadcasting'])
        else:
            Drama.objects.filter(title=title).update(is_broadcasting=False)

    for live_drama in crawler.get_live_drama_list():
        if live_drama not in title_list:
            detail = crawler.get_detail(live_drama)
            if detail:
                drama = Drama.objects.create(title=detail['title'],
                                             rating=detail['rating'],
                                             summary=detail['summary'],
                                             broadcasting_station=detail['broadcasting_station'],
                                             is_broadcasting=detail['is_broadcasting'],
                                             broadcasting_start_time=detail['broadcasting_start_time'],
                                             broadcasting_end_time=detail['broadcasting_end_time'],
                                             poster_url=detail['poster_url'],
                                             episode=detail['episode'])
                for day in detail['broadcasting_day']:
                    drama.broadcasting_day.add(day)

                for genre in crawler.get_genre(live_drama).replace(' ', '').split(','):
                    drama.genre.add(genre)

                # one to one feed 모델 생성
                Feed.objects.create(drama=drama)


if __name__ == "__main__":
    update_drama()
