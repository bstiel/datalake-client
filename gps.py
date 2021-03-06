import logging


logger = logging.getLogger(__name__)


def _to_decimal(v):
    """Convert lat/long to decimal
       e.g. 5133.75141 => 51 degrees 33.75141' => 51 + 33.75141/60 => 51.5625235
    """
    degrees = float(v[:2])
    minutes = float(v[2:])
    d = degrees + minutes / 60.
    return d


def parse(data):
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        logger.debug('Parse $GPRMC: %s' % data)
        if sdata[2] == 'V':
            logger.warning('No satellite data available')
            return
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = sdata[3]
        north_south = sdata[4] # latitude direction N/S
        lon = sdata[5] # longitute
        east_west = sdata[6] #longitude direction E/W
        speed = sdata[7] # speed in knots
        track = sdata[8] # True course
        timestamp = "20" + sdata[9][4:6] + "-" + sdata[9][2:4] + "-" + sdata[9][0:2] + "T" + time + "+00:00"
        return {
            'datetime': timestamp,
            'latitude': _to_decimal(lat) * (-1 if north_south == 'S' else 1),
            'longitude': _to_decimal(lon) * (-1 if east_west == 'W' else 1),
            'speed': float(speed) * 1.852,
            'track': float(track) if track != '' else None 
        }

    if data[0:6] == "$GPGGA":
        sdata = data.split(",")
        logger.debug('Parse $GPGGA: %s' % data)
        if sdata[6] == '0':
            logger.warning('No satellite data available')
            return
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = sdata[2]
        north_south = sdata[3] # latitude direction N/S
        lon = sdata[4] # longitute
        east_west = sdata[5] #longitude direction E/W
        altitude = sdata[9] # altitude
        return {
            'time': time,
            'latitude': _to_decimal(lat) * (-1 if north_south == 'S' else 1),
            'longitude': _to_decimal(lon) * (-1 if east_west == 'W' else 1),
            'altitude': float(altitude)
        }
