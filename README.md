# twitter2wordcloud

![image](sample.png "sample")

## About
make word-cloud-image from one's twitter in Japanese



## Setup
1. Install some library(matplotlib.pyplot, wordcloud, tweepy)
```shell
# word_cloud
git clone https://github.com/amueller/word_cloud
cd word_cloud
sudo python setup.py install
# this repo
git clone https://github.com/fnwiya/twitter2wordcloud
cd twitter2wordcloud
pip instal -r pip.txt
```
2. Get your twitter keys from [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)
3. Set keys and fonts
4. At  console
```shell
python witter2wordcloud.py ACCOUNT_NAME
```
