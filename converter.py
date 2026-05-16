import pdfplumber
import json

file_name = 'Spring 2026 - Final Exam Schedule.pdf' 
final_data = []

with pdfplumber.open(file_name) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table[1:]: # Ben-seb el header
                # Edit el indexes de 3ala 7asab tartib el columns f malafak
                # Masalan: 0=Date, 1=Time, 2=Room, 3=Course, 4=IDs
                ids_string = str(row[4]) if row[4] else ""
                ids_list = ids_string.split('+')
                
                for s_id in ids_list:
                    clean_id = s_id.strip()
                    if clean_id:
                        final_data.append({
                            "id": clean_id,
                            "course": str(row[3]),
                            "date": str(row[0]),
                            "time": str(row[1]),
                            "room": str(row[2])
                        })

with open('final_exams.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4)

print(f"Done! Extracted {len(final_data)} entries from PDF.")