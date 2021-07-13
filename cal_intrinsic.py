#df_intrinsicをdf_xyzと同じように並び替える関数
def sort_df_intrinsic(df_intrinsic, df_xyz):
    df_intrinsic = df_intrinsic.reindex(index=df_xyz.index)
    return df_intrinsic

#xの値が変化する番号をリストに保存
# #TODO delta_df_xyzと同じ処理をしている
def cal_x_change_num_list_and_x(x_array):
    mod = 0.00001
    x_list = x_array.tolist()
    x_change_num_list = []
    x_change_list = []

    for i in range(len(x_array)):
        x = x_list[i]
        if ( i == 0) or ( x+mod < x_before):
            x_change_num_list.append(i)
            x_change_list.append(x)
        #xm > xm-1
        elif (x > x_before+mod):
            x_change_num_list.append(i)
            x_change_list.append(x)
        #xm = xm-1
        elif(x == x_before):
            pass
        x_before = x
    
    return x_change_num_list, x_change_list





# δx*を計算する関数
def cal_inherent_x(df_xyz, df_intrinsic, x_changes_num_list):
    #dfから値を抽出
    delta_y_list = df_xyz['Δy'].tolist()
    delta_z_list = df_xyz['Δz'].tolist()
    h_list = df_xyz['h'].tolist()
    intrinsic_x_list = df_intrinsic['塑性ひずみ(X)'].tolist()
    
    inherent_x_list = []
    for i in range(len(x_changes_num_list)):
       #分割行番号
        x_num = x_changes_num_list[i]
        if i == len(x_changes_num_list)-1 :#最後
            x_num_next = len(df_xyz)
        else:
            x_num_next = x_changes_num_list[i+1]

        inherent_x = 0
        for j in range(x_num, x_num_next):
            delta_z = delta_z_list[j]
            delta_y = delta_y_list[j]
            intrinsic_x = intrinsic_x_list[j]
            h = h_list[j]

            inherent_x += delta_y * delta_z * intrinsic_x / h
        inherent_x_list.append(inherent_x)
    
    return inherent_x_list


#δy*を計算する関数
def cal_inherent_y(df_xyz, df_intrinsic, x_changes_num_list):
    #dfから値を抽出
    delta_y_list = df_xyz['Δy'].tolist()
    delta_z_list = df_xyz['Δz'].tolist()
    h_list = df_xyz['h'].tolist()
    intrinsic_y_list = df_intrinsic['塑性ひずみ(Y)'].tolist()
    
    inherent_y_list = []
    for i in range(len(x_changes_num_list)):
       #分割行番号
        x_num = x_changes_num_list[i]
        if i == len(x_changes_num_list)-1 :#最後
            x_num_next = len(df_xyz)
        else:
            x_num_next = x_changes_num_list[i+1]

        inherent_y = 0
        for j in range(x_num, x_num_next):
            delta_z = delta_z_list[j]
            delta_y = delta_y_list[j]
            intrinsic_y = intrinsic_y_list[j]
            h = h_list[j]

            inherent_y += delta_y * delta_z * intrinsic_y / h
        inherent_y_list.append(inherent_y)
    
    return inherent_y_list

#θx*を計算する関数
def cal_theta_x(df_xyz, df_intrinsic, x_changes_num_list):
    #dfから値を抽出
    delta_y_list = df_xyz['Δy'].tolist()
    delta_z_list = df_xyz['Δz'].tolist()
    h_list = df_xyz['h'].tolist()
    zc_list = df_xyz['zc'].tolist()
    z_list = df_xyz['中心(Z)'].tolist()
    intrinsic_x_list = df_intrinsic['塑性ひずみ(X)'].tolist()

    theta_x_list = []
    for i in range(len(x_changes_num_list)):
       #分割行番号
        x_num = x_changes_num_list[i]
        if i == len(x_changes_num_list)-1 :#最後
            x_num_next = len(df_xyz)
        else:
            x_num_next = x_changes_num_list[i+1]

        theta_x = 0
        for j in range(x_num, x_num_next):
            delta_z = delta_z_list[j]
            delta_y = delta_y_list[j]
            intrinsic_x = intrinsic_x_list[j]
            h = h_list[j]
            zc = zc_list[j]
            z = z_list[j]


            theta_x += delta_y * delta_z * intrinsic_x * (z-zc) / (h**3/12)
        theta_x_list.append(theta_x)
    
    return theta_x_list