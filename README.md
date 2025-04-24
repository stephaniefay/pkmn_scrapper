### pkmn_scrapper

> [!CAUTION]
> Disclaimer: This repository is in no way, shape or form an example (or demo) on how to do a good crawler. I'm actually not sure of what I'm doing, but here we are

This project was created only to keep a history of changes done to any of the files, as I'm trying to learn how to properly do a crawling bot (before it can be deployed eventually)


# scrapper

The purpose of this scrapper is to look up and fetch information from some (very) specific pages that will be used in a future API (hopefully)

# spiders
There are (currently) three spiders in this project

## index_spider
The first spider to be executed, responsible for fetching all information for the "index", if we can call it that. In a more clear explanation; it will fetch all current editions (and its respective links) on a brazillian page of Pokémon cards and export the information in a .csv file (inside the export folder).

**run command**

` scrapy crawl index_spider`

## edition_spider
Although it has a "confusing" name, this spider job is to fetch all cards from each collection, putting all information in a .csv file (inside the export folder).

**run command**

` scrapy crawl edition_spider`

## download_images_spider
The only responsibility of this spider is to download images from links in a .csv file (properly formatted) and save it in a path like:

`images\<type>\<id> (if needed)\original_file_name.extension`

It was intentionally separated from the other spiders (for icons and cards) because the act of downloading images can be *very* slow and expensive. Perhaps it's not the best case/scenario, or even the best use of the spider, but it was a choice made purely by **my** use case.

**run command**

` scrapy crawl download_images -a file_name=<your_file_name>`

# installation
Truth be told, I followed all steps in the [scrapy website](https://scrapy.org/ "scrapy website") (since I had absolutely no idea of what I was doing), but this project was made using Python 3.13.3 and scrapy 2.12.0.
## pre-requisites
- Scrapy (`pip install scrapy`) (the man itself)
- Pillow (`pip install pillow`) (for downloading images)
- Scrapy Impersonate (`pip install scrapy-impersonate`) (not required, but it was used!)

There were mentions of **crochet** lib, but only for unsuccessful tests.

## overwrite urls
Since I didn't want to commit the URLs used in this project (not only because I could, and probably will, change searching pages, but also because I don't think it is very polite of me to expose this brazillian site randomly - if you want the correct links just email me!) it will be necessary to change the placeholders in the project.

The placeholders are the follow (just `ctrl+f` in the project)
- `temp_url` (temporary url used to download images, only one request is done to this page, and it can be *any* page)
- `your_url` (url used to start the request of the spider)
- `repo_url` (repository url to download images from)

(yes, I do intend to put some global variables, but for the current state of this project it is not necessary)

# running
As I already kinda indicated you can run each spider separetelly (the spected order is index > edition > download_images), I did want some automation to run it *all* in some cases (like first fetch)

This is the point where everything goes wrong; turns out since I was making this all in a Windows environment (and too lazy to change it to another) all the demos explained in the scrapy documentation wouldn't work when we were considering *many* executions.

The first problem was with `ReactorNotRestartable()` because I was using a `CrawlerProcess` instead of `CrawlerRunner`, but after I changed I started having problems with `twisted.internet.selectreactor.SelectReactor` (that should be `twisted.internet.asyncioreactor.AsyncioSelectorReactor`) which is related to the Windows environment.

(for anyone having this problem, hey just simply import your asyncio lib directly **above** the line you are trying to use the reactor, it worked for me!)

Turns out that aproach creates **n** threads (and **n** concurrently executions) which Windows promply warned me that it hated it (and, I mean, fair. I was opening more than 100+ executions) and I changed to a queue approach (and thought myself a genious for that!) but Windows also didn't like to have a master process opening n child processes.

And, mind I add, I never intended to have it executing concurrently, I actually wanted something more like do `A > do B > iterate doing C > do D`, so I was desperate searching for *other* solutions, ending with a .bat that executes on its own and everything works (it is on the project! is the run.bat, and it should be executed from inside the directory he is currently on)

And that's it.

I don't know if this will help someone (actually, I hope no one finds this, because it is a mess), but it will help me when I inevitably forget what I've done when I pick up this project again after a couple of months.
