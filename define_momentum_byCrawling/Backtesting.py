from GetNews import *
from GetSentiment import *
from GetStocks import *
import pickle
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
from konlpy.tag import *

okt = Okt()
from tqdm import tqdm

path = 'C:/Users/Hi/Jupyter/Project/define_momentum_byCrawling/pickle'


def tw_tokenizer(text):
    tokens_ko = okt.morphs(text)
    return tokens_ko


with open(path + '/lr_clf.pickle', "rb") as fr:
    lr_clf = pickle.load(fr)

with open(path + '/tfidf_vec.pickle', "rb") as fr:
    tfidf_vec = pickle.load(fr)

with open(path + '/total_df.pickle', "rb") as fr:
    total_df = pickle.load(fr)

# 주말 제거
tmp = total_df.fillna(-1)
tmp['check'] = tmp.sum(axis=1)
weekend_index = tmp[tmp['check'] == -943].index

total_df = total_df.drop(weekend_index)

return_df = total_df.pct_change()
return_df = return_df.resample('M').last()
return_df = return_df.iloc[:, :30]  # 시가총액 기준 상위 30개에 대해 진행
return_df = return_df.iloc[215:]  # 5년정도 테스트

returns = [] # return log용 리스트
invest_stock_list = [] # 투자한 종목들 log 용 리스트
stock_list = [] # 투자할 종목들

for index, row in return_df.iterrows():
    print(index, end=' ')

    # 전 달에 계산한걸로 수익률 계산
    tmp = row.loc[stock_list].mean()
    print(tmp, end=' ')

    returns.append(tmp)
    invest_stock_list.append(stock_list)


    # 투자할 대상 선정
    start = index.strftime('%Y-%m-01')
    end = index.strftime('%Y-%m-%d')

    candidate_stocks = row.dropna().index.tolist()

    result = find_stocks(start=start, end=end, search_list=candidate_stocks,
                         predict_model=lr_clf, vectorizer_model=tfidf_vec, top_n=10)
    stock_list = [x[0] for x in result if x[1] > 1]  # 감성점수가 0.5가 넘을 때만 투자한다.

    print(stock_list)

return_df['returns'] = returns
return_df['invest_stocks'] = invest_stock_list

with open(path + '/result_df_2.pickle', "wb") as fw:
    pickle.dump(return_df, fw)