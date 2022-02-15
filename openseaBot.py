import requests
from bs4 import BeautifulSoup
import json
import cloudscraper
from requests_html import HTMLSession
from fake_useragent import UserAgent
import time
import sys


def GetNameOfCollection(link):
    name = link.split('/collection/')[1]
    name = name.split('/')[0]
    return name
#print(GetNameCollection(link))

def GetLinkApiJson(link):
    name = GetNameOfCollection(link)
    Linkapijson = 'https://api.opensea.io/api/v1/collection/'+str(name)+'/stats?format=json'
    return Linkapijson


def FloorPrice(link):
    response = requests.get(GetLinkApiJson(link))
    response = response.text
    response = json.loads(response)
    floorprice = response["stats"]["floor_price"]
    if floorprice != None:
        return floorprice
    else:
        floorprice = 'No Floor Price'
        return floorprice
    


def LinklistFloorPrice(link):
    name= GetNameOfCollection(link)
    linklistfloorprice = 'https://opensea.io/collection/'+str(name)+'?search[sortAscending]=true&search[sortBy]=PRICE&search[toggles][0]=BUY_NOW'
    return linklistfloorprice


def NFTFloor(link):
    if FloorPrice(link) == 'No Floor Price' :
        return 'No Floor Price in this Collection ==> ' + str(GetNameOfCollection(link))
    else :
        link = LinklistFloorPrice(link)
        scraper = cloudscraper.create_scraper()
        data = scraper.get(link).text
        soup = BeautifulSoup(data, 'html.parser')
        for link in soup.findAll('a',{"class":"styles__StyledLink-sc-l6elh8-0 ekTmzq Asset--anchor"}):
            links = (link.get('href'))
            links = 'https://opensea.io' + str(links)
            break
        return links



def main():
    while(True):
        print('---------------------------------------------------------------------------------------')
        print(NFTFloor(link))
        print('Name: '+str(GetNameOfCollection(link)) +' | '+'Price: '+str(FloorPrice(link)) + ' ETH')


link = sys.argv[1]
main()

