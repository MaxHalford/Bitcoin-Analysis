from bs4 import BeautifulSoup
import re
import pandas as pd
import os.path


def existing_path(filepath):
    ''' Teste si un fichier existe 
        filepath: répertoire du fichier (str)

        output: réponse (bool)
    '''
    if os.path.isfile(filepath):
        return True
    else:
        return False


def get_usernames(tweet_type, year):
    print("usernames-{0}-{1}".format(tweet_type, year))
    fname = "../data/tweets/{0}/{1}.html".format(tweet_type, year)
    if existing_path(fname):
        with open(fname, 'r') as fichier:
            html = fichier.read()
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll(
            'span', attrs={"class": "username js-action-profile-name"})
        usernames = [div.get_text() for div in divs]
        return usernames
    else:
        print("{} n'exite pas.".format(fname))
        return


def get_fullnames(tweet_type, year):
    print("fullnames-{0}-{1}".format(tweet_type, year))
    fname = "../data/tweets/{0}/{1}.html".format(tweet_type, year)
    if existing_path(fname):
        with open(fname, 'r') as fichier:
            html = fichier.read()
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll(
            'strong', attrs={"class": "fullname"})
        fullnames = [div.get_text() for div in divs]
        return fullnames
    else:
        print("{} n'exite pas.".format(fname))
        return


def get_tweets(tweet_type, year):
    print("tweets-{0}-{1}".format(tweet_type, year))
    fname = "../data/tweets/{0}/{1}.html".format(tweet_type, year)
    if existing_path(fname):
        with open(fname, 'r') as fichier:
            html = fichier.read()
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll('p', attrs={"class": "TweetTextSize"})
        tweets = [div.get_text() for div in divs]
        return tweets
    else:
        print("{} n'exite pas.".format(fname))
        return


def get_retweets(tweet_type, year):
    print("retweets-{0}-{1}".format(tweet_type, year))
    fname = "../data/tweets/{0}/{1}.html".format(tweet_type, year)
    if existing_path(fname):
        with open(fname, 'r') as fichier:
            html = fichier.read()
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll(
            'span', attrs={"class": "ProfileTweet-action--retweet"})
        RT = [div.find(
            'span', attrs={"class": "ProfileTweet-actionCountForAria"}) for div in divs]
        retweets = [re.sub(r"\D", "", rt.get_text()) for rt in RT]
        return retweets
    else:
        print("{} n'exite pas.".format(fname))
        return


def get_likes(tweet_type, year):
    print("likes-{0}-{1}".format(tweet_type, year))
    fname = "../data/tweets/{0}/{1}.html".format(tweet_type, year)
    if existing_path(fname):
        with open(fname, 'r') as fichier:
            html = fichier.read()
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll(
            'span', attrs={"class": "ProfileTweet-action--favorite"})
        FAV = [div.find(
            'span', attrs={"class": "ProfileTweet-actionCountForAria"}) for div in divs]
        likes = [re.sub(r"\D", "", fav.get_text()) for fav in FAV]
        return likes
    else:
        print("{} n'exite pas.".format(fname))
        return


def get_timestamps(tweet_type, year):
    print("timestamps-{0}-{1}".format(tweet_type, year))
    fname = "../data/tweets/{0}/{1}.html".format(tweet_type, year)
    if existing_path(fname):
        with open(fname, 'r') as fichier:
            html = fichier.read()
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll(
            'span', attrs={"class": "_timestamp"})
        timestamps = [re.sub(r"\D", "", div['data-time-ms']) for div in divs]
        return timestamps
    else:
        print("{} n'exite pas.".format(fname))
        return


def items_equal(items):
    check = all(x == items[0] for x in items)
    return check


def empty_list(items):
    check = all(x == 0 for x in items)
    return check


def compute_df(tweet_type, year, save=False):
    usernames = get_usernames(tweet_type, year)
    fullnames = get_fullnames(tweet_type, year)
    tweets = get_tweets(tweet_type, year)
    retweets = get_retweets(tweet_type, year)
    likes = get_likes(tweet_type, year)
    timestamps = get_timestamps(tweet_type, year)
    array_length = [len(usernames), len(fullnames), len(
        tweets), len(retweets), len(likes), len(timestamps)]

    if not items_equal(array_length):
        return 'Les listes récupérées ne sont pas de la même taille'
    elif empty_list(array_length):
        return 'Les listes sont vides'
    else:
        d = {'username': usernames,
             'fullname': fullnames,
             'tweet': tweets,
             'retweets': retweets,
             'likes': likes,
             'timestamp': timestamps}

        df = pd.DataFrame(d)

        if save:
            df.to_csv(
                '../data/dataframes/{0}_{1}.csv'.format(tweet_type, year))

        return df


def compute_dataframes(tweet_type, annees, save=False):
    dataframes = [compute_df(tweet_type, annee, save=True) for annee in annees]
    df = dataframes[0].append(dataframes[1:])
    df = df.reset_index(drop=True)

    if save:
        df.to_csv(
            '../data/dataframes/{}.csv'.format(tweet_type))

    return df

if __name__ == '__main__':
    print(compute_dataframes('negatifs', [2009, 2011]))