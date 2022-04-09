import tweepy
import pandas as pd
import numpy as np
# TwetAnalyzer

from openpyxl.workbook import Workbook

from textblob import TextBlob   ##za dobre/slabe tweete
import re   ## regularni izrazi, da dobimo ven besede
import matplotlib.pyplot as plt


api_key = "YoLSoQOTOeZk45dpIxxyn8HUN"
api_secrets = "a7g4sCZeUmo6bXEyJpoOJiEIRyYWhuBl81UrJaLSmMkKhxrC6K"
access_token = "1379169625011859459-eko5LNMGyH32NyHnB3QpnyJxc6Mdka"
access_secret = "Ybazl2RrrboyCKzNjdgmbYqZKHAoQEBF9ssaTIRWjEBeL"
 
# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit = True)


#tweepy.Cursor()  ##da ni limita 200


## funkciji ki nam pomagata povedati ali je tweet dober ali slab
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
        
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


# ## po različnih userjih
# users = ['elonmusk', 'TheNotoriousMMA', '3gerardpique', 'VancityReynolds', 'FCBarcelona', 'premierleague', 'joerogan']
# limit = 10
# columns = ['Time', 'User', 'Tweet', 'Followers', 'Retweets', 'Likes']
# data = []
# 
# ## naredimo dataframe glede na userje, velikosti limit, s stolpci columns
# for user in users:
#     tweets = api.user_timeline(screen_name = user, count = limit, tweet_mode = 'extended')
#     ### tweets = tweepy.Cursor(api.user_timeline, screen_name = user, count = 200, tweet_mode = 'extended').items(limit)
#     for tweet in tweets:
#         data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text, tweet.user.followers_count, tweet.retweet_count, tweet.favorite_count])
# 
# pd.set_option('display.max_rows', None)  ## da pokaze vse vrstice
# pd.set_option('display.max_columns', None)   ## da pokaze vse stolpce
# df = pd.DataFrame(data, columns = columns)
# # print(df)

## ce iscemo tweete po neki besedi
keywords = 'Putin'
limit = 200
columns = ['Time', 'User', 'Tweet', 'Retweets']
data = []


tweets = tweepy.Cursor(api.search_tweets, q = keywords, count = 200, tweet_mode = 'extended').items(limit)
for tweet in tweets:
    if tweet.lang == 'en':   ## ce tweet ni v anglescini ga izlocimo
        data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text, tweet.retweet_count])
    
pd.set_option('display.max_rows', None)  ## da pokaze vse vrstice
pd.set_option('display.max_columns', None)   ## da pokaze vse stolpce
df = pd.DataFrame(data, columns = columns)
# print(df)

## pogledamo kaksni so bili tweeti (pozitivni/nevtralni/negativni)
sentiments = []
for sentiment in df['Tweet']:
    sentiments.append(analyze_sentiment(sentiment))
    
df['Sentiment'] = sentiments


## pogledamo koliko znakov imajo tweeti
lengths = []
for text in df['Tweet']:
    lengths.append(len(text))

df['Length'] = lengths

#pd.set_option('display.max_columns', None)

#df.to_csv('poskus.csv')
#print(df)



## Poglejmo povprečno dolžino
print(f"Average length: {round(np.mean(df['Length']), 1)}")


## Največ retweetov
print(f"Most reetwets: {np.max(df['Retweets'])}")



#Time Series
time_likes = pd.Series(data=df['Retweets'].values, index=df['User'])
time_likes.plot(figsize=(16, 4), color='r')
# plt.show()
    
#time_favs = pd.Series(data=df['likes'].values, index=df['date'])
#time_favs.plot(figsize=(16, 4), color='r')
#plt.show()

#time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
#time_retweets.plot(figsize=(16, 4), color='r')
#plt.show()

# Layered Time Series:
#time_likes = pd.Series(data=df['likes'].values, index=df['date'])
#time_likes.plot(figsize=(16, 4), label="likes", legend=True)

#time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
#time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
#plt.show()



pos_tweets = []
neg_tweets = []
neu_tweets = []

#picking positive tweets from tweets
for i in range(len(df['Sentiment'])):
    if df['Sentiment'][i] == 1:
        pos_tweets.append(df['Tweet'][i])
# percentage of positive tweets
positive = round(100*len(pos_tweets)/len(df['Sentiment']), 1)  #procent pozitivnih tweetov
print("Positive tweets percentage: {} %".format(positive))
# picking negative tweets from tweets
for i in range(len(df['Sentiment'])):
    if df['Sentiment'][i] == -1:
        neg_tweets.append(df['Tweet'][i])
# percentage of negative tweets
negative = round(100*len(neg_tweets)/len(df['Sentiment']), 1)   ## procent negativnih tweetov
print("Negative tweets percentage: {} %".format(negative))
# percentage of neutral tweets
neutral = round(100*(len(df['Sentiment']) - (len(neg_tweets)+len(pos_tweets)))/len(df['Sentiment']), 1)  ##procent nevtralnih
print("Neutral tweets percentage: {} %".format(neutral))
#   
## printing first 10 positive tweets
# print("\n\nPositive tweets:")
# for tweet in pos_tweets[:10]:
#     print(tweet)
    
    
#Creating PieCart
labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['green', 'blue','red']
#patches, texts =
#colors=colors
plt.pie(sizes, labels = labels, colors = colors)  ## lahko dodamo explode = [0.2, 0, 0, 0] da bo en odmaknjen, isto lahko startangle = 90, da zacne zgoraj
#plt.style.use('default')
#plt.legend(labels) ##nekaj ni prav
plt.title('Sentiment Analysis')
#plt.axis('equal')
plt.show()












# ## funkciji ki nam pomagata povedati ali je tweet dober ali slab
# def clean_tweet(tweet):
#     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
# 
# def analyze_sentiment(tweet):
#     analysis = TextBlob(clean_tweet(tweet))
#         
#     if analysis.sentiment.polarity > 0:
#         return 1
#     elif analysis.sentiment.polarity == 0:
#         return 0
#     else:
#         return -1
    
    
## ce iscemo tweete po neki besedi
    
# keywords = 'Putin'
# limit = 50
# columns = ['User', 'Tweet']
# data = []
# 
# 
# tweets = api.search_tweets(q = keywords, count = limit, tweet_mode = 'extended')
# for tweet in tweets:
#     data.append([tweet.user.screen_name, tweet.full_text])
# 
# df = pd.DataFrame(data, columns = columns)
# # print(df)
# 
# 
# ## koda nam pove ali je tweet pozitiven ali negativen
# tweet_analyzer = TweetAnalyzer()
# data1 = []
# for a in df['Tweet']:
#     data1.append(analyze_sentiment(a))
#     
# sent = pd.DataFrame(data1, columns = ['Sentiment'])
# print(df.append(sent).head(50))


#print(df['Tweet'])

# tweet_analyzer = TweetAnalyzer()

# df = tweet_analyzer.df
# df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])







# columns = ['Time', 'Tweet', 'User']
# data = []
# for tweet in public_tweets:
#     data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
# 
# df = pd.DataFrame(data, columns = columns)


# user = 'elonmusk'
# limit = 100

# tweets = api.user_timeline(id='elonmusk', count=200)
# tweets_extended = api.user_timeline(id='elonmusk', tweet_mode='extended', count=200)
#  
# # Print number of tweets
# print(len(tweets))

# tweets = api.user_timeline(screen_name = user, count = limit, tweet_mode = 'extended')
# 
# columns = ['User', 'Tweet']
# data = []
# 
# for tweet in tweets:
#     data.append([tweet.user.screen_name, tweet.full_text])
#     
# df = pd.DataFrame(data, columns = columns)
# print(df)


# columns = ['Time', 'User', 'Tweet']
# data = []
# for tweet in public_tweets:
#     data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
# 
# df = pd.DataFrame(data, columns = columns)
# 
# df.to_csv('tweets.csv')

# ### Tweets
#  
# tweets = api.user_timeline(id='Aljaz32412310', count=10)
# tweets_extended = api.user_timeline(id='Aljaz32412310', tweet_mode='extended', count=10)
#  
# # Print number of tweets
# print(tweets)
# #200
# 
# to_extract = [
#     'id',
#     'created_at',
#     'text',
#     'full_text',
# #     'retweeted',
# #     'favorited',
# #     'is_quote_status',
# #     'retweet_count',
# #     'favorite_count',
# #     'lang',
# #     'in_reply_to_status_id',
# #     'in_reply_to_user_id'
#     ]
#  
# tweet_entities = [
#     ('hashtags','text'),
#     ('user_mentions','screen_name'),
#     ('urls','expanded_url')
# ]
# tweets_data = []
#  
# for tweet in tweets_extended:
#     tweet = tweet._json
#     tweet_data = {}
#     for e in to_extract:
#         try:
#             tweet_data[e]=tweet[e]
#         except:
#             continue
#     for entity in tweet_entities:
#         entity_list = []
#         for t in tweet['entities'][entity[0]]:
#             entity_list.append(t[entity[1]])
#         tweet_data[entity[0]] = entity_list
#  
#     tweets_data.append(tweet_data)
#     # Get Tweet data
# df = pd.DataFrame(tweets_data)

# user = api.get_user('Aljaz32412310')
# user._json
# print(f"user.name: {user.name}")
# print(f"user.screen_name: {user.screen_name}")
# print(f"user.location: {user.location}")
# print(f"user.description: {user.description}")
# print(f"user.followers_count: {user.followers_count}")
# print(f"user.listed_count: {user.listed_count}")
# print(f"user.statuses_count: {user.statuses_count}")
# 
# print('Latest Followers:')
# for follower in user.followers():
#     print('Name: ' + str(follower.name))
#     print('Username: ' + str(follower.screen_name))
# 
# user = api.get_user('elonmusk')
# user._json
# print(f"user.name: {user.name}")
# print(f"user.screen_name: {user.screen_name}")
# print(f"user.location: {user.location}")
# print(f"user.description: {user.description}")
# print(f"user.followers_count: {user.followers_count}")
# print(f"user.listed_count: {user.listed_count}")
# print(f"user.statuses_count: {user.statuses_count}")

