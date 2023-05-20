import tkinter
from tkinter import ttk,messagebox
import pyaudio  #マイク入力
import wave # WAVEファイル保存
import speech_recognition  #音声認識API
import googletrans
from googletrans import Translator  #google翻訳
from gtts import gTTS   # 文字->音声ファイル化
from playsound import playsound  #音声ファイルを再生
import os
from os import path
import threading    #スレッド


#言語テーブル
LANG_TBL_NAME=0
LANG_TBL_PARAME=1   # 翻訳、読み上げ
LANG_TBL_RECOG=2    # 音声認識
lang_tbl = [
    ["Japanese (日本語)", "ja", "ja-JP"],
    ["English (英語)", "en", "en-US"],
    ["German (ドイツ語)", "de", "de-DE"],
    ["French (フランス語)", "fr", "fr-FR"],
    ["Italian (イタリア語)", "it", "it-IT"],
    ["Spanish (スペイン語)", "es", "eu-ES"],
    ["Portuguese (ポルトガル語)", "pt", "pt-PT"],
    ["Russian (ロシア語)", "ru", "ru-RU"],
    ["Korean (韓国語)", "ko", "ko-KR"],
    ["chinese (中国語)", "zh-cn", "zh"],
    ["Vietnamese (ベトナム語)", "vi", "vi-VN"]
]

#一時ファイル
TMP_FILENAME = "tmp.wav"
TMP_PLAY_FILENAME = "tmp_play.mp3"

loop = True
task_id = 0


############################################################
# マイク入力録音タスク
############################################################
def rec_task():
    global loop
    loop = True

    # マイク入力設定
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        rate=44100,
                        channels=1,
                        input_device_index=1,
                        input=True,
                        frames_per_buffer=1024)

    # WAVE保存設定
    wave_f = wave.open(TMP_FILENAME, 'wb') #ファイルオープン
    wave_f.setnchannels(1)  # チャンネル指定
    wave_f.setsampwidth(2)  # サンプル幅:16bit
    wave_f.setframerate(44100)  #フレームレート

    while loop:
        data = stream.read(1024)
        wave_f.writeframes(data)

    # WAVEファイルの作成
    wave_f.close()
    # Audioデバイスの解放
    stream.stop_stream()
    stream.close()
    audio.terminate()


############################################################
# PTTボタン押下した
############################################################
def click_ptt_btn():
    global task_id,loop,sts
    recong_flag=False
    trans_flag=False

    if ptt_btn['text'] == "開始":
        ptt_btn['text'] = "停止"
        ptt_btn.update()

        # テキスト領域をクリアする
        clr_text()

        # マイク入力録音タスクを起動する
        task_id = threading.Thread(target=rec_task)
        task_id.start()

    else:
        ptt_btn['text'] = "開始"
        ptt_btn.update()

        # マイク入力録音タスクを停止する
        stop_task()

        # WAVファイルの絶対パス
        audio_path = os.getcwd()+"\\"+TMP_FILENAME;

        #音声認識言語の確定
        lang_src = ""
        for val in lang_tbl:
            if val[LANG_TBL_NAME] == cb_recog.get():
                lang_src = val[LANG_TBL_RECOG]
                break

        # 音声認識開始
        sprec = speech_recognition.Recognizer()  # インスタンスを生成
        with speech_recognition.AudioFile(audio_path) as sprec_file:
            try:
                sprec_audio = sprec.record(sprec_file)
                sprec_text = sprec.recognize_google(sprec_audio, language=lang_src)

                # テキスト領域に出力
                text_recog.config(state=tkinter.NORMAL)  # 入力許可
                text_recog.insert(tkinter.END, sprec_text)  # 書き込み
                text_recog.config(state=tkinter.DISABLED)  # 入力規制
                text_recog.update()  # 表示更新

                recong_flag = True; # 音声認識あり

            except speech_recognition.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except Exception as e:
                print(f"voice recognition err: {str(e)}")

        # WAVファイルを削除
        if os.path.exists(audio_path) == True:
            os.remove(audio_path)      

        #翻訳
        if recong_flag == True:
            #音声認識結果テキストの読み出し
            text = text_recog.get('1.0', tkinter.END)
            #print(text)
            #text = "こんにちは"
            
            #翻訳元言語の確定
            lang_src = ""
            for val in lang_tbl:
                if val[LANG_TBL_NAME] == cb_recog.get():
                    lang_src = val[LANG_TBL_PARAME]
                    break
            
            #翻訳先言語の確定
            lang_dest = ""
            for val in lang_tbl:
                if val[LANG_TBL_NAME] == cb_trans.get():
                    lang_dest = val[LANG_TBL_PARAME]
                    break

            #翻訳実行
            try:
                trans = Translator()
                result = trans.translate(text, src=lang_src, dest=lang_dest)
                print(result.text)

                # 翻訳結果を出力
                text_trans.config(state=tkinter.NORMAL)
                text_trans.insert(tkinter.END, result.text)
                text_trans.config(state=tkinter.DISABLED)
                text_trans.update()

                trans_flag = True # 翻訳成功

            except Exception as e:
                print(e)

        #再生実行
        if trans_flag == True:
            #翻訳テキストの内容取得
            text = text_trans.get('1.0', tkinter.END)

            #音声ファイル化
            try:
                out = gTTS(text, lang=lang_dest, slow=False)
                out.save(TMP_PLAY_FILENAME)
            except Exception as e:
                print("save err: "+str(e))

            #音声ファイルを再生
            try:
                playsound(TMP_PLAY_FILENAME)
            except Exception as e:
                print("play err: "+str(e))

            #音声ファイルを削除
            if os.path.exists(TMP_PLAY_FILENAME) == True:
                os.remove(TMP_PLAY_FILENAME)


############################################################
# タスク停止
############################################################
def stop_task():
    global loop,task_id

    if task_id != 0:
        loop = False
        # タスク終了まで待つ
        task_id.join()


############################################################
# テキスト領域のクリア
############################################################
def clr_text():
    # 音声認識結果テキスト領域をクリア
    text_recog.config(state=tkinter.NORMAL)
    text_recog.delete('1.0', tkinter.END)
    text_recog.config(state=tkinter.DISABLED)

    #　翻訳結果テキスト領域をクリア
    text_trans.config(state=tkinter.NORMAL)
    text_trans.delete('1.0', tkinter.END)
    text_trans.config(state=tkinter.DISABLED)


############################################################
#フレームの終了「×」を押された時のイベント
############################################################
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
    text_trans = tkinter.Text(frame_right, relief=tkinter.SOLID, width=60, height=40, padx=10)
    text_trans.config(state=tkinter.DISABLED)
    text_trans.config(bg="gray97", bd=0)
    text_trans.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


    # ---------- Widget配置 ----------
    # Button
    ptt_btn = tkinter.Button(frame_bottom, text="開始", command=click_ptt_btn)
    ptt_btn.pack(padx=20, pady=20)

    #終了ボタン押下イベント登録
    root.protocol("WM_DELETE_WINDOW", click_close)

    root.mainloop()