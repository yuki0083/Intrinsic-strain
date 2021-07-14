import csv
import utils
import cal_xyz
import cal_intrinsic

#座標関連の計算をする関数
def make_df_xyz(xyz_path):
    #csvを読み込みdfに変換
    df_xyz = utils.make_data_from_csv(xyz_path)#(要素数, 4( 要素番号, x, y ,z))

    #TODO #数値を丸める
    df_xyz = utils.round_df_xyz(df_xyz, 2)#小数点以下4桁で丸める
    
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
    #θx*を計算
    theta_y_list = cal_intrinsic.cal_theta_y(df_xyz, df_intrinsic, x_changes_num_list)
    
    inherent_deformtaions_list = [x_list, inherent_x_list, inherent_y_list, theta_x_list, theta_y_list]

    return inherent_deformtaions_list

