import csv
import utils


def calculation(xyz_path = './xyz-coordinate.csv', intrinsic_path='./power-data/1000w-intrinsic.csv', h=0.7, E=175000.0):
    #csvを読み込みdfに変換
    df_xyz = utils.make_data_from_csv(xyz_path)#(要素数, 4( 要素番号, x, y ,z))
    df_intrinsic = utils.make_data_from_csv(intrinsic_path)#(要素数, 7( 要素番号, 塑性ひずみx, 塑性ひずみy ,塑性ひずみz, 塑性ひずみxy, 塑性ひずみyz, 塑性ひずみzx))
    df_xyz = utils.sort_df_xyz(df_xyz)#座標dfを昇順に並び替え


    #delta_xの列を追加
    df_xyz['Δx']=0
    df_xyz['Δy']=0
    df_xyz['Δz']=0



    #Δxの計算
    df_xyz, x_changes_num_list = utils.delta_df_xy(df_xyz, col_num=1)
    #Δyの計算
    df_xyz, y_changes_num_list = utils.delta_df_xy(df_xyz, col_num=2)
    #Δzの計算
    #df_xyz = utils.delta_df_xyz(df_xyz, col_num=3)
    df_xyz = utils.delta_df_z(df_xyz, y_changes_num_list)

    print('hとzcを計算')


      #Δx,Δy,Δzの計算
    """
    #dataを結合
    xyz_intrinsic_data = utils.combine(df_xyz, df_intrinsic)
    """


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

