import urllib
from collections import OrderedDict

class HTMLExport():

    calendar = OrderedDict()
    calendar = {"01-2019": "january.html",
                "02-2019": "february.html",
                "03-2019": "march.html",
                "04-2019": "april.html",
                "05-2019": "may.html",
                "06-2019": "june.html",
                "07-2019": "july.html",
                "08-2019": "august.html",
                "09-2019": "september.html",
                "10-2019": "october.html",
                "11-2019": "november.html",
                "12-2019": "december.html"
                }

    def export_to_html(self):
        link = "https://simkl.com/tv/calendar"
        calendar_id = "1437817"

        for key, value in HTMLExport.calendar.iteritems():
            print ("Extracting html info for " + key)
            # instantiate the parser and fed it some HTML
            #urllib.urlretrieve("https://simkl.com/tv/calendar/04-2019/1437817/", "test_april.html")
            urllib.urlretrieve(link + "/" + key + "/" + str(calendar_id), "html/" + value)


def main():
    exporter = HTMLExport()
    exporter.export_to_html()




if __name__ == "__main__":
    main()