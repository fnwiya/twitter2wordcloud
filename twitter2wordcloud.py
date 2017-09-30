#!/usr/bin/env python2
# coding:utf-8
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import tweepy
import sys
import MeCab


# 認証
def certify(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def drop_share_title(text):
    return text.split("/")[0]

# 前処理
def filter(text):
    # "RT @user:"を削除
    if "RT " in text:
        text = text.split(":", 1)[1]
    # "@user"を削除
    if "@" in text and " " in text:
        text = text.split(" ", text.count("@"))[-1]
    # "#tag"を削除
    if "#" in text:
        text = text.split("#", 1)[0]
    # "URL"を削除
    if "http" in text:
        text = text.split("http", 1)[0]
    return drop_share_title(text)


# 形態素解析
def morphologicalAnalysis(mecab, tweet, word2freq):
    text = filter(tweet.text.encode("utf-8"))
    node = mecab.parseToNode(text)
    while node:
        word_type = node.feature.split(",")[0]
        if word_type in ["形容詞", "動詞", "名詞", "副詞"]:
            word = node.surface
            word2freq[word] += 1
        node = node.next
    return word2freq


# 最新の投稿を取得
def getTweets(api, name):
    # 形態素解析の準備
    mecab = MeCab.Tagger()
    # キーワードの出現頻度を保持する辞書
    from collections import defaultdict
    word2freq = defaultdict(int)
    user_timeline = api.user_timeline(count=30, page=1, screen_name=name)
    for tweet in user_timeline:
        # 形態素解析
        word2freq = morphologicalAnalysis(mecab, tweet, word2freq)
    return word2freq


def create_wordcloud(text):
    # ここはPCの環境による。日本語を解析する場合設定必須。
    # for OSX
    # fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
    # for Ubuntu16.10
    fpath = "/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf"

    # ストップワードの設定
    # stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと',\
    #                u'これ', u'さん', u'して', u'くれる', u'やる', u'くださる',\
    #                u'そう', u'せる', u'した',  u'思う', u'それ', u'ここ', u'ちゃん',\
    #                u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た',\
    #                u'し', u'で', u'ない', u'も', u'な', u'い', u'か', u'ので',\
    #                u'よう', u'']
    stop_words = [ 'てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと',\
                   'これ', 'さん', 'して', 'くれる', 'やる', 'くださる',\
                   'そう', 'せる', 'した',  '思う', 'それ', 'ここ', 'ちゃん',\
                   'くん', '', 'て','に','を','は','の', 'が', 'と', 'た',\
                   'し', 'で', 'ない', 'も', 'な', 'い', 'か', 'ので',\
                   'よう', '']

    wordcloud = WordCloud(background_color="white", width=900, height=500,\
                          font_path=fpath, stopwords=set(stop_words)).generate(text)

    plt.figure(figsize=(15, 12))
    plt.imshow(wordcloud)
    wordcloud.to_file("twitter.png")
    plt.axis("off")
    plt.show()


# メイン
if __name__ == "__main__":
    # 解析したいユーザ名
    name = "@" + sys.argv[1]
    # 認証
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = ""
    ACCESS_SECRET = ""
    api = certify(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    word2freq = getTweets(api, name)
    create_wordcloud(" ".join(word2freq).decode('utf-8'))
