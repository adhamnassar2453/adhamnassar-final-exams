import pdfplumber
import json

pdf_path = "Spring 2026 - Final Exam Schedule (1).pdf"
output_json = "final_exams.json"

exams_data = []

print("Starting to extract PDF data... Please wait.")

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
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
            
            if not date or "Day" in str(date) or not course:
                continue
                
            exams_data.append({
                "course": str(course).strip(),
                "date": str(date).replace('\n', ' ').strip(),
                "time": str(time).replace('\n', ' ').strip(),
                "room": str(room).replace('\n', ' ').strip(),
                "students_sets": str(students_sets_text).replace('\n', ' ').strip() if students_sets_text else ""
            })
        print(f"Page {page_num} processed successfully.")

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(exams_data, f, ensure_ascii=False, indent=4)

print(f"Done! Successfully saved {len(exams_data)} rows into {output_json}")