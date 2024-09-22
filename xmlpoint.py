'''
Created on 2024/09/18

@author: sue-t
'''
# https://houmukyoku.moj.go.jp/gifu/content/001342280.pdf
# https://www.moj.go.jp/content/000116464.pdf

__version__ = '0.03'

if __name__ == '__main__':
    pass

from lxml import etree

str_file_name = '27128-1200-38.xml'
list_chiban = {('城見', '２丁目', '', '2-6'), ('城見', '２丁目', '', '2-1'), ('城見', '２丁目', '', '2-7')}
# list_chiban = {('城見', '１丁目', '', '3-1'), ('城見', '１丁目', '', '4-1') }

# str_file_name = '23202-1803-19.xml'
# list_chiban = {('井田町', '', '字二本木東', '37') }

str_file_name = '27106-1203-8.xml'
list_chiban = {('千代崎', '３丁目', '', '15-1'), ('千代崎', '３丁目', '', '15-1'), ('千代崎', '３丁目', '', '15-2'),('千代崎', '３丁目', '', '15-3'),('千代崎', '３丁目', '', '15-4'),('千代崎', '３丁目', '', '15-5'),('千代崎', '３丁目', '', '15-6'),('千代崎', '３丁目', '', '15-7')}
list_chiban = {('千代崎', '３丁目', '', '19')}
list_chiban = {('千代崎', '３丁目', '', '15-1'), ('千代崎', '３丁目', '', '15-1'), ('千代崎', '３丁目', '', '15-2'),('千代崎', '３丁目', '', '15-3'),('千代崎', '３丁目', '', '15-4'),('千代崎', '３丁目', '', '15-5'),('千代崎', '３丁目', '', '15-6'),('千代崎', '３丁目', '', '15-7'), ('千代崎', '３丁目', '', '19')}

display_flag = 1    # 0

g_chiban_keijo = {}  # { '城見', '119') : 'F000000xxx' , ... }
g_chiban_kyokai = {}  # { '119': 境界リスト, ... }
                        # 境界 ("C0000xxxxx", P1, P2))
g_point_set = set()     # { (P1,P2), ... }
g_point_dict0 = {}      # { P1: (P2,P3), ... }
g_point_dict1 = {}      # { P2: (P1,P4), ... }
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
    if len(chiban) != 4:
        print("エラー",
                "土地は、大字名・丁目名・小字名・地番で指定します")
        exit(1)
    str_xml_hitsu = './/nm:筆'
    if chiban[0] != '':
        str_xml_hitsu += '/nm:大字名[text()="' + chiban[0] + '"]/..'
    if chiban[1] != '':
        str_xml_hitsu += '/nm:丁目名[text()="' + chiban[1] + '"]/..'
    if chiban[2] != '':
        str_xml_hitsu += '/nm:小字名[text()="' + chiban[2] + '"]/..'
    if chiban[3] != '':
        str_xml_hitsu += '/nm:地番[text()="' + chiban[3] + '"]/..'
    list_hitsu = tree.xpath(str_xml_hitsu, namespaces=_nm)
    if len(list_hitsu) != 1:
        print("エラー", chiban[0], chiban[1], chiban[2], chiban[3],
                len(list_hitsu), "筆")
        exit(-1)
    # print(list_hitsu[0])
    list_keijo = list_hitsu[0].xpath('./nm:形状/@idref',
            namespaces=_nm)
    if len(list_keijo) != 1:
        print("エラー", chiban[0], chiban[1], chiban[2], chiban[3],
                len(list_keijo), "形状")
        exit(-1)
    # print(list_keijo[0])
    g_chiban_keijo[chiban] = list_keijo[0]
del list_hitsu
del list_keijo 
print("フェイズ１")
# print(g_chiban_keijo)
print(len(g_chiban_keijo), "筆")

count_curve = 0
for (ooaza, choume, koaza, chiban), keijo in g_chiban_keijo.items():
    str_xml_surface = './/zmn:GM_Surface[@id="' + \
        keijo + '"]'
    # print(str_xml_surface)
    list_surface = tree.xpath(str_xml_surface, namespaces=_nm)
    if len(list_surface) != 1:
        print("エラー", ooaza, choume, koaza, chiban, keijo,
                len(list_surface), "surface")
        exit(-1)
    # print(list_surface[0])
    str_xml_surface_curve = './/zmn:GM_CompositeCurve.generator'
    list_surface_curve = list_surface[0].xpath(
            str_xml_surface_curve, namespaces=_nm)
    if len(list_surface_curve) == 0:
        print("エラー", ooaza, choume, koaza, chiban, keijo,
                len(list_surface_curve), "curve")
        exit(-1)
    # print(list_surface_curve)
    list_kyokai = []
    for curve in list_surface_curve:
        str_xml_curve = './/zmn:GM_Curve[@id="' + \
                curve.get("idref") + '"]'
        # print(str_xml_curve)
        list_curve = tree.xpath(str_xml_curve, namespaces=_nm)
        if len(list_curve) != 1:
            print("エラー",  ooaza, choume, koaza, chiban, keijo,
                    curve.get("idref"), len(list_curve), "curve")
            exit(-1)
        # print(list_curve[0])
        str_xml_curve_point = './/zmn:GM_PointRef.point'
        # print(str_xml_curve_point)
        list_point = list_curve[0].xpath(str_xml_curve_point,
                namespaces=_nm)
        if len(list_point) != 2:
            print("エラー",  ooaza, choume, chiban, keijo,
                    curve.get("idref"), len(list_point), "point")
            exit(-1)
        # list_kyokai.append((curve.get("idref"),
        #         list_point[0].get("idref"),
        #         list_point[1].get("idref")))
        # バージョンアップ
        curve_id = curve.get("idref")
        pointA = list_point[0].get("idref")
        pointB = list_point[1].get("idref")
        # ポイントの順番を、ここで特定
        if pointA < pointB:
            list_kyokai.append((curve_id, pointA, pointB))
        else:
            list_kyokai.append((curve_id, pointB, pointA))
        # print(list_kyokai)
        count_curve += 1
    g_chiban_kyokai[(ooaza, choume, chiban)] = list_kyokai
del list_surface
del list_curve
print("フェイズ２")
# print(g_chiban_kyokai)
print(len(g_chiban_kyokai), "筆")
print(count_curve, "境界")
# カーブ数もカウントして表示

set_kyokai_point = set()
for list_kyokai in g_chiban_kyokai.values():
    for kyokai in list_kyokai:
        # バージョンアップ
        # 常に、[1] < [2]
        if (kyokai[1], kyokai[2]) in set_kyokai_point:
            g_jogai_point_set.add(kyokai[1])
            g_jogai_point_set.add(kyokai[2])
            set_kyokai_point.remove((kyokai[1], kyokai[2]))
        else:
            set_kyokai_point.add((kyokai[1], kyokai[2]))
# print(set_kyokai_point)
while len(set_kyokai_point) > 0:
    kyokai_point = set_kyokai_point.pop()
    g_point_set.add(kyokai_point)
del set_kyokai_point
print("フェイズ３")
# print(g_point_set)
# print(len(g_point_set))
# print(set_kyokai_point)
# print(g_jogai_point_set)
print(len(g_point_set), "ポイント")

# jogai_point_setから、g_point_setに含まれるものを除外する
for point in g_point_set:
    if point[0] in g_point_dict0:
        l = g_point_dict0[point[0]]
        l.append(point[1])
        g_point_dict0[point[0]] = l
    else:
        g_point_dict0[point[0]] = [point[1]]
    if point[1] in g_point_dict1:
        l = g_point_dict1[point[1]]
        l.append(point[0])
        g_point_dict1[point[1]] = l
    else:
        g_point_dict1[point[1]] = [point[0]]
    if point[0] in g_jogai_point_set:
        g_jogai_point_set.remove(point[0])
    if point[1] in g_jogai_point_set:
        g_jogai_point_set.remove(point[1])
print("フェイズ４")
# print(g_jogai_point_set)
# print(g_point_dict0)
# print(g_point_dict1)
print("除外", len(g_jogai_point_set), "ポイント")

# g_point_set から、順番にポイントをリストに
(point0, point1) = g_point_set.pop()
g_point_list.append(point0)
g_point_list.append(point1)
# print(point0)
# print(point1)
l = g_point_dict0[point0]
if len(l) == 1:
    if l[0] == point1:
        g_point_dict0.pop(point0)
else:
    l.remove(point1)
    g_point_dict0[point0] = l
l = g_point_dict1[point1]
if len(l) == 1:
    if l[0] == point0:
        g_point_dict1.pop(point1)
else:
    l.remove(point0)
    g_point_dict1[point1] = l
# print(g_point_dict0)
# print(g_point_dict1)
while True:
    # print(point1)
    # print(g_point_dict0)
    # print(g_point_dict1)
    if point1 in g_point_dict0:
        list_pointB = g_point_dict0[point1]
        if len(list_pointB) != 1:
            print("エラー", point1, list_pointB)
            exit(1)
        pointB = list_pointB[0]
        g_point_list.append(pointB)
        # print(point1, pointB)
        g_point_dict0.pop(point1, list_pointB)
        # g_point_dict1.pop(pointB, point1)
        l = g_point_dict1[pointB]
        if len(l) == 1:
            g_point_dict1.pop(pointB, l)
        else:
            l.remove(point1)
            g_point_dict1[pointB] = l
        g_point_set.remove((point1, pointB))
    elif point1 in g_point_dict1:
        list_pointB = g_point_dict1[point1]
        if len(list_pointB) != 1:
            print("エラー", point1, list_pointB)
            exit(1)
        pointB = list_pointB[0]
        g_point_list.append(pointB)
        # print(pointB, point1)
        g_point_dict1.pop(point1, list_pointB)
        l = g_point_dict0[pointB]
        if len(l) == 1:
            g_point_dict0.pop(pointB, l)
        else:
            l.remove(point1)
            g_point_dict0[pointB] = l
        # g_point_dict0.pop(point1, list_pointB)
        g_point_set.remove((pointB, point1))
    else:
        if point1 != g_point_list[0]:
            print("ERR")
            print(g_point_list)
            print(g_point_set)
            print(g_point_dict0)
            print(g_point_dict1)
            print("エラー",  point1, "つながる先がない")
            exit(-1)
        print(g_point_set)
        print("警告 指定された土地が隣接していない")
        break
    if len(g_point_set) == 0:
        g_point_list.remove(pointB)
        break
    point1 = pointB
print("フェイズ５")
# print(g_point_list)
# print(g_point_set)
print(len(g_point_list), "ポイント")

# 順番に座標をリストに
for point in g_point_list:
    str_xml_point = './/zmn:GM_Point[@id="' + \
            point + '"]'
    list_point = tree.xpath(str_xml_point, namespaces=_nm)
    if (len(list_point) != 1):
        print("エラー",  point, len(list_point), "point")
        exit(-1)
    list_x = list_point[0].xpath('.//zmn:X/text()',
            namespaces=_nm)
    if (len(list_x) != 1):
        print("エラー",  point, "X", len(list_x))
        exit(-1)
    list_y = list_point[0].xpath('.//zmn:Y/text()',
            namespaces=_nm)
    if (len(list_x) != 1):
        print("エラー",  point, "Y", len(list_x))
        exit(-1)
    g_zahyo_list.append((list_x[0], list_y[0]))
print("フェイズ６")
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
for point_pair in zip(g_point_list, g_zahyo_list):
    print(point_pair[0], ",", point_pair[1][0], ",", point_pair[1][1])
print("-------------------------------")
print(len(g_point_list))


if display_flag:
    import matplotlib.pyplot as plt
    
    plt.figure()
    
    x = []
    y = []
    for zahyo in g_zahyo_list:
        x.append(float(zahyo[0]))
        y.append(float(zahyo[1]))
    
    min_x = min(x) - 20
    max_x = max(x) + 20
    min_y = min(y) - 20
    max_y = max(y) + 20
    plt.gca().set_ylim(min_x, max_x)
    plt.gca().set_xlim(min_y, max_y)
    plt.gca().set_aspect(1)
    
    x.append(float(g_zahyo_list[0][0]))
    y.append(float(g_zahyo_list[0][1]))
    plt.plot(y, x, marker = "o")
    
    avgx = sum(x) / len(x)
    avgy = sum(y) / len(y) 
    a = 1
    l = 4
    for i in range(len(g_point_list)):
        if x[i] > avgx:
            signx = 1
        else:
            signx = -4
        if y[i] > avgy:
            signy = 2
        else:
            signy = -4 * l
        x0 = x[i] + signx * a
        y0 = y[i] + signy * a
        plt.text(y0, x0, g_point_list[i][len(g_point_list[i])-l:])
    
    plt.show()