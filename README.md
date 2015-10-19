# Guantanamo

This is a simple Twitter bot to maintain awareness of people
being held in the United States' Guantanamo Bay detention camp. Many people have now been held in the military prison at Guantanamo Bay for over a decade. Many prisoners are recommended for release yet remain imprisoned, while many others are still awaiting trial. I wanted to have a service that would send notifications with how long each prisoner has been in prison with their name and where they are from. It is live on `@guantanamobot`.

## How it works

### Web Scraping

Web scraper is stored in `guantanabot/scrapey.py` for grabbing data from the NYT's excellent tracker of Guantanamo prisoners [0]. The scraper runs every few days and crawls the Times site to grab the most recent information and then serializes the output in JSON.

### Twitter Bot

The Twitter bot is for tweeting how long each person has been imprisoned and their status is in `guantanabot/guantanabot.py`. It will tweet every few days with a status update of a random prisoner.

## Resources
 
[0] [NYT Guantanamo Docket](http://projects.nytimes.com/guantanamo/detainees/current)
 
[1] [Time since Obama promised to release the remaining prisoners cleared for release](http://www.gtmoclock.com/)