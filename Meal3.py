import http.client
import json
from datetime import datetime, timedelta

def get_school_meal_info(school_code, middle_school_code):
    url = "/hub/mealServiceDietInfo"

    current_date = datetime.now().strftime("%Y%m%d")
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

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

    payload_tomorrow = {
        "KEY": "c3bfcbc6be3548ea975dde21061bee96",
        "Type": "json",
        "pIndex": 1,
        "pSize": 1,
        "ATPT_OFCDC_SC_CODE": middle_school_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": tomorrow_date,
    }

    conn.request("GET", url + "?" + "&".join([f"{key}={value}" for key, value in payload_tomorrow.items()]), headers=headers)
    response_tomorrow = conn.getresponse()
    data_tomorrow = response_tomorrow.read()

    try:
        meal_data_today = json.loads(data_today)["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info_today = "\n".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data_today.split("<br/>"))
    except KeyError:
        cleaned_info_today = "급식 정보를 불러올 수 없습니다."

    try:
        meal_data_tomorrow = json.loads(data_tomorrow)["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info_tomorrow = "\n".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data_tomorrow.split("<br/>"))
    except KeyError:
        cleaned_info_tomorrow = "급식 정보를 불러올 수 없습니다."

    conn.close()
    return cleaned_info_today, cleaned_info_tomorrow

school_code = "9022116"
middle_school_code = "S10"

today_meal, tomorrow_meal = get_school_meal_info(school_code, middle_school_code)

with open("TodayMeals.txt", "w", encoding="utf-8") as today_file:
    today_file.write(today_meal)

with open("TomorrowMeals.txt", "w", encoding="utf-8") as tomorrow_file:
    tomorrow_file.write(tomorrow_meal)

print("급식 정보가 TodayMeals.txt와 TomorrowMeals.txt 파일로 저장되었습니다.")
