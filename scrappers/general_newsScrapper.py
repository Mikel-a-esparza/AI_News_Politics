import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

import os

from newspaper import Article, Source


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}

list_of_newspapers = ['20Minutos', 'ElMundo', 'ElPais', 'LaVanguardia']
list_of_url = ['https://www.20minutos.es/nacional/', 'https://www.elmundo.es/espana', 'https://elpais.com/espana', 'https://www.lavanguardia.com/politica']


for i,url in enumerate(list_of_url):

  newspaper_name = list_of_newspapers[i]

  # Opens up the connection and grabs the requested webpage.

  request = urllib.request.Request(url, None, headers)

  news_connection = uReq(request)

  html = news_connection.read()
  news_connection.close()

  news_soup = soup(html, "html.parser")

  # Finds the articles on the main page.
  containers = news_soup.find_all("article")

  # Creates a .csv file of the articles.

  if not os.path.isdir("newsPapers/" + newspaper_name):
    os.makedirs("newsPapers/" + newspaper_name)


  # Loops through all the articles on the technology page.

  try:
    for container in containers:
      article_link = str(container.a['href'])
      if newspaper_name == "ElPais":
        article_link = 'https://elpais.com' + article_link
      article = Article(article_link, language = 'es')
      article.download()
      article.parse()

      # Gets the data from the website.
      article_title = article.title

      article_authors = str(article.authors)

      date = article.publish_date

      year, month, day = str(date).split()[0].split("-")

      article_text = article.text.replace("\n"," ")

      article.nlp()
      article_keywords = str(article.keywords)
      artcle_summary = article.summary.replace("\n"," ")


      if not os.path.isdir("newsPapers/" +  newspaper_name + "/" + year + "-" + month + "-" + day):
        os.makedirs("newsPapers/" + newspaper_name + "/" + year + "-" + month + "-" + day)

      file_name = article_title.replace(u'\xa0', u' ').replace("|","").replace('"',"").replace("?","").replace("¿","").replace("'","").replace(":"," ").replace("/","")

      fp = open("newsPapers/" + newspaper_name + "/" + year + "-" + month + "-" + day + "/" + file_name + ".txt","w", encoding="utf-8")
      fp.write("title: " + article_title + "\n")
      fp.write("nlp_summary: " + artcle_summary + "\n")
      fp.write("text: " + article_text + "\n")
      fp.write("nlp_keywords: " + article_keywords + "\n")
      fp.write("link: " + article_link + "\n")
      fp.write("authors: " + article_authors + "\n")

      fp.close()

  except Exception as e:
    print(e)
    print(article_link)