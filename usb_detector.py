 # usb_detector.py
import pyudev
import time

print("--- USB Detector Script ---")
print("Initializing USB monitoring...")

try:
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    # Filter for block devices (like disks, partitions) being added
    monitor.filter_by(subsystem='block', device_type='partition')
    print("Monitoring started. Waiting for a USB storage partition to be added...")
except Exception as e:
    print(f"Error initializing pyudev monitor: {e}")
    print("Make sure pyudev is installed ('pip install pyudev') and you have necessary permissions.")
    exit()

while True: 
    try:
        device = monitor.poll(timeout=1) # Check every 1 second

        if device is not None and device.action == 'add':
            print(f"\n[+] Partition Added!")
            print(f"  - Device Node: {device.device_node}")
            print(f"  - SysPath: {device.sys_path}")
            # Check for common properties indicating a USB storage partition
            if device.get('ID_BUS') == 'usb' and device.get('ID_FS_TYPE'):
                print(f"  - Detected as USB Storage Partition")
                print(f"  - File System: {device.get('ID_FS_TYPE')}")
                # You could add code here later to automatically find the mount point
            else:
                print("  - (Not identified as USB storage or no filesystem detected yet)")
            print("\nWaiting for next event...")

        # Add a small delay to prevent high CPU usage in the loop if poll returns immediately
        time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting script.")
        break
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        time.sleep(5) # Wait before retrying
