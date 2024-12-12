import time
import pyautogui
import pygetwindow as gw
import pyperclip

def relative_to_absolute(x_rel, y_rel):
	screen_width, screen_height = pyautogui.size()
	x_abs = x_rel * screen_width
	y_abs = y_rel * screen_height
	return x_abs, y_abs

def save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False):
	pyperclip.copy('0')

	abs_start_x, abs_start_y = relative_to_absolute(rel_start_x, rel_start_y)
	abs_end_x, abs_end_y = relative_to_absolute(rel_end_x, rel_end_y)

	if sap_paste:
		pyautogui.hotkey("ctrl", "y")
	pyautogui.moveTo(abs_start_x, abs_start_y)
	pyautogui.mouseDown()
	pyautogui.moveTo(abs_end_x, abs_end_y)
	pyautogui.mouseUp()

	pyautogui.hotkey("ctrl", "c")
	time.sleep(0.1)
	return pyperclip.paste()

def force_clipboard_content(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False, direction='Down', horizontal=False):
	down = 1
	if direction == 'up':
		down = -1
	message = save_from_clipboard(rel_start_x, rel_start_y, rel_end_x, rel_end_y, sap_paste=False)
	if not message:
		if not horizontal:
			return force_clipboard_content(rel_start_x, rel_start_y + (0.008 * down), rel_end_x, rel_end_y + (0.008 * down), sap_paste)
		else:
			return force_clipboard_content(rel_start_x + (0.008 * down), rel_start_y, rel_end_x + (0.008 * down), rel_end_y, sap_paste)
	else:
		return message

def wait_for_window(window_title, timeout=7):
	start_time = time.time()
	while time.time() - start_time < timeout:
		active_window_title = gw.getActiveWindow().title
		if active_window_title == window_title:
			return True
		time.sleep(0.5)
	return False

def press_key(key, times=1):
	for _ in range(times):
		pyautogui.press(key)

def enter_value(value):
	pyautogui.typewrite(value)
	time.sleep(0.2)
	press_key('enter')

def exit_if_not_window(value):
	if not wait_for_window(value):
		exit(f"Couldn't reach {value}")
