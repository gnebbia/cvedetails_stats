# -*- encoding: utf-8 -*-
# cvedetails_stats v0.1.0
# A software to get insights and statistics on CVEs
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
This is the scrapy spider which will take all the vulnerabilities details
from cvedetails.com

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""

import sys
import itertools
import scrapy
from scrapy.selector import Selector



class CVESpider(scrapy.Spider):
    name = "cvespider"
    # allowed_domains = ["example.com"]
    base_domain = 'https://www.cvedetails.com'
    start_urls = (
            'https://www.cvedetails.com/index.php',
    )

    def parse(self, response):
        # Pulling all links referring to different years
        urls = response.xpath('//td[@class="num"]/a[@href]/@href').getall()
        for url in urls:
            #url = urlparse.urljoin(response.url, url)
            url = response.urljoin(url)
            print("Found URL: {}".format(url))

            yield scrapy.Request(url, callback = self.parse_pages)

    def parse_pages(self, response):
        # Pulling all links in a specific year, referring to a specific page
        urls = response.css("div.paging a::attr(href)").getall()
        for url in urls:
            url = response.urljoin(url)
            print("Found URL: {}".format(url))
            yield scrapy.Request(url, callback = self.parse_tables)


    def parse_tables(self, response):
        # Extracting all the informations from the found tables
        table = response.xpath('//*[@class="searchresults sortable"]')

        # get the descriptions
        descs_selectors = table.xpath('./tr/td[@class="cvesummarylong"]') 

        descriptions = []
        for d in descs_selectors: 
            descriptions.append(''.join(d.xpath('.//text()').extract()).strip()) 
        
        ### get the rows
        rows = table.xpath('./tr[@class="srrowns"]')
        
        # get url links to CVE webpages
        links = rows.xpath('./td[2]/a[@href]/@href').extract() 
        links = [self.base_domain + l for l in links]                                                                                                                                      
        
        # get CVE IDs
        cves = rows.xpath('./td[2]/a/text()').extract()
        
        # get CWE_IDs
        cwes = []
        cwe_strings = rows.xpath('./td[3]').getall()
        for cwe in cwe_strings:
            if "CWE" in cwe:
                cwes.append(Selector(text=cwe).xpath('//a/text()').get())
            else:
                cwes.append('')
        
        
        # get vulnerability_types
        vultype_l = rows.xpath('./td[5]/text()').extract()
        vultype_l = [v.strip() for v in vultype_l]
        
        # get publish date
        pubdates = rows.xpath('./td[6]/text()').extract()
        
        # get update_date 
        updates = rows.xpath('./td[7]/text()').extract()

        # get vulnerability scores
        scores = rows.xpath('./td[8]/div/text()').extract()

        # get gained access levels
        gal_l = rows.xpath('./td[9]/text()').extract() 

        # get access requirements
        acc_l = rows.xpath('./td[10]/text()').extract() 

        # get complexities
        compl_l = rows.xpath('./td[11]/text()').extract() 

        # get auth_required_list
        auth_l = rows.xpath('./td[12]/text()').extract()

        # get confidentiality_list
        conf_l = rows.xpath('./td[13]/text()').extract()

        # get integrity_list
        integ_l = rows.xpath('./td[14]/text()').extract()

        # get availability_list
        avail_l = rows.xpath('./td[15]/text()').extract()

        ref = len(cves)

        if not (len(cves) == len(cwes) == len(descriptions) == len(links) ==\
            len(vultype_l) == len(pubdates) == len(updates) == len(scores) ==\
            len(gal_l) == len(compl_l) == len(auth_l) == len(acc_l) ==\
            len(conf_l) == len(integ_l) == len(avail_l)):

            print(len(cves))
            print(len(cwes))
            print(len(descriptions))
            print(len(links))
            print(len(vultype_l))
            print(len(pubdates))
            print(len(updates))
            print(len(scores))
            print(len(gal_l))
            print(len(compl_l))
            print(len(auth_l))
            print(len(acc_l))
            print(len(conf_l))
            print(len(integ_l))
            print(len(avail_l))
            
            print(response.url)
            sys.exit('Error in Parsing: Fields do not have the same lengths')

        item = []
        for i in range(len(cves)):
            yield {
                'cve_id' : cves[i],
                'cwe_id':  cwes[i],
                'description': descriptions[i],
                'link': links[i],
                'type': vultype_l[i],
                'date_publish': pubdates[i],
                'date_last_update': updates[i],
                'score': scores[i],
                'gained_access_level': gal_l[i],
                'complexity': compl_l[i],
                'authenticatiton_requirements': auth_l[i],
                'access_requirements': acc_l[i],
                'confidentiality_impact': conf_l[i],
                'integrity_impact': integ_l[i],
                'availability_impact': avail_l[i],
            }
