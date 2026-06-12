import streamlit as st
import pandas as pd

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
    background: linear-gradient(135deg, #08111F 0%, #0F172A 50%, #172554 100%);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.hero {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 28px;
    padding: 40px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 56px;
    color: white;
    margin-bottom: 10px;
}

.hero h2 {
    color: #CBD5E1;
    font-size: 24px;
}

.hero p {
    color: #E5E7EB;
    font-size: 17px;
    line-height: 1.8;
}

.card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
}

.card h3 {
    color: white;
}

.card p {
    color: #CBD5E1;
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
# DATA FUNCTIONS
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
                "يجب النص على إشعار العميل قبل تغيير الرسوم بمدة واضحة مع توضيح آلية الاعتراض أو الإنهاء.",
                "إضافة بند يوضح طريقة تقديم الشكاوى ومدة الرد وآلية التصعيد.",
                "توضيح متى ولماذا تتم مشاركة البيانات ومع من، مع الالتزام بسياسة الخصوصية.",
                "تحديد حالات الإيقاف بوضوح مثل الاشتباه في احتيال أو مخالفة الشروط، مع إشعار العميل متى ما أمكن.",
                "إضافة بند واضح يشرح حالات تضارب المصالح وكيفية إدارتها والإفصاح عنها.",
                "إضافة بند أو إجراء يحدد صلاحيات الاعتماد والمراجعة الداخلية قبل توقيع العقد."
            ]
        }
        return pd.DataFrame(data)


def extract_text_from_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    return ""


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

        if "الشركة" in match_source and authority != "Internal":
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


# =========================
# HERO
# =========================

st.markdown("""
<div class="hero">
    <h1>ممتثل</h1>
    <h2>منصة ذكية لمحاكاة مخاطر الامتثال والعواقب التنظيمية</h2>
    <p>
    ممتثل يساعد الشركات المالية وشركات الفنتك على فحص العقود والسياسات،
    ومطابقتها أولا مع سياسات الشركة الداخلية، ثم مع لوائح SAMA و CMA.
    المنصة تكشف البنود الخطرة، العواقب المحتملة، والصياغات البديلة.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# HOW IT WORKS
# =========================

st.header("كيف تعمل المنصة؟")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="card">
        <h3>1. رفع المستند</h3>
        <p>يرفع المستخدم عقدا أو سياسة.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>2. اختيار المطابقة</h3>
        <p>سياسات الشركة أو SAMA أو CMA.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h3>3. وضعية القراءة</h3>
        <p>عميل، جهة رقابية، امتثال، أو قانوني.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card">
        <h3>4. تقرير المخاطر</h3>
        <p>درجة خطورة، عواقب، وتوصيات.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# REVIEW MODES
# =========================

st.header("وضعيات قراءة العقد")

m1, m2, m3 = st.columns(3)

with m1:
    st.info("قراءة كجهة رقابية SAMA: تركز على حماية العميل، الرسوم، الإفصاح، والإسناد الخارجي.")

with m2:
    st.info("قراءة كجهة رقابية CMA: تركز على الإفصاح، تضارب المصالح، وحماية المستثمر.")

with m3:
    st.info("قراءة كعميل متضرر: تبحث عن البنود التي قد تسبب شكوى أو اعتراض.")

m4, m5, m6 = st.columns(3)

with m4:
    st.info("قراءة كمسؤول امتثال داخلي: تبحث عن البنود الناقصة وضعف الإجراءات.")

with m5:
    st.info("قراءة كمراجع قانوني: تركز على الصياغة والمسؤوليات والثغرات.")

with m6:
    st.info("محاكاة هجوم تنظيمي: تختبر أسوأ السيناريوهات المحتملة.")


# =========================
# INPUT
# =========================

st.header("ابدأ الفحص")

left, right = st.columns([1.1, 0.9])

with left:
    uploaded_file = st.file_uploader(
        "ارفع ملف العقد أو السياسة",
        type=["txt"]
    )

    match_source = st.selectbox(
        "اختر مصدر المطابقة",
        [
            "مراجعة شاملة",
            "سياسات الشركة الداخلية فقط",
            "لوائح SAMA فقط",
            "لوائح CMA فقط"
        ]
    )

    review_mode = st.selectbox(
        "اختر وضعية قراءة العقد",
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
        "شهية المخاطر",
        [
            "محافظ",
            "متوازن",
            "مرتفع"
        ]
    )

    confidential_mode = st.checkbox("تفعيل وضع المراجعة السرية")
    analyze = st.button("ابدأ الفحص الآن")

with right:
    st.markdown("""
    <div class="card">
        <h3>ماذا يفعل ممتثل؟</h3>
        <p>
        يقرأ العقد، يطابقه مع الداتا، يكتشف المخاطر،
        يوضح العواقب، ثم يقترح صياغة أفضل.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# RESULTS
# =========================

if analyze and not uploaded_file:
    st.warning("ارفع ملف TXT أولا عشان يبدأ الفحص.")

if uploaded_file and analyze:
    contract_text = extract_text_from_file(uploaded_file)
    results = analyze_contract(contract_text, match_source)

    st.header("نتيجة الفحص")

    st.write("وضعية القراءة المختارة:", review_mode)
    st.write("شهية المخاطر:", risk_appetite)
    st.write("وضع السرية:", "مفعل" if confidential_mode else "غير مفعل")

    if not results:
        st.success("لم يتم اكتشاف مخاطر واضحة بناء على قاعدة البيانات الحالية.")
    else:
        st.error(f"تم اكتشاف {len(results)} مخاطر محتملة")

        high_count = sum(1 for item in results if item["risk_level"] == "High")
        medium_count = sum(1 for item in results if item["risk_level"] == "Medium")

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("إجمالي المخاطر", len(results))
        with k2:
            st.metric("مخاطر عالية", high_count)
        with k3:
            st.metric("مخاطر متوسطة", medium_count)

        for i, item in enumerate(results, start=1):
            st.subheader(f"الخطر رقم {i}: {item['topic']}")

            st.write("الجهة المرتبطة:", item["authority"])
            st.write("مستوى الخطورة:", item["risk_level"])
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

            st.divider()
