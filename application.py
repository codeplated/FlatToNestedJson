import flask, json
from flask import request, jsonify, make_response, render_template
import urllib.request
from flatToNested import FlatToNested
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['BASIC_AUTH_USERNAME'] = 'full-stack'
app.config['BASIC_AUTH_PASSWORD'] = 'hayermee'
basic_auth = BasicAuth(app)

def addTags(tag, word):
    return '<%s>%s</%s>' % (tag, word, tag)

@app.route('/', methods=['GET'])
def home():
    apiName = addTags('h1', 'Flat to dynamic nested JSON')
    keyList = addTags('p', 'key list: mag, place, time, updated, tz, url, detail, felt, cdi, mmi, alert, status, tsunami, sig, net, code, ids, sources, types, nst, dmin, rms, gap, magType, type, title')
    keyDetail = addTags('p', 'keys detail: https://tinyurl.com/ybbp5kfg')
    endpoint1 = addTags('p','endpoint example: /quakeData?sortingOrder=mag|place|type|time')
    endpoint2 = addTags('p','endpoint example: /nestJson?sortingOrder=currency|country|city|town|amount')
    info1 = addTags('h3', 'Pass any number of keys as request parameter to /quakeData? endpoint and wait for a dynamic nested JSON!')
    info2 = addTags('h3', 'Pass a flat JSON body and provide a "|" seperated sorting order in POST request.')  
    usgsAPI = addTags('p', 'Data source: https://tinyurl.com/y5uttm6n')
    return apiName+info1+endpoint1+keyList+keyDetail+usgsAPI+endpoint2+info2

@app.route('/quakeData', methods=['GET'])
@basic_auth.required
def nestGeoJson():
    try: 
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojsonp"
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        date = urllib.request.urlopen(req)
    except urllib2.URLError as e:
        res = make_response('Earthquake feed unavailable: '+ str(e.reason), 500)
        return res
    except Exception:
        res = make_response('Earthquake feed unavailable: ', 500)
        return res  
    
    geoData = data.read()
    geoData = geoData[16:-2]
    geoDataStr = geoData.decode('utf8').replace('\u0101', '')

    #Load files from local director
    """with open('input.json', 'r') as myfile:
        geoDataStr= myfile.read()"""

    jsonData = json.loads(geoDataStr)
    order = request.args.get('sortingOrder')
    sortingOrder = order.split('|')
    
    flatToNested = FlatToNested()
    flatToNested.newDict('nestedJson')
    filteredJson = flatToNested.filterJson(sortingOrder, jsonData)
    nestedJson = flatToNested.nestJson(sortingOrder, filteredJson)

    geoJsonData = json.dumps(nestedJson, indent=2)
    with open('output.json', 'w') as fp:
        print(geoJsonData, file=fp)

    response_body = geoJsonData
    res = make_response(response_body, 200)
    return res

@app.route('/nestJson', methods=['POST'])
@basic_auth.required
def flatToNestJson():
    if request.is_json:
        flatJson = request.get_json()
        order = request.args.get('sortingOrder')
        
        flatToNested = FlatToNested()
        flatToNested.newDict('nestedJson')
        sortingOrder = order.split('|')
        nestedJson = flatToNested.nestJson(sortingOrder, flatJson)
        response_body = nestedJson
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

if __name__ == '__main__':
   app.run()