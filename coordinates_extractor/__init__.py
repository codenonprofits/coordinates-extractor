import re
import sys
import requests
import vobject

from urlparse import urlparse, parse_qs
from bs4 import BeautifulSoup


class CoordinatesExtractor(object):

    def __init__(self, text=None, file_path=None, *args, **kwargs):
        assert text or file_path, 'text or file_path are required'
        self.google_maps_urls_start = ('https://goo.gl', 'https://maps.google', 'https://www.google', 'https://maps.app',)
        self.text = text
        self.lat = None
        self.long = None
        self.file_path = file_path
        self.regex = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'

    def get_coordinates_from_file(self):
        try:
            with open(self.file_path, 'r') as f:
                file_as_str = f.read()
                
            file_card = vobject.readOne(file_as_str)
            if hasattr(file_card, 'contents'):
                content = file_card.contents
                url = content.get('url', None)
                if url:
                    parse_url = urlparse(url[0].value)
                    parse_query = parse_qs(parse_url.query)
                    coordinates = parse_query.get('ll')
                    self.lat, self.long = coordinates[0].split(',')
        except Exception as e:
            print('Error: %s' % e.args)

        return self.lat, self.long

    def text_check(self):
        match = re.findall(self.regex, self.text)
        url_match = [url for url in match if url.startswith(self.google_maps_urls_start) and 'maps' in url]
        return True if url_match and 'maps' in url_match[0] else False

    def get_match(self):
        match = re.findall(self.regex, self.text)
        url_match = [url for url in match if url.startswith(self.google_maps_urls_start) and 'maps' in url]

        if not url_match:
            raise Exception('No URL found.')
        elif 'maps' not in url_match[0]:
            raise Exception('Google Maps URL not found. Try again.')
        else:
            return url_match[0]

    def _check_coordinates_on_url(self, url):
        url_regex = r'(\-?\d+(\.\d+)?)(!4d|,)-\s*(\-?\d+(\.\d+)?)'
        match = re.findall(url_regex, url)

        try:
            (lat, lat_end, separator, long, lng_end) = match[-1] if match else (None, None, None, None, None)
            lat = float(lat) if lat else None
            long = float(long) if long else None
        except Exception as e:
            lat, long = None, None
            print('>> Error: %s' % e.args)

        return lat, long

    def get_coordinates(self):
        response = requests.get(self.get_match(), timeout=10)

        (lat, long) = self._check_coordinates_on_url(response.url)

        if lat and long:
            self.lat = lat
            self.long = long
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.head.find_all('script')

            if script_tags:
                tag = script_tags[0]
                text = tag.get_text()

                its_ok = False

                try:
                    items = text.split('"')

                    string_with_coordinates = items[62]
                    string_with_coordinates_split = string_with_coordinates.split(',')

                    try:
                        lat = '{lat}'.format(lat=string_with_coordinates_split[4])
                        self.lat = float(lat.replace('[', '').replace(']', ''))
                        long = '{long}'.format(long=string_with_coordinates_split[3])
                        self.long = float(long.replace('[', '').replace(']', ''))
                        its_ok = True
                    except:
                        raise Exception

                except Exception:
                    items = text.split('"')

                    string_with_coordinates = items[58]
                    string_with_coordinates = string_with_coordinates.replace('[', '').replace(']', '')
                    string_with_coordinates_split = string_with_coordinates.split(',')

                    try:
                        lat = '{lat}'.format(lat=string_with_coordinates_split[1])
                        self.lat = float(lat.replace('[', '').replace(']', ''))
                        long = '{long}'.format(long=string_with_coordinates_split[2])
                        self.long = float(long.replace('[', '').replace(']', ''))
                        its_ok = True
                    except:
                        pass

                finally:
                    if its_ok == False:
                        items = text.split(',')

                        try:
                            lat = '{lat}'.format(lat=items[2])
                            self.lat = float(lat.replace('[', '').replace(']', ''))
                            long = '{long}'.format(long=items[1])
                            self.long = float(long.replace('[', '').replace(']', ''))
                        except:
                            pass
        
        return self.lat, self.long
