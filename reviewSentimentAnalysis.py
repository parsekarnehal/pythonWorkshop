import webbrowser
import csv
from requests import request
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def scoreAnalyser(sentence):
    score = analyser.polarity_scores(sentence)
    return score['compound']


def fetch_reviews(soup, url):
    file = csv.writer(open(movieName+".csv", 'w'))
    file.writerow(['Author', 'Review', 'score', 'starRating', 'star'])
    pagination = soup.find('span', {'class': 'pageInfo'})
    noOfReviewPage = int(pagination.text[10:])+1
    stars = []
    for x in range(1, noOfReviewPage):
        print("processing reviews on review page "+str(x))
        newUrl = url+"?page="+str(x)
        newPage = request('GET', newUrl)
        newSoup = BeautifulSoup(newPage.text, 'html.parser')
        for review in newSoup.find_all("div", {"class": "review_table_row"}):
            for reviewText in review.find_all("div", {"class": "the_review"}):
                theReview = reviewText.text
            score = scoreAnalyser(theReview)
            star = rating(score)
            stars.append(star)
            for author in review.find_all("a", {"class": "articleLink"}):
                theAuthor = author.text
            file.writerow([theAuthor, theReview, score, star])
    print("check "+movieName+".csv file")
    num = len(stars)
    starSum = sum(stars)
    print("Overall rating is", starSum/num)


def rating(score):
    if(score > -1 and score < -0.5):
        return 1
    elif(score > -0.5 and score <= 0):
        return 2
    elif(score > 0 and score < 0.5):
        return 3
    elif(score > 0.5 and score < 1):
        return 4


def webpage_url(url):
    page = request('GET', url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        fetch_reviews(soup, url)
    else:
        print("Check your movie name")


movieName = input("Please Enter the Movie Name :").replace(" ", "_")
url = "https://www.rottentomatoes.com/m/"+movieName+"/reviews"

webpage_url(url)
