import feedparser
import re

def get_titles_by_ssl(start, end, search_name, verbose1=False, verbose2=False, is_preprocessed=True):
    """
    start : 데이터를 조회할 시작 날짜 -> Str (ex:2022-06-01),
    end : 데이터를 조회할 마지막 날짜 -> Str (ex:2022-10-31),
    search_name  : 검색할 이름 -> Str, 
    verbose1 : 과정을 출력할지 여부 -> Bool,
    verbose2 : 결과를 출력할지 여부 -> Bool,
    is_preprocessed : 전처리할지 여부 -> Bool, 
    return : 뉴스 제목 리스트 -> List
    """

    ssl_url = f'https://news.google.com/news?hl=ko&gl=kr&ie=UTF-8&q={search_name}+after:{start}+before:{end}&output=rss'

    parse_res = feedparser.parse(ssl_url)

    titles = []
    
    for p in parse_res.entries:
        if verbose1:
            print(p.title)
        titles.append(p.title)
        
    if verbose2:
        print(len(titles))
    
    if is_preprocessed:
        titles = preprocessing(titles)
        
    return titles

def preprocessing(titles):
    # 출처 제거하기
    new_titles = []

    for title in titles:
        if title.find('-', -1) != -1:
            index = title.find('-', -1)
        else:
            index = title.find('-')
        new_titles.append(title[:index])

    # 한국어만 남기기
    new_titles_2 = []

    for title in new_titles:
        new_title = re.sub("[^가-힣]", " ", title)
        new_title = new_title.strip()
        new_titles_2.append(new_title)
        
    return new_titles_2