from acrawler import Crawler, Request, ParselItem, Handler, register, get_logger


def process_time(value):
    # a self-defined field processing function
    # process time to minutes
    # '3h 1min' -> 181
    if value:
        res = 0
        segs = value.split(" ")
        for seg in segs:
            if seg.endswith("min"):
                res += int(seg.replace("min", ""))
            elif seg.endswith("h"):
                res += 60 * int(seg.replace("h", ""))
        return res
    return value


class MovieItem(ParselItem):
    css = {
        "title": "h1::text",
        "date": ".subtext a[href*=releaseinfo]::text",
        "time": [".subtext time::text", process_time],
        "rating": "span[itemprop=ratingValue]::text",
        "rating_count": "span[itemprop=ratingCount]::text",
        "metascore": ".metacriticScore span::text",
        "genres": "[.subtext a[href*=genres]::text]",
        "director": "[h4:contains(Director) ~ a[href*=name]::text]",
        "writers": "[h4:contains(Writer) ~ a[href*=name]::text]",
        "stars": "[h4:contains(Star) ~ a[href*=name]::text]",
    }


class IMDBCrawler(Crawler):
    config = {"MAX_REQUESTS": 4, "DOWNLOAD_DELAY": 1}

    async def start_requests(self):
        yield Request("https://www.imdb.com/chart/moviemeter")

    async def parse(self, response):
        for tr in response.sel.css(".lister-list tr"):
            link = tr.css(".titleColumn a::attr(href)").get()
            if link:
                yield Request(link, callback=self.parse_movie)

    async def parse_movie(self, response):
        url = response.url_str
        yield MovieItem(response.sel, extra={"url": url.split("?")[0]})


@register()
class HorrorHandler(Handler):
    family = "MovieItem"
    logger = get_logger("horrorlog")

    async def handle_after(self, item):
        if item["genres"] and "Horror" in item["genres"]:
            self.logger.warning(f"({item['title']}) is a horror movie!!!!")


if __name__ == "__main__":
    IMDBCrawler().run()
