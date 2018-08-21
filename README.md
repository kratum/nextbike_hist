# nextbike_hist

With this tool you can get the last locations of every https://www.nextbike.de/de/ in Cologne. A working example can be found on https://geolution.eu/bikehist/


### getter:

A python script that is called every 10 minutes by a cronjob and fetched the current location of all the bikes in cologne. The script calls this api https://api.nextbike.net/maps/nextbike-live.xml?city=14


### api:
Here is a php-script that serves the last locations by bike_id
