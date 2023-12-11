import http.client
import json
from datetime import datetime
import tkinter as tk
from tkinter import Text, Scrollbar

def getmeal(sc, msc):
    url = "/hub/mealServiceDietInfo"

    current_date = datetime.now().strftime("%Y%m%d")

    headers = {
        "Content-type": "application/json",
    }

    conn = http.client.HTTPSConnection("open.neis.go.kr")
    payload_today = {
        "KEY": "700899c1168e4cffa03e89a7aa650f5d",
        "Type": "json",
        "pIndex": 1,
        "pSize": 1,
        "ATPT_OFCDC_SC_CODE": msc,
        "SD_SCHUL_CODE": sc,
        "MLSV_YMD": current_date,
    }

    conn.request("GET", url + "?" + "&".join([f"{key}={value}" for key, value in payload_today.items()]), headers=headers)
    response_today = conn.getresponse()
    data_today = response_today.read()

    try:
        meal_data_today = json.loads(data_today)["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info_today = "\n".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data_today.split("<br/>"))
    except KeyError:
        cleaned_info_today = "Can't acess to info"

    conn.close()
    return cleaned_info_today

def show_meal_info():
    meal_info = getmeal("9022116", "S10")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, meal_info)

# Create the main Tkinter window
root = tk.Tk()
root.title("급식 정보")


result_text = Text(root, wrap=tk.WORD, width=40, height=10)
result_text.pack()

scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Call show_meal_info immediately after creating the window
show_meal_info()

# Start the Tkinter event loop
root.mainloop()
