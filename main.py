from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import requests

app = Flask(__name__)

API_KEY = "3337e2b41509cb82f67155d38496af87"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

PROVINCES = [
    "กรุงเทพมหานคร", "เชียงใหม่", "ชัยภูมิ", "ขอนแก่น", "ภูเก็ต", "อยุธยา", 
    "พัทยา", "นครราชสีมา", "สงขลา", "เชียงราย", 
    "สุราษฎร์ธานี", "นครศรีธรรมราช", "อุดรธานี", "บุรีรัมย์",
    "ระยอง", "ตรัง", "กระบี่", "ลำปาง", "ลำพูน", "หนองคาย",
    "สุโขทัย", "เพชรบุรี", "พิษณุโลก", "เลย", "ร้อยเอ็ด",
    "สมุทรปราการ", "สมุทรสงคราม", "สมุทรสาคร", "จันทบุรี",
    "ตราด", "ยะลา", "นราธิวาส", "สตูล", "แม่ฮ่องสอน", "น่าน",
    "พะเยา", "แพร่", "อุตรดิตถ์", "นครสวรรค์", "อุทัยธานี",
    "ชัยนาท", "สิงห์บุรี", "ลพบุรี", "สระบุรี", "นครนายก",
    "ปราจีนบุรี", "สระแก้ว", "เพชรบูรณ์", "หนองบัวลำภู", "อำนาจเจริญ",
    "มุกดาหาร", "ยโสธร", "กาฬสินธุ์", "สกลนคร", "นครพนม",
    "พิจิตร", "กำแพงเพชร", "ตาก", "สุพรรณบุรี", "กาญจนบุรี",
    "ราชบุรี", "ประจวบคีรีขันธ์", "ชุมพร", "ระนอง", "พังงา",
    "สตูล", "ตรัง", "กระบี่", "พัทลุง", "นราธิวาส", "ยะลา",
    "สงขลา", "ปัตตานี"
]

@app.route("/", methods=["GET", "POST"])
def weather_dashboard():
    weather_data = None
    selected_city = None

    if request.method == "POST":
        selected_city = request.form.get("city")
        if selected_city:
            # ดึงข้อมูลจาก API
            url = f"{BASE_URL}?q={selected_city}&appid={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # แปลชื่อเมืองและคำอธิบายสภาพอากาศ
                city_th = GoogleTranslator(source="en", target="th").translate(data["name"])
                weather_description_th = GoogleTranslator(source="en", target="th").translate(data["weather"][0]["description"])
                
                # เก็บข้อมูลจาก API
                weather_data = {
                    "city": city_th,
                    "weather": weather_description_th,
                    "temperature": data["main"]["temp"] - 273.15,  # Convert Kelvin to Celsius
                    "rain": data.get("rain", {}).get("1h", 0),
                    "cloud": data.get("clouds", {}).get("all", 0),
                }
            else:
                weather_data = {"error": "ไม่สามารถดึงข้อมูลได้ กรุณาลองใหม่อีกครั้ง"}

    return render_template("index.html", weather_data=weather_data, provinces=PROVINCES, selected_city=selected_city)

if __name__ == "__main__":
    app.run(debug=True)
