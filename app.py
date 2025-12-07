import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import date

# כותרת האפליקציה (מתוקנת)
st.title("Living Stone - מחולל הסכמי הלוואה")

st.write("מלא את הפרטים למטה כדי לייצר מסמך Word מוכן לחתימה.")

# --- איסוף נתונים ---
st.header("פרטי הצדדים")

# פרטי המלווה
st.subheader("פרטי המלווה")
lender_name = st.text_input("שם המלווה")
lender_id = st.text_input("מספר חברה / ת.ז. של המלווה")
lender_place = st.text_input("מקום התאגדות המלווה (מדינה/עיר)")

# פרטי הלווה
st.subheader("פרטי הלווה")
borrower_name = st.text_input("שם הלווה")
borrower_place = st.text_input("מקום התאגדות הלווה (מדינה/עיר)")

# פרטי ההלוואה
st.header("תנאי ההלוואה")
amount = st.number_input("סכום ההלוואה", min_value=0)
interest = st.number_input("ריבית שנתית (%)", min_value=0.0, step=0.1)
date_string = date.today().strftime("%d/%m/%Y")

# --- סעיף 8.3 (סמכות שיפוט) ---
st.subheader("סמכות שיפוט (סעיף 8.3)")
jurisdiction_option = st.selectbox(
    "בחר את מדינת השיפוט והעיר:",
    (
        "מדינת ישראל והעיר ת\"א",
        "גרמניה והעיר אסן",
        "הולנד והעיר אמסטרדם"
    )
)

# לוגיקה לתרגום הבחירה לנתונים במסמך
if jurisdiction_option == "מדינת ישראל והעיר ת\"א":
    jurisdiction_country = "Israel"
    jurisdiction_city = "Tel Aviv"
elif jurisdiction_option == "גרמניה והעיר אסן":
    jurisdiction_country = "Germany"
    jurisdiction_city = "Essen"
else:
    jurisdiction_country = "Netherlands"
    jurisdiction_city = "Amsterdam"

# --- כפתור יצירה ---
if st.button("צור הסכם הלוואה"):
    # טעינת התבנית
    doc = DocxTemplate("template.docx")

    # יצירת המילון (Context) עם כל הנתונים החדשים
    context = {
        "lender_name": lender_name,
        "lender_id": lender_id,
        "lender_place": lender_place,
        "borrower_name": borrower_name,
        "borrower_place": borrower_place,
        "amount": amount,
        "interest": interest,
        "country": jurisdiction_country,
        "city": jurisdiction_city,
        "date": date_string
    }

    # רנדור המסמך
    doc.render(context)

    # שמירה לזיכרון והורדה
    bio = io.BytesIO()
    doc.save(bio)
    
    st.download_button(
        label="הורד קובץ Word",
        data=bio.getvalue(),
        file_name="Loan_Agreement_Generated.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
