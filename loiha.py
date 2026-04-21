import tkinter as tk
from tkinter import messagebox
import requests
import re # Narxni qidirish uchun (Regular Expressions)
from deep_translator import GoogleTranslator

def qidirish():
    model = entry.get().strip()
    if not model:
        messagebox.showwarning("Xato", "Iltimos, mashina nomini kiriting!")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # 1-QADAM: Maqolani qidirish
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={model}&limit=1&namespace=0&format=json"
        search_data = requests.get(search_url, headers=headers).json()

        if len(search_data[1]) > 0:
            aniq_nomi = search_data[1][0]
            
            # 2-QADAM: Ma'lumotni olish
            info_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{aniq_nomi.replace(' ', '_')}"
            data = requests.get(info_url, headers=headers).json()
            matn = data.get('extract', '')

            # 3-QADAM: Narxni matn ichidan qidirish (Sodda usul)
            # Matn ichidan $ belgisi bilan kelgan raqamlarni qidiradi
            narx_topildi = re.findall(r'\$[\d,]+', matn)
            narx_matni = f"Taxminiy narxi: {narx_topildi[0]}" if narx_topildi else "Narxi haqida aniq ma'lumot topilmadi (Wiki matnida yo'q)."

            # 4-QADAM: Tarjima
            tarjima = GoogleTranslator(source='en', target='uz').translate(matn)
            
            # Natijani chiqarish
            result_label.config(text=f"📌 {data['title']}:", fg="darkgreen")
            price_label.config(text=f"💰 {narx_matni}", fg="red") # Narxni alohida ko'rsatish
            
            description_text.config(state=tk.NORMAL)
            description_text.delete(1.0, tk.END)
            description_text.insert(tk.END, tarjima)
            description_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Topilmadi", "Bunday mashina topilmadi.")

    except Exception as e:
        messagebox.showerror("Xato", f"Xatolik: {e}")

# --- GUI ---
root = tk.Tk()
root.title("Avto-Narx va Ma'lumot")
root.geometry("500x650")

tk.Label(root, text="🚗 Mashina nomini kiriting:", font=("Arial", 12, "bold")).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), width=30, justify='center')
entry.pack(pady=5)
entry.bind('<Return>', lambda e: qidirish())

tk.Button(root, text="🔎 QIDIRISH", command=qidirish, bg="#4CAF50", fg="white", 
          font=("Arial", 10, "bold"), padx=20, pady=10).pack(pady=15)

# Narx uchun maxsus joy
price_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
price_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 11, "bold"))
result_label.pack()

description_text = tk.Text(root, font=("Arial", 11), height=15, width=55, 
                           wrap=tk.WORD, padx=10, pady=10, state=tk.DISABLED)
description_text.pack(pady=10)

root.mainloop()
