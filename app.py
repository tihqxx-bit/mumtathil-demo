import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

st.set_page_config(
    page_title="ممتثل",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# STYLE
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #08111F 0%, #0F172A 55%, #172554 100%);
    color: white;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

.main-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 26px;
    padding: 34px;
    margin-bottom: 22px;
}

.main-card h1 {
    font-size: 52px;
    color: white;
    margin-bottom: 6px;
}

.main-card p {
    color: #CBD5E1;
    font-size: 17px;
    line-height: 1.8;
}

.result-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 22px;
    padding: 24px;
    margin-top: 20px;
}

.red-box {
    background: rgba(239,68,68,0.14);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 16px;
    padding: 16px;
}

.green-box {
    background: rgba(34,197,94,0.14);
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 16px;
    padding: 16px;
}

.yellow-box {
    background: rgba(245,158,11,0.14);
    border: 1px solid rgba(245,158,11,0.4);
    border-radius: 16px;
    padding: 16px;
}

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    background: linear-gradient(90deg, #2563EB, #14B8A6);
    color: white;
    border: none;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================

def load_regulations():
    try:
        return pd.read_csv("regulations.csv")
    except Exception:
        data = {
            "authority": ["SAMA", "SAMA", "SAMA", "SAMA", "CMA", "Internal"],
            "topic": [
                "الإفصاح عن الرسوم",
                "شكاوى العملاء",
                "مشاركة البيانات",
                "إيقاف الخدمة",
                "تضارب المصالح",
                "سياسة الشركة الداخلية"
            ],
            "keywords": [
                "رسوم,تعديل الرسوم,تغيير الرسوم,بدون إشعار,دون إشعار",
                "شكوى,شكاوى,اعتراض,تظلم,خدمة العملاء",
                "بيانات,مشاركة البيانات,طرف ثالث,مزود خدمة,خصوصية",
                "إيقاف الخدمة,تعليق الحساب,إغلاق الحساب,حظر",
                "تضارب المصالح,مصالح,إفصاح,استثمار,مستثمر",
                "اعتماد,موافقة,صلاحية,تفويض"
            ],
            "risk_level": ["High", "Medium", "High", "Medium", "High", "Medium"],
            "problem": [
                "البند قد يسمح بتغيير الرسوم دون إشعار واضح للعميل.",
                "لا يظهر وجود آلية واضحة لاستقبال ومعالجة شكاوى العملاء.",
                "البند قد يسمح بمشاركة بيانات العميل مع أطراف خارجية دون ضوابط واضحة.",
                "البند قد يمنح الشركة صلاحية إيقاف الخدمة دون سبب أو إشعار واضح.",
                "قد لا يكون هناك إفصاح كاف عن تضارب المصالح في الخدمات الاستثمارية.",
                "العقد قد لا يوضح من يملك صلاحية الموافقة أو الاعتماد داخليا."
            ],
            "consequence": [
                "قد يؤدي إلى شكاوى عملاء أو إلزام الشركة بتعديل البند أو إجراء رقابي.",
                "قد يؤدي إلى ضعف حماية العميل وتصعيد الشكاوى للجهات المختصة.",
                "قد يؤدي إلى مخاطر خصوصية ومساءلة تنظيمية وفقدان ثقة العملاء.",
                "قد يؤدي إلى شكاوى عملاء أو اعتبار البند غير متوازن.",
                "قد يؤدي إلى مخاطر تنظيمية مرتبطة بحماية المستثمر والإفصاح.",
                "قد يخالف سياسات الشركة الداخلية أو يسبب ضعفا في الحوكمة."
            ],
            "suggested_fix": [
                "إشعار العميل قبل تغيير الرسوم بمدة واضحة مع توضيح آلية الاعتراض أو الإنهاء.",
                "إضافة بند يوضح طريقة تقديم الشكاوى ومدة الرد وآلية التصعيد.",
                "توضيح متى ولماذا تتم مشاركة البيانات ومع من، مع الالتزام بسياسة الخصوصية.",
                "تحديد حالات الإيقاف بوضوح مع إشعار العميل متى ما أمكن.",
                "إضافة بند يشرح حالات تضارب المصالح وكيفية إدارتها والإفصاح عنها.",
                "تحديد صلاحيات الاعتماد والمراجعة الداخلية قبل توقيع العقد."
            ]
        }
        return pd.DataFrame(data)


def extract_text_from_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if file_name.endswith(".pdf"):
        text = ""
        file_bytes = uploaded_file.read()
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text

    return ""


def analyze_contract(contract_text, match_source):
    regulations = load_regulations()
    results = []
    contract_text_lower = contract_text.lower()

    for _, row in regulations.iterrows():
        authority = str(row["authority"])
        keywords = str(row["keywords"]).split(",")

        if match_source == "سياسات الشركة الداخلية فقط" and authority != "Internal":
            continue

        if match_source == "لوائح SAMA فقط" and authority != "SAMA":
            continue

        if match_source == "لوائح CMA فقط" and authority != "CMA":
            continue

        matched_keywords = []

        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and keyword.lower() in contract_text_lower:
                matched_keywords.append(keyword)

        if matched_keywords:
            results.append({
                "authority": row["authority"],
                "topic": row["topic"],
                "risk_level": row["risk_level"],
                "matched_keywords": "، ".join(matched_keywords),
                "problem": row["problem"],
                "consequence": row["consequence"],
                "suggested_fix": row["suggested_fix"]
            })

    return results


def calculate_scores(results):
    high_count = sum(1 for item in results if item["risk_level"] == "High")
    medium_count = sum(1 for item in results if item["risk_level"] == "Medium")
    low_count = sum(1 for item in results if item["risk_level"] == "Low")

    risk_score = min((high_count * 25) + (medium_count * 12) + (low_count * 5), 100)
    compliance_score = max(100 - risk_score, 0)

    return risk_score, compliance_score, high_count, medium_count, low_count


def get_final_message(risk_score, results_count):
    if results_count == 0:
        return "ملفك سليم بناء على قاعدة البيانات الحالية، ولم يتم اكتشاف مخاطر واضحة.", "success"

    if risk_score >= 75:
        return "ملفك عالي الخطورة ويحتاج مراجعة قانونية وامتثالية قبل الاعتماد.", "error"

    if risk_score >= 40:
        return "ملفك يحتوي على مخاطر متوسطة، ويحتاج تعديل بعض البنود قبل الاعتماد.", "warning"

    return "ملفك يحتوي على ملاحظات بسيطة، لكنه قريب من الوضع المقبول بعد مراجعة نهائية.", "info"


# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("إعدادات إضافية")

    review_mode = st.selectbox(
        "وضعية قراءة العقد",
        [
            "قراءة عامة",
            "قراءة كجهة رقابية SAMA",
            "قراءة كجهة رقابية CMA",
            "قراءة كعميل متضرر",
            "قراءة كمسؤول امتثال داخلي",
            "قراءة كمراجع قانوني",
            "محاكاة هجوم تنظيمي"
        ]
    )

    risk_appetite = st.radio(
        "شهية المخاطر",
        [
            "محافظ",
            "متوازن",
            "مرتفع"
        ]
    )

    confidential_mode = st.checkbox("وضع المراجعة السرية")
    show_extracted_text = st.checkbox("عرض النص المستخرج")

    st.divider()

    st.markdown("""
    **ممتثل** يفحص العقود والسياسات ويكشف:
    
    - البنود الخطرة  
    - البنود الناقصة  
    - العواقب المحتملة  
    - الإجراء المقترح  
    - نسبة الخطورة  
    """)


# =========================
# MAIN PAGE
# =========================

st.markdown("""
<div class="main-card">
    <h1>ممتثل</h1>
    <p>
    منصة بسيطة لفحص امتثال العقود والسياسات. ارفع ملفك، اختر مصدر المطابقة،
    ثم احصل على نتيجة مختصرة توضح نسبة الخطورة والملاحظات الأساسية.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "ارفع ملف العقد أو السياسة",
    type=["txt", "pdf"]
)

match_source = st.selectbox(
    "مصدر المطابقة",
    [
        "مراجعة شاملة",
        "لوائح SAMA فقط",
        "لوائح CMA فقط",
        "سياسات الشركة الداخلية فقط"
    ]
)

analyze = st.button("ابدأ الفحص")

# =========================
# RESULTS
# =========================

if analyze and not uploaded_file:
    st.warning("ارفع ملف TXT أو PDF أولا عشان يبدأ الفحص.")

if uploaded_file and analyze:
    contract_text = extract_text_from_file(uploaded_file)

    if show_extracted_text:
        st.text_area("النص المستخرج من الملف", contract_text, height=220)

    if not contract_text.strip():
        st.error("لم يتمكن النظام من قراءة النص من الملف. جرّب ملف TXT أو PDF يحتوي على نص قابل للنسخ.")
    else:
        results = analyze_contract(contract_text, match_source)
        risk_score, compliance_score, high_count, medium_count, low_count = calculate_scores(results)
        final_message, message_type = get_final_message(risk_score, len(results))

        st.markdown("""
        <div class="result-card">
            <h2>نتيجة الفحص</h2>
        </div>
        """, unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.metric("نسبة الخطورة", f"{risk_score}%")

        with k2:
            st.metric("درجة الامتثال", f"{compliance_score}/100")

        with k3:
            st.metric("مخاطر عالية", high_count)

        with k4:
            st.metric("مخاطر متوسطة", medium_count)

        if message_type == "success":
            st.success(final_message)
        elif message_type == "error":
            st.error(final_message)
        elif message_type == "warning":
            st.warning(final_message)
        else:
            st.info(final_message)

        st.caption(f"وضعية القراءة: {review_mode} | شهية المخاطر: {risk_appetite} | وضع السرية: {'مفعل' if confidential_mode else 'غير مفعل'}")

        if not results:
            st.markdown("""
            <div class="green-box">
            لم يتم اكتشاف مخاطر واضحة في هذا الملف بناء على قاعدة البيانات الحالية.
            هذه النتيجة لا تعتبر رأيا قانونيا نهائيا.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.subheader("المخاطر المكتشفة")

            for i, item in enumerate(results, start=1):
                with st.expander(f"الخطر رقم {i}: {item['topic']} - {item['risk_level']}"):
                    st.write("الجهة المرتبطة:", item["authority"])
                    st.write("الكلمات المكتشفة:", item["matched_keywords"])

                    st.markdown(f"""
                    <div class="yellow-box">
                    <b>المشكلة:</b><br>
                    {item["problem"]}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="red-box">
                    <b>العواقب المحتملة:</b><br>
                    {item["consequence"]}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="green-box">
                    <b>الإجراء المقترح:</b><br>
                    {item["suggested_fix"]}
                    </div>
                    """, unsafe_allow_html=True)

            st.subheader("الخلاصة")

            if risk_score >= 75:
                st.error("لا ينصح باعتماد الملف قبل تعديل البنود عالية الخطورة ومراجعته قانونيا.")
            elif risk_score >= 40:
                st.warning("يفضل تعديل البنود متوسطة وعالية الخطورة قبل الاعتماد.")
            else:
                st.info("الملف قريب من القبول، لكن يحتاج مراجعة نهائية حسب حساسية العقد.")
