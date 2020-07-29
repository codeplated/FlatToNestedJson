# FlatToNestedJson
Python flask API to dynamincally nest flat JSONs


# Endpoints
1) /quakeData [GET]
Takes one query parameter "sortingOrder" with any number of "|" seperated keys to dynamically nest JSON. This end point fetch Earthquake data from the US Government website and return nested JSON based on provided parameter in sequential order.

key list: mag, place, time, updated, tz, url, detail, felt, cdi, mmi, alert, status, tsunami, sig, net, code, ids, sources, types, nst, dmin, rms, gap, magType, type, title

keys detail: https://tinyurl.com/ybbp5kfg
Data source: https://tinyurl.com/y5uttm6n

2) /nestJson [POST]
Takes one query parameter "sortingOrder" with any number of "|" seperated keys and a flat JSON body to dynamically nest in sequential order. A sample file "input.json" can be used to provide in request body.   
