# a = [
#
# {'zm': 'A', 'title': '奥迪', 'id': 3},
# {'zm': 'A', 'title': '阿尔法-罗密欧', 'id': 50},
# {'zm': 'B', 'title': '保时捷', 'id': 4},
# {'zm': 'B', 'title': '奔驰', 'id': 1},
# {'zm': 'B', 'title': '宝马', 'id': 6},
# {'zm': 'B', 'title': '奔驰唯雅诺3.0', 'id': 7},
# {'zm': 'B', 'title': '本田', 'id': 14},
# {'zm': 'B', 'title': '宾利', 'id': 19},
# {'zm': 'B', 'title': '宝马5系', 'id': 21},
# {'zm': 'B', 'title': '北汽', 'id': 23},
# {'zm': 'B', 'title': '比亚迪', 'id': 26},
# {'zm': 'B', 'title': '标致', 'id': 42},
# {'zm': 'B', 'title': '别克', 'id': 2},
# {'zm': 'C', 'title': '传祺', 'id': 37},
# {'zm': 'D', 'title': '大通', 'id': 27},
# {'zm': 'D', 'title': '大众', 'id': 13},
# {'zm': 'F', 'title': '丰田', 'id': 5},
#
# ]
# temp = []
# c = ""
# for i in range(65,91):
#     temp.append({chr(i): [],"zm":chr(i)})
#
# for ii in temp:
#     for i in a:
#         t = ii.get(i["zm"], None)
#         if t != None:
#             ii[i["zm"]].append(i)
#
#
# for i in temp:
#     print(i[i["zm"]])