import tkinter as tkimport pyautoguidef showAlert(message,button='OK'):    pyautogui.alert(message,timeout=None,button=button) # type: ignoredef showYesNo(message):    return pyautogui.confirm(message, buttons=['Yes','No'],timeout=None) # type: ignoredef showMsgCustom(message, buttons):    return pyautogui.confirm(message, buttons=buttons,timeout=None) # type: ignoreimport tkinter as tk
import pyautogui

def showAlert(message,button='OK'):
    pyautogui.alert(message,timeout=None,button=button) # type: ignore

def showYesNo(message):
    return pyautogui.confirm(message, buttons=['Yes','No'],timeout=None) # type: ignore

def showMsgCustom(message, buttons):
import tkinter as tk
