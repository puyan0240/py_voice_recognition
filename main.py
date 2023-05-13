import tkinter
from tkinter import ttk,messagebox
import pyaudio  #マイク入力
import wave # WAVEファイル保存
import time
import threading    #スレッド


#言語テーブル
LANG_TBL_NAME=0
LANG_TBL_PARAME=1
lang_tbl = [
    ["Japanese (日本語)", "ja"],
    ["English (英語)", "en"],
    ["German (ドイツ語)", "de"],
    ["French (フランス語)", "fr"],
    ["Italian (イタリア語)", "it"],
    ["Spanish (スペイン語)", "es"],
    ["Portuguese (ポルトガル語)", "pt"],
    ["Russian (ロシア語)", "ru"],
    ["Korean (韓国語)", "ko"],
    ["chinese (中国語)", "zh-cn"],
    ["Vietnamese (ベトナム語)", "vi"]
]


#状態
STS_IDLE = 0
STS_REC = 1
STS_RECOG = 2
STS_PLAY = 3
sts = STS_IDLE

TMP_FILENAME = "tmp.wav"


loop = True
task_id = 0

# メインタスク
def rec_task():
    global loop
    loop = True

    print("start rec_task")

    # マイク入力設定
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, rate=44100, channels=1, input_device_index=1, input=True, frames_per_buffer=1024)

    # WAVE保存設定
    wave_f = wave.open(TMP_FILENAME, 'wb') #ファイルオープン
    wave_f.setnchannels(1)  # チャンネル指定
    wave_f.setsampwidth(2)  # サンプル幅:16bit
    wave_f.setframerate(44100)  #フレームレート


    while loop:
        print("+")
        data = stream.read(1024)
        wave_f.writeframes(data)

    # WAVEファイルの作成
    wave_f.close()
    # Audioデバイスの解放
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("end rec_task")



# PTTボタン押下
def click_ptt_btn():
    global task_id,loop,sts

    print(f"click_ptt_btn  sts:{sts}")

    if sts == STS_IDLE:
        sts = STS_REC

        ptt_btn['text'] = "停止"

        # 録音タスクを起動する
        task_id = threading.Thread(target=rec_task)
        task_id.start()

    else:
        sts = STS_IDLE
        stop_task()

        ptt_btn['text'] = "開始"

    #ボタン押下禁止
    ptt_btn.config(state=tkinter.DISABLED)
    ptt_btn.update()

    #ボタン押下禁止解除
    ptt_btn.config(state=tkinter.NORMAL)
    ptt_btn.update()


# タスク停止
def stop_task():
    global loop,task_id
    print("stop task")

    if task_id != 0:
        loop = False
        # タスク終了まで待つ
        task_id.join()
        print("complete")


#フレームの終了「×」を押された時のイベント
def click_close():
    if messagebox.askokcancel("確認", "アプリを終了しますか？"):
        # タスク停止
        stop_task()

        # tkinter終了
        root.destroy()


if __name__ == '__main__':

    root = tkinter.Tk()

    # ---------- Window作成 ---------- 
    root.title("音声認識くん")  # 画面タイトル
    #root.geometry('500x500')   # 画面サイズ
    root.resizable(False, False)  # リサイズ不可


    # ---------- Frame作成 ----------
    frame_left   = tkinter.Frame(root)
    frame_center = tkinter.Frame(root)
    frame_right  = tkinter.Frame(root)
    frame_bottom = tkinter.Frame(root)

    # ---------- Frame配置 ----------
    frame_left.grid(row=0, column=0)
    frame_center.grid(row=0, column=1)
    frame_right.grid(row=0, column=2)
    frame_bottom.grid(row=1, column=0, columnspan=3)

    #
    label_recog = tkinter.Label(frame_left, text="話す言葉")
    label_recog.grid(row=0, column=0, padx=5, pady=10, sticky=tkinter.E)

    # Combobox
    cb_recog_menu = [] #メニューリスト
    for val in lang_tbl:
        cb_recog_menu.append(val[LANG_TBL_NAME])
    cb_recog= ttk.Combobox(frame_left, textvariable=tkinter.StringVar(),values=cb_recog_menu,state="readonly",width=25)
    cb_recog.current(0)
    cb_recog.grid(row=0, column=1, padx=5, pady=10,sticky=tkinter.W)

    # Text
    text_recog = tkinter.Text(frame_left, relief=tkinter.SOLID, width=60, height=40)
    text_recog.config(state=tkinter.DISABLED)
    text_recog.config(bg="gray97", bd=0)
    text_recog.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


    # Label
    label_trans = tkinter.Label(frame_right, text="翻訳する言語")
    label_trans.grid(row=0, column=0, padx=5, pady=10, sticky=tkinter.E)

    # Combobox
    cb_trans_menu = [] #メニューリスト
    for val in lang_tbl:
        cb_trans_menu.append(val[LANG_TBL_NAME])
    cb_trans = ttk.Combobox(frame_right, textvariable=tkinter.StringVar(),values=cb_trans_menu,state="readonly",width=25)
    cb_trans.current(0)
    cb_trans.grid(row=0, column=1, padx=5, pady=10, sticky=tkinter.W)

    # Text
    text_recog = tkinter.Text(frame_right, relief=tkinter.SOLID, width=60, height=40, padx=10)
    text_recog.config(state=tkinter.DISABLED)
    text_recog.config(bg="gray97", bd=0)
    text_recog.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


    # ---------- Widget配置 ----------
    # Button
    ptt_btn = tkinter.Button(frame_bottom, text="開始", command=click_ptt_btn)
    ptt_btn.pack(padx=20, pady=20)

    #終了ボタン押下イベント登録
    root.protocol("WM_DELETE_WINDOW", click_close)

    root.mainloop()