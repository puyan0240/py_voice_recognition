import tkinter
from tkinter import ttk
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


def record_task():
    print("start record_task")

    #ボタン押下禁止解除
    ptt_btn.config(state=tkinter.NORMAL)
    ptt_btn.update()


def click_ptt_btn():
    print("click_ptt_btn")

    #ボタン押下禁止
    ptt_btn.config(state=tkinter.DISABLED)
    ptt_btn.update()

    #録音は専用のタスクで実施する
    task_id = threading.Thread(target=record_task)
    task_id.start()


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

    root.mainloop()