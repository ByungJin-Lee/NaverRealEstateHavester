from haversine import haversine
from nre.con import *
import requests

BASE_API_URL = "https://new.land.naver.com/api/"
IS_LOGGING = True

def get(url = "", params = {}):
    if IS_LOGGING is True : print('Get', BASE_API_URL + url)
    rep = requests.get(BASE_API_URL + url, params=params, headers={'User-Agent': '*'})
    if rep.status_code != 200: raise Exception('Response Error')
    return rep.json()

def get_neighborhood(loc : NLocation, nType = ''):
    param = loc.get_around_param()
    param.update({ 'type' : nType, 'zoom' : loc.zoom })
    res = get(NRE_ROUTER.NEIGHBORHOOD, param)
    return parse_neighbor(res)

def make_param_thing(sector : NSector, addon : NAddon = NAddon.get_default()):
    param = {
        'zoom': sector.loc.zoom,
        'priceType': 'RETAIL',
        'markerId': '',
        'markerType': '',
        'selectedComplexNo': '',
        'selectedComplexBuildingNo': '',
        'fakeComplexMarker': '',
        'tag': '::::::::',
        'rentPriceMin':0,
        'rentPriceMax':900000000,
        'priceMin':0,
        'priceMax': 900000000,
        'areaMin':0,
        'areaMax':900000000,
        'oldBuildYears':'',
        'recentlyBuildYears':'',
        'minHouseHoldCount':'',
        'maxHouseHoldCount':'',
        'showArticle':True,
        'sameAddressGroup':False,
        'minMaintenanceCost':'',
        'maxMaintenanceCost':'',
    }
    param.update(sector.get_param())
    param.update(addon.get_param())
    return param

def get_things(sector: NSector, addon = NAddon.get_default()):
    res = get(NRE_ROUTER.COMPLEX2, make_param_thing(sector, addon))
    return parse_things(res)

def make_param_sector(loc : NLocation):
    return  {'centerLat':loc.lat, 'centerLon':loc.lon, 'zoom': loc.zoom}

def get_sector(loc : NLocation):
    res = get(NRE_ROUTER.CORTARS, make_param_sector(loc))
    return parse_sector(res)

def make_param_region(code):
    return {'cortarNo': code}

def get_region_list(code = "0000000000"):
    res = get(NRE_ROUTER.REGION_LIST, make_param_region(code))
    return parse_region(res)

def parse_region(region_obj = {}):
    if len(region_obj) < 1:
        return []
    regions = [] # type: list[NRegion]
    for obj in region_obj['regionList']:
        regions.append(NRegion(
            obj['cortarName'],
            NLocation(obj['centerLat'], obj['centerLon']), 
            obj['cortarNo']))
    return regions

def parse_sector(sector_json : dict):
    return NSector(sector_json['sectorName'], NLocation(sector_json['centerLat'], sector_json['centerLon']) , sector_json['sectorNo'], sector_json['cityName'], sector_json['divisionName'], sector_json['cortarVertexLists'])

def parse_neighbor(data):
    res = [] # type: list[NNeighbor]
    nType = data['type']
    for v in data['neighborhoods']:
        res.append(NNeighbor(
            nType,
            v['name'],
            NLocation(v['latitude'], v['longitude'])
        ))
    return res

def parse_things(results):
    res = [] # type: list[NThing]
    for v in results:
        if 'minDealPrice' not in v and 'minLeasePrice' not in v:
            continue
        if v['dealCount'] == 0 and v['leaseCount'] == 0:
            continue
        res.append(NThing(
            v['complexName'],
            v['realEstateTypeName'],
            v['completionYearMonth'],
            NLocation(v['latitude'], v['longitude']),
            NArea(v['minArea'], v['maxArea'], v['representativeArea'], v['floorAreaRatio']),
            NPrice(v['minDealPrice'], v['maxDealPrice'], None if 'medianDealPrice' not in v else v['medianDealPrice']),
            NPrice(v['minLeasePrice'],v['maxLeasePrice'] , None if 'medianLeasePrice' not in v else v['medianLeasePrice']),
            NPrice(v['minDealUnitPrice'], v['maxDealUnitPrice'], None if 'medianDealUnitPrice' not in v else v['medianDealUnitPrice']),
            NPrice(v['minLeaseUnitPrice'], v['maxLeaseUnitPrice'], None if 'medianLeaseUnitPrice' not in v else  v['medianLeaseUnitPrice'])
        ))
    return res

def distance_between(l1 : NLocation, l2 : NLocation):
    return round(haversine(l1.get_tuple(), l2.get_tuple(), unit='m'))

def get_distance_standard(standard = {}):
    default_standard = {
        'BUS': 500,
        'METRO' : 500,
        'INFANT' : 750,
        'PRESCHOOL' : 750,
        'SCHOOLPOI' : 2000,
        'HOSPITAL' : 5000,
        'PARKING' : 500,
        'MART' : 500,
        'CONVENIENCE': 250,
        'WASHING': 500,
        'BANK' : 1000,
        'OFFICE' : 2000
    }
    default_standard.update(standard)
    return default_standard