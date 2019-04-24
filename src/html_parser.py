from collections import OrderedDict
from bs4 import BeautifulSoup
import requests

class CalendarDate():
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
        self.today = []

class TVShow():
    def __init__(self, title, season, episode):
        self.title = title
        self.season = season
        self.episode = episode


class HTMLParser():

    calendar = OrderedDict()
    calendar = {
                #"01-2019": "january.html",
                #"02-2019": "february.html",
                #"03-2019": "march.html",
                "04-2019": "april.html"
                #"05-2019": "may.html",
                #"06-2019": "june.html",
                #"07-2019": "july.html",
                #"08-2019": "august.html",
                #"09-2019": "september.html",
                #"10-2019": "october.html",
                #"11-2019": "november.html",
                #"12-2019": "december.html"
                }
    def get_tv_show_data(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        month = soup.find_all('td', class_='SimklTVCalendarColumn')
        for d in month:
            tv_shows = d.find_all(class_='SimklTVCalendarDayListLink')
            for t in tv_shows:
                print (t.get_text())



    def get_html(self):
        link = "https://simkl.com/tv/calendar"
        calendar_id = "1437817"

        for key, value in HTMLParser.calendar.iteritems():
            page = requests.get(link + "/" + key + "/" + str(calendar_id), "html/" + value)
            self.get_tv_show_data(page)



def main():
    exporter = HTMLParser()
    exporter.get_html()




if __name__ == "__main__":
    main()