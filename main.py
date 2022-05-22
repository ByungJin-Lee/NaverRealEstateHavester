import havester as hv

# loc = hv.NLocation(35.18213, 128.1366) # 진주 충무공동
loc = hv.NLocation(37.49911, 127.065463) # 강남 대치동

sector = hv.NSector.parse_sector_json(
    hv.get_sector(loc).json()
)

print(sector)

# #남양에 전세, 매매, 오피스텔, 아파트
# addon = hv.NAddon(
#     [
#         hv.NAddon.DIR_SS
#     ],
#     [
#         hv.NAddon.TRADE_DEAL,
#         hv.NAddon.TRADE_LEASE
#     ],
#     [
#         hv.NAddon.ESTATE_APT,
#         hv.NAddon.ESTATE_OPST
#     ]
# )

# # rep = havester.get_price(sector, addon=addon)

# rep = havester.get_neighborhood(sector.loc, hv.NNeighbor.BUS)

# print(rep.request.url)

# if rep.status_code == 200:
#     res = hv.NNeighbor.parse_neighbor_json(rep.json())

#     for v in res:
#         print(v)

#     # for v in NREResult.parse_result_list(res):
#     #     print(v)