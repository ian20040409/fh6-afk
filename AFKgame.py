import vgamepad as vg
import time
import random
import threading

print("========================================")
print("Forza Horizon 6 掛機腳本 (純油門 + 起步防滑版)")
print("========================================")
print("提示：直接按下 Enter 鍵即可使用括號內的預設值")
print("注意：請務必以系統管理員身分執行此腳本。")
print("")

def input_float(prompt_text, default_value):
    value = input(prompt_text)
    try:
        return float(value) if value.strip() else default_value
    except ValueError:
        print("輸入格式錯誤，自動使用預設值：" + str(default_value))
        return default_value

# 基本油門設定
input_rt = input_float("請輸入「正常行駛」油門力道（0 到 100，預設 100）：", 100.0)
RT_VALUE = max(0.0, min(1.0, input_rt / 100.0))

# 起步階段設定 (純油門限制)
input_startup_sec = input_float("請輸入「起步防滑」持續秒數（預設 60.0，輸入 0 關閉）：", 60.0)
STARTUP_DURATION = max(0.0, input_startup_sec)

input_startup_rt = input_float("請輸入「起步防滑」期間的油門力道（0 到 100，預設 50）：", 50.0)
STARTUP_RT_VALUE = max(0.0, min(1.0, input_startup_rt / 100.0))

# 油門加速度設定（線性增加）
input_rt_accel = input_float("請輸入油門加速度（%/秒，預設 50，輸入 0 關閉線性加速）：", 50.0)
RT_ACCELERATION = max(0.0, min(1.0, input_rt_accel / 100.0))  # 轉換為 0-1 範圍

# 防掛機設定
input_rt_release = input_float("請輸入「放開油門」間隔秒數（預設 15.0，輸入 0 關閉）：", 15.0)
RT_RELEASE_INTERVAL = max(0.0, input_rt_release)

DELAY_START_SEC = max(0.0, input_float("請輸入延遲啟動秒數（預設 10.0）：", 10.0))

LOOP_INTERVAL = 0.05

print("")
print("========================================")
print("【停止掛機方法】：請按 Alt + Tab 切換出遊戲，直接關閉此黑色視窗即可。")
print("========================================")

# 初始化虛擬控制器
gamepad = vg.VX360Gamepad()
state_lock = threading.RLock()

# 狀態變數
current_rt = -1
last_rt_release_time = 0.0
next_rt_interval = RT_RELEASE_INTERVAL
actual_rt = 0.0  # 實際油門值（用於線性加速）

def set_rt(rt_val: float):
    global current_rt
    with state_lock:
        rt_int = int(rt_val * 255)
        
        if current_rt != rt_int:
            current_rt = rt_int
            gamepad.right_trigger(rt_int)
            gamepad.update()

# 執行倒數計時
for i in range(int(DELAY_START_SEC), 0, -1):
    print("距離掛機啟動還有 " + str(i) + " 秒...")
    time.sleep(1)

print("掛機正式啟動！(請確保您目前在遊戲畫面內)")

# 初始化時間
now_perf = time.perf_counter()
session_start_time = now_perf
last_rt_release_time = now_perf
last_accel_time = now_perf  # 用於追踪油門加速時間
startup_phase_printed = False
normal_phase_printed = False

try:
    while True:
        now = time.perf_counter()
        elapsed_time = now - session_start_time
        
        # 決定當下的目標油門
        if elapsed_time < STARTUP_DURATION:
            target_rt = STARTUP_RT_VALUE
            if not startup_phase_printed:
                print("進入「起步防滑」模式：油門限制 " + str(int(STARTUP_RT_VALUE * 100)) + "%")
                startup_phase_printed = True
        else:
            target_rt = RT_VALUE
            if not normal_phase_printed and STARTUP_DURATION > 0:
                print("起步階段結束，恢復正常油門力道：" + str(int(RT_VALUE * 100)) + "%")
                normal_phase_printed = True

        # 防掛機偵測：定期短暫放開油門
        if RT_RELEASE_INTERVAL > 0 and (now - last_rt_release_time >= next_rt_interval):
            time_str = time.strftime('%H:%M:%S', time.localtime())
            print("防掛機機制：放開油門 (" + time_str + ")")
            
            # 放開油門
            set_rt(0.0)
            actual_rt = 0.0  # 重置實際油門值
            time.sleep(random.uniform(0.1, 0.3))
            
            last_rt_release_time = time.perf_counter()
            last_accel_time = time.perf_counter()  # 重置加速計時
            next_rt_interval = max(5.0, random.uniform(RT_RELEASE_INTERVAL - 2.0, RT_RELEASE_INTERVAL + 2.0))
        else:
            # 線性加速邏輯
            if RT_ACCELERATION > 0 and actual_rt < target_rt:
                # 計算時間差並增加油門
                time_delta = now - last_accel_time
                actual_rt += RT_ACCELERATION * time_delta
                
                # 不能超過目標油門值
                if actual_rt > target_rt:
                    actual_rt = target_rt
                
                last_accel_time = now
            else:
                # 如果關閉線性加速或已達目標，直接使用目標油門
                actual_rt = target_rt
            
            # 正常執行實際油門狀態
            set_rt(actual_rt)

        time.sleep(LOOP_INTERVAL)

except KeyboardInterrupt:
    pass
except Exception as e:
    print("發生錯誤：" + str(e))
finally:
    try:
        gamepad.right_trigger(0)
        gamepad.update()
    except Exception:
        pass
    print("已安全釋放虛擬控制器按鍵。")
