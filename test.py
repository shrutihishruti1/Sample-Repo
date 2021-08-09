import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import itertools

url = '''https://www.imdb.com/search/title/?title_type=feature&groups=top_100&sort=user_rating,desc&count=100'''
response = requests.get(url)
movies_soup = BeautifulSoup(response.text, 'html.parser')

#print(movies_soup)

# Get all the <a> tag without a class
movie_tags = movies_soup.find_all('a', attrs={'class': None})
# Filter the a-tags to get just the titles
movie_tags = [tag.attrs['href'] for tag in movie_tags 
              if tag.attrs['href'].startswith('/title') & tag.attrs['href'].endswith('/')]
# Remove duplicate links
movie_tags = list(dict.fromkeys(movie_tags))

# print("In total we have " + str(len(movie_tags)) + " movie titles") # Comment out afterwards
# print("Displaying 10 titles") # Comment out afterwards
# print(movie_tags[:10]) # Comment out afterwards

base_url = "https://www.imdb.com"
# Get movie links with reviews
movie_links = [base_url + tag + 'reviews' for tag in movie_tags]

# print("In total we have " + str(len(movie_links)) + " movie user reviews") # Comment out afterwards
# print("Displaying 10 user reviews links") # Comment out afterwards
# print(movie_links[:10]) # Comment out afterwards

# Create a helper function to get review links
def getReview(soup):
    # Get all the review tags
    user_review_list = soup.find_all('a', attrs={'class':'title'})
    # Get the first review tag
    review_tag = user_review_list[0]
    # Return the none review link
    review_link = "https://www.imdb.com" + review_tag['href']
    return review_link

# Get a list of soup objects. This takes a while
movie_review_soups = [BeautifulSoup(requests.get(link).text, 'html.parser') for link in movie_links]
# Get all 100 movie review links
movie_review_list = [getReview(movie_review_soup) for movie_review_soup in movie_review_soups]

# print("There are a total of " + str(len(movie_review_list)) + " individual movie reviews") # Comment out afterwards
# print("Displaying 10 reviews") # Comment out afterwards
# print(movie_review_list[:10]) # Comment out afterwards

# Create lists for dataframe and csv later
review_texts = []
movie_titles = []

# Loop through the movie reviews
for url in movie_review_list:
    # Get the review page
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    # Find div tags with class text show-more__control, then get its text
    review_tag = soup.find('div', attrs={'class': 'text show-more__control'}).getText()
    # Add the review text in the review list
    review_texts += [review_tag]
    # Find the h1 tag and get the second element i.e. the title
    title_tag = list(soup.find('h1').children)[1].getText()
    # Add the title in the title list
    movie_titles += [title_tag]

    print(review_texts)
    print(movie_titles)
    # Construct a dataframe
df = pd.DataFrame({'movie': movie_titles, 'user_review_permalink': movie_review_list,'user_review': review_texts})
# Put into .csv file
df.to_csv('userReviews.csv', index=False)

