from shapely.geometry import Point, Polygon

class NLocation:
    def __init__(self, lat, lon, zoom = 16):
        self.lat = lat if type(lat) == 'float' else float(lat)
        self.lon = lon if type(lon) == 'float' else float(lon)
        self.zoom = zoom

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

class NMap:
    def __init__(self, shape_vertexs = []) -> None:
        self.polys = [Polygon(vs) for vs in shape_vertexs]
    def is_in(self, loc : NLocation):
        p = Point(loc.lat, loc.lon)
        for poly in self.polys:
            if p.within(poly) is True:
                return True
        return False

class NSector:
    def __init__(self, name, loc, no, city, divisition, vertex) -> None:
        self.divisition = divisition
        self.city = city
        self.name = name
        self.loc = loc # type: NLocation
        self.no = no
        self.map = NMap(vertex)
    def get_param(self):
        around = self.loc.get_around_param()
        around.update({'cortarNo': self.no})
        return around
    def __str__(self) -> str:
        return "%s %s %s %s %s" % (self.city, self.divisition, self.name, self.no, self.loc)

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
        self.mn = mn if mn != 0 else None
        self.mx = mx if mx != 0 else None
        self.med = med if med != 0 else None

    def __str__(self) -> str:
        return "%f %f" % (self.mn, self.mx)

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
