# Web service for crawling the data from CCASS
* Crawl the shareholding data from [CCASS](https://www.hkexnews.hk/sdw/search/searchsdw.aspx) for a period
* Display the data of shareholding and transaction detection between two participants
* Stocks and Codes can be found [here](https://www.hkex.com.hk/mutual-market/stock-connect/eligible-stocks/view-all-eligible-securities?sc_lang=zh-hk)
* Participant ID can be found [here](https://www.hkexnews.hk/sdw/search/partlist.aspx?sortby=partid)

## ENVIRONMENT
* python3.6

## Clone the Project
<pre>
git clone https://github.com/aarontong95/CCASS-Crawler.git
</pre>

## Install the Packages
<pre>
pip install -r requirements.txt
</pre>

## Deploy the Service
<pre>
python api.py
</pre>

## Quick Deploy with Docker
<pre>
docker-compose up
</pre>

## Get Started
<pre>
Go to http://localhost:5000
</pre>

## Todo
* Using asynchronous methods to crawl the data
* Add validation of the code

## Webpage
![alt text](https://github.com/aarontong95/CCASS-Crawler/blob/main/docs/shareholding.png)

![alt text](https://github.com/aarontong95/CCASS-Crawler/blob/main/docs/trend_plot.png)
  
![alt text](https://github.com/aarontong95/CCASS-Crawler/blob/main/docs/transaction_finder.png)
