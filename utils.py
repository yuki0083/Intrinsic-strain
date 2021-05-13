import csv

#csvを読み込みリストに変換する関数
def make_data_from_csv(csv_file_path):
    data_from_csv = []
    with open(csv_file_path) as f:
        reader = csv.reader(f)
        row_num = 0
        for row in reader:
            # 先頭の2行を無視
            row_num += 1
            if row_num <= 2:
               continue
            # float型に変換
            col_num = 0
            for i in row:
                row[col_num] = float(i)
                col_num += 1
            data_from_csv.append(row)
        return data_from_csv




#dataを結合する関数
def combine(data1,data2):
    combined_data = []
    if len(data1) != len(data2):
        print('列の数が異なります')
        return

    for i in range(len(data1)):
        if data1[i][1] != data2[i][1]:
            print('要素番号が異なります')
            return
        else:
           combined_col = data1[i] + data2[i][2:]
        combined_data.append(combined_col)

    return combined_data





#xyz_intrinsic_dataをxの値で分割する関数
def x_divide(xyz_intrinsic_data):
    x_dict = {}
    x_dict_value = []

    x_before = xyz_intrinsic_data[0][2]#x_before = 0.165017

    for col_xyz_intrinsic in xyz_intrinsic_data:
        x_after = col_xyz_intrinsic[2]
        if x_before < x_after:#x方向に隣に移動したとき
            x_dict[x_before] = x_dict_value
            x_dict_value = []
            x_before = x_after
        x_dict_value.append(col_xyz_intrinsic)

    # xの値をリストにまとめる
    x_dict_keys = []
    for x in x_dict.keys():
        x_dict_keys.append(x)

    return x_dict, x_dict_keys

#Δxを計算
def calculata_deltax(x_dict_keys,i):
    if i == 0:
        delta_x = x_dict_keys[i]*2
    else:
        delta_x = x_dict_keys[i]-x_dict_keys[i-1]#Δxを計算

    return delta_x




#data(同じxで分割したデータ)からΔyΔzを計算
def calculate_deltay_and_deltaz(data):
    # yi ziを計算
    yi = []
    zi = []

    for j in range(len(data)):
        yi.append(data[j][3])
        zi.append(data[j][4])
    # ΔyΔzを計算
    delta_y = []
    delta_z = []

    l = 0  # yi+1 < yi となってからの数
    y_before = yi[0]

    delta_z_when_changed_list = []  # 変化(一段下がった時)Δzを保存
    for k in range(len(data)):  # k=60

        if yi[k] > y_before:  # 通常時
            # Δyを計算
            l += 1
            sum_yil = sum(delta_y[k - l:])
            delta_y.append(2 * (yi[k] - sum_yil))

            # Δzを計算
            delta_z.append(abs(delta_z[k - l]))

        else:
            # Δyを計算
            delta_y.append(2 * yi[k])
            l = 0
            y_before = yi[0]
            # Δzを計算
            sum_delta_z = sum(delta_z_when_changed_list)
            delta_z_when_changed = 2 * (abs(zi[k]) - sum_delta_z)
            delta_z_when_changed_list.append(delta_z_when_changed)

            delta_z.append(delta_z_when_changed)

    return delta_y, delta_z

 # εx*,εy*,zをdataから取り出す
def extract_from_data_to_list(data, row_num):
    extracted_list = []
    for col in data:
        extracted_list.append(col[row_num])

    return extracted_list

# δLを計算を計算する関数
def cal_delta_L(data, delta_z_list, delta_y_list, intrinsic_x_list, h):
    delta_L = 0
    for i in range(len(data)):
        delta_z = delta_z_list[i]
        delta_y = delta_y_list[i]
        intrinsic_x = intrinsic_x_list[i]

        delta_L += delta_y * delta_z * intrinsic_x
    return delta_L/h

# δTを計算を計算する関数
def cal_delta_T(data, delta_z_list, delta_y_list, intrinsic_y_list, h):
    delta_T = 0
    for i in range(len(data)):
        delta_z = delta_z_list[i]
        delta_y = delta_y_list[i]
        intrinsic_y = intrinsic_y_list[i]

        delta_T += delta_y * delta_z * intrinsic_y
    return delta_T/h

#Iを計算
def cal_I(data, z_list, delta_x, delta_z_list, h):
    cal_I = 0
    for i in range(len(data)):
        z = z_list[i]
        delta_z = delta_z_list[i]
        cal_I += delta_x * delta_z * ((z + h/2)**2)

    return cal_I
""" 
#θLを計算
def cal_theta_L(data, z_list, delta_x, delta_z_list, intrinsic_x_list, h, I):
    theta_L = 0
    for i in range(len(data)):
        z = z_list[i]
        delta_z = delta_z_list[i]
        intrinsic_x = intrinsic_x_list[i]        
        theta_L += delta_x * delta_z * (z + h/2) * intrinsic_x
        
    return theta_L/I
"""

# θTを計算
def cal_theta_T(data, z_list, delta_y_list, delta_z_list, intrinsic_y_list, h, I):
    theta_T = 0
    for i in range(len(data)):
        z = z_list[i]
        delta_y = delta_y_list[i]
        delta_z = delta_z_list[i]
        intrinsic_y = intrinsic_y_list[i]
        theta_T += delta_y * delta_z * (z + h / 2) * intrinsic_y

    return theta_T / I

