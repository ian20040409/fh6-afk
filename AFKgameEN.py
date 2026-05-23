import vgamepad as vg
import time
import random
import threading

print("========================================")
print("Forza Horizon 6 AFK Script (throttle only + soft start)")
print("========================================")
print("Tip: press Enter to use the default value shown in parentheses.")
print("Important: run this script as Administrator.")
print("")

def input_float(prompt_text, default_value):
    value = input(prompt_text)
    try:
        return float(value) if value.strip() else default_value
    except ValueError:
        print("Invalid input. Using default value: " + str(default_value))
        return default_value

# Basic throttle settings
input_rt = input_float("Normal driving throttle (0 to 100, default 100): ", 100.0)
RT_VALUE = max(0.0, min(1.0, input_rt / 100.0))

# Soft-start settings (throttle limit only)
input_startup_sec = input_float("Soft-start duration in seconds (default 60.0, enter 0 to disable): ", 60.0)
STARTUP_DURATION = max(0.0, input_startup_sec)

input_startup_rt = input_float("Soft-start throttle (0 to 100, default 50): ", 50.0)
STARTUP_RT_VALUE = max(0.0, min(1.0, input_startup_rt / 100.0))

# Throttle acceleration settings (linear ramp)
input_rt_accel = input_float("Throttle acceleration (% per second, default 50, enter 0 to disable ramping): ", 50.0)
RT_ACCELERATION = max(0.0, min(1.0, input_rt_accel / 100.0))  # Convert to the 0-1 range.

# Anti-AFK settings
input_rt_release = input_float("Throttle release interval in seconds (default 15.0, enter 0 to disable): ", 15.0)
RT_RELEASE_INTERVAL = max(0.0, input_rt_release)

DELAY_START_SEC = max(0.0, input_float("Start delay in seconds (default 10.0): ", 10.0))

LOOP_INTERVAL = 0.05

print("")
print("========================================")
print("How to stop: press Alt + Tab to leave the game, then close this console window.")
print("========================================")

# Initialize the virtual controller.
gamepad = vg.VX360Gamepad()
state_lock = threading.RLock()

# Runtime state
current_rt = -1
last_rt_release_time = 0.0
next_rt_interval = RT_RELEASE_INTERVAL
actual_rt = 0.0  # Actual throttle value used for linear ramping.

def set_rt(rt_val: float):
    global current_rt
    with state_lock:
        rt_int = int(rt_val * 255)
        
        if current_rt != rt_int:
            current_rt = rt_int
            gamepad.right_trigger(rt_int)
            gamepad.update()

# Start countdown.
for i in range(int(DELAY_START_SEC), 0, -1):
    print("AFK mode starts in " + str(i) + " seconds...")
    time.sleep(1)

print("AFK mode started. Make sure the game window is active.")

# Initialize timers.
now_perf = time.perf_counter()
session_start_time = now_perf
last_rt_release_time = now_perf
last_accel_time = now_perf  # Used to track throttle ramp timing.
startup_phase_printed = False
normal_phase_printed = False

try:
    while True:
        now = time.perf_counter()
        elapsed_time = now - session_start_time
        
        # Pick the target throttle for the current phase.
        if elapsed_time < STARTUP_DURATION:
            target_rt = STARTUP_RT_VALUE
            if not startup_phase_printed:
                print("Soft-start mode: throttle limited to " + str(int(STARTUP_RT_VALUE * 100)) + "%")
                startup_phase_printed = True
        else:
            target_rt = RT_VALUE
            if not normal_phase_printed and STARTUP_DURATION > 0:
                print("Soft-start ended. Normal throttle restored to " + str(int(RT_VALUE * 100)) + "%")
                normal_phase_printed = True

        # Anti-AFK: briefly release the throttle at random-ish intervals.
        if RT_RELEASE_INTERVAL > 0 and (now - last_rt_release_time >= next_rt_interval):
            time_str = time.strftime('%H:%M:%S', time.localtime())
            print("Anti-AFK: releasing throttle (" + time_str + ")")
            
            # Release throttle.
            set_rt(0.0)
            actual_rt = 0.0  # Reset actual throttle value.
            time.sleep(random.uniform(0.1, 0.3))
            
            last_rt_release_time = time.perf_counter()
            last_accel_time = time.perf_counter()  # Reset ramp timing.
            next_rt_interval = max(5.0, random.uniform(RT_RELEASE_INTERVAL - 2.0, RT_RELEASE_INTERVAL + 2.0))
        else:
            # Linear throttle ramp.
            if RT_ACCELERATION > 0 and actual_rt < target_rt:
                # Increase throttle based on elapsed time.
                time_delta = now - last_accel_time
                actual_rt += RT_ACCELERATION * time_delta
                
                # Do not exceed the target throttle.
                if actual_rt > target_rt:
                    actual_rt = target_rt
                
                last_accel_time = now
            else:
                # If ramping is disabled or complete, use the target throttle.
                actual_rt = target_rt
            
            # Apply the actual throttle state.
            set_rt(actual_rt)

        time.sleep(LOOP_INTERVAL)

except KeyboardInterrupt:
    pass
except Exception as e:
    print("Error: " + str(e))
finally:
    try:
        gamepad.right_trigger(0)
        gamepad.update()
    except Exception:
        pass
    print("Virtual controller inputs released safely.")
