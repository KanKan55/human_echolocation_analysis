import numpy as np
## ロボット」から吐き出されたoutputデータを読み込む
def read_multi_dat(datapath):
    l = []
    r = []
    with open(datapath) as f:
        datalist = f.read().split("\n")
        for i in range(1, len(datalist) - 1):
            datalist[i] = (datalist[i].replace('"', "")).split(" ")
            l.append(float(datalist[i][0]))
            r.append(float(datalist[i][1]))
    f.close()
    return np.array(l), np.array(r)


## 選択したフォルダー内に何個フォルダーがあるか数える
def count_id_subdir(path):
    num_of_sub_dirs = 0
    #print(path)
    for f in path.glob("*"):
        if f.is_dir():
            num_of_sub_dirs += 1

    return num_of_sub_dirs


## 選択したフォルダー内にあるフォルダーの名前を格納
def count_name_subdir(path):
    folder = os.listdir(path)
    return folder

## データの実効値をとる
def rms(data):
    sum = 0
    for i in range(len(data)):
        sum += np.float_power(data[i], 2)

    rms_data = np.sqrt(sum / len(data))
    return rms_data