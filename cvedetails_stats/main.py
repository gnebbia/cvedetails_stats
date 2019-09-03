# -*- encoding: utf-8 -*-
# cvedetails_stats v0.1.0
# A software to get insights and statistics on CVEs
# Copyright © 2019, Giuseppe Nebbione.
# See /LICENSE for licensing information.

"""
This is the main module of cvedetails_stats

:Copyright: © 2019, Giuseppe Nebbione.
:License: BSD (see /LICENSE).
"""

__all__ = ()

import time
import scrapy 
from scrapy.crawler import CrawlerProcess
from cvedetails_stats.spider.cvedetails import CVESpider

def main():
    """Main routine of cvedetails_stats."""

    curr_datetime = time.strftime("%d%m%Y-%H%M%S")
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'CVE_' + curr_datetime + '.csv',
        'LOG_LEVEL': 'WARNING',
    })

    process.crawl(CVESpider)
    process.start()
