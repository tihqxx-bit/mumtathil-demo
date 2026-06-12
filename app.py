import streamlit as st

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
    background: linear-gradient(135deg, #0B1220 0%, #111827 45%, #172554 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.hero {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 28px;
    padding: 42px;
    margin-bottom: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.hero h1 {
    font-size: 58px;
    font-weight: 800;
    margin-bottom: 8px;
    color: #FFFFFF;
}

.hero h3 {
    font-size: 24px;
    color: #CBD5E1;
    margin-bottom: 18px;
}

.hero p {
    font-size: 17px;
    line-height: 1.9;
    color: #E5E7EB;
}

.badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.16);
    color: #86EFAC;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 14px;
    border: 1px solid rgba(134,239,172,0.25);
    margin-bottom: 18px;
}

.card {
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 18px;
}

.card h3 {
    color: #FFFFFF;
    font-size: 22px;
    margin-bottom: 8px;
}

.card p {
    color: #CBD5E1;
    font-size: 15px;
    line-height: 1.8;
}

.feature {
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px;
    min-height: 145px;
}

.feature h4 {
    color: #FFFFFF;
    margin-bottom: 8px;
}

.feature p {
    color: #CBD5E1;
    font-size: 14px;
    line-height: 1.7;
}

.result-box {
    background: rgba(15,23,42,0.72);
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 20px;
    padding: 24px;
    margin-top: 18px;
}

.red-box {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 16px;
    padding: 16px;
}

.green-box {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.35);
    border-radius: 16px;
    padding: 16px;
}

.yellow-box {
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.35);
    border-radius: 16px;
    padding: 16px;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.09);
    padding: 18px;
    border-radius: 18px;
    border: 1px dashed rgba(255,255,255,0.25);
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 54px;
    background: linear-gradient(90deg, #2563EB, #14B8A6);
    color: white;
    border: none;
    font-size: 18px;
    font-weight: 700;
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
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="badge">RegTech AI Platform</div>
    <h1>⚖️ مُمتَثِل</h1>
    <h3>محاكي المخاطر والعواقب التنظيمية للعقود والسياسات</h3>
    <p>
    منصة ذكية تساعد شركات الفنتك والقطاع المالي على فحص العقود والسياسات،
    ومطابقتها أولًا مع سياسات الشركة الداخلية، ثم مع لوائح SAMA وCMA،
    مع كشف البنود الخطرة، العواقب المحتملة، والصياغات البديلة.
    </p>
</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature">
        <h4>🔍 فحص ذكي للبنود</h4>
        <p>تحليل البنود الخطرة والناقصة وربطها بمصادر تنظيمية واضحة.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature">
        <h4>⚠️ محرك العواقب</h4>
        <p>يوضح أثر المخالفة المحتمل: شكوى، غرامة، إلزام بالتعديل أو ضرر سمعة.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature">
        <h4>🔐 وضع المراجعة السرية</h4>
        <p>إخفاء البيانات الحساسة قبل التحليل وحماية المستندات داخل بيئة آمنة.</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown("""
    <div class="card">
        <h3>ابدأ فحص المستند</h3>
        <p>ارفع عقدًا أو سياسة، ثم اختر نوع المراجعة المطلوبة.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "ارفع ملف العقد أو السياسة",
        type=["pdf", "docx", "txt"]
    )

    review_type = st.selectbox(
        "اختر نوع المراجعة",
        [
            "مطابقة مع سياسة الشركة الداخلية",
            "مطابقة مع لوائح SAMA",
            "مطابقة مع لوائح CMA",
            "مراجعة شاملة: الشركة + SAMA + CMA"
        ]
    )

    confidential_mode = st.checkbox("تفعيل وضع المراجعة السرية Confidential Review")

    analyze = st.button("ابدأ الفحص الآن")

with right:
    st.markdown("""
    <div class="card">
        <h3>كيف يعمل مُمتَثِل؟</h3>
        <p>
        1. يقرأ العقد ويقسمه إلى بنود.<br>
        2. يطابقه مع سياسات الشركة الداخلية.<br>
        3. يراجعه مقابل لوائح SAMA وCMA.<br>
        4. يعطي درجة خطورة وعواقب محتملة.<br>
        5. يقترح صياغة بديلة قابلة للمراجعة القانونية.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>مناسب لـ</h3>
        <p>
        شركات الفنتك، شركات المدفوعات، التمويل، الاستثمار،
        الإدارات القانونية، وأقسام الامتثال.
        </p>
    </div>
    """, unsafe_allow_html=True)


if uploaded_file and analyze:
    st.markdown("""
    <div class="result-box">
        <h2>📊 نتيجة الفحص الأولية</h2>
        <p>هذه نتيجة تجريبية للـ MVP توضح شكل مخرجات المنصة.</p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("درجة الخطورة", "78%", "مرتفع")
    with m2:
        st.metric("بنود خطرة", "4")
    with m3:
        st.metric("بنود ناقصة", "3")
    with m4:
        st.metric("درجة الامتثال", "62/100")

    st.markdown("### 🚩 بند عالي الخطورة")

    st.markdown("""
    <div class="red-box">
        <b>البند:</b><br>
        يحق للشركة تعديل الرسوم في أي وقت دون إشعار العميل.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### لماذا هذا البند خطر؟")

    st.markdown("""
    <div class="yellow-box">
        هذا البند يمنح الشركة صلاحية واسعة لتغيير الرسوم دون إشعار واضح،
        مما قد يسبب خطرًا متعلقًا بالإفصاح وحماية العميل.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### العواقب المحتملة")

    st.write("""
    - شكوى عميل بسبب عدم وضوح الرسوم.
    - إلزام الشركة بتعديل البند.
    - إجراء رقابي أو غرامة حسب تقدير الجهة المختصة.
    - أثر سلبي على السمعة والثقة.
    """)

    st.markdown("### الصياغة المقترحة")

    st.markdown("""
    <div class="green-box">
        يحق للشركة تعديل الرسوم بعد إشعار العميل بمدة واضحة قبل التطبيق،
        مع توضيح سبب التعديل وآلية الاعتراض أو الإنهاء.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### المطابقة مع السياسات واللوائح")

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
                "غير مرتبط مباشرة"
            ],
            "ملاحظة": [
                "لا توجد آلية إشعار واضحة",
                "قد يتعارض مع متطلبات الإفصاح",
                "لا توجد علاقة مباشرة في هذا المثال"
            ]
        },
        use_container_width=True
    )

    st.markdown("### 📌 البنود الناقصة")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.warning("لا يوجد بند واضح لآلية شكاوى العملاء.")
    with c2:
        st.warning("لا يوجد بند واضح للإفصاح عن تغيير الرسوم.")
    with c3:
        st.warning("لا يوجد بند يوضح مشاركة بيانات العميل مع طرف ثالث.")

    st.markdown("### ملخص للإدارة")

    st.info("""
    التوصية: لا يُنصح باعتماد العقد بصيغته الحالية.
    يحتاج العقد إلى تعديل البنود المتعلقة بالرسوم، الشكاوى، ومشاركة البيانات
    قبل إرساله للمراجع القانوني النهائي.
    """)

elif analyze and not uploaded_file:
    st.warning("ارفع ملفًا أولًا عشان يبدأ الفحص.")
