class BigQuery:

    def __init__(self, searchQuery):
        self.searchQuery = searchQuery
    
    def wolframalphaSearch(self):
        import wolframalpha
        question = self.searchQuery

        app_id = 'your own app id'
        client = wolframalpha.Client(app_id)

        res = client.query(question)

        try:
            answer = next(res.results).text
        except StopIteration:
            answer = " "
        return answer



    def googleSearch(self):
        from requests_html import HTMLSession
        from nltk import tokenize
        s = HTMLSession()
        searchQuery = tokenize.word_tokenize(self.searchQuery)
        query = ""
        for x in range(len(searchQuery)):
            query += f'{searchQuery[x]}+'
        query = query[:-1]
        url = f'https://www.google.com/search?q={query}'
        r = s.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'})
        try:
            scientificInformation = r.html.find('div.kno-rdesc', first=True).text

        except AttributeError:
            scientificInformation = "no scientific information found"

        try:
            generalInformation = r.html.find('span.hgKElc', first=True).text

        except AttributeError:
            generalInformation = "no general information found"

        try:
            scientificFactOne = r.html.find('div.sATSHe', first=True).text

        except AttributeError:
            scientificFactOne = "no scientific fact found"

        return scientificInformation, scientificFactOne, generalInformation


    def wikiSearch(self):
        import wikipedia
        try:
            ans = wikipedia.summary(self.searchQuery, sentences=10)
        except wikipedia.exceptions.DisambiguationError:
            ans = " "
        return ans


