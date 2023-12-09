import http.client
import json
from datetime import datetime
import tkinter as tk
from tkinter import Text, Scrollbar

def get_today_meal_info(school_code, middle_school_code):
    url = "/hub/mealServiceDietInfo"

    current_date = datetime.now().strftime("%Y%m%d")

    headers = {
        "Content-type": "application/json",
    }

    conn = http.client.HTTPSConnection("open.neis.go.kr")
    payload_today = {
        "KEY": "c3bfcbc6be3548ea975dde21061bee96",
        "Type": "json",
        "pIndex": 1,
        "pSize": 1,
        "ATPT_OFCDC_SC_CODE": middle_school_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": current_date,
    }

    conn.request("GET", url + "?" + "&".join([f"{key}={value}" for key, value in payload_today.items()]), headers=headers)
    response_today = conn.getresponse()
    data_today = response_today.read()

    try:
        meal_data_today = json.loads(data_today)["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info_today = "\n".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data_today.split("<br/>"))
    except KeyError:
        cleaned_info_today = "급식 정보를 불러올 수 없습니다."

    conn.close()
    return cleaned_info_today

def show_meal_info():
    today_meal = get_today_meal_info(school_code_entry.get(), middle_school_code_entry.get())
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, today_meal)

# Create the main Tkinter window
root = tk.Tk()
root.title("급식 정보")

# Create and place widgets in the window
school_code_label = tk.Label(root, text="학교 코드:")
school_code_label.pack()

school_code_entry = tk.Entry(root)
school_code_entry.pack()

middle_school_code_label = tk.Label(root, text="시도교육청 코드:")
middle_school_code_label.pack()

middle_school_code_entry = tk.Entry(root)
middle_school_code_entry.pack()

show_meal_button = tk.Button(root, text="급식 보기", command=show_meal_info)
show_meal_button.pack()

result_text = Text(root, wrap=tk.WORD, width=40, height=10)
result_text.pack()

scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Start the Tkinter event loop
root.mainloop()
