# ExpertSearch - Extracting relevant information

<p>This is the final project for the UIUC Text Information Systems course. For a visual walkthrough you can use the following links:

<p>You can find the video about how to instal and run: https://mediaspace.illinois.edu/media/1_sktdzqnu <br>
You can find the video about how the code works: https://mediaspace.illinois.edu/media/1_ht2q1bdw <br>
To view presentation go to: https://1drv.ms/u/s!AsAuk2iSocrzkKROEBv6Q6XLC0_Rbw?e=8fbitD </p>

# Overview

<p>The puropose of this project is to be able to crawl through faculty pages and gather info on professors that gets stored in a structured data format. This structured that would have the fields that the Expert Search system currently has, like email, name and faculty, but additionally I'm trying to gather top terms that can be used to give a better idea of the bio's expertise.</p>

# Implementation

<p>To gather the top terms I used the nltk library to tokenize the professor's bio. Then I calculate the maximum frequency and normalize the counts of all the terms using this figure. After giltering for stopwords and single characters, I order by frequency and take the first five elements.</p>

      bio = visible_text.strip()

      stopwords = nltk.corpus.stopwords.words('english')
      word_frequencies = {}
      for word in nltk.word_tokenize(bio):
          if word not in stopwords:
              if word not in word_frequencies.keys():
                  word_frequencies[word] = 1
              else:
                  word_frequencies[word] += 1
      max_frequency = max(word_frequencies.values())
      for word in word_frequencies.keys():
          word_frequencies[word] = (word_frequencies[word] / max_frequency)
      word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
      top_terms = list(k[0] for k in word_frequencies if len(k[0]) > 1)[:5]
     
<p>To generate the json, I crawled through faculty pages from MP2.1's sheet looking for hyperlinks. If the hyperlink has content that resembles a name and a valid href it starts the mining. It asumes the name is nearby. It browses to the url, gathers all non-html text and does a little format as the bio. It looks for some types of tags and looks top see if they match an email regex, or departments after tokenizing and filtering for small sentences that include at least one word related to the description of a department. After that it collects everything in a json (for this code look at Crawler/sample/main.py line 113)</p>

# Limitations

<p>The professor gathering algorithm is a hit and miss, because it has many false positives, like Student Info, Academic Resources, etc. I didn't compare it against a database of common names (and I guess someone could be named Academic Resources). Maybe main failure was connecting it with the Expert Search App, as it depends of some certain valid formats that the corpus that gets fed to MeTApy. I couldn't make it work of Json, or strip MeTApy entirely an replce the ranking code with a different library, like nltk.</p>
