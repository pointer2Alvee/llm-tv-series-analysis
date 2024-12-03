import scrapy
from bs4 import BeautifulSoup
"""
* Note:-
BlogSpider inherits from scrapy.Spider. 
Spider is a crawler, crawls multiple web pages and 
ability to traverse thorugh web pages. 
This class has all the functionalities to crawl the data and put it into our structured dataset

"""
class BlogSpider(scrapy.Spider): 
    
    name = 'narutospider' # can be renamed
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response): # response in the webpage
        # this loop iterates through the webpage/objects in a single page we are to crawl
        for href in response.css('.smw-columnlist-container')[0].css("a::attr(href)").extract(): 
            #.css is filtering html page to anything has the 'smw-columnlist-container' class
            # this is only 1 div so [0] and we want every anchor tag inside smw-columnlist-container
            
            # we need href to visit the page
            # basically viiting inside links like: https://naruto.fandom.com/10-hit-combo pages 
            extracted_data = scrapy.Request("https://naruto.fandom.com"+href, callback=self.parse_jutsu)  # puts data from the page and put in a dict
            yield extracted_data # extracted_data is a dict
            
        # this loop iterates over pages (1,2,3..100..etc) using class : mw-nextlink
        for next_page in response.css('a.mw-nextlink'): # added class : mw-nextlink from webpage inspect
            yield response.follow(next_page, self.parse)
            
    
    def parse_jutsu(self, respose):
        
        # GET JUTSU TITLE
        jutsu_name = respose.css("span.mw-page-title-main::text").extract()[0]
        jutsu_name = jutsu_name.strip() # strips off any leading or trailing spaces
        
        div_selector = respose.css("div.mw-parser-output")[0]
        div_html = div_selector.extract()
             
        # filtering out html needs to install : pip install beautiful soup
        soup = BeautifulSoup(div_html).find('div') # gets the first div that it has in the html
        
        
        # GET JUTSU CLASSIFICATION / JUTSU TYPE
        jutsu_type = ""
        if soup.find('aside'):
            aside = soup.find('aside')
            
            # loop through all divs in div and find class : pi-data 
            for cell in aside.find_all('div', {'class' : 'pi-data'}):
                # from pi-data get only the classification
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip() # clears spaces
                    if cell_name == "classification":
                        # if cell is classification get value like : Taijutsu
                        jutsu_type = cell.find('div').text.strip()
                        
              
        # GET JUTSU DESCRIPTION      
        soup.find('aside').decompose()
        jutsu_description = soup.text.strip()
        jutsu_description = jutsu_description.split('Trivia')[0].strip() # get everything before the title Trivia
        
        return dict(
            jutsu_name = jutsu_name,
            jutsu_type = jutsu_type,
            jutsu_description = jutsu_description
        )