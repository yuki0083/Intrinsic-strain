import csv
import utils
import cal_xyz
import cal_intrinsic

#座標関連の計算をする関数
def make_df_xyz(xyz_path):
    #csvを読み込みdfに変換
    df_xyz = utils.make_data_from_csv(xyz_path)#(要素数, 4( 要素番号, x, y ,z))
    #df_intrinsic = utils.make_data_from_csv(intrinsic_path)#(要素数, 7( 要素番号, 塑性ひずみx, 塑性ひずみy ,塑性ひずみz, 塑性ひずみxy, 塑性ひずみyz, 塑性ひずみzx))
    df_xyz = cal_xyz.sort_df_xyz(df_xyz)#座標dfを昇順に並び替え
    #delta_xの列を追加
    df_xyz['Δx']=0
    df_xyz['Δy']=0
    df_xyz['Δz']=0
    #Δxとx_arrayの変わる番号の計算
    df_xyz, x_changes_num_list = cal_xyz.delta_df_xy(df_xyz, col_num=1)
    #Δyとy_array(z1_num)の変わる番号の計算
    df_xyz, y_changes_num_list = cal_xyz.delta_df_xy(df_xyz, col_num=2)

    #z_topを入力
    z_top = float(input('z_top(x最小,y最小の要素の内zが最も大きい要素の表面の座標)を入力:'))
    #Δzの計算
    df_xyz = cal_xyz.delta_df_z(df_xyz, y_changes_num_list, z_top)
    
    #hとzcの列を追加
    df_xyz['h']=0
    df_xyz['zc']=0
    #hとzcを計算
    df_xyz = cal_xyz.cal_h_zc(df_xyz, y_changes_num_list)

    return df_xyz

#塑性ひずみのファイルをdf_xyzと同じように並び変える
def make_df_intrisic(intrinsic_path, df_xyz):
    df_intrinsic = utils.make_data_from_csv(intrinsic_path)
    #df_xyzと同じようにdf_intrinscを並び変える
    df_intrinsic = cal_intrinsic.sort_df_intrinsic(df_intrinsic, df_xyz)
    
    return df_intrinsic

#固有変形を計算　[x, tendon_force, delta_T, theta_T, theta_L ]
def cal_inherent_deformations(df_xyz, df_intrinsic):
    #xを計算
    x_series = df_xyz['中心(X)']#panda series
    x_changes_num_list, x_list = cal_intrinsic.cal_x_change_num_list_and_x(x_series)
    #δx*を計算
    inherent_x_list = cal_intrinsic.cal_inherent_x(df_xyz, df_intrinsic, x_changes_num_list)
    #δy*を計算
    inherent_y_list = cal_intrinsic.cal_inherent_y(df_xyz, df_intrinsic, x_changes_num_list)
    #θx*を計算
    theta_x_list = cal_intrinsic.cal_theta_x(df_xyz, df_intrinsic, x_changes_num_list)
    return 0

"""
    #dataを結合
    xyz_intrinsic_data = utils.combine(df_xyz, df_intrinsic)
    


    #xyz_intrinsic_dataをxの値で分割(x_dict_keysはxの値が入ってる)
    x_dict, x_dict_keys = utils.x_divide(xyz_intrinsic_data)
    #x_dict(要素数, 11(列, 要素番号, x, y ,z, 塑性ひずみx, 塑性ひずみy ,塑性ひずみz, 塑性ひずみxy, 塑性ひずみyz, 塑性ひずみzx))

    #固有変形を計算
    results = []
    for i in range(len(x_dict_keys)):
        x = x_dict_keys[i]

        data = x_dict[x]#同じxで分割したデータ (列, 要素番号, x, y ,z, 塑性ひずみx, 塑性ひずみy ,塑性ひずみz, 塑性ひずみxy, 塑性ひずみyz, 塑性ひずみzx)

        #Δxを計算
        delta_x = utils.calculata_deltax(x_dict_keys, i)

        #ΔyΔzを計算
        delta_y_list, delta_z_list = utils.calculate_deltay_and_deltaz(data)

        #εx*,εy*,zをdataから取り出す
        z_list = utils.extract_from_data_to_list(data, row_num=4)#z
        intrinsic_x_list = utils.extract_from_data_to_list(data, row_num=5)#εx*
        intrinsic_y_list = utils.extract_from_data_to_list(data, row_num=6)#εy*

        #δL,δTを計算
        delta_L = utils.cal_delta_L(data, delta_z_list, delta_y_list, intrinsic_x_list, h)
        delta_T = utils.cal_delta_T(data, delta_z_list, delta_y_list, intrinsic_y_list, h)

        #縦収縮(tendon force)
        tendon_force = E * delta_L

        #Iを計算
        I = utils.cal_I(data, z_list, delta_x, delta_z_list, h)

        #θTを計算
        theta_T = utils.cal_theta_T(data, z_list, delta_y_list, delta_z_list, intrinsic_y_list, h, I)

        #θLを計算
        theta_L = utils.cal_theta_L(data, z_list, delta_y_list, delta_z_list, intrinsic_x_list, h, I)

        result = [x, tendon_force, delta_T, theta_T, theta_L ]
        results.append(result)

    return results

"""