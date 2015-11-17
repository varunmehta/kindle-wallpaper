import codecs
import urllib2
from xml.dom import minidom

# Code of my city, if you don't know what to do here, read the README
CODE = "12760759"
WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=' + CODE + '&u=c'


def parse_forecast(forecast, day, svg):
    '''
    Parses the xml tag yweather:forecast and parses the info available from it.

    <yweather:forecast day="Mon" date="2 Nov 2015" low="6" high="18" text="Partly Cloudy" code="29"/>

    :param forecast:
    :param day:
    :param svg:
    :return:
    '''
    low = forecast.getAttribute('low')
    high = forecast.getAttribute('high')
    code = forecast.getAttribute('code')
    date = forecast.getAttribute('date')
    fday = forecast.getAttribute('day')
    code_text = forecast.getAttribute('text')

    # Insert icons and temperatures
    svg = svg.replace(day + '_DATE', fday + ', ' + date)
    svg = svg.replace(day + '_ICON', parse_code(code))
    svg = svg.replace(day + '_HIGH', high)
    svg = svg.replace(day + '_LOW', low)
    svg = svg.replace(day + '_CODE_TEXT', code_text)

    return svg


def parse_code(code):
    image_url = '../icons/' + code_to_image(code) + '.svg'

    # Read icon (Just the path line)
    f = codecs.open(image_url, 'r', encoding='utf-8')
    f.readline()  # read file line to waste.
    f.readline()  # read file line to waste.
    f.readline()  # read file line to waste.
    f.readline()  # read file line to waste.
    icon = f.readline()  # this is the <path> line.
    f.close()

    return icon


def code_to_image(code):
    code = int(code)
    img = ''
    if code == 0:
        img = 'tornado'
    elif code == 1 or code == 37 or code == 38 or code == 39 or code == 45 or code == 47:
        img = 'day-storm-showers'
    elif code == 2:
        img = 'hurricane'
    elif code == 3 or code == 4:
        img = 'thunderstorm'
    elif code == 5 or code == 6 or code == 7:
        img = 'rain-mix'
    elif code == 8 or code == 10 or code == 17:
        img = 'hail'
    elif code == 9 or code == 11 or code == 12 or code == 40:
        img = 'showers'
    elif code == 13 or code == 16 or code == 42 or code == 46:
        img = 'snow'
    elif code == 14:
        img = 'day-snow'
    elif code == 15 or code == 41 or code == 43:
        img = 'snow-wind'
    elif code == 18 or code == 35:
        img = 'rain-mix'
    elif code == 19:
        img = 'dust'
    elif code == 20:
        img = 'fog'
    elif code == 21:
        img = 'windy'
    elif code == 22:
        img = 'smoke'
    elif code == 23 or code == 24:
        img = 'strong-wind'
    elif code == 25:
        img = 'snowflake-cold'
    elif code == 26:
        img = 'cloudy'
    elif code == 27 or code == 29:
        img = 'night-cloudy'
    elif code == 28 or code == 30:
        img = 'day-cloudy'
    elif code == 31:
        img = 'night-clear'
    elif code == 32:
        img = 'day-sunny'
    elif code == 33:
        img = 'night-partly-cloudy'
    elif code == 34 or code == 44:
        img = 'day-sunny-overcast'
    elif code == 36:
        img = 'hot'
    elif code == 3200:
        img = 'stars'

    return img


# ** Main Program **
weather_xml = urllib2.urlopen(WEATHER_URL).read()
print(WEATHER_URL)
dom = minidom.parseString(weather_xml)

# Open SVG to process
template = codecs.open('../icons/kindle-display.svg', 'r', encoding='utf-8').read()

# <yweather:condition text="Fair" code="33" temp="15" date="Mon, 02 Nov 2015 5:49 pm EST"/>
current = dom.getElementsByTagName('yweather:condition')[0]
current_code = current.getAttribute('text')
current_temp = current.getAttribute('temp')
last_updated = current.getAttribute('date')

template = template.replace('CURRENT_TEMP', current_temp)
template = template.replace('CURRENT_CODE', current_code)
template = template.replace('LAST_UPDATED', last_updated)

# Get weather Tags
xml_temperatures = dom.getElementsByTagName('yweather:forecast')

# Parse and replace in svg file.
template = parse_forecast(xml_temperatures[0], 'DAY_0', template)
template = parse_forecast(xml_temperatures[1], 'DAY_1', template)
template = parse_forecast(xml_temperatures[2], 'DAY_2', template)

# Write output
codecs.open('after-weather.svg', 'w', encoding='utf-8').write(template)
