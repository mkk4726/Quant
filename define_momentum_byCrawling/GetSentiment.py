import pandas as pd

def get_sentiment_score(predict_model, vectorizer_model, titles, return_df=False):
    """
    predict_model : 해당 뉴스 제목이 긍정인지 부정인지 판별하는 모델, 
    vectorizer_model : 뉴스 제목을 벡터화시킬 모델,
    titles : 뉴스제목 리스트 -> List,
    return_df : df를 반환할지 여부 -> Bool
    
    """
    tfidf_matrix_titles = vectorizer_model.transform(titles)
    pred = predict_model.predict(tfidf_matrix_titles)
    pred_prob_0 = predict_model.predict_proba(tfidf_matrix_titles)[:, 0]
    
    df = pd.DataFrame()
    df['titles'] = titles
    df['pred'] = pred

    # 애매한 것들 (0일 확률이 0.45~0.55인 것들)은 3으로 처리한다.
    df['prob_0'] = pred_prob_0
    df['is_3'] = df['prob_0'].apply(lambda x: 0.45 < x and x < 0.55)
    for i in range(len(df)):
        if df.iloc[i, 3]:
            df.iloc[i, 1] = 3
            
    n_1 = df['pred'].value_counts().loc[1]
    n_3 = df['pred'].value_counts().loc[3]
    n_0 = df['pred'].value_counts().loc[0]

    # sentiment_score 정의
    sentiment_score = (n_1) / (n_3 + n_0) 
    
    if return_df:
        return sentiment_score, df
    else:
        return sentiment_score