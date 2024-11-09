import pyudev
import subprocess
from time import sleep


def get_bluetooth_audio_devices():
    """Get currently connected Bluetooth audio devices using pyudev"""
    context = pyudev.Context()
    devices = []

    for device in context.list_devices(subsystem='sound'):
        # Check if it's a Bluetooth audio device
        if device.get('ID_BUS') == 'bluetooth':
            devices.append(device.device_node)

    return devices


def get_audio_frequency(device_path):
    """Get the current audio frequency using arecord"""
    try:
        cmd = f"arecord -D {device_path} --dump-hw-params 2>&1"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()[0].decode()

        for line in output.split('\n'):
            if 'RATE' in line:
                # Extract rate values from the line
                rates = [int(r) for r in line.split()[1:] if r.isdigit()]
                if rates:
                    return max(rates)  # Return the highest supported rate
        return None
    except Exception as e:
        print(f"Error getting audio frequency: {e}")
        return None


def get_active_sink():
    """Get the currently active audio sink using pactl"""
    try:
        cmd = "pactl list sinks | grep -A 2 'State: RUNNING'"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()[0].decode()

        if output:
            return True
        return False
    except Exception as e:
        print(f"Error checking active sink: {e}")
        return False

def map_to_rgb(freq: float) -> (int, int, int): # returns 3-tuple (r, g, b)
    freq_lower_bound = 20
    freq_upper_bound = 4000

    if freq <= freq_lower_bound:
        return 0, 0, 255
    elif freq >= freq_upper_bound:
        return 255, 0, 0

def monitor_frequency() -> int:
    """Monitor and display the Bluetooth audio frequency"""
    print("Starting Bluetooth audio frequency monitor...")
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='sound')

    while True:
        devices = get_bluetooth_audio_devices()

        if devices:
            print("\nFound Bluetooth audio devices:")
            for device in devices:
                print(f"Device: {device}")
                if get_active_sink():
                    frequency = get_audio_frequency(device)
                    if frequency:
                        return
                    else:
                        print("Could not determine audio frequency")
                else:
                    print("No active audio stream detected")
        else:
            print("No connected Bluetooth audio devices found")

        sleep(2)


if __name__ == "__main__":
    monitor_frequency()