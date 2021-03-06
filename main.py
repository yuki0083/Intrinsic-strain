import calculation
import openpyxl
import utils_excel
import glob
import os


#列の名前
col_name = [['x', '固有縦収縮(δx*)', '固有横収縮(δy*)', '固有角変形(θx*)','固有角変形(θy*)']]
col_num = len(col_name[0])

#変数
#h = 0.7 

E = 175000.0 #ヤング率

#xyz_path = './xyz-coordinate.csv' #xyz座標csvファイルノパス

xyz_path = input('座標のcsvファイルのパスを入力:')
xyz_path = xyz_path.replace('"', '')# "を削除

#input_directory_path = './power-data'
input_directory_path = input('塑性ひずみcsvファイルのあるディレクトリパスを入力:')#csvファイルのあるディレトリを指定
input_directory_path = input_directory_path.replace('"', '')# "を削除

glob_for_csv = input_directory_path + '/*.csv'
intrinsic_path_list = glob.glob(glob_for_csv) #固有ひずみcsvファイルのパスを取得

#excelファイルに書き込み
utils_excel.write_excel_sheet(intrinsic_path_list, input_directory_path, col_num=col_num, col_name=col_name, xyz_path=xyz_path)

