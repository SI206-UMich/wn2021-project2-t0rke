from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

# Suneeth Torke and Brandon Huggard


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(filename,'r',encoding="utf8") as f:
        soup = BeautifulSoup(str(f.read()),'html.parser')

    books = [i.text.strip() for i in soup.find_all('a', class_= 'bookTitle')]
    authors = [i.text.strip() for i in soup.find_all('a', class_= 'authorName')]

    return [(books[i], authors[i]) for i in range(0, len(books))]


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    r = requests.get('https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc')
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('a', class_='bookTitle')
    return ['https://www.goodreads.com' + str(tag.get('href', None)) for tag in tags[:10]]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1').text.strip()
    author = soup.find('a', class_='authorName').text.strip()
    count = int(soup.find('span', itemprop='numberOfPages').text.split()[0])

    return (title, author, count)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """

    with open(filepath,'r',encoding="utf8") as f:
        soup = BeautifulSoup(str(f.read()),'html.parser')
    
    final = []
    for i in soup.findAll('div', class_='category clearFix'):
        b = i.find('a').get('href').replace('/n','')
        category = i.find('a').find('h4').text.strip()
        title = i.find('img', class_="category__winnerImage").get('alt').strip()
        final.append((str(category),str(title),str(b)))
    
    return final


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Book title','Author Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for datum in data:
            writer.writerow({'Book title': datum[0], 'Author Name': datum[1]})


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        local = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(local), 20)

        # check that the variable you saved after calling the function is a list
        self.assertTrue(isinstance(local, list))

        # check that each item in the list is a tuple
        self.assertTrue(all(isinstance(val, tuple) for val in local))

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(local[0][1], "J.K. Rowling")
        
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(local[0][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        lst = get_search_links()
        self.assertTrue(isinstance(lst, list))
    
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(lst), 10)

        # check that each URL in the TestCases.search_urls is a string
        self.assertTrue(all(isinstance(val, str) for val in lst))

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        self.assertTrue(all('https://www.goodreads.com/book/show/' in string for string in lst))


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in get_search_links():
            summaries.append(get_book_summary(url))

        self.assertTrue(isinstance(summaries, list))
        
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        # check that each item in the list is a tuple
        self.assertTrue(all(isinstance(val, tuple) for val in summaries))

        # check that each tuple has 3 elements
        self.assertTrue(all(len(val)==3 for val in summaries))

        # check that the first two elements in the tuple are string
        self.assertTrue(all(isinstance(val[0], str) and isinstance(val[1], str) for val in summaries))

        # check that the third element in the tuple, i.e. pages is an int
        self.assertTrue(all(isinstance(val[2], int) for val in summaries)) # failing for some reason lol

        # check that the first book in the search has 337 pages
        self.assertTrue(summaries[0][2]==337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        var = summarize_best_books('best_books_2020.htm')

        # check that we have the right number of best books (20)
        self.assertEqual(len(var), 20)

        # assert each item in the list of best books is a tuple
        self.assertTrue(all(isinstance(item, tuple) for item in var))

        # check that each tuple has a length of 3
        self.assertTrue(all(len(item)==3 for item in var))

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertTrue(var[0][0] == 'Fiction' and var[0][1] == 'The Midnight Library' and var[0][2] == 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertTrue(var[-1][0] == 'Picture Books' and var[-1][1] == 'Antiracist Baby' and var[-1][2] == 'https://www.goodreads.com/choiceawards/best-picture-books-2020')


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        result = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(result,'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'rt',encoding="utf8") as f:
            csv_lines = (f.readlines())

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0].strip(),'Book title,Author Name')

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1].strip(), '"Harry Potter and the Deathly Hallows (Harry Potter, #7)",J.K. Rowling')

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1].strip(),'"Harry Potter: The Prequel (Harry Potter, #0.5)",Julian Harrison')


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



