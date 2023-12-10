import http.client
import json
from datetime import datetime
from datetime import date
import tkinter as tk
from tkinter import Text, Scrollbar, Entry

today = date.today()

def get_meal_info(school_code, middle_school_code, selected_date):
    url = "/hub/mealServiceDietInfo"

    headers = {
        "Content-type": "application/json",
    }

    conn = http.client.HTTPSConnection("open.neis.go.kr")
    payload = {
        "KEY": "c3bfcbc6be3548ea975dde21061bee96",
        "Type": "json",
        "pIndex": 1,
        "pSize": 1,
        "ATPT_OFCDC_SC_CODE": middle_school_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": selected_date,
    }

    conn.request("GET", url + "?" + "&".join([f"{key}={value}" for key, value in payload.items()]), headers=headers)
    response = conn.getresponse()
    data = response.read()

    try:
        meal_data = json.loads(data)["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info = "\n".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data.split("<br/>"))
    except KeyError:
        cleaned_info = "급식 정보를 불러올 수 없습니다."

    conn.close()
    return cleaned_info

def show_meal_info():
    selected_date = today
    meal_info = get_meal_info("9022116", "S10", selected_date)
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
