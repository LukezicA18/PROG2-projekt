import tweepy
import pandas as pd
import numpy as np
import re
import string  # to get all letters

from openpyxl.workbook import Workbook
from textblob import TextBlob     ## for positive/negative tweets
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


## Twitter keys
api_key = "YoLSoQOTOeZk45dpIxxyn8HUN"
api_secrets = "a7g4sCZeUmo6bXEyJpoOJiEIRyYWhuBl81UrJaLSmMkKhxrC6K"
access_token = "1379169625011859459-eko5LNMGyH32NyHnB3QpnyJxc6Mdka"
access_secret = "Ybazl2RrrboyCKzNjdgmbYqZKHAoQEBF9ssaTIRWjEBeL"
 

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit = True)



## functions that we will need

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(tweet):
    '''To see if the tweet is positive, negative or neutral.'''
    analysis = TextBlob(clean_tweet(tweet))
        
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def polarity(tweet):
    '''To get polarity of the tweet.'''
    analysis = TextBlob(clean_tweet(tweet))
    return round(analysis.sentiment.polarity, 3)

def subjectivity(tweet):
    '''To get polarity of the tweet.'''
    analysis = TextBlob(clean_tweet(tweet))
    return round(analysis.sentiment.subjectivity, 3)



## Tweets that contain a specific word/hashtag
keyword = input('Tweets with wich word/hashtag do you want to analyze? ')
limit = int(input('How many tweets do you want to analyze? ')) 
columns = ['Time', 'User', 'Tweet', 'Retweets']
data = []

tweets = tweepy.Cursor(api.search_tweets, q = keyword, count = 200, tweet_mode = 'extended').items(limit)
# Cursor: that we can see more tweets
for tweet in tweets:
    if tweet.lang == 'en':   ## if tweet is not in english, delete it
        data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text, tweet.retweet_count])
    
pd.set_option('display.max_rows', None)  ## that wee can see all rows
pd.set_option('display.max_columns', None)   ## that we can se all columns
df = pd.DataFrame(data, columns = columns)
# print(df)

## to see if tweet is positivei/neutral/negative
sentiments = []
for sentiment in df['Tweet']:
    sentiments.append(analyze_sentiment(sentiment))
    
df['Sentiment'] = sentiments


## polarity
polarities = []
for text in df['Tweet']:
    polarities.append(polarity(text))
    
df['Polarity'] = polarities


## subjectivity
subjectivities = []
for text in df['Tweet']:
    subjectivities.append(subjectivity(text))
    
df['Subjectivity'] = subjectivities



## number of characters of tweets
lengths = []
for text in df['Tweet']:
    lengths.append(len(text))

df['Length'] = lengths

#pd.set_option('display.max_columns', None)
#df.to_csv('poskus.csv')
print(df)



def pos_neg_neu(number):
    '''Tells if the number is positive, negative or neutral(0).'''
    if number > 0:
        return 'positive'
    elif number < 0:
        return 'negative'
    else:
        return 'neutral'

## Average polarity of tweets
print(f"\nAverage polarity: {round(np.mean(df['Polarity']), 3)} ({pos_neg_neu(np.mean(df['Polarity']))})")

## Average subjectivity of tweets
print(f"Average subjectivity: {round(np.mean(df['Subjectivity']), 3)}")


print(f"\nMaximal polarity: {np.max(df['Polarity'])}")
print(f"Maximal subjectivity: {np.max(df['Subjectivity'])}")
print(f"Minimal polarity: {np.min(df['Polarity'])}")
print(f"Minimal subjectivity: {np.min(df['Subjectivity'])}")



## The most positive and the most negative tweet

print('\n')
print('The most positive tweet (one of): ')
for i in range(len(df['Polarity'])):
    if df['Polarity'][i] == np.max(df['Polarity']):
        print(df['Tweet'][i])
        print('\n')
        break     # if more tweets have the same polarity we print just one

print('The most negative tweet (one of): ')
for i in range(len(df['Polarity'])):
    if df['Polarity'][i] == np.min(df['Polarity']):
        print(df['Tweet'][i])
        print('\n')
        break


print('The most subjective tweet (one of): ')
for i in range(len(df['Subjectivity'])):
    if df['Subjectivity'][i] == np.max(df['Subjectivity']):
        print(df['Tweet'][i])
        print('\n')
        break     # if more tweets have the same subjectivity we print just one

print('The most objective tweet (one of): ')
for i in range(len(df['Subjectivity'])):
    if df['Subjectivity'][i] == np.min(df['Subjectivity']):
        print(df['Tweet'][i])
        print('\n')
        break
    
    

pos_tweets = []
neg_tweets = []
neu_tweets = []

#picking positive tweets from tweets
for i in range(len(df['Sentiment'])):
    if df['Sentiment'][i] == 'positive':
        pos_tweets.append(df['Tweet'][i])
# percentage of positive tweets
positive = round(100 * len(pos_tweets) / len(df['Sentiment']), 1)  #percentage of positive tweets
print("Positive tweets percentage: {} %".format(positive))

# picking negative tweets from tweets
for i in range(len(df['Sentiment'])):
    if df['Sentiment'][i] == 'negative':
        neg_tweets.append(df['Tweet'][i])
# percentage of negative tweets
negative = round(100 * len(neg_tweets) / len(df['Sentiment']), 1)   #percentage of negative tweets
print("Negative tweets percentage: {} %".format(negative))
# picking neutral tweets from tweets
for i in range(len(df['Sentiment'])):
    if df['Sentiment'][i] == 'neutral':
        neu_tweets.append(df['Tweet'][i])
# percentage of neutral tweets
#neutral = round(100 * (len(df['Sentiment']) - (len(neg_tweets)+len(pos_tweets)))/len(df['Sentiment']), 1) 
neutral = round(100 * len(neu_tweets) / len(df['Sentiment']), 1)   #percentage of neutral tweets
print("Neutral tweets percentage: {} %".format(neutral))

# ## printing first 5 positive tweets
# print("\nPositive tweets:")
# for tweet in pos_tweets[:5]:
#     print(tweet)
    

##Let's see if there is a connection between polarity and subjectivity
# We can see that if subjectivity is big, polarity is also big (mostly)
x = np.array(df['Subjectivity'])
y = np.array(abs(df['Polarity']))  ##abs vrednost zato da se lepše vidi ali so bolj nevtralni tweeti tudi bolj subjektivni

x0, y0 = np.polyfit(x, y, 1) #find the line that fits best
plt.scatter(x, y)  #draw a plot with points
plt.plot(x, x0 * x + y0)  #add line that fits best to the plot

plt.xlabel("Subjectivity")
plt.ylabel("Polarity")
plt.title('Connection between subjectivity and polarity(absolute value)')
plt.show()



# Histogram
array_podatkov = np.array([df['Polarity'][i] for i in range(len(df['Polarity']))])
plt.hist(array_podatkov)
plt.xlabel("Sentiment")
plt.ylabel("Number of tweets")
plt.title(f"Sentiment Analysis")
plt.xticks(np.arange(-1, 1, 0.25))
plt.xlim([-1, 1])
plt.show()



#Creating PieCart
marks = ['Positive (' + str(len(pos_tweets)) + ', ' + str(positive) + '%)' , 'Neutral (' + str(len(neu_tweets)) + ', ' + str(neutral) + '%)','Negative (' + str(len(neg_tweets)) + ', ' + str(negative) + '%)']
sizes = [positive, neutral, negative]
colors = ['green', 'orange', 'red']
plt.pie(sizes, labels = marks, colors = colors)  ## lahko dodamo explode = [0.2, 0, 0, 0] da bo en odmaknjen, isto lahko startangle = 90, da zacne zgoraj
plt.title('Sentiment Analysis')
plt.show()



## Word Cloud
text = " ".join(tweet for tweet in df['Tweet'])
text = clean_tweet(text)

letters = list(string.ascii_lowercase)

stop_words = ['RT', 'https', 'co', 're', 've']  + list(STOPWORDS) + letters
wordcloud = WordCloud(stopwords = stop_words, background_color="white").generate(text)  #stopwords=stop_words da se znebi kaksnih besed
plt.imshow(wordcloud)
plt.axis("off")    ## ne pokaže vrednosti (x, y os)
plt.show()





