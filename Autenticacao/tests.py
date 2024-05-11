# from win32api import *
# from win32gui import *
# import win32con
# import sys, os
# import struct
# import time

# class WindowsBalloonTip:
#     def __init__(self, title, msg):
#         message_map = {
#                 win32con.WM_DESTROY: self.OnDestroy,
#         }
#         # Register the Window class.
#         wc = WNDCLASS()
#         hinst = wc.hInstance = GetModuleHandle(None)
#         wc.lpszClassName = "PythonTaskbar"
#         wc.lpfnWndProc = message_map # Também poderia especificar uma wndproc.
#         classAtom = RegisterClass(wc)
#         # Criar a Janela.
#         style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
#         self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
#                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
#                 0, 0, hinst, None)
#         UpdateWindow(self.hwnd)
        
#         # Defina o caminho para o seu ícone
#         iconPathName = os.path.abspath("./logo.ico")  # Substitua "icone.ico" pelo nome do seu ícone
        
#         icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
#         try:
#            hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
#         except:
#           hicon = LoadIcon(0, win32con.IDI_APPLICATION)
#         flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
#         nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
#         Shell_NotifyIcon(NIM_ADD, nid)
#         Shell_NotifyIcon(NIM_MODIFY, \
#                          (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
#                           hicon, "Balloon  tooltip",msg,200,title))
#         # self.show_balloon(title, msg)
#         time.sleep(10)
#         DestroyWindow(self.hwnd)
#     def OnDestroy(self, hwnd, msg, wparam, lparam):
#         nid = (self.hwnd, 0)
#         Shell_NotifyIcon(NIM_DELETE, nid)
#         PostQuitMessage(0)

# def balloon_tip(title, msg):
#     w=WindowsBalloonTip(title, msg)

# if __name__ == '__main__':
#     balloon_tip("Atenção", "Você recebeu um novo pedido!")


import pywhatkit

# Send a WhatsApp Message to a Contact at 1:30 PM
pywhatkit.sendwhatmsg("+5591993233036", "teste", 20, 57)