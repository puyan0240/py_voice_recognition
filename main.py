import tkinter
from tkinter import ttk

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

def click_ptt_btn():
    print("押されました")

if __name__ == '__main__':

    root = tkinter.Tk()

    # ---------- Window作成 ---------- 
    root.title("音声認識くん")  # 画面タイトル
    root.geometry('500x500')   # 画面サイズ
    root.resizable(False, False)  # リサイズ不可

    # ---------- Frame作成 ---------- 
    frame_top   = tkinter.Frame(root)
    frame_sel   = tkinter.Frame(root)
    frame_recog = tkinter.Frame(root)
    frame_trans = tkinter.Frame(root)


    # ---------- Frame配置 ----------
    frame_top.grid(row=0, column=0)
    frame_sel.grid(row=0, column=1)
    frame_recog.grid(row=1, column=0, columnspan=2)
    frame_trans.grid(row=2, column=0, columnspan=2)
    

    # ---------- Widget配置 ----------
    # Button
    ptt_btn = tkinter.Button(frame_top, text="開始", command=click_ptt_btn)
    ptt_btn.pack()

    # Label
    label_src = tkinter.Label(frame_sel, text="言語")
    label_src.grid(row=0,column=0)
    label_dst = tkinter.Label(frame_sel, text="翻訳言語")
    label_dst.grid(row=0,column=1)

    # Combobox
    cb_src_menu = [] #メニューリスト
    for val in lang_tbl:
        cb_src_menu.append(val[LANG_TBL_NAME])
    cb_src = ttk.Combobox(frame_sel, textvariable=tkinter.StringVar(),values=cb_src_menu,state="readonly",width=25)
    cb_src.current(0)
    cb_src.grid(row=1,column=0)

    # Combobox
    cb_dst_menu = [] #メニューリスト
    for val in lang_tbl:
        cb_dst_menu.append(val[LANG_TBL_NAME])
    cb_dst = ttk.Combobox(frame_sel, textvariable=tkinter.StringVar(),values=cb_dst_menu,state="readonly",width=25)
    cb_dst.current(0)
    cb_dst.grid(row=1,column=1)


    root.mainloop()