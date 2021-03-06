from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import timedelta
import pickle
import os.path
from pytz import timezone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarDate():
    def __init__(self, day, month, year, str_day):
        self.day = day
        self.month = month
        self.year = year
        self.str_day = str_day
        self.today = []

class TVShow():
    def __init__(self, title, season, episode, est_time):
        self.title = title
        self.season = season
        self.episode = episode
        self.est_time = est_time


class HTMLParser():
    def __init__(self):
        self.link = "https://simkl.com"
        self.calendar_id = "1437817"
        self.all_events = []
        self.all_events_summary = []
        self.k = ""

    #calendar = ["01-2019", "02-2019", "03-2019", "04-2019",
    #           "05-2019", "06-2019", "07-2019", "08-2019",
    #          "09-2019", "10-2019", "11-2019", "12-2019"]

    calendar = ["06-2019", "07-2019", "08-2019",
                "09-2019", "10-2019", "11-2019",
                "12-2019", "01-2020", "02-2020"]


    def get_tv_show_data(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        cal_item = soup.find_all('td', class_='SimklTVCalendarColumn')
        for i in cal_item:
            date = str(i.find('table', class_='SimklTVCalendarDayTitle', title=True)['title'])

            str_day = date.split()[0]
            month = date.split()[1].split('/')[0]
            day = date.split()[1].split('/')[1]
            year = date.split()[1].split('/')[2]


            tv_shows = i.find_all(class_='SimklTVCalendarWatching')
            if len(tv_shows) == 0:
                continue
            else:
                for t in tv_shows:
                    show_name = str(t.find_all(class_='SimklTVCalendarDayListLink')[0].get_text())
                    season = str(t.find_all(class_='SimklTVCalendarDayListLink')[1].get_text().split()[1])
                    episode = str(t.find_all(class_='SimklTVCalendarDayListLink')[1].get_text().split()[4])
                    show_id = str(t.find_all(class_='SimklTVCalendarDayListLink')[0].find('a')['href'])
                    fixed_time = self.get_time(show_id)
                    end_time = str((int(fixed_time.split(':')[0]) + 1) % 24)

                    start_datetime = datetime.datetime(int(year), int(month), int(day),
                                                        int(fixed_time.split(':')[0]), int(fixed_time.split(':')[1]),
                                                       tzinfo=timezone('America/New_York'))
                    ##  Because of the weird Time Zone System in Turkey
                    start_datetime = start_datetime + timedelta(hours=-1)
                    end_datetime = start_datetime + timedelta(hours=1)

                    datetime_object_start_str = start_datetime.isoformat()
                    datetime_object_end_str = end_datetime.isoformat()

                    s = TVShow(show_name, season, episode, fixed_time)

                    event = {
                        'summary': show_name + ' S:' + season + 'E:' + episode,
                        'start': {
                            'dateTime': datetime_object_start_str,
                            'timeZone': 'America/New_York',
                        },
                        'end': {
                            'dateTime': datetime_object_end_str,
                            'timeZone': 'America/New_York',
                        }
                    }

                    self.all_events.append(event)
                    self.all_events_summary.append(event['summary'])


    def get_time(self, show_id):
        show_page = requests.get(self.link + str(show_id))
        show_page_soup = BeautifulSoup(show_page.content, 'html.parser')
        try:
            est_time_hour = int(show_page_soup.find('td', class_='SimklTVAboutYearCountry').get_text().split()[5].split(':')[0])
            est_time_minute = str(show_page_soup.find('td', class_='SimklTVAboutYearCountry').get_text().split()[5].split(':')[1])
        except ValueError:
            est_time_hour = 21
            est_time_minute = "00"

        am_pm = show_page_soup.find('td', class_='SimklTVAboutYearCountry').get_text().split()[6]
        if am_pm == 'PM':
            est_time_hour += 12
        else:
            est_time_hour = '0' + str(est_time_hour)
        return str(est_time_hour) + ':' + str(est_time_minute)

    def print_calendar(self, day):
        print (str(day.day) + "-" + str(day.month) + "-" + str(day.year) + " " + day.str_day)
        for s in day.today:
            print (s.title)
            print (s.est_time)
            print ("S:" + s.season + " E:" + s.episode)
            print ("\n")

    def add_2_calendar(self, all_events):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting events from calendar.')
        events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                              orderBy='startTime').execute()
        event_sum = []
        events = events_result.get('items', [])
        for k in events:
            try:
                event_sum.append(str(k['summary']))
            except Exception:
                event_sum.append("problematic text")
        if not events:
            print('No upcoming events found.')

        print('There are ' + str(len(all_events)) + ' events to add.')
        for google_e in all_events:
            if google_e['summary'] not in event_sum:
                add_event = service.events().insert(calendarId='primary', body=google_e).execute()
                print('Adding ' + google_e['summary'] + ' to Google calendar...')
            else:
                print('Duplicate, passing: ' + google_e['summary'])

    def get_html(self):

        for month in HTMLParser.calendar:
            page = requests.get(self.link + "/tv/calendar/" + month + "/" + str(self.calendar_id))
            self.get_tv_show_data(page)
        self.add_2_calendar(self.all_events)


def main():
    exporter = HTMLParser()
    exporter.get_html()

if __name__ == "__main__":
    main()
