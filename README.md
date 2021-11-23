# Pedestrian Detection for Fishman Overwork Detection

此行人檢測系統為基於漁工過勞檢測系統所開發

**✍️ 誠摯的感謝我的夥伴** Annie 郭怡靚他幫我de了許多的bug

---

## Getting Started

很可惜這個程式並沒有隨付什麼一鍵完成的按鈕，要執行這個程式，你必須準備不只有你的影片，以下會帶大家一步步執行

---
* [事前準備](#事前準備)
* [環境建立](#環境建立)
* [程式執行](#程式執行)

---
## 事前準備

這份說明是基於windows上寫的，因此，如果你用的是 linux 或 mac os，指令可能會不太一樣，但我相信應該會差不多!

首先，先將本程式的程式碼下載下來，你可以直接使用

```console
git clone https://github.com/AmazingWilson-hub/fishman_AI
```

來將整個程式碼下載，或著你也可以直接點選[這裡](https://codeload.github.com/AmazingWilson-hub/fishman_AI/zip/refs/heads/main)來下載

---
## 環境建立

本程式是利用python來撰寫，裡所當然你的電腦需要 python 的環境來執行，並且我們需要pip來安裝一些額外的  libaries ，我們可以利用以下簡單的兩個指令來檢查:

```console
py --version
```
>正常應該會顯示 Python 3.X.X


```console
pip --version
```
>正常應該會顯示 pip 21.X.X from ~ (python 3.X)

如果出來的結果顯示錯誤，那代表你的電腦沒有安裝python或遺失了 pip 套件(正常來說 pip 會連同你在安裝 python 時一起安裝)，那可能要請你自行去google。

接下來要安裝擴充的函示庫，建議在你下載的程式碼的根目錄資料夾執行:

```concole
pip install opencv-python
pip install imutils
pip install numpy
pip install pafy
```

---
## 程式執行

上述的步驟都完成之後，恭喜你，你可以開始執行本程式啦~

執行程式的指令基本上就是:

```concole
python main.py argument path
```

根據來源的不同，可以選擇不同的指令來執行

- -v for video
- -i for image
- -s for youtube

舉例來說，如果你要輸入一個影片，你只需要:

```concole
python main.py -v ‘Path_to_video’
```
特別註明，youtube連結不管是直播還是影片都能用喔，不過那個功能有點不穩定，如果出現錯誤多試幾次就可以了。

---

## Meet the Team

郭弘偉
郭怡靚
許庭涵
陳怡靜
孫嘉成
沈芳儀


---

## Support

如果你有任何問題，歡迎聯絡我
amazingwilson@csie.io
我會盡一切可能幫助你