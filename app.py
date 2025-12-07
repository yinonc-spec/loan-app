import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import date

# כותרת האפליקציה
st.title("Living Stone - מחולל הסכמי הלוואה")
st.write("מלא את הפרטים למטה כדי לייצר מסמך Word מוכן לחתימה.")

# --- 1. פרטי חתימה כלליים ---
st.header("פרטים כלליים")
signing_date = date.today().strftime("%d/%m/%Y")
signing_location = st.text_input("מקום החתימה (לדוגמה: Tel Aviv, Israel)", value="Tel Aviv, Israel")

# --- 2. פרטי המלווה (Lender) ---
st.header("פרטי המלווה (Lender)")
lender_name = st.text_input("שם המלווה (Lender Name)")
lender_id = st.text_input("מספר חברה/מזהה המלווה (Registration Num)")
lender_address = st.text_input("כתובת המלווה")
lender_place = st.text_input("מקום התאגדות המלווה (Lender Jurisdiction)")
signer_lender = st.text_input("שם החותם מטעם המלווה (Signer Name)")

# --- 3. פרטי הלווה (Borrower) ---
st.header("פרטי הלווה (Borrower)")
borrower_name = st.text_input("שם הלווה (Borrower Name)")
borrower_id = st.text_input("מספר חברה/מזהה הלווה")
borrower_address = st.text_input("כתובת הלווה")
borrower_place = st.text_input("מקום התאגדות הלווה (Borrower Jurisdiction)")
borrower_email = st.text_input("אימייל הלווה")
signer_borrower = st.text_input("שם החותם מטעם הלווה (Signer Name)")

# --- 4. תנאי ההלוואה ---
st.header("תנאי ההלוואה")
loan_amount = st.number_input("סכום ההלוואה (מספר בלבד)", min_value=0)
interest_rate = st.number_input("ריבית שנתית (%)", min_value=0.0, step=0.1)
loan_years = st.number_input("משך ההלוואה בשנים", min_value=0, step=1, value=2)
repayment_date = st.text_input("תאריך פירעון סופי (לדוגמה: 31/12/2026)")
extension_date = st.text_input("תאריך פירעון במקרה של הארכה (לדוגמה: 31/12/2031)")

# --- 5. סמכות שיפוט (סעיף 8.3) ---
st.subheader("סמכות שיפוט (סעיף 8.3)")
jurisdiction_option = st.selectbox(
    "בחר את מדינת השיפוט והעיר:",
    (
        "מדינת ישראל והעיר ת\"א",
        "גרמניה והעיר אסן",
        "הולנד והעיר אמסטרדם"
    )
)

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

    # יצירת המילון (Context) - מיפוי המשתנים לתבנית
    context = {
        # כללי
        [cite_start]"signing_date": signing_date,           # [cite: 2]
        [cite_start]"signing_location": signing_location,   # [cite: 2]
        
        # מלווה
        [cite_start]"lender_name": lender_name,             # [cite: 2]
        [cite_start]"lender_id": lender_id,                 # [cite: 2]
        [cite_start]"lender_address": lender_address,       # [cite: 2]
        [cite_start]"lender_place": lender_place,           # [cite: 2]
        [cite_start]"signer_lender": signer_lender,         # [cite: 38]

        # לווה
        [cite_start]"borrower_name": borrower_name,         # [cite: 2]
        [cite_start]"borrower_id": borrower_id,             # [cite: 2]
        [cite_start]"borrower_address": borrower_address,   # [cite: 2]
        "borrower_place": borrower_place,       # שים לב: ב-Word זה חייב להיות עם קו תחתון!
        [cite_start]"borrower_email": borrower_email,       # [cite: 29]
        [cite_start]"signer_borrower": signer_borrower,     # [cite: 38]

        # הלוואה
        "loan_amount": f"{loan_amount:,}",      # מוסיף פסיקים למספרים (1,000)
        [cite_start]"loan_years": str(loan_years),          # [cite: 9]
        [cite_start]"repayment_date": repayment_date,       # [cite: 10]
        [cite_start]"interest_rate": f"{interest_rate}%",   # [cite: 12] מוסיף סימן אחוז
        [cite_start]"extension_date": extension_date,       # [cite: 13]

        # שיפוט
        [cite_start]"country": jurisdiction_country,        # [cite: 19]
        [cite_start]"city": jurisdiction_city               # [cite: 19]
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
