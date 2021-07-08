import csv
import pandas as pd
import numpy as np

#csvを読み込みリストに変換する関数
def make_data_from_csv(csv_file_path):

  
    #一行目をheaderとして、csv読み込み
    df = pd.read_csv(csv_file_path, header=1, encoding='shift-jis')   
    df = df.drop(df.columns[0],axis='columns')#0列目を削除

    return df

#座標のdfを並び替える関数
def sort_df_xyz(df_xyz):
    df_xyz = df_xyz.sort_values(['中心(X)', '中心(Y)', '中心(Z)'])
    return df_xyz



#大小関係の数値誤差を抑制する変数
mod = 0.00001
#Δx,Δy,Δzを計算する関数  #x_array,y_arrayの値が変わる位置を計算する関数
def delta_df_xy(df_xyz, col_num):#col_num=1 == 中心(x)
    
    col_name = df_xyz.columns[col_num]#列の名前
    delta_col_name = df_xyz.columns[col_num+3]#Δ列の名前

    delta_x_array = np.empty(0)#delta_xのarray
    x_array = df_xyz[col_name].to_numpy()#xのarray

    x_change_num_list = []#x_arrayの値が変わる位置のlist

    #m-1
    x_before = None 
    delta_x_before = None

    for i in range(len(df_xyz)):
        x = x_array[i]

        #xm < xm-1
        if ( i == 0) or ( x+mod < x_before):
            x_next = cal_x_next(x_array, i) 
            delta_x = abs(x_next - x)
            x_change_num_list.append(i)
        #xm > xm-1
        elif (x > x_before+mod):
            delta_x = 2*((x - x_before) - 1/2 * delta_x_before)
            x_change_num_list.append(i)
        #xm = xm-1
        elif(x == x_before):
            delta_x = delta_x_before
        
        delta_x_array = np.append(delta_x_array, delta_x)

        delta_x_before = delta_x
        x_before = x

    #delta_xのarrayをdfに代入
    df_xyz[delta_col_name] = delta_x_array
    return df_xyz, x_change_num_list
        
#x_nextを求める関数
def cal_x_next(x_array, i):
    x = x_array[i]
    while True:
        i+=1
        x_next = x_array[i]
        if (x_next > x+mod):
            break
    
    return x_next


#delta_zを計算する関数
def delta_df_z(df_xyz, y_changes_num_list):
    col_name = df_xyz.columns[3]#z(中心)列の名前
    delta_col_name = df_xyz.columns[3+3]#Δ列の名前

    delta_z_array = np.empty(0)#delta_zのarray
    z_array = df_xyz[col_name].to_numpy()#zのarray

    z_top = 0
    i = 0
    y_changes_num_list.append(len(z_array))
    while True:
        z1_num = y_changes_num_list[i]
        zf_num = y_changes_num_list[i+1] - 1
        #zf_num = cal_zf_num(z_array,z1_num)
        z_array_divided = z_array[z1_num :zf_num+1]#z_arrayから抽出
        if (i != 0):#z_topを計算
            zf = z_array[zf_num]
            z_top = z_top + (zf - zf_old)
        
        delta_z_array_divided, zf_old = cal_delta_z(z_array_divided, z_top)
        delta_z_array = np.append(delta_z_array, delta_z_array_divided)
        
        #TODO z_cを計算

        if(zf_num+1 == len(z_array)):
            df_xyz[delta_col_name] = delta_z_array  #df_xyzに書き込み
            return df_xyz

        z1_num = zf_num + 1
        i+=1


#Δzを計算する関数
def cal_delta_z(z_array_divided, z_top):
    delta_z_divided_list = []
    for i in range(len(z_array_divided)):
        z_m = z_array_divided[len(z_array_divided)-i-1]#zfから取り出し
        

        if (i == 0):#zfの場合
            delta_z = 2*abs(z_top - z_m)
            z_f = z_m
        else:

            delta_z = 2*(abs(z_m_before - z_m)-delta_z_before/2)
        
        z_m_before = z_m#zm+1
        delta_z_before = delta_z#Δzm+1

        delta_z_divided_list.append(delta_z)
               
    delta_z_divided_list.reverse()#反転
    delta_z_divided_array = np.array(delta_z_divided_list)
    return delta_z_divided_array, z_f



#hを計算する関数
def cal_h_zc(df_xyz, y_changes_num_list):
    z_col_name = df_xyz.columns[3]#z(中心)列の名前
    z_array = df_xyz[z_col_name].to_numpy()#zのarray

    delta_z_col_name = df_xyz.columns[3+3]#Δ列の名前
    delta_z_array = df_xyz[delta_z_col_name].to_numpy()#delta_zのarray

    h_array = np.empty(0)#hのarray
    zc_array = np.empty(0)#zcのarray
    
    y_changes_num_list = y_changes_num_list[:-1]#y_change_num_listに余計なものがあるので修正した

    for i in range(len(y_changes_num_list)):
        z1_col_num = y_changes_num_list[i]
        z1 = z_array[z1_col_num]
        delta_z1 = delta_z_array[z1_col_num]

        if (i != len(y_changes_num_list)-1):
            zf_col_num = y_changes_num_list[i+1] - 1
        else:
            zf_col_num = len(df_xyz) - 1
            
        zf = z_array[zf_col_num]
        delta_zf = delta_z_array[zf_col_num]


        z_top = zf + delta_zf / 2
        z_bottom = z1 - delta_z1 /2
        #h,zcを計算
        h = (z_top - z_bottom)
        zc = (z_top + z_bottom) / 2
        #同じ値のリストを作成
        same_h_zc_num = zf_col_num - z1_col_num + 1
        h_list_divided = [h]* same_h_zc_num
        zc_list_divided = [zc] * same_h_zc_num

        h_array = np.append(h_array, h_list_divided)
        zc_array = np.append(zc_array, zc_list_divided)
    
    #df_xyzに書き込み
    df_xyz['h'] = h_array
    df_xyz['zc'] = zc_array

    return df_xyz    





    


















#dataを結合する関数
def combine(data1,data2):
    combined_data = []
    if len(data1) != len(data2):
        print('要素数が異なります')
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
    cal_I = h**3/12

    return cal_I

#θLを計算
def cal_theta_L(data, z_list, delta_y_list, delta_z_list, intrinsic_x_list, h, I):
    theta_L = 0
    for i in range(len(data)):
        z = z_list[i]
        delta_y = delta_y_list[i]
        delta_z = delta_z_list[i]
        intrinsic_x = intrinsic_x_list[i]        
        theta_L += delta_y * delta_z * (z + h/2) * intrinsic_x
        
    return theta_L/I


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

