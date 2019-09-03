# Scrapy Useful Queries for cvedetails.com

## Get links for all the years
response.css('th a::attr(href)').getall()

## Get links for each page
response.css("div.paging a::attr(href)").getall()


## Parse the Entire Table (i.e., Mess)

```py
table = response.xpath('//*[@class="searchresults sortable"]') 
```
### get the descriptions

```py
descriptions = table.xpath('./tr/td[@class="cvesummarylong"]/text()').getall()
descriptions = [d.strip() for d in descriptions]
```


### get the rows with most details except description
### must get the title and link

```py
rows = table.xpath('./tr[@class="srrowns"]')
```

### links

```py
links = rows.xpath('./td[2]/a[@href]/@href').extract() 
links = ["https://www.cvedetails.com" + l for l in links]
```

### cve_ids
```py
cve_ids = rows.xpath('./td[2]/a/text()').extract()
```

### CWE_ID

```py
cwes = []
cwe_strings = rows.xpath('./td[3]').getall()
for cwe in cwe_strings:
    if "CWE" in cwe:
        cwes.append(Selector(text=cwe).xpath('//a/text()').get())
    else:
        cwes.append('')
```



### vulnerability_types

```py
vulnerability_types = rows.xpath('./td[5]/text()').extract()
vulnerability_types = [v.strip() for v in vulnerability_types]
```

### pubdate

```py
publish_dates = rows.xpath('./td[6]/text()').extract()
```

### update_date 

```py
update_dates = rows.xpath('./td[7]/text()').extract()
```

### scores
```py
scores = rows.xpath('./td[8]/div/text()').extract()
```

### gained_access_level
```py
gained_access_levels = rows.xpath('./td[9]/text()').extract() 
```

### access
```py
accesses = rows.xpath('./td[10]/text()').extract() 
```

### complexities
```py
complexities = rows.xpath('./td[11]/text()').extract() 
```

### auth_required_list
```py
auth_required = rows.xpath('./td[12]/text()').extract()
```

### confidentiality_list
```py
confidentiality_list = rows.xpath('./td[13]/text()').extract()
```


### integrity_list
```py
integrity_list = rows.xpath('./td[14]/text()').extract()
```

### availability_list
```py
availability_list = rows.xpath('./td[15]/text()').extract()
```


### Test edge cases, last one, first one, edge,
### last page, middle page, first page


```python
table = response.xpath('//*[@class="searchresults sortable"]')
table = response.xpath('//*[@class="searchresults sortable"]/tr')
for row in table:
    cve = {
        'description' : table.xpath('//td[@class="cvesummarylong"]/text()').extract_first().strip(),
        'link': table.xpath('//tr[@class="srrowns"]/td/a[@href]/@href').extract_first(),
        'cve_id' : table.xpath('//tr[@class="srrowns"]/td/a[@href]/text()').extract_first()
    }
print(cve)
```
