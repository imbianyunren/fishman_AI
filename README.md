# Pedestrian Detection for Fishman Overwork Detection

此行人檢測系統為基於漁工過勞檢測系統所開發

**✍️ 誠摯的感謝我的夥伴** Annie 郭怡靚他幫我de了許多的bug

---

## Getting Started

很可惜這個程式並沒有隨附什麼一鍵完成的按鈕，要執行這個程式，只準備影片是不夠的，以下會帶大家一步步執行

---
* [事前準備](#事前準備)
* [環境建立](#環境建立)
* [程式執行](#程式執行)
* [執行結果](#執行結果)
* [輸出檔案](#輸出檔案)(ver1.1 新增)

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

本程式是利用python來撰寫，裡所當然你的電腦需要 python 的環境來執行，並且我們需要pip來安裝一些額外的  libraries ，我們可以利用以下簡單的兩個指令來檢查:

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
py -m pip install --user opencv-python pafy youtube_dl imutils numpy scipy matplotlib ipython jupyter pandas sympy nose seaborn
```

---
## 程式執行

上述的步驟都完成之後，恭喜你，你可以開始執行本程式啦~

執行程式的指令基本上就是:

```console
python main.py argument path
```

根據來源的不同，可以選擇不同的指令來執行

- -v for video
- -i for image
- -s for youtube

舉例來說，如果你要輸入一個影片，你只需要:

Windows
```console
python main.py -v ‘Path_to_video’
```

Linux
```console
python3 main.py -v ‘Path_to_video’
```
PS : youtube連結不管是直播還是影片都能用喔，不過那個功能有點不穩定，如果出現錯誤多試幾次就可以了。<br>
     另外若出現`KeyError: 'dislike_count'`、`KeyError: 'dislike_count'`此錯誤，解決方式請詳見文件末端的錯誤處理的部分。


PSS : 如果你稍微去研究一下程式碼，會發現其實有一個 argument 是 -o，功能是輸出結果，但他目前是不能用的狀態，預計於下一個版本維修完成。

---

## 執行結果

大概會長的跟下圖差不多


![result_001](./sample/result_001.png)


---

## 輸出檔案

1.1版本新增了輸出檔案的功能，其內容包括了:

原文           | 功能  | 
------------  | ----  | 
Frames per second using | 原影片幀率 | 
Remaining frames    | 不到一小時的剩於幀數 | 
Remaining times  | 不到一小時的剩於時間 |
Remaining people appear frames  | 不到一小時的有人出現的幀 |
Remaining people appear times  | 不到一小時的有人出現的時間 |
Remaining weighted frames in one hour  | 不到一小時的有權重的幀 |
Remaining weighted times in one hour  | 不到一小時的有權重的時間 |
Remaining appears people  | 不到一小時的出現總人數 |
Remaining average people  | 不到一小時的平均出現人數 |
Total frames  | 在結束前的所有幀數 |
Total times  | 在結束前的所有時間 |
Total people appears frames  | 不到一小時的剩於時間 | 
Total people appears times | 在結束前的所有時間 |
Total weighted frames  | 在結束前的所有有權重的幀 |
Average people in this video | 每幀的平均人數 |

---
 ## 錯誤處理
 #### KeyError: 'dislike_count'、KeyError: 'like_count'
 由於youtube近期改版取消dislike顯示(部分影片會選擇不顯示like數)，導致pafy函式庫在存取youtube影片會出問題，
 因此需要手動調整pafy對於youtube存取的程式碼內容<br>
 以下為`KeyError: 'dislike_count'`錯誤處理方式，若錯誤為`KeyError: 'like_count'`解決方式也相同
 
 
 若您執行時遇到下圖的狀況(以windows powershell執行圖為例):
 
 ![image](https://user-images.githubusercontent.com/60705979/147848758-028cb5f8-d0b0-4a51-bd19-5d13e76806b5.png)

 
 請您照以下步驟解決:
 
1. 使用任意編輯器(ex. 記事本、vim、vscode等等)開啟backend_youtube_dl.py檔案，以下以記事本為例

   * 先將上圖backend_youtube_dl.py檔案位置複製起來
     ![image](https://user-images.githubusercontent.com/60705979/147848439-cdbaa046-61bb-423b-b9bc-a06e7fddcdeb.png)
   * 接著開啟記事本，點選左上角檔案，並點擊裡面的開啟選項，將剛複製的檔案位置貼在箭頭指的位置並開啟
   ![image](https://user-images.githubusercontent.com/60705979/147849403-946d8e5f-2c81-47dd-80d6-5c11677ffd80.png)
   
2. 編輯backend_youtube_dl.py文件內容，在`self._dislikes = self._ydl_info['dislike_count']`此行(line 54，可用尋找功能)前面加上`#`註解
   ```python
   #self._dislikes = self._ydl_info['dislike_count']
   ```
3. 修改完成後重新測試即可順利執行，並不影響原程式功能
   


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
