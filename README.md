# Stock Crawler

## 透過 yahoo finance api 撈取股價資訊

![alt text](https://imgur.com/SEyXbAC.png)

## 教學
### 套件安裝
需要的套件已經包在 requirements.txt 的文字檔中，將此檔案放入專案路徑中，然後在終端機輸入以下指令即可
> 安裝套件之前請先確認你的環境有安裝 [Python 3.7.6](https://www.python.org/downloads/release/python-376/)
```
pip install -r requirements.txt
```

## 執行範例
* 請先建立一個 txt 的檔案，名稱可自行命名，格式如下
```
2317.TW,2020-09-01,2021-09-25
2330.TW,2020-09-01,2021-09-25
6758.T,2020-09-01,2021-09-25
```

* 撈取一個 (以上) 公司的股價
* 引數化指定欲撈取的股價其公司資訊與 csv 檔案輸出的路徑 (-t 是欲撈取股價的公司清單, -o 是 csv 檔案輸出的路徑)

```
python crawler_stock.py -t D:\Files\Project\Stock_Crawler\stock_info_list.txt -o D:\Files\Project\Output\stock
```
> 若想要了解引數的作用，可輸入 python crawler_stock.py --help 查看

```
optional arguments:
  -h, --help            show this help message and exit
  -t TASK, --task TASK  stock ticker and country list
  -o OUTPUT, --output OUTPUT  stock info output path
```

### 執行畫面
![alt text](https://imgur.com/F2fYuOY.png)

### 輸出資料夾
![alt text](https://imgur.com/SNMz0I3.png)

* 將 python 檔案製作成一個 .exe 檔案

> -p 會將執行檔需要的模組一起包進去，若沒有加會導致執行檔無法找到其模組

```
pyinstaller.exe --specpath ./execute/ --distpath ./execute/dist --workpath ./execute/build -p "D:\Files\Project\Stock_Crawler\module;." -D crawler_stock.py
```
![alt text](https://imgur.com/m35Aun6.png)

* 另外，也有將 python 的檔案包成一個執行檔讓批次檔 (.bat) 去執行，同樣要給予引數，引述部分請參閱上方的執行範例，這裡就不再贅述

> 執行過程會紀錄在 log 檔中，若需要查看執行過程，可至 {專案路徑}\execute\dist\crawler_stock\matplotlib\mpl-data\logs 的路徑中
```
call D:\Files\Project\Stock_Crawler\execute\dist\crawler_stock\crawler_stock.exe -t C:\Users\YiQuan\Desktop\stock_info_list.txt -o D:\Files\Project\Output\stock
```

![alt text](https://imgur.com/gU0sVEz.png)

# 執行環境
* Python 3.7.6