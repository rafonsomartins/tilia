import time
import pyautogui
import pygetwindow as gw
import pyperclip

def wait_for_window(window_title, timeout=7, wait=0.5):
	start_time = time.time()
	while time.time() - start_time < timeout:
		active_window_title = gw.getActiveWindow().title
		if active_window_title == window_title:
			return True
		time.sleep(wait)
	return False

def relative_to_absolute(x_rel, y_rel):
	screen_width, screen_height = pyautogui.size()
	x_abs = x_rel * screen_width
	y_abs = y_rel * screen_height
	return x_abs, y_abs

def mouse_click(x, y, absolute=False, wait=0):
	if not absolute:
		x, y = relative_to_absolute(x, y)
	pyautogui.moveTo(x, y)
	time.sleep(wait)
	pyautogui.click()

def press_key(key, times=1):
	for _ in range(times):
		pyautogui.press(key)

def enter_value(value, wait=0.2):
	pyautogui.typewrite(value)
	time.sleep(wait)
	press_key('enter')

def exit_if_not_window(value, timeout=7, wait=0.5):
	if not wait_for_window(value, timeout, wait):
		exit(f"Couldn't reach {value}")

def save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, absolute=False):
	pyperclip.copy('0')

	if not absolute:
		abs_start_x, abs_start_y = relative_to_absolute(rel_start_x, rel_start_y)
		abs_end_x, abs_end_y = relative_to_absolute(rel_end_x, rel_end_y)
	else:
		abs_start_x, abs_start_y = rel_start_x, rel_start_y
		abs_end_x, abs_end_y = rel_end_x, rel_end_y

	if sap_paste:
		pyautogui.hotkey("ctrl", "y")
	pyautogui.moveTo(abs_start_x, abs_start_y)
	pyautogui.mouseDown()
	pyautogui.moveTo(abs_end_x, abs_end_y)
	pyautogui.mouseUp()

	pyautogui.hotkey("ctrl", "c")
	time.sleep(0.1)
	return pyperclip.paste()

def force_clipboard_content(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, absolute=False, direction='Down', horizontal=False, ratio=0.008):
	down = 1
	if direction == 'up':
		down = -1
	message = save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste)
	if not message or message == '0':
		if not horizontal:
			return force_clipboard_content(rel_start_x, rel_start_y + (ratio * down), rel_end_x, rel_end_y + (ratio * down), sap_paste, absolute)
		else:
			return force_clipboard_content(rel_start_x + (ratio * down), rel_start_y, rel_end_x + (ratio * down), rel_end_y, sap_paste, absolute)
	else:
		return message
