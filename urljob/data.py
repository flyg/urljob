# class passed between server and client
class url_job:
    url = "",
    category = "",

    def __init__(self, url, category, sub_category):
        self.url = url
        self.category = category
        self.sub_category = sub_category