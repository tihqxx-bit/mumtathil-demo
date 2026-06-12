import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from docx import Document

st.set_page_config(
    page_title="مُمتَثِل | منصة الامتثال الذكية",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

.stApp {
    background: linear-gradient(135deg, #08111F 0%, #0F172A 45%, #172554 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

.hero {
    background: linear-gradient(135deg, rgba(37,99,235,0.22), rgba(20,184,166,0.14));
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 30px;
    padding: 42px;
    margin-bottom: 26px;
    box-shadow: 0 18px 70px rgba(0,0,0,0.28);
}

.hero h1 {
    font-size: 60px;
    font-weight: 800;
    margin: 0;
    color: #FFFFFF;
}

.hero h2 {
    font-size: 25px;
    color: #DCEAFE;
    margin-top: 14px;
    margin-bottom: 16px;
}

.hero p {
    font-size: 17px;
    line-height: 1.95;
    color: #E5E7EB;
    max-width: 900px;
}

.badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.15);
    color: #86EFAC;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 14px;
    border: 1px solid rgba(134,239,172,0.26);
    margin-bottom: 18px;
}

.section-title {
    font-size: 27px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 12px;
    color: #FFFFFF;
}

.section-subtitle {
    color: #CBD5E1;
    font-size: 15px;
    margin-bottom: 18px;
}

.card {
    background: rgba(255,255,255,0.085);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
}

.card h3 {
    color: #FFFFFF;
    font-size: 21px;
    margin-bottom: 8px;
}

.card p, .card li {
    color: #CBD5E1;
    font-size: 15px;
    line-height: 1.8;
}

.step-card {
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 20px;
    padding: 20px;
    min-height: 170px;
}

.step-number {
    width: 36px;
    height: 36px;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563EB, #14B8A6);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin-bottom: 12px;
}

.step-card h4 {
    color: #FFFFFF;
    font-size: 18px;
    margin-bottom: 8px;
}

.step-card p {
    color: #CBD5E1;
    font-size: 14px;
    line-height: 1.75;
}

.mode-card {
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(148,163,184,0.23);
    border-radius: 18px;
    padding: 18px;
    min-height: 150px;
}

.mode-card h4 {
    color: #FFFFFF;
    margin-bottom: 8px;
}

.mode-card p {
    color: #CBD5E1;
    font-size: 14px;
    line-height: 1.7;
}

.result-box {
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 24px;
    padding: 26px;
    margin-top: 22px;
}

.red-box {
    background: rgba(239,68,68,0.13);
    border: 1px solid rgba(239,68,68,0.38);
    border-radius: 16px;
    padding: 16px;
    color: #FEE2E2;
}

.green-box {
    background: rgba(34,197,94,0.13);
    border: 1px solid rgba(34,197,94,0.35);
    border-radius: 16px;
    padding: 16px;
    color: #DCFCE7;
}

.yellow-box {
    background: rgba(245,158,11,0.13);
    border: 1px solid rgba(245,158,11,0.35);
    border-radius: 16px;
    padding: 16px;
    color: #FEF3C7;
}

.blue-box {
    background: rgba(37,99,235,0.14);
    border: 1px solid rgba(96,165,250,0.35);
    border-radius: 16px;
    padding: 16px;
    color: #DBEAFE;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    border: 1px dashed rgba(255,255,255,0.26);
}

.stButton > button {
    width: 100%;
    border-radius: 15px;
    height: 56px;
    background: linear-gradient(90deg, #2563EB, #14B8A6);
    color: white;
    border: none;
    font-size: 18px;
    font-weight: 800;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1D4ED8, #0F766E);
    color: white;
}

[data-testid="stMetricValue"] {
    color: white;
}

[data-testid="stMetricLabel"] {
    color: #CBD5E1;
}

hr {
    border-color: rgba(255,255,255,0.12);
}
</style>
""", unsafe_allow_html=True)
</style>
""", unsafe_allow_html=True)


def extract_text_from_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    elif file_name.endswith(".pdf"):
        text = ""
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        return text

    elif file_name.endswith(".docx"):
        doc = Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    return ""


def load_regulations():
    return pd.read_csv("regulations.csv")


def analyze_contract(contract_text, match_source):
    regulations = load_regulations()
    results = []

    contract_text_lower = contract_text.lower()

    for _, row in regulations.iterrows():
        authority = str(row["authority"])
        keywords = str(row["keywords"]).split(",")

        if "SAMA" in match_source and authority != "SAMA":
            continue

        if "CMA" in match_source and authority != "CMA":
            continue

        if "سياسات الشركة" in match_source and authority != "Internal":
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


# بعدها كود الواجهة يكمل عادي
st.markdown("""
<div class="hero">
...


# =========================
# 1. HERO
# =========================

st.markdown("""
<div class="hero">
    <div class="badge">RegTech AI Platform</div>
    <h1>⚖️ مُمتَثِل</h1>
    <h2>منصة ذكية لمحاكاة مخاطر الامتثال والعواقب التنظيمية</h2>
    <p>
    مُمتَثِل لا يراجع العقد كمستند فقط، بل يقرأه من عدة زوايا:
    كجهة رقابية، كعميل متضرر، كمسؤول امتثال، وكمراجع قانوني.
    المنصة تطابق العقد أولًا مع سياسات الشركة الداخلية، ثم مع لوائح SAMA وCMA،
    وتكشف البنود الخطرة والناقصة وتقترح صياغات بديلة.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# 2. HOW IT WORKS
# =========================

st.markdown('<div class="section-title">كيف تعمل المنصة؟</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">رحلة واضحة من رفع العقد إلى تقرير قابل للمراجعة القانونية.</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <h4>رفع المستند</h4>
        <p>يرفع المستخدم عقدًا أو سياسة بصيغة PDF أو DOCX أو TXT.</p>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <h4>اختيار مصدر المطابقة</h4>
        <p>مطابقة مع سياسات الشركة، أو SAMA، أو CMA، أو مراجعة شاملة.</p>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <h4>اختيار وضعية القراءة</h4>
        <p>قراءة العقد كجهة رقابية، عميل متضرر، مراجع قانوني، أو مسؤول امتثال.</p>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">4</div>
        <h4>تقرير المخاطر</h4>
        <p>درجة خطورة، عواقب محتملة، بنود ناقصة، وصياغات بديلة.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 3. REVIEW MODES
# =========================

st.markdown('<div class="section-title">وضعيات قراءة العقد</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">هذه الوضعيات تميز مُمتَثِل عن المراجعة التقليدية، لأنها تغير زاوية تحليل العقد.</div>', unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="mode-card">
        <h4>🏦 قراءة كجهة رقابية SAMA</h4>
        <p>يركز على حماية العميل، الإفصاح، الرسوم، المدفوعات، الإسناد الخارجي، وضوابط القطاع المالي.</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="mode-card">
        <h4>📈 قراءة كجهة رقابية CMA</h4>
        <p>يركز على الإفصاح، تضارب المصالح، حماية المستثمر، الحوكمة، وعقود الأنشطة الاستثمارية.</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="mode-card">
        <h4>🙋 قراءة كعميل متضرر</h4>
        <p>يبحث عن البنود التي قد يستخدمها العميل لتقديم شكوى، مثل الرسوم غير الواضحة أو إيقاف الخدمة دون إشعار.</p>
    </div>
    """, unsafe_allow_html=True)

m4, m5, m6 = st.columns(3)

with m4:
    st.markdown("""
    <div class="mode-card">
        <h4>🛡️ قراءة كمسؤول امتثال</h4>
        <p>يبحث عن البنود الناقصة، ضعف الإجراءات، وسجل المراجعة المطلوب قبل الاعتماد الداخلي.</p>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown("""
    <div class="mode-card">
        <h4>⚖️ قراءة كمراجع قانوني</h4>
        <p>يركز على الصياغة، المسؤوليات، التزامات الأطراف، الثغرات، والعبارات الواسعة أو الغامضة.</p>
    </div>
    """, unsafe_allow_html=True)

with m6:
    st.markdown("""
    <div class="mode-card">
        <h4>🚨 محاكاة هجوم تنظيمي</h4>
        <p>يختبر العقد بسيناريوهات: ماذا لو اشتكى العميل؟ ماذا لو تغيرت الرسوم؟ ماذا لو طلبت الجهة السجلات؟</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 4. INPUT AREA
# =========================

st.markdown('<div class="section-title">ابدأ الفحص</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">اختر نوع المطابقة ووضعية القراءة ثم ارفع المستند.</div>', unsafe_allow_html=True)

left, right = st.columns([1.1, 0.9])

with left:
    st.markdown("""
    <div class="card">
        <h3>إعدادات الفحص</h3>
        <p>هذه الإعدادات تحدد كيف ستقرأ المنصة العقد ومن أي زاوية ستقيم المخاطر.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "ارفع ملف العقد أو السياسة",
        type=["pdf", "docx", "txt"]
    )

    match_source = st.selectbox(
        "أولًا: اختر مصدر المطابقة",
        [
            "1) سياسات الشركة الداخلية فقط",
            "2) لوائح SAMA فقط",
            "3) لوائح CMA فقط",
            "4) مراجعة شاملة: سياسات الشركة + SAMA + CMA"
        ]
    )

    review_mode = st.selectbox(
        "ثانيًا: اختر وضعية قراءة العقد",
        [
            "قراءة كجهة رقابية SAMA",
            "قراءة كجهة رقابية CMA",
            "قراءة كعميل متضرر",
            "قراءة كمسؤول امتثال داخلي",
            "قراءة كمراجع قانوني",
            "محاكاة هجوم تنظيمي"
        ]
    )

    risk_appetite = st.radio(
        "ثالثًا: شهية المخاطر لدى الشركة",
        [
            "محافظ: أقل مخاطرة ممكنة",
            "متوازن: حماية الشركة مع تقليل الخطر",
            "مرتفع: إبقاء المرونة التجارية مع معرفة العواقب"
        ],
        horizontal=False
    )

    confidential_mode = st.checkbox("تفعيل وضع المراجعة السرية Confidential Review")
    delete_after_review = st.checkbox("حذف الملف بعد إصدار التقرير Analyze & Delete")

    analyze = st.button("ابدأ الفحص الآن")

with right:
    st.markdown("""
    <div class="card">
        <h3>ماذا تفعل المنصة في هذه المرحلة؟</h3>
        <ul>
            <li>تقرأ العقد وتقسمه إلى بنود.</li>
            <li>تطابق البنود مع سياسة الشركة الداخلية.</li>
            <li>تقارن البنود بلوائح SAMA وCMA حسب اختيارك.</li>
            <li>تقرأ العقد من الزاوية المختارة: عميل، جهة رقابية، قانوني، أو امتثال.</li>
            <li>تعطيك درجة خطورة وعواقب محتملة وصياغة بديلة.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>ملاحظة مهمة</h3>
        <p>
        هذه النسخة Demo للهاكاثون. لاحقًا يتم ربط المنصة بقاعدة معرفة حقيقية
        من سياسات الشركة ولوائح SAMA وCMA عبر RAG.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 5. RESULTS
# =========================

if analyze and not uploaded_file:
    st.warning("ارفع ملفًا أولًا عشان يبدأ الفحص.")

if uploaded_file and analyze:
    st.markdown("""
    <div class="result-box">
        <h2>📊 نتيجة الفحص الأولية</h2>
        <p>هذه نتيجة تجريبية توضّح شكل مخرجات منصة مُمتَثِل في الديمو.</p>
    </div>
    """, unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.metric("درجة الخطورة", "78%", "مرتفع")
    with r2:
        st.metric("درجة الامتثال", "62/100")
    with r3:
        st.metric("بنود خطرة", "4")
    with r4:
        st.metric("بنود ناقصة", "3")

    st.markdown("### إعدادات الفحص المستخدمة")

    st.dataframe(
        {
            "العنصر": [
                "مصدر المطابقة",
                "وضعية قراءة العقد",
                "شهية المخاطر",
                "وضع السرية",
                "حذف الملف بعد التقرير"
            ],
            "القيمة": [
                match_source,
                review_mode,
                risk_appetite,
                "مفعل" if confidential_mode else "غير مفعل",
                "مفعل" if delete_after_review else "غير مفعل"
            ]
        },
        use_container_width=True
    )

    st.markdown("### 🚩 بند عالي الخطورة")

    st.markdown("""
    <div class="red-box">
        <b>البند:</b><br>
        يحق للشركة تعديل الرسوم في أي وقت دون إشعار العميل.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### تحليل البند حسب وضعية القراءة")

    if review_mode == "قراءة كعميل متضرر":
        st.markdown("""
        <div class="yellow-box">
            كعميل، يمكن الاعتراض على هذا البند لأنه يسمح بتغيير الرسوم دون إشعار واضح.
            هذا قد يفتح باب الشكاوى بسبب ضعف الشفافية.
        </div>
        """, unsafe_allow_html=True)

    elif review_mode == "قراءة كجهة رقابية SAMA":
        st.markdown("""
        <div class="yellow-box">
            من زاوية SAMA، الخطر مرتبط بحماية العميل والإفصاح عن الرسوم.
            البند يحتاج آلية إشعار واضحة قبل تطبيق أي تغيير.
        </div>
        """, unsafe_allow_html=True)

    elif review_mode == "قراءة كجهة رقابية CMA":
        st.markdown("""
        <div class="yellow-box">
            من زاوية CMA، يتم التركيز على وضوح الإفصاح وعدم وجود بنود قد تضلل المستثمر أو العميل.
            إذا كان العقد مرتبطًا بمنتج استثماري فقد يصبح الخطر أعلى.
        </div>
        """, unsafe_allow_html=True)

    elif review_mode == "قراءة كمسؤول امتثال داخلي":
        st.markdown("""
        <div class="yellow-box">
            كمسؤول امتثال، يظهر أن العقد لا يحتوي على ضابط داخلي واضح لاعتماد تغيير الرسوم
            ولا يوضح متى وكيف يتم إشعار العميل.
        </div>
        """, unsafe_allow_html=True)

    elif review_mode == "قراءة كمراجع قانوني":
        st.markdown("""
        <div class="yellow-box">
            كمراجع قانوني، صياغة البند واسعة جدًا وتعطي الشركة سلطة مطلقة.
            الأفضل تقييدها بإشعار مسبق وسبب واضح وآلية اعتراض.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="yellow-box">
            في محاكاة الهجوم التنظيمي، السيناريو المحتمل هو:
            عميل يشتكي بعد رفع الرسوم دون إشعار، ثم تطلب الجهة الرقابية توضيح آلية الإفصاح والموافقة.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### العواقب المحتملة لو أبقت الشركة هذا البند")

    st.markdown("""
    <div class="red-box">
        <ul>
            <li>ارتفاع احتمالية شكاوى العملاء.</li>
            <li>إلزام الشركة بتعديل البند لاحقًا.</li>
            <li>إجراء رقابي أو غرامة حسب تقدير الجهة المختصة.</li>
            <li>ضرر على السمعة والثقة.</li>
            <li>تأخير اعتماد العقد داخليًا أو قانونيًا.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### الخيارات المقترحة حسب شهية المخاطر")

    st.dataframe(
        {
            "الخيار": [
                "تعديل محافظ",
                "تعديل متوازن",
                "إبقاء البند مع معرفة العواقب"
            ],
            "الصياغة / القرار": [
                "لا يتم تعديل الرسوم إلا بعد إشعار العميل بمدة محددة وموافقة واضحة عند الحاجة.",
                "يحق للشركة تعديل الرسوم بعد إشعار العميل مسبقًا مع منحه حق الاعتراض أو الإنهاء.",
                "إبقاء البند كما هو يمنح مرونة عالية لكنه يرفع خطر الشكاوى والإجراءات الرقابية."
            ],
            "مستوى الخطر": [
                "منخفض",
                "متوسط",
                "مرتفع"
            ]
        },
        use_container_width=True
    )

    st.markdown("### الصياغة المقترحة")

    st.markdown("""
    <div class="green-box">
        يحق للشركة تعديل الرسوم بعد إشعار العميل بمدة واضحة قبل التطبيق،
        مع توضيح سبب التعديل وآلية الاعتراض أو الإنهاء، وبما لا يتعارض مع المتطلبات النظامية ذات العلاقة.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### مطابقة البند مع مصادر الامتثال")

    st.dataframe(
        {
            "مصدر المطابقة": [
                "سياسة الشركة الداخلية",
                "لوائح SAMA",
                "لوائح CMA"
            ],
            "الحالة": [
                "يحتاج مراجعة",
                "خطر عالي",
                "غير مرتبط مباشرة في هذا المثال"
            ],
            "سبب الملاحظة": [
                "لا توجد آلية إشعار داخلية واضحة",
                "قد يتعارض مع متطلبات الإفصاح وحماية العميل",
                "يرتبط فقط إذا كان العقد لمنتج استثماري أو إفصاح مالي"
            ]
        },
        use_container_width=True
    )

    st.markdown("### 📌 البنود الناقصة")

    n1, n2, n3 = st.columns(3)

    with n1:
        st.warning("لا يوجد بند واضح لآلية شكاوى العملاء.")
    with n2:
        st.warning("لا يوجد بند واضح للإفصاح عن تغيير الرسوم.")
    with n3:
        st.warning("لا يوجد بند يوضح ضوابط مشاركة بيانات العميل مع طرف ثالث.")

    st.markdown("### ملخص للإدارة")

    st.markdown("""
    <div class="blue-box">
        <b>التوصية:</b><br>
        لا يُنصح باعتماد العقد بصيغته الحالية. يجب تعديل البنود المتعلقة بالرسوم،
        الشكاوى، ومشاركة البيانات قبل إرساله للمراجع القانوني النهائي.
        </br></br>
        <b>الأثر المتوقع بعد التعديل:</b><br>
        تقليل المخاطر التنظيمية، تحسين وضوح العقد، وتقليل احتمالية الشكاوى.
    </div>
    """, unsafe_allow_html=True)
