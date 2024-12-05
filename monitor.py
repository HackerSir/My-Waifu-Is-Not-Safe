import subprocess

def run_command(command, capture_output=False, timeout = 50) -> str| None:
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            
            # if result.returncode != 0:
            #     print(f"Command failed: {command}\nError: {result.stderr}")
            #     return None
            return result.stdout.strip()
        else:
            result = subprocess.run(command, shell=True, capture_output=True, timeout=timeout, text=True)
    except subprocess.CalledProcessError as result:
        print(f"Error running command: {command}\n")
        result = result.output.decode()
        return result if capture_output else None
    except subprocess.TimeoutExpired as result:
        print(f"Timeout occurred: {command}")
        result = result.output.decode()
        return result if capture_output else None
    
class Monitor:
    def setup_monitor_mode(interface='wlan0', test=True, retries=4) -> None:
        print("setup monitor mode...")
        run_command(f"ifconfig {interface} down")
        run_command("airmon-ng check kill")
        run_command(f"iwconfig {interface} mode monitor")
        run_command(f"ifconfig {interface} up")
        run_command(f"airmon-ng start {interface}")
        if test and retries:
            out = run_command(f"aireplay-ng --test {interface}", capture_output=True)
            if 'Found 0 APs' in out:
                Monitor.setup_monitor_mode(retries=retries-1)


    def reset_mode(interface) -> None:
        print("Resetting interface to managed mode...")
        run_command(f"airmon-ng stop {interface}")
        run_command(f"ifconfig {interface} down")
        run_command("service NetworkManager restart")
