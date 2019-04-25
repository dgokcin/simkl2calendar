from collections import OrderedDict
from bs4 import BeautifulSoup
import requests

class CalendarDate():
    def __init__(self, day, month, year, str_day):
        self.day = day
        self.month = month
        self.year = year
        self.str_day = str_day
        self.today = []

class TVShow():
    def __init__(self, title, season, episode):
        self.title = title
        self.season = season
        self.episode = episode


class HTMLParser():

    calendar = ["01-2019", "02-2019", "03-2019", "04-2019",
                "05-2019", "06-2019", "07-2019", "08-2019",
                "09-2019", "10-2019", "11-2019", "12-2019"]

    def get_tv_show_data(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        cal_item = soup.find_all('td', class_='SimklTVCalendarColumn')
        for i in cal_item:
            date = str(i.find('table', class_='SimklTVCalendarDayTitle', title=True)['title'])

            str_day = date.split()[0]
            month = date.split()[1].split('/')[0]
            day = date.split()[1].split('/')[1]
            year = date.split()[1].split('/')[2]

            tmp = CalendarDate(day, month, year, str_day)

            tv_shows = i.find_all(class_='SimklTVCalendarWatching')
            if len(tv_shows) == 0:
                continue
            else:
                for t in tv_shows:
                    show_name = str(t.find_all(class_='SimklTVCalendarDayListLink')[0].get_text())
                    season = str(t.find_all(class_='SimklTVCalendarDayListLink')[1].get_text().split()[1])
                    episode = str(t.find_all(class_='SimklTVCalendarDayListLink')[1].get_text().split()[4])

                    s = TVShow(show_name, season, episode)
                    tmp.today.append(s)

            self.print_calendar(tmp)

    def print_calendar(self, day):
        print (str(day.day) + "-" + str(day.month) + "-" + str(day.year) + " " + day.str_day)
        for s in day.today:
            print s.title
            print "S:" + s.season + " E:" + s.episode
            print "\n"

    def get_html(self):
        link = "https://simkl.com/tv/calendar"
        calendar_id = "1437817"

        for month in HTMLParser.calendar:
            page = requests.get(link + "/" + month + "/" + str(calendar_id))
            self.get_tv_show_data(page)


def main():
    exporter = HTMLParser()
    exporter.get_html()

if __name__ == "__main__":
    main()
