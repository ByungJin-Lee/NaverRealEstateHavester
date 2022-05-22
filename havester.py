from tkinter import OFF
from haversine import haversine
import requests

BASE_API_URL = "https://new.land.naver.com/api/"
IS_LOGGING = True

class NRE_ROUTER:
    REGION_LIST='regions/list'
    CORTARS='cortars'
    COMPLEX2='complexes/single-markers/2.0'
    NEIGHBORHOOD='regions/neighborhoods'

class NNeighborAround:
    HEADER = ['BUS','METRO','INFANT','PRESCHOOL','SCHOOLPOI','HOSPITAL',
    'PARKING','MART','CONVENIENCE','WASHING','BANK','OFFICE']

    def __init__(self) -> None:
        self.counter = {
            'BUS': 0,
            'METRO' : 0,
            'INFANT' : 0,
            'PRESCHOOL' : 0,
            'SCHOOLPOI' : 0,
            'HOSPITAL' : 0,
            'PARKING' : 0,
            'MART' : 0,
            'CONVENIENCE': 0,
            'WASHING': 0,
            'BANK' : 0,
            'OFFICE' : 0
        }   

    def increase(self, tag = ''):
        self.counter[tag] += 1

    def get_list(self):
        return self.counter.values()

class NNeighbor:
    BUS = 'BUS' # 버스정류장
    METRO = 'METRO' # 지하철
    KID = 'INFANT' # 어린이집
    PRESCHOOL = 'PRESCHOOL' # 유치원
    SCHOOL = 'SCHOOLPOI' # 학교
    HOSPITAL = 'HOSPITAL' # 병원
    PARKING = 'PARKING' # 주차장
    MART = 'MART' # 마트
    CONVENIENCE = 'CONVENIENCE' # 편의점
    WASHING = 'WASHING' # 세탁소
    BANK = 'BANK' # 은행
    OFFICE = 'OFFICE' # 관공서

    EACH = [BUS, METRO, KID, PRESCHOOL, SCHOOL, HOSPITAL, PARKING, MART, CONVENIENCE, WASHING, BANK, OFFICE]

    def __init__(self, type, name, loc) -> None:
        self.type = type
        self.name = name
        self.loc = loc # type: NLocation
    
    def __str__(self) -> str:
        return "%s %s %s" % (self.type, self.name, self.loc)

class NArea:
    def __init__(self, mn, mx, representative, floorRatio) -> None:
        self.mn = mn
        self.mx = mx
        self.representative = representative
        self.floorRatio = floorRatio

class NPrice:
    def __init__(self, mn, mx, med) -> None:
        self.mn = mn
        self.mx = mx
        self.med = med
        self.avg = (mn + mx) / 2

    def __str__(self) -> str:
        return "%f %f" % (self.mn, self.mx)

class NLocation:
    def __init__(self, lat, lon):
        self.lat = lat if type(lat) == 'float' else float(lat)
        self.lon = lon if type(lon) == 'float' else float(lon)

    def get_around_param(self):
        return {
            'leftLon': self.lon - 0.0137329,
            'rightLon': self.lon + 0.0137329,
            'topLat': self.lat + 0.0069786,
            'bottomLat': self.lat - 0.0069786
        }

    def get_tuple(self):
        return (self.lat, self.lon)
        
    def __str__(self) -> str:
        return "loc(%f | %f)" % (self.lat, self.lon)

class NThing:
    HEADER = ['Name', 'Type', 'Build', 'Dir' ,'minArea', 'maxArea', 'representativeArea', 'floorAreaRatio', 
        'minDeal', 'maxDeal', 'medianDeal', 'minLease', 'maxLease', 'medianLease', 'minDealUnit', 'maxDealUnit', 'medianDealUnit', 'minLeaseUnit', 'maxLeaseUnit', 'medianLeaseUnit','Lat', 'Lon']

    def __init__(self, name, type, buildTime, loc, area, deal, lease, udeal, ulease) -> None:
        self.type = type
        self.buildTime = buildTime
        self.area = area # type: NArea
        self.name = name # type: str
        self.loc = loc # type: NLocation
        self.deal = deal # type: NPrice
        self.udeal = udeal # type: NPrice
        self.lease = lease # type: NPrice
        self.ulease = ulease # type: NPrice
        self.dir = ''
        self.neiAround = NNeighborAround()

    def get_list(self):
        return [self.name, self.type, self.buildTime, self.dir, self.area.mn, self.area.mx, self.area.representative, self.area.floorRatio,
        self.deal.mn, self.deal.mx, self.deal.med, self.lease.mn, self.lease.mx, self.lease.med, self.udeal.mn, self.udeal.mx, self.udeal.med, self.ulease.mn, self.ulease.mx, self.ulease.med, self.loc.lat, self.loc.lon]

    def __str__(self) -> str:
        return "%s %s %s %s | %s" % (self.name, self.type, self.buildTime, self.deal, self.lease)

class NSector:
    def __init__(self, name, loc, no, city, divisition) -> None:
        self.divisition = divisition
        self.city = city
        self.name = name
        self.loc = loc # type: NLocation
        self.no = no
    def get_param(self):
        around = self.loc.get_around_param()
        around.update({'cortarNo': self.no})
        return around
    def __str__(self) -> str:
        return "%s %s %s %s %s" % (self.city, self.divisition, self.name, self.no, self.loc)

class NRegion:
    def __init__(self, name='', loc = None, no = '') -> None:
        self.name = name
        self.loc = loc # type: NLocation
        self.no = no
    def __str__(self) -> str:
        return "%s %s %s" % (self.name, self.no, self.loc)

class NAddon:
    TRADE_DEAL = 'A1' #매매
    TRADE_LEASE = 'B1' #전세
    #월세 : 미구현 Don't use it!
    #TRADE_MON = 'B2'
    ##단기 임대 : 미구현 Don't use it! 
    TRADE_SHO = 'B3'
    ESTATE_APT = 'APT' #아파트
    ESTATE_APT_AREA = 'ABYG' #아파트 분양권
    ESTATE_APT_RESTRUCT = 'JGC' #재건축
    ESTATE_OPST = 'OPST' #오피스텔
    ESTATE_OPST_AREA = 'OBYG' #오피스텔 분양권
    ESTATE_REMAKE = 'JGB' #재개발
    DIR_EE = 'EE' #동
    DIR_ES = 'ES' #남동
    DIR_WW = 'WW' #서
    DIR_WS = 'WS' #남서
    DIR_SS = 'SS' #남
    DIR_EN = 'EN' #북동
    DIR_NN = 'NN' #북
    DIR_WN = 'WN' #북서
    DIR_EACH = [DIR_EE, DIR_ES, DIR_WW, DIR_WS, DIR_SS, DIR_EN, DIR_NN, DIR_WN]

    def __init__(self, direction = [], tradeType = [], estateType = []) -> None:
        self.direction = direction
        self.tradeType = tradeType
        self.estateType = estateType
    
    def get_param(self):
        return {
            'direction' : ':'.join(self.direction),
            'tradeType' : ':'.join(self.tradeType),
            'realEstateType' : ':'.join(self.estateType)
        }
    @classmethod
    def get_default(cls):
        return NAddon([], [cls.TRADE_DEAL], [cls.ESTATE_APT])

def get(url = "", params = {}):
    if IS_LOGGING is True : print('Get', BASE_API_URL + url)
    rep = requests.get(BASE_API_URL + url, params=params, headers={'User-Agent': '*'})
    if rep.status_code != 200: raise Exception('Response Error')
    return rep.json()

def get_neighborhood(loc : NLocation, nType = ''):
    param = loc.get_around_param()
    param.update({ 'type' : nType, 'zoom' : 16 })
    res = get(NRE_ROUTER.NEIGHBORHOOD, param)
    return parse_neighbor(res)

def get_things(sector: NSector, addon = NAddon.get_default()):
    con = {
        'zoom': 16,
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
        'showArticle':False,
        'sameAddressGroup':False,
        'minMaintenanceCost':'',
        'maxMaintenanceCost':'',
    }
    con.update(sector.get_param())
    con.update(addon.get_param())
    res = get(NRE_ROUTER.COMPLEX2, con)
    return parse_things(res)


def get_sector(loc : NLocation):
    res = get(NRE_ROUTER.CORTARS, {'centerLat':loc.lat, 'centerLon':loc.lon})
    return parse_sector(res)

def get_region_list(code = "0000000000"):
    res = get(NRE_ROUTER.REGION_LIST, {'cortarNo': code})
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
    return NSector(sector_json['sectorName'], NLocation(sector_json['centerLat'], sector_json['centerLon']) , sector_json['sectorNo'], sector_json['cityName'], sector_json['divisionName'])

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
        res.append(NThing(
            v['complexName'],
            v['realEstateTypeName'],
            v['completionYearMonth'],
            NLocation(v['latitude'], v['longitude']),
            NArea(v['minArea'], v['maxArea'], v['representativeArea'], v['floorAreaRatio']),
            NPrice(v['minDealPrice'], v['maxDealPrice'], '' if 'medianDealPrice' not in v else v['medianDealPrice']),
            NPrice(v['minLeasePrice'],v['maxLeasePrice'] , '' if 'medianLeasePrice' not in v else v['medianLeasePrice']),
            NPrice(v['minDealUnitPrice'], v['maxDealUnitPrice'], '' if 'medianDealUnitPrice' not in v else v['medianDealUnitPrice']),
            NPrice(v['minLeaseUnitPrice'], v['maxLeaseUnitPrice'], '' if 'medianLeaseUnitPrice' not in v else  v['medianLeaseUnitPrice'])
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