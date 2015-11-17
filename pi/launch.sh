#!/bin/sh

cd "$(dirname "$0")"

python programs/parse_weather.py
# python programs/parse_ical.py

convert programs/after-weather.svg after-weather.png

#We optimize the image
pngcrush -c 0 -ow after-weather.png done.png

#We move the image where it needs to be
rm /var/www/kindle/done.png
mv done.png /var/www/kindle/done.png

-- rm basic.ics
rm after-weather.svg
-- rm almost_done.png
-- rm almost_done.svg

