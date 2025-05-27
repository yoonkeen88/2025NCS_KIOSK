# app.py
import tkinter as tk
from tkinter import messagebox
from typing import Any
from kiosk import Menu, DiscountPolicy, OrderSystem
from datetime import datetime
from kiosk import KioskApp


if __name__ == '__main__':
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()