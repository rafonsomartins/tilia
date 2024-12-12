import pyautogui
import time
from utils.pyautogui_utils import exit_if_not_window, enter_value, wait_for_window, press_key

def close_sap():
	pyautogui.hotkey("alt", "f4")
	time.sleep(0.2)
	press_key("tab")
	press_key("enter")
	return

def open_sap(username, password):
	press_key('winleft')
	time.sleep(0.2)
	exit_if_not_window("Search")
	enter_value("SAP")

	exit_if_not_window("SAP Logon 740")

	press_key('enter')

	exit_if_not_window("SAP")

	pyautogui.typewrite(str(username))
	time.sleep(0.1)
	press_key('down')
	enter_value(str(password))

	exit_if_not_window("SAP Easy Access")

	pyautogui.hotkey("alt", "space")
	press_key("x")

	time.sleep(0.2)

	return 1

def go_to_main_page():
	for _ in range(5):
		if wait_for_window("SAP Easy Access", 0.5):
			return 1
		press_key('esc')
	exit("Coudn't reach SAP main page")
