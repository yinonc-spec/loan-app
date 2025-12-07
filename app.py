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
        "signing_date": signing_date,
        "signing_location": signing_location,
        
        # מלווה
        "lender_name": lender_name,
        "lender_id": lender_id,
        "lender_address": lender_address,
        "lender_place": lender_place,
        "signer_lender": signer_lender,

        # לווה
        "borrower_name": borrower_name,
        "borrower_id": borrower_id,
        "borrower_address": borrower_address,
        "borrower_place": borrower_place,
        "borrower_email": borrower_email,
        "signer_borrower": signer_borrower,

        # הלוואה
        "loan_amount": f"{loan_amount:,}",
        "loan_years": str(loan_years),
        "repayment_date": repayment_date,
        "interest_rate": f"{interest_rate}%",
        "extension_date": extension_date,

        # שיפוט
        "country": jurisdiction_country,
        "city": jurisdiction_city
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
