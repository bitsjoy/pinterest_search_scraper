import scrapy

import json 
import requests


class Pinterest(scrapy.Spider):
 
    name = 'pinterest'

    #query i.e. what do you want to search for
    query = 'job'

    #number of images you want to scrape, it should be a multiple of 25
    number_of_images = 100


    #see this quick youtube video on how to set this cookie and x_crsftoken
    cookie = 'csrftoken=97b01583d6330b33b7e72656a4d5ed1c; _pinterest_sess=TWc9PSZSNnhlV2xkTWpGTFltVVEvQkRBbmxDWlRPcEx6MEhSdGRYR3g0ZmJaWUk5WVVXakQwS29Ia0F1RGZiYlpSdXByTy9mckF5dDRzTG9sU2FYV3ZlbXZNUFpDOFpqYVB1c1FYV2oxWk15MEQyTT0meU1oTWZRSGR5Q1Z6Zjd5bXc0a0gvejFPR1R3PQ==; _auth=0; _routing_id="b5a67db2-93e5-4513-ab31-05ca021c6667"; sessionFunnelEventLogged=1'
    x_crsftoken = '97b01583d6330b33b7e72656a4d5ed1c'


    start_urls = ['https://in.pinterest.com/resource/BaseSearchResource/get/?source_url=%2Fsearch%2Fpins%2F%3Fq%3D' + query + '%26rs%3Dtyped%26term_meta%5B%5D%3D' + query + '%257Ctyped&data=%7B%22options%22%3A%7B%22article%22%3A%22%22%2C%22appliedProductFilters%22%3A%22---%22%2C%22query%22%3A%22' + query + '%22%2C%22scope%22%3A%22pins%22%2C%22auto_correction_disabled%22%3A%22%22%2C%22top_pin_id%22%3A%22%22%2C%22filters%22%3A%22%22%7D%2C%22context%22%3A%7B%7D%7D&_=1660591241435']

    next_options = None

    crawlTime = 0

    collectionItems = []

    def parse(self, response): 
 
        response_body = response.body

        p = json.loads(response_body.decode('UTF-8'))
        results = p['resource_response']['data']['results']
        print(response_body.decode('UTF-8'))
        self.next_options = p['resource']['options']


        for result in results:
            print(result)
            if 'images' in result:
                self.collectionItems.append({
                    "title": result['title'],
                    "image": result['images']['orig'],
                    "pinner": result['pinner'],
                    "board": result['board']
                })

        # loopign 25 times to simulate webpage scroll
        while self.crawlTime <  (self.number_of_images-25)/25:

            # request
            url = "https://www.pinterest.com.au/resource/BaseSearchResource/get/"

            payload = json.dumps({
            "source_url": '/search/pins/?q=' + self.query + '&rs=typed&term_meta[]=' + self.query + '%7Ctyped',
            "data": {
                "options": self.next_options,
                "context": {}
            }
            })
            headers = {
            'cookie': self.cookie,
            'x-csrftoken': self.x_crsftoken,
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            self.next_options = json.loads(response.text)['resource']['options']

            moreResults = json.loads(response.text)['resource_response']['data']['results']
            for result in moreResults:
                if 'images' in result:
                    self.collectionItems.append({
                    "title": result['title'],
                    "image": result['images']['orig'],
                    "pinner": result['pinner'],
                    "board": result['board']
                })
            print(json.loads(response.text)['resource_response']['data']['results'][5]['images']['orig']) 
            print('/search/pins/?q=' + self.query + '&rs=typed&term_meta[]=' + self.query + '%7Ctyped')

            self.crawlTime += 1


        #creates a json file with the data of search images
        jsonString = json.dumps(self.collectionItems)
        jsonFile = open("searchResults.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()