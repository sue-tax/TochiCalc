'''
Created on 2024/09/18

@author: sue-t
'''

if __name__ == '__main__':
    pass

from lxml import etree

str_file_name = '27128-1200-38.xml'
list_chiban = (('城見', '２丁目', '2-6'), ('城見', '２丁目', '2-1'), ('城見', '２丁目', '2-7'))

g_chiban_keijo = {}  # { '城見', '119') : 'F000000xxx' , ... }
g_chiban_kyokai = {}  # { '119': 境界リスト, ... }
                        # 境界 ("C0000xxxxx", P1, P2))
g_point_set = set()     # { (P1,P2), ... }
g_jogai_point_set = set()   # [ P9, P8, ... ]
g_point_list = []     # [ P1, P2, ... ]
g_zahyo_list = []   # [(x,y), ... ]


tree = etree.parse(str_file_name)
root = tree.getroot()
_nm = {}
_nm['nm'] = root.nsmap[None]
_nm['zmn'] = root.nsmap["zmn"]
_nm['xsi'] = root.nsmap["xsi"]

for chiban in list_chiban:
    if chiban[1] == '':
        str_xml_hitsu = './/nm:筆/nm:大字名[text()="' + \
                chiban[0] + '"]/../nm:地番[text()="' + \
                chiban[2] + '"]/..' 
    else:
        str_xml_hitsu = './/nm:筆/nm:大字名[text()="' + \
                chiban[0] + '"]/../nm:丁目名[text()="' + \
                chiban[1] + '"]/../nm:地番[text()="' + \
                chiban[2] + '"]/..' 
    # print(str_xml_hitsu)
    list_hitsu = tree.xpath(str_xml_hitsu, namespaces=_nm)
    if len(list_hitsu) != 1:
        print("エラー", chiban[0], chiban[1], chiban[2], len(list_hitsu), "筆")
        exit(-1)
    # print(list_hitsu[0])
    list_keijo = list_hitsu[0].xpath('./nm:形状/@idref', namespaces=_nm)
    if len(list_keijo) != 1:
        print("エラー", chiban[0], chiban[1], chiban[2], len(list_keijo), "形状")
        exit(-1)
    # print(list_keijo[0])
    g_chiban_keijo[chiban] = list_keijo[0] 
# print("フェイズ１")
# print(g_chiban_keijo)

for (ooaza, choume, chiban), keijo in g_chiban_keijo.items():
    str_xml_surface = './/zmn:GM_Surface[@id="' + \
        keijo + '"]'
    # print(str_xml_surface)
    list_surface = tree.xpath(str_xml_surface, namespaces=_nm)
    if len(list_surface) != 1:
        print("エラー", ooaza, choume, chiban, keijo, len(list_surface), "surface")
        exit(-1)
    # print(list_surface[0])
    str_xml_surface_curve = './/zmn:GM_CompositeCurve.generator'
    list_surface_curve = list_surface[0].xpath(str_xml_surface_curve,
            namespaces=_nm)
    if len(list_surface_curve) == 0:
        print("エラー", ooaza, choume, chiban, keijo, len(list_surface_curve), "curve")
        exit(-1)
    # print(list_surface_curve)
    list_kyokai = []
    for curve in list_surface_curve:
        str_xml_curve = './/zmn:GM_Curve[@id="' + \
                curve.get("idref") + '"]'
        # print(str_xml_curve)
        list_curve = tree.xpath(str_xml_curve, namespaces=_nm)
        if len(list_curve) != 1:
            print("エラー",  ooaza, chiban, keijo, curve.get("idref"), len(list_curve), "curve")
            exit(-1)
        # print(list_curve[0])
        str_xml_curve_point = './/zmn:GM_PointRef.point' # /@idref'
        # print(str_xml_curve_point)
        list_point = list_curve[0].xpath(str_xml_curve_point, namespaces=_nm)
        if len(list_point) != 2:
            print("エラー",  ooaza, choume, chiban, keijo, curve.get("idref"), len(list_point), "point")
            exit(-1)
        list_kyokai.append((curve.get("idref"),
                list_point[0].get("idref"), list_point[1].get("idref")))
        # print(list_kyokai)
    g_chiban_kyokai[(ooaza, choume, chiban)] = list_kyokai
# print("フェイズ２")
# print(g_chiban_kyokai)

list_kyokai_point = []
for chiban_kyokai in g_chiban_kyokai.values():
    for kyokai in chiban_kyokai:
        list_kyokai_point.append((kyokai[1], kyokai[2]))
# print(list_kyokai_point)
while len(list_kyokai_point) > 0:
    kyokai_point = list_kyokai_point.pop(0)
    if kyokai_point in list_kyokai_point:
        g_jogai_point_set.add(kyokai_point[0])
        g_jogai_point_set.add(kyokai_point[1])
        list_kyokai_point.remove(kyokai_point)
    elif (kyokai_point[1], kyokai_point[0]) in list_kyokai_point:
        g_jogai_point_set.add(kyokai_point[0])
        g_jogai_point_set.add(kyokai_point[1])
        list_kyokai_point.remove(
                (kyokai_point[1], kyokai_point[0]))
    else:
        g_point_set.add(kyokai_point)
# print("フェイズ３")
# print(g_point_set)
# print(len(g_point_set))
# print(list_kyokai_point)
# print(g_jogai_point_set)

# jogai_point_setから、g_point_setに含まれるものを除外する
for point in g_point_set:
    if point[0] in g_jogai_point_set:
        g_jogai_point_set.remove(point[0])
    if point[1] in g_jogai_point_set:
        g_jogai_point_set.remove(point[1])
# print("フェイズ４")
# print(g_jogai_point_set)

# g_point_set から、順番にポイントをリストに
(point0, point1) = g_point_set.pop()
g_point_list.append(point0)
g_point_list.append(point1)
while True:
    for (pointA, pointB) in g_point_set:
        if pointA == point1:
            g_point_list.append(pointB)
            g_point_set.remove((pointA, pointB))
            point1 = pointB
            break
        elif pointB == point1:
            g_point_list.append(pointA)
            g_point_set.remove((pointA, pointB))
            point1 = pointA
            break
    if len(g_point_set) == 0:
        g_point_list.remove(point1)
        break
# print("フェイズ５")
# print(g_point_list)
# print(g_point_set)

# 順番に座標をリストに
for point in g_point_list:
    str_xml_point = './/zmn:GM_Point[@id="' + \
            point + '"]'
    list_point = tree.xpath(str_xml_point, namespaces=_nm)
    if (len(list_point) != 1):
        print("エラー",  point, len(list_point), "point")
        exit(-1)
    list_x = list_point[0].xpath('.//zmn:X/text()', namespaces=_nm)
    if (len(list_x) != 1):
        print("エラー",  point, "X", len(list_x))
        exit(-1)
    list_y = list_point[0].xpath('.//zmn:Y/text()', namespaces=_nm)
    if (len(list_x) != 1):
        print("エラー",  point, "Y", len(list_x))
        exit(-1)
    g_zahyo_list.append((list_x[0], list_y[0]))
# print("フェイズ６")
# print(g_zahyo_list)

print("================================")
print("土地内部のポイント")
for jogai_point in g_jogai_point_set:
    print(jogai_point)
if len(g_jogai_point_set) == 0:
    print("なし")
print("================================")
for point_pair in zip(g_point_list, g_zahyo_list):
    print(point_pair)
print("================================")
for point in g_point_list:
    print(point)
print("-------------------------------")
for zahyo in g_zahyo_list:
    print(float(zahyo[0]), ",", float(zahyo[1]))
print("-------------------------------")
print(len(g_point_list))