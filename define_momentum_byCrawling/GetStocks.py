from GetNews import *
from GetSentiment import *
import pickle
from konlpy.tag import *
okt = Okt()
import pandas as pd
from GetNews import *
import warnings
warnings.filterwarnings('ignore')


# 상위 n개의 stock을 골라주는 함수.
def find_stocks(start, end, search_list, predict_model ,vectorizer_model, top_n=10):
    """
    start : 조회할 기간 중 시작 날짜 -> Str (ex:2022-06-01),
    end : 조회할 기간 중 끝 날짜 -> Str (ex:2022-12-01),
    top_n : 조회할 상위 n 개 -> Int,
    search_list : 조회할 종목 이름 -> List,
    return : 이름과 감성점수가 키, 벨류로 구성된 dict로, 구성된 리스트 -> List
    
    """
    sentiment_score_dict= {}

    for search_name in search_list:
        try:
            titles = get_titles_by_ssl(start=start, end=end, search_name=search_name)
            sentiment_score = get_sentiment_score(predict_model=predict_model, vectorizer_model=vectorizer_model, titles=titles, return_df=False)
        except:
            sentiment_score = 0

        sentiment_score_dict[search_name] = sentiment_score
        
    sorted_dict_list = sorted(sentiment_score_dict.items(), key = lambda item: item[1], reverse = True)
    sorted_dict_list = sorted_dict_list[:top_n]
         
    return sorted_dict_list

