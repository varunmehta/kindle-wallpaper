import codecs
import urllib2
from xml.dom import minidom

# Code of my city, if you don't know what to do here, read the README
CODE = "12760759"
WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=' + CODE + '&u=c'


# <yweather:forecast day="Mon" date="2 Nov 2015" low="6" high="18" text="Partly Cloudy" code="29"/>
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
    image = forecast.getAttribute('code')
    date = forecast.getAttribute('date')
    fday = forecast.getAttribute('day')
    code_text = forecast.getAttribute('text')
    image_url = 'icons/' + image + '.svg'

    # Read icon (Just the path line)
    f = codecs.open(image_url, 'r', encoding='utf-8')
    f.readline()  # read file line to waste.
    icon = f.readline()  # this is the <path> line.
    f.close()

    # Insert icons and temperatures
    svg = svg.replace(day + '_DATE', fday + ', ' + date)
    svg = svg.replace(day + '_ICON', icon)
    svg = svg.replace(day + '_HIGH', high)
    svg = svg.replace(day + '_LOW', low)
    svg = svg.replace(day + '_CODE_TEXT', code_text)

    return svg


# ** Main Program **
weather_xml = urllib2.urlopen(WEATHER_URL).read()
dom = minidom.parseString(weather_xml)

# Open SVG to process
template = codecs.open('icons/kindle-display.svg', 'r', encoding='utf-8').read()

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
