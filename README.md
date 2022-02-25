# nextbike_hist

With this tool you can get the last locations of every https://www.nextbike.de/de/ in Cologne. 

### getter:

The getter script is supposed to be called like every 10 minutes by a cronjob. The script fetches the current locations of all the bikes in cologne, by calling this api https://api.nextbike.net/maps/nextbike-live.xml?city=14, and writes cleand data to a postgres db.


### api:
Here is an example php-script that serves the last locations by bike_id
