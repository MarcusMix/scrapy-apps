BOT_NAME = "googlewebscraping"

SPIDER_MODULES = ["googlewebscraping.spiders"]
NEWSPIDER_MODULE = "googlewebscraping.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
FEED_FORMAT = "csv"
# FEED_URI = "test.json"
