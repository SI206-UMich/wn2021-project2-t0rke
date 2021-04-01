# Your name: Anjana Pisupati
# Your student id:7080 1639
# Your email: pisupati@umich.edu
# List who you worked with on this homework:I worked by myself.

#Hi! I had to do this project on an older laptop because my current laptop is broken so I am super sorry for this extra stuff at the top.
# I just wanted to make sure I had all the correct libraries installed on this laptop so I just tried to follow  steps on Google. 
# The code might take a while to run and there might some weird stuff at the top, but the tests still all pass! :)

import pip
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

install("kora")
install("bs4")
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
from kora.selenium import wd


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of book titles (as printed on the Goodreads website)
    in the format given below. Make sure to strip() any newlines from the book titles.

    ['Book title 1', 'Book title 2'...]
    """
    final_book_list =[]
    html_text = ''
    with open(filename,'r',encoding='utf8') as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text,"html.parser")
    all_book_title = soup.findAll('a',{'class':'bookTitle'})
    for i in all_book_title:
        span = i.find('span',{'itemprop':'name'})
        final_book_list.append(span.text.strip())

    return final_book_list


def get_new_releases():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/genres/fantasy". Parse through the object and return a list of URLs for each
    of the books in the "NEW RELEASES TAGGED 'FANTASY'" section using the following format:

    ['https://www.goodreads.com/book/show/23106013-battle-ground', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to
    your list, and discard the rest.
    """
    final_list = []
    wd.get("https://www.goodreads.com/genres/fantasy")
    html_text = wd.page_source
    soup = BeautifulSoup(html_text,"html.parser")

    fantasy_html = soup.find('div',{'class':'coverBigBox clearFloats bigBox'})
    a_tag = fantasy_html.findAll('a')
    for i in a_tag:
        if i.get('href').strip().find("/book/show/") != -1:
            final_list.append("https://www.goodreads.com"+i.get('href').strip())
    return final_list


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and star-rating.
    This function should return a tuple in the following format:

    ('Some book title', 'the book's author', 'its star rating')

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and star rating.
    """
    final_list = []
    wd.get(book_url)
    html_text = wd.page_source
    soup = BeautifulSoup(html_text,'html.parser')

    title = soup.find('h1',{'id':'bookTitle'}).text.strip()
    author_ = soup.find('div',{'class':'authorName__container'})
    author = author_.find('span').text.strip()
    rating  = soup.find('span',{"itemprop":"ratingValue"}).text.strip()

    return (title,author,float(rating))

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2019"
    page in "best_books.htm". This function should create a BeautifulSoup object from a
    filepath and return a list of (category, book title, URL) tuples.

    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2019, then you should append
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2019")
    to your list of tuples.
    """
    html_text = ''
    with open(filepath,'r',encoding="utf8") as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text,'html.parser')

    final_list=[]
    for i in soup.findAll('div',{'class':'category clearFix'}):
        url_b = i.find('a').get('href').replace('/n','')
        category = i.find('a').find('h4').text.strip()
        book_title = i.find('img',{"class":"category__winnerImage"}).get('alt').strip()
        final_list.append((str(category),str(book_title),str(url_b)))
    return final_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by summarize_best_books()), writes the data to a
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Category", "Book title", and
    "URL", respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

        Category,Book title,URL
    Some category,Book1,url1
    Another category,Book2,url2
    Yet another category,Book3,url3


    This function should not return anything.
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Category','Book title','URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in data:
            writer.writerow({'Category': i[0], 'Book title': i[1],'URL':i[2]})


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    html_text = ''
    with open(filepath,'r',encoding="utf8") as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text,'html.parser')

    paragraph = soup.find("span",{"id":"freeText4791443123668479528"}).text
    text1 = paragraph.strip()
    text2 = text1.split()
    output =[]
    for index,value in enumerate(text2):
      if not value.islower():
        if index <= len(text2) -1:
          if not text2[index+1].islower():
            output.append(value +" "+text2[index+1])
    output3 = []
    for i in output:
      list_en = i.split()
      list_en = [f.replace(",","").replace(".","").replace(" ","").strip() for f in list_en]
      if not len(list_en[0]) <= 3:
        output3.append(" ".join(list_en))
    output2 =[]
    for i in output3:
      try:
        float(i)
      except:
        output2.append(i)
    return output2




class TestCases(unittest.TestCase):

    
    new_release_urls = get_new_releases()

    def test_get_titles_from_search_results(self):
        title_search = get_titles_from_search_results('search_results.htm')
        if len(title_search) == 20:
            pass 
        else:
            pass 
            self.assertTrue(False)
        if type(title_search) != list:
            self.assertTrue(False)
        title_string = "Passed"
        for i in title_search:
            if type(i) != str:
                title_string = "Failed"
                self.assertTrue(False)
        pass 
        if title_search[0] == "Harry Potter and the Deathly Hallows (Harry Potter, #7)":
            pass 
        else:
            pass 
            self.assertTrue(False)
        if title_search[len(title_search) -1] == "Harry Potter: The Prequel (Harry Potter, #0.5)":
            pass 
        else:
            pass
            self.assertTrue(False)
        self.assertTrue(True)




    def test_get_new_releases(self):
        if(type(TestCases.new_release_urls)) == list:
            pass 
        else:
            pass 
            self.assertTrue(False)
        if(len(TestCases.new_release_urls) == 15):
            pass 
        else:
            pass 
            self.assertTrue(False)
        test_url_type = "Passed"
        for i in TestCases.new_release_urls:
            if type(i) != str:
                test_url_type = "Failed"
                self.assertTrue(False)
        pass 
        test_correct_url = "Passed"
        for i in TestCases.new_release_urls:
            if not '/book/show/' in i :
                test_correct_url = "Failed"
                self.assertTrue(False)
        pass 
        self.assertTrue(True)
    def test_get_book_summary(self):
        summaries = []
        for i in TestCases.new_release_urls:
            summaries.append(get_book_summary(i))
        if len(summaries) == 15:
            pass 
        else:
            pass 
            self.assertTrue(False)
        test_type = "Passed"
        for i in summaries:
            if type(i) != tuple:
                test_type ="Failed"
                self.assertTrue(False)
        test_len = "Passed"
        for i in summaries:
            if len(i) != 3:
                test_len ="Failed"
                self.assertTrue(False)
        pass 
        pass 


        second_tuple = summaries[1]
        if type(second_tuple[0]) == str :
            pass 
        else:
            self.assertTrue(False)
        if type(second_tuple[1]) == str:
            pass 
        else:
            self.assertTrue(False)
        if type(second_tuple[2]) == float:
            pass 
        else:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_summarize_best_books(self):
        best_books = summarize_best_books("best_books.htm")
        if len(best_books) == 20:
            pass 
        else:
            pass 
            self.assertTrue(False)
        for i in best_books:
            if len(i) == 3:
                pass 
                pass 
            else:
                self.assertTrue(False)
        first_tuple = best_books[0]
        if first_tuple[0] == "Fiction":
            pass 
        else:
            self.assertTrue(False)
        if first_tuple[1] == "The Testaments (The Handmaid's Tale, #2)":
            pass  
        else:
            self.assertTrue(False)
        if first_tuple[2] ==  'https://www.goodreads.com/choiceawards/best-fiction-books-2019':
            pass
        else:
            self.assertTrue(False)
        last_tuple = best_books[len(best_books) -1]
        if last_tuple[0] == "Picture Books":
            pass
        else:
            self.assertTrue(False)
        if last_tuple[1].strip() == "A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers".strip():
            pass
        else:
            pass 
            self.assertTrue(False)
        if last_tuple[2] ==  'https://www.goodreads.com/choiceawards/best-picture-books-2019':
            pass
        else:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_write_csv(self):
        result = summarize_best_books("best_books.htm")
        write_csv(result,"101.csv")
        header_row =''
        first_row =''
        last_row =''

        with open("101.csv", 'rt',encoding="utf8") as f:
            global lines
            lines = f.readlines()
            if len(lines) == 21:
                pass 
            else:
                pass 
                pass 
                self.assertTrue(False)
            if lines[0].strip() == "Category,Book title,URL":
                pass 
            else:
                pass 
                pass 
                self.assertTrue(False)
            if lines[1].strip() == """Fiction,"The Testaments (The Handmaid's Tale, #2)",https://www.goodreads.com/choiceawards/best-fiction-books-2019""":
                pass 
            else:
                pass 
                pass 
                self.assertTrue(False)
            if lines[-1].strip() == "Picture Books,A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers,https://www.goodreads.com/choiceawards/best-picture-books-2019":
                pass 
            else:
                pass 
                self.assertTrue(False)
        self.assertTrue(True)

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)