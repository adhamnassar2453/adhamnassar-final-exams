import pdfplumber
import json
import re

pdf_path = "Spring 2026 - Final Exam Schedule (1).pdf"
json_path = "final_exams.json"

exams = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
            
        lines = text.split("\n")
        current_date = ""
        current_time = ""
        
        for line in lines:
            # لقط التاريخ
            if "2026" in line and any(m in line for m in ["January", "February", "March", "April", "May", "June"]):
                current_date = line.strip()
                continue
                
            # لقط الوقت
            if "AM" in line or "PM" in line:
                current_time = line.strip()
                continue
                
            # فلترة: لو السطر فيه ID ومكتوب فيه "Lab" أو "LAB" أعمل له Skip علطول
            if "Lab" in line or "LAB" in line:
                continue
                
            # لقط السطر اللي فيه الـ ID والمادة والمدرج
            match = re.search(r"(\d{9})\s+([A-Z]{3,4}\d{3})\s+(.*)", line)
            if match:
                student_id = match.group(1)
                course = match.group(2)
                room = match.group(3).strip()
                
                exams.append({
                    "id": student_id,
                    "course": course,
                    "date": current_date,
                    "time": current_time,
                    "room": room
                })

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(exams, f, indent=4, ensure_ascii=False)

print(f"Done! Saved {len(exams)} final exams to {json_path}")