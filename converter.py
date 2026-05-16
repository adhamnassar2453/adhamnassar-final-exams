import pdfplumber
import json

# اسم الملف اللي شغال عليه (سواء FinalLabExam.pdf أو MTH216-class6.pdf)
file_name = 'FinalLabExam.pdf' 
final_data = []

with pdfplumber.open(file_name) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if not table:
            continue
            
        header = [str(cell).strip().lower() if cell else "" for cell in table[0]]
        
        # تحديد أماكن الأعمدة بالظبط
        id_idx, first_name_idx, last_name_idx, room_idx, time_idx = -1, -1, -1, -1, -1
        for idx, cell in enumerate(header):
            if 'id' in cell:
                id_idx = idx
            elif 'first' in cell:
                first_name_idx = idx
            elif 'last' in cell:
                last_name_idx = idx
            elif 'room' in cell:
                room_idx = idx
            elif 'start' in cell or 'time' in cell:
                time_idx = idx

        # قيم افتراضية لو الـ Columns مش واضحة
        if id_idx == -1: id_idx = 2
        if first_name_idx == -1: first_name_idx = 0
        if last_name_idx == -1: last_name_idx = 1
        if room_idx == -1: room_idx = 3
        if time_idx == -1: time_idx = 5

        # الـ Forward Fill للجروبات واللجان
        last_room = "53 (27C)" if "mth" in file_name.lower() else "N/A"
        last_time = "7:30 PM" if "mth" in file_name.lower() else "N/A"
        
        default_course = "MTH216" if "mth" in file_name.lower() else "Lab Exam"
        default_date = "17/5/2026"

        for row in table[1:]:
            if not row or id_idx >= len(row) or row[id_idx] is None:
                continue
                
            ids_string = str(row[id_idx]).strip()
            if ids_string.lower() in ['id', 'id number', 'signature', '#', '']:
                continue
            
            # قراءة اسم الطالب عشان الـ JSON ميبقاش ناقص
            f_name = str(row[first_name_idx]).strip() if first_name_idx < len(row) and row[first_name_idx] else ""
            l_name = str(row[last_name_idx]).strip() if last_name_idx < len(row) and row[last_name_idx] else ""
            full_name = f"{f_name} {l_name}".strip()

            # تحديث القاعة والوقت لو السطر فيه بيانات الجروب الجديد
            if room_idx < len(row) and row[room_idx] and str(row[room_idx]).strip(): 
                last_room = str(row[room_idx]).strip()
            if time_idx < len(row) and row[time_idx] and str(row[time_idx]).strip(): 
                last_time = str(row[time_idx]).strip()
                if time_idx + 1 < len(row) and row[time_idx + 1] and 'end' in header[time_idx + 1]:
                    last_time += f" - {str(row[time_idx + 1]).strip()}"

            ids_list = ids_string.split('+')
            for s_id in ids_list:
                clean_id = s_id.strip()
                if clean_id and clean_id.isdigit():
                    # الـ Object كامل بجميع الـ Keys اللي الـ Website مستنيها
                    final_data.append({
                        "id": clean_id,
                        "name": full_name,
                        "course": default_course,
                        "date": default_date,
                        "time": last_time,
                        "room": last_room
                    })

# حفظ الفايل بنفس الاسم وبصيغة سليمة 100% يقرأها الـ JavaScript
with open('final_exams.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"Done! Created final_exams.json with {len(final_data)} entries.")