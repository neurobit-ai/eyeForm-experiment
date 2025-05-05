## 這個資料夾放的版本是在本機端開發的版本
## 使用IDE : VSCODE 安裝LIVE SERVER
## 本機端開發與在github上開發不同之處在於
### 1 在github上修改時，無法立即看到結果，需要等一段時間讓系統執行deploy，而修改python後delploy所需的時間比html還要久很多，使用live server則是可以及時到變化
### 2 在github建立的網頁中，html要傳變數給python時可以使用localStorage儲存，python再使用json來讀取即可，本機端則是無法使用同樣方式，要另外宣告一個變數給python使用，html之間的傳遞還是可以使用loaclStorage
### 3 因為有COOP政策的影響，使用本機端無法套用GOOGLE的登入工具，開發時需要關閉此功能
### 4 在本機端只要在目標的html上按右鍵點選live server即可，在python檔案上按右鍵則不會出現live server選項
### 5 本資料夾的檔案有新增功能註解，這些註解僅針對有新增或改動的部分


