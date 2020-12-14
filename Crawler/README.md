# CS410 MP2---Search Engines

In this 4-part MP, you will get familiar with building and evaluating Search Engines.

## Part 1

### Due: Sept 20, 2020 at 11:59 pm

We will start by building a dataset consisting of the homepages of faculty memebers from different universities' Engineering and Science departments.
To achieve this, you first need to identify the faculty directory listing page where all the faculty members of your chosen department are listed and get the urls for the homepages of all faculty members.
You then need to scrape all the text information, such as the faculty bio, from the faculty homepage.

Specifically, you need to perform the following tasks:

1. Find an Engineering and/or Science department faculty listing page of a university of your choice and fill the [sign up sheet](https://docs.google.com/spreadsheets/d/198HqeztqhCHbCbcLeuOmoynnA3Z68cVxixU5vvMuUaM/edit?usp=sharing). You will need to login with your Illinois email id to access the sign up sheet. While choosing the university you must ensure the following: 
    **a.** The faculty directory page and the faculty home pages are in English. 
    **b.** The selected university department is different from the ones already present on the sign up sheet. If you do run out of options for university departments toward the end, you may choose a non Engineering/Science department from an already selected university **except UIUC**.

2. Scrape the faculty listing page and all the faculty homepages using Python. Finally, you should generate two output .txt files called **bios.txt** and **bio_urls.txt**. 'bio_urls.txt' should contain the urls of all the faculty homepages and have one url per line. 'bios.txt' should contain the text scraped from all the urls in 'bio_urls.txt', and again have one document per line. The two files must have the same order, that is, the first line in 'bios.txt' should correspond to the text extracted from the url in the first line of 'bio_urls.txt'. There should be no empty lines in between (including lines with only spaces).

3. Place all your code in one folder and name it **scraper_code**.  

A sample script for scraping UIUC CS department faculty homepages has been provided to you under the sample folder in the form a jupyter notebook. You can download it and run it on your machine using the [jupyter notebook command](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html). We also provide the two output files generated from the script under the same folder. This should help you get started with developing scrapers for other universities' faculty homepages as well. 

Additionally, you might find the following resources useful:

Python Libraries:
- [Beautiful Soup] (https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Useful for parsing HTML extracted from websites.
- [urllib.request](https://docs.python.org/3/library/urllib.request.html): Useful for downloading content from urls
- [Selenium](https://seleniumhq.github.io/selenium/docs/api/py/): Useful when Requests is unable to download content rendered by Javascript
    
Some Tutorials:
- https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
- https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f. 
   
Finally, the browser developer tools are highly useful to inspect and identify the HTML elements where the required information resides in the webpage. 


### Grading

We will use the following rubric for grading. Points are awarded in a sequential manner (e.g., you get no points for c. if b. is not satisfied) and are additive. Thus, there are 4 possible points: 0, 0.1, 0.3 and 1, or equivalently 0, 10, 30, and 100 points on Coursera. 

a. Submitted all the files. There should be at least six URLs in "bio_urls.txt". Also, please remove non-ascii characters. -- 0.1 points 

		Your repo should have the following files:

			├── README.md
			├── bio_urls.txt
			├── bios.txt
			├── livedatalab_config.json
			├── sample
			│   ├── bio_urls.txt
			│   ├── bios.txt
			│   └── scraper.ipynb
			└── scraper_code
			    └── scraper.ipynb  OR scraper.py


b. "bios.txt" and "bio_urls.txt" are properly formatted as mentioned in 2. above -- +0.2 points  

c. Submitted URLs in "bio_urls.txt" don't overlap with other students' submissions including previous years' submissions (max 5 overlapping URLs allowed). -- +0.7 points
