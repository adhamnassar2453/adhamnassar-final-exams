import pdfplumber
import json
import re

pdf_path = "Spring 2026 - Final Exam Schedule (1).pdf"
output_json = "final_exams.json"

exams_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if not table:
            continue
            
        for row in table:
            if not row or len(row) < 5:
                continue
                
            date = row[0]
            time = row[1]
            room = row[2]
            course = row[3]
            students_sets_text = row[4]
            
            if "Day" in str(date) or not course:
                continue
                
            if students_sets_text:
                student_ids = re.findall(r'\b\d{9}\b', str(students_sets_text))
                for s_id in student_ids:
                    exams_data.append({
                        "id": str(s_id).strip(),
                        "course": str(course).strip(),
                        "date": str(date).replace('\n', ' ').strip(),
                        "time": str(time).replace('\n', ' ').strip(),
                        "room": str(room).replace('\n', ' ').strip()
                    })

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(exams_data, f, ensure_ascii=False, indent=4)