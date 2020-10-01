# FlatToNestedJson
Python flask API to dynamincally nest a flat JSON

# how to run
1) $ python application.py
2) example URL: 127.0.0.1:5000/quakeData?sortingOrder=mag|place|type|time
3) username: johny / password: english
4) to beutify json https://jsonbeautify.com

# Endpoints
1) /quakeData [GET]
Takes one query parameter "sortingOrder" with any number of "|" seperated keys to dynamically nest JSON. This end point fetch Earthquake data in flat json format from the US Government website and return nested JSON based on provided parameter in sequential order.

key list: mag, place, time, updated, tz, url, detail, felt, cdi, mmi, alert, status, tsunami, sig, net, code, ids, sources, types, nst, dmin, rms, gap, magType, type, title

example: /quakeData?sortingOrder=mag|place|type|time

keys detail: https://tinyurl.com/ybbp5kfg
Data source: https://tinyurl.com/y5uttm6n

2) /nestJson [POST]
Takes one query parameter "sortingOrder" with any number of "|" seperated keys and a flat JSON body to dynamically nest in sequential order. A sample file "input.json" can be used to provide in request body.
example : 127.0.0.1:5000/nestJson?sortingOrder=currency|country|city|town|amount
