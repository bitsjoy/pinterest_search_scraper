import scrapy

import json 
import requests


class Opentable(scrapy.Spider):
 
    name = 'opentable'

 
    start_urls = ['https://www.opentable.com/r/izakaya-sasaya-west-los-angeles?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/ye-olde-kings-head-santa-monica?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/gyu-kaku-santa-monica?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/thai-district?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/black-angus-steakhouse-whittier?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/tlv-tapas-los-angeles?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/gyu-kaku-topanga-canyon-canoga-park?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/vale-lounge-los-angeles?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/le-petit-paris?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/barton-g-the-restaurant-los-angeles-west-hollywood?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/nusr-et-steakhouse-beverly-hills-los-angeles?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/r/culichi-town-bell?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00','https://www.opentable.com/vino-wine-and-tapas-room?corrid=48bced6a-e88a-43d6-9271-9d82cc70d369&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2022-11-24T22%3A30%3A00']

    next_options = None

    crawlTime = 0

    collectionItems = []

    def parse(self, response): 
 
        response_body = response.body 
        
        # $x("//h1[@class='eM9Li2wbkQvvjxZB11sV LpNRJPWAkIFWmkz7MQXJ']")[0].outerText;
        url = response.url
        naam = str(response.xpath("//h1[@class='eM9Li2wbkQvvjxZB11sV LpNRJPWAkIFWmkz7MQXJ']")[0].get()).split(">")[1].split("<")[0] #innerHtml
        address = str(response.xpath("//p[@class='aAmRZnL9EescJ80holSh']")[0].get()).split(">")[1].split("<")[0]
        price = str(response.xpath("//div[@id='priceBandInfo']")[0].get()).split("span")[3].split(">")[1].split("<")[0]
        bookingFrequency = str(response.xpath("//span[@class='Rv4uk4xWG5CqQmf74o1v BoZ_Hzg4GGZ1XXDaNyct']")[0].get()).split("</span>")[1] 
        cusines = str(response.xpath("//div[@class='ZQUIHOcNUeU7wqraxFtp']")[1].get()).split('<p class="c_qirB1mFl5VRKHYJqTz">')[1].split("<")[0]
        diningStyle = str(response.xpath("//div[@class='ZQUIHOcNUeU7wqraxFtp']")[0].get()).split('<p class="c_qirB1mFl5VRKHYJqTz">')[1].split("<")[0]
        ratingFood = str(response.xpath("//span[@class='q5KV_STbBbfMbIeljXUO D6DX5qrhdlsX8NtPW71B']")[0].get()).split(">")[1].split("<")[0]
        ratingService = str(response.xpath("//span[@class='q5KV_STbBbfMbIeljXUO D6DX5qrhdlsX8NtPW71B']")[1].get()).split(">")[1].split("<")[0]
        ratingAmbience = str(response.xpath("//span[@class='q5KV_STbBbfMbIeljXUO D6DX5qrhdlsX8NtPW71B']")[2].get()).split(">")[1].split("<")[0]
        ratingValue = str(response.xpath("//span[@class='q5KV_STbBbfMbIeljXUO D6DX5qrhdlsX8NtPW71B']")[3].get()).split(">")[1].split("<")[0]
        ratingMain = str(response.xpath("//span[@class='QBMm80naGcMZ6qlVk6OI BoZ_Hzg4GGZ1XXDaNyct']")[0].get()).split(">")[1].split("<")[0]

        entry = { 
            "Rest Name": naam,
            "Address": address,
            "Price": price,
            "Booking Frequency": bookingFrequency,
            "Cuisines": cusines,
            "Dining Style": diningStyle,
            "Rating Food": ratingFood,
            "Rating Service": ratingService,
            "Rating Ambience": ratingAmbience,
            "Rating Value": ratingValue,
            "Rating Main": ratingMain,
            "Number of Menu Items": '',
            "Latitude": '',
            "Longitude": '', 
            "url": url
        }

        self.collectionItems.append(entry)

        f = open("open_table_data.json", "w")
        f.write(str(self.collectionItems).replace("'",'"'))
        f.close()

        # collection of urls
        # populate the start_urls array with the urls
        # run the spider
        # convert json file to xlsx format
        # populate the total number of menu items
 