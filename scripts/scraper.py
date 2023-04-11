
# import required modules
from bs4 import BeautifulSoup
import requests
 

def links_from_mainpage():
    output_links = []
    # get URL
    page = requests.get("https://en.m.wikipedia.org/wiki/Lists_of_twin_towns_and_sister_cities")
    
    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for i in range(6):
        section = soup.find_all("section", class_="mf-section-"+str(i+1))[0]
        links = section.find_all('a')
        continent = None
        for index,link in enumerate(links):
            if index == 0:
                continent = link.text.split()[-1]
                if continent == 'America': # find out if it is South or North America
                    continent = link.text.split()[-2:]
                    continent = ' '.join(continent)
                continue # first link in section is about the continent 
            link = link['href']
            link = "https://en.m.wikipedia.org" + link
            output_links.append((link,continent))

    return output_links[:-2] # last two links are from the "list of list" page and an arrow picture 


if __name__ == "__main__":
    [print(l) for l in links_from_mainpage()]