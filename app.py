import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
import datetime

# הגדרות עמוד
st.set_page_config(page_title="מחולל הסכמי הלוואה", layout="wide")

st.title("📄 מחולל הסכמי הלוואה - Living Stone / Cyrus")
st.markdown("מלא את הפרטים למטה כדי לייצר מסמך Word מוכן לחתימה.")

# --- טופס הזנת נתונים ---
with st.form("loan_form"):
    
    # 1. פרטי העסקה והחתימה
    st.markdown("### 1. פרטי חתימה")
    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        signing_location = st.text_input("📍 מקום החתימה (עיר)", "Amsterdam")
    with col_gen2:
        signing_date = st.date_input("📅 תאריך חתימה", datetime.date.today())

    st.divider()

    # 2. צדדים להסכם
    col_lender, col_borrower = st.columns(2)
    
    with col_borrower:
        st.markdown("### 🏠 הלווה (Borrower)")
        borrower_name = st.text_input("שם הלווה", "Cyrus N.M.A. LTD")
        borrower_id = st.text_input("ח.פ / זיהוי", "516370434")
        borrower_address = st.text_input("כתובת", "Tuval 13, Ramat-Gan, 4491000, Israel")
        borrower_email = st.text_input("אימייל", "roy@ibeco.co.il")
        signer_borrower = st.text_input("שם החותם (לווה)", "Roy Mashal")

    with col_lender:
        st.markdown("### 💰 המלווה (Lender)")
        lender_name = st.text_input("שם המלווה", "Living Stone Immo B.V")
        lender_address = st.text_input("כתובת", "Herengracht 564, 1017CH Amsterdam")
        # המייל פה הוא אופציונלי כי הוא קבוע בתבנית שלך, אבל השארתי אותו למקרה שתשנה בעתיד
        lender_email = st.text_input("אימייל", "info@credo-eu.com") 
        signer_lender = st.text_input("שם החותם (מלווה)", "Daniel Rozovski")

    st.divider()

    # 3. תנאים פיננסיים
    st.markdown("### 📊 תנאי ההלוואה")
    col_fin1, col_fin2, col_fin3 = st.columns(3)
    
    with col_fin1:
        loan_amount = st.number_input("סכום ההלוואה (Euro)", value=450000, step=1000)
        interest_rate = st.text_input("ריבית שנתית", "4.5%")
    
    with col_fin2:
        loan_years = st.number_input("משך ההלוואה (שנים)", value=5)
        # חישוב אוטומטי לתאריך פירעון
        default_repayment = signing_date.replace(year=signing_date.year + 5)
        repayment_date = st.date_input("תאריך פירעון", default_repayment)
    
    with col_fin3:
        # חישוב אוטומטי לאופציה (ברירת מחדל: 5 שנים אחרי הפירעון)
        default_extension = default_repayment.replace(year=default_repayment.year + 5)
        extension_date = st.date_input("תאריך אופציית הארכה", default_extension)

    # כפתור שליחה
    submitted = st.form_submit_button("✅ צור קובץ Word להורדה", type="primary")

# --- יצירת המסמך ---
if submitted:
    try:
        # טעינת התבנית
        doc = DocxTemplate("template.docx")

        # יצירת המילון להחלפה - אלו המפתחות ששתלנו בוורד
        context = {
            'signing_location': signing_location,
            'signing_date': signing_date.strftime("%d %B %Y"), # פורמט: 27 October 2024
            
            'borrower_name': borrower_name,
            'borrower_id': borrower_id,
            'borrower_address': borrower_address,
            'borrower_email': borrower_email,
            'signer_borrower': signer_borrower,
            
            'lender_name': lender_name,
            'lender_address': lender_address,
            'lender_email': lender_email, # אם שינית בתבנית, זה יעבוד. אם לא, זה לא יפריע.
            'signer_lender': signer_lender,
            
            'loan_amount': f"{loan_amount:,.0f}", # מוסיף פסיקים (450,000)
            'interest_rate': interest_rate,
            'loan_years': loan_years,
            'repayment_date': repayment_date.strftime("%d %B %Y"),
            'extension_date': extension_date.strftime("%d %B %Y")
        }

        # ביצוע ההחלפה
        doc.render(context)
        
        # שמירה לזיכרון
        bio = BytesIO()
        doc.save(bio)
        bio.seek(0)

        st.success(f"המסמך עבור {borrower_name} מוכן!")
        
        # כפתור הורדה
        st.download_button(
            label="📥 הורד קובץ Word",
            data=bio,
            file_name=f"Loan_Agreement_{borrower_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except Exception as e:
        st.error("⚠️ שגיאה: לא מצאתי את הקובץ template.docx")
        st.info("נא לוודא ששם הקובץ ב-GitHub הוא בדיוק template.docx (אותיות קטנות)")
