from pitman_body import genFir
def initilize():
    ##　時変FIRフィルターの設定
    genfir_setting={
        ## 音をどれだけ下げるのか
        "pitch":40,
        ## 分解能
        "tap" : 1024
    }
    ## DownFIRフィルタの設計
    downFirfilter, sub = genFir(genfir_setting["pitch"], genfir_setting["tap"])
    ## 使用したRobotの設定
    robot_setting ={
        ## 開始周波数
        "fi" : 50000 ,
        ## 終端周波数 
        "ft" : 10000 ,
        ## 使用した信号の名前
        "Callname" : "LPM",
        ## サンプリング周波数
        "fs" : 1000000,
        ## 発信した信号長
        "dur" : 0.0036,
        ## マイク間距離[mm]
        "micDur": 28
    }
    ## 出力するサウンドの設定
    process_audio_setting = {
        ##　保存先 
        "folder" :  "",
        ## ヘッドホンの規格で調整して下さい 
        "output_fs" : 96000,
        ## モノラル or ステレオ
        "channel" : 2,
        ## buzz音も出力したい場合 :True
        "buzz" : {
            "used" : True,
            ## パルス放射間隔 [s]
            "IPI" : 0.5, 
            ## 繰り返し音 [回]
            "nrepeat":4
        }
    }
    ## 出力したいグラフの設定
    ## TODO めんどくさいので後回し
    plot_setting = {
        "raw_data_analysis" : True, 
        "raw_simulation" : True
    }

    return genfir_setting, downFirfilter, sub, robot_setting, process_audio_setting, plot_setting

