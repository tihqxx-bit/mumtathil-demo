import os
from io import BytesIO

import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import arabic_reshaper
from bidi.algorithm import get_display


st.set_page_config(
    page_title="ممتثل",
    page_icon="⚖️",
    layout="centered"
)


# =========================
# تصميم بسيط
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #08111F 0%, #0F172A 55%, #172554 100%);
    color: white;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

.main-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 22px;
}

.main-card h1 {
    color: white;
    font-size: 48px;
    margin-bottom: 8px;
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

.blue-box {
    background: rgba(37,99,235,0.14);
    border: 1px solid rgba(96,165,250,0.4);
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

.stDownloadButton > button {
    width: 100%;
    height: 50px;
    border-radius: 14px;
    background: #16A34A;
    color: white;
    border: none;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# =========================
# بيانات SAMA التجريبية
# =========================

def load_sama_rules():
    """
    إذا كان عندك ملف sama_rules.csv سيقرأه.
    إذا ما كان موجود، يستخدم داتا تجريبية مدمجة.
    """
    try:
        return pd.read_csv("sama_rules.csv")
    except Exception:
        data = {
            "authority": [
                "SAMA",
                "SAMA",
                "SAMA",
                "SAMA",
                "SAMA"
            ],
            "topic": [
                "الإفصاح عن الرسوم",
                "شكاوى العملاء",
                "مشاركة بيانات العميل",
                "إيقاف الخدمة أو الحساب",
                "الإسناد الخارجي"
            ],
            "keywords": [
                "رسوم,تعديل الرسوم,تغيير الرسوم,بدون إشعار,دون إشعار",
                "شكوى,شكاوى,اعتراض,تظلم,خدمة العملاء",
                "بيانات,مشاركة البيانات,طرف ثالث,مزود خدمة,خصوصية",
                "إيقاف الخدمة,تعليق الحساب,إغلاق الحساب,حظر",
                "إسناد خارجي,مزود خارجي,طرف خارجي,تعهيد,مزود خدمة"
            ],
            "risk_level": [
                "High",
                "Medium",
                "High",
                "Medium",
                "High"
            ],
            "regulation_reference": [
                "SAMA - الإفصاح والشفافية",
                "SAMA - معالجة شكاوى العملاء",
                "SAMA - حماية بيانات العملاء",
                "SAMA - وضوح إجراءات الخدمة",
                "SAMA - الإسناد الخارجي"
            ],
            "regulation_text": [
                "يجب أن تكون الرسوم والشروط الجوهرية واضحة للعميل، وأن يتم إشعاره بالتغييرات المؤثرة قبل تطبيقها وفق المتطلبات التنظيمية ذات العلاقة.",
                "ينبغي وجود آلية واضحة لاستقبال شكاوى العملاء ومعالجتها خلال مدة محددة، مع توثيق الشكوى وآلية التصعيد عند الحاجة.",
                "يجب التعامل مع بيانات العملاء بسرية، وعدم مشاركتها مع أطراف خارجية إلا وفق ضوابط واضحة وموافقة أو أساس نظامي مناسب.",
                "يجب أن تكون إجراءات إيقاف أو تعليق الخدمة واضحة ومبنية على أسباب محددة، مع إشعار العميل متى ما كان ذلك ممكنًا نظاميًا.",
                "ينبغي أن تكون ترتيبات الإسناد الخارجي خاضعة لضوابط واضحة تضمن حماية البيانات واستمرارية الخدمة ومسؤولية الجهة المالية."
            ],
            "problem": [
                "البند قد يسمح بتغيير الرسوم دون إشعار واضح للعميل.",
                "لا يظهر وجود آلية واضحة لاستقبال ومعالجة شكاوى العملاء.",
                "البند قد يسمح بمشاركة بيانات العميل مع أطراف خارجية دون ضوابط واضحة.",
                "البند قد يمنح الشركة صلاحية إيقاف الخدمة دون سبب أو إشعار واضح.",
                "غياب ضوابط واضحة عند الاستعانة بطرف خارجي قد يسبب خطرًا تنظيميًا."
            ],
            "consequence": [
                "قد يؤدي إلى شكاوى عملاء أو إلزام الشركة بتعديل البند أو إجراء رقابي.",
                "قد يؤدي إلى ضعف حماية العميل وتصعيد الشكاوى للجهات المختصة.",
                "قد يؤدي إلى مخاطر خصوصية ومساءلة تنظيمية وفقدان ثقة العملاء.",
                "قد يؤدي إلى شكاوى عملاء أو اعتبار البند غير متوازن.",
                "قد يؤدي إلى مخاطر تشغيلية أو مساءلة تنظيمية عند فشل مزود الخدمة أو تسرب البيانات."
            ],
            "suggested_fix": [
                "إشعار العميل قبل تغيير الرسوم بمدة واضحة مع توضيح آلية الاعتراض أو الإنهاء.",
                "إضافة بند يوضح طريقة تقديم الشكاوى ومدة الرد وآلية التصعيد.",
                "توضيح متى ولماذا تتم مشاركة البيانات ومع من، مع الالتزام بسياسة الخصوصية والمتطلبات النظامية.",
                "تحديد حالات الإيقاف بوضوح مثل الاشتباه في احتيال أو مخالفة الشروط، مع إشعار العميل متى ما أمكن.",
                "إضافة بند يحدد مسؤوليات مزود الخدمة، حماية البيانات، استمرارية الخدمة، وآلية الرقابة."
            ]
        }
        return pd.DataFrame(data)


# =========================
# قراءة الملفات
# =========================

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


# =========================
# التحليل
# =========================

def analyze_contract_against_sama(contract_text):
    rules = load_sama_rules()
    results = []
    contract_text_lower = contract_text.lower()

    for _, row in rules.iterrows():
        keywords = str(row["keywords"]).split(",")
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
                "regulation_reference": row["regulation_reference"],
                "regulation_text": row["regulation_text"],
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
        return "ملفك سليم بناءً على قاعدة البيانات الحالية، ولم يتم اكتشاف بنود غير متوافقة مع متطلبات SAMA.", "success"

    if risk_score >= 75:
        return "ملفك عالي الخطورة ويحتوي على بنود لا تتماشى مع متطلبات SAMA. ينصح بعدم اعتماده قبل المراجعة والتعديل.", "error"

    if risk_score >= 40:
        return "ملفك يحتوي على مخاطر متوسطة مرتبطة بمتطلبات SAMA. يفضل تعديل البنود المشار إليها قبل الاعتماد.", "warning"

    return "ملفك يحتوي على ملاحظات بسيطة، ويحتاج مراجعة نهائية حسب حساسية المستند.", "info"


# =========================
# PDF
# =========================

def setup_pdf_font():
    """
    يحاول استخدام خط يدعم العربية داخل بيئة Streamlit.
    """
    possible_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "DejaVuSans.ttf"
    ]

    for font_path in possible_fonts:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont("ArabicFont", font_path))
            return "ArabicFont"

    return "Helvetica"


def ar_text(text):
    text = str(text)
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception:
        return text


def create_pdf_report(results, risk_score, compliance_score, high_count, medium_count, final_message):
    buffer = BytesIO()
    font_name = setup_pdf_font()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ArabicTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName=font_name,
        fontSize=20,
        leading=28,
        textColor=colors.HexColor("#0F172A")
    )

    heading_style = ParagraphStyle(
        "ArabicHeading",
        parent=styles["Heading2"],
        alignment=TA_RIGHT,
        fontName=font_name,
        fontSize=14,
        leading=22,
        textColor=colors.HexColor("#1E3A8A")
    )

    normal_style = ParagraphStyle(
        "ArabicNormal",
        parent=styles["Normal"],
        alignment=TA_RIGHT,
        fontName=font_name,
        fontSize=10,
        leading=17
    )

    small_style = ParagraphStyle(
        "ArabicSmall",
        parent=styles["Normal"],
        alignment=TA_RIGHT,
        fontName=font_name,
        fontSize=9,
        leading=15,
        textColor=colors.HexColor("#334155")
    )

    story = []

    story.append(Paragraph(ar_text("تقرير فحص الامتثال مقابل متطلبات SAMA"), title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(ar_text("ملخص الفحص"), heading_style))
    story.append(Paragraph(ar_text(f"مصدر المطابقة: البنك المركزي السعودي SAMA"), normal_style))
    story.append(Paragraph(ar_text(f"نسبة الخطورة: {risk_score}%"), normal_style))
    story.append(Paragraph(ar_text(f"درجة الامتثال: {compliance_score}/100"), normal_style))
    story.append(Paragraph(ar_text(f"عدد المخاطر العالية: {high_count}"), normal_style))
    story.append(Paragraph(ar_text(f"عدد المخاطر المتوسطة: {medium_count}"), normal_style))
    story.append(Paragraph(ar_text(f"النتيجة النهائية: {final_message}"), normal_style))
    story.append(Spacer(1, 18))

    if not results:
        story.append(Paragraph(ar_text("حالة المستند"), heading_style))
        story.append(Paragraph(ar_text("لم يتم اكتشاف بنود غير متوافقة مع متطلبات SAMA بناءً على قاعدة البيانات الحالية."), normal_style))
        story.append(Spacer(1, 12))
    else:
        story.append(Paragraph(ar_text("البنود التي لا تتماشى مع متطلبات SAMA"), heading_style))
        story.append(Spacer(1, 8))

        for i, item in enumerate(results, start=1):
            story.append(Paragraph(ar_text(f"الخطر رقم {i}: {item['topic']}"), heading_style))
            story.append(Paragraph(ar_text(f"مستوى الخطورة: {item['risk_level']}"), normal_style))
            story.append(Paragraph(ar_text(f"الكلمات المكتشفة في المستند: {item['matched_keywords']}"), normal_style))
            story.append(Spacer(1, 6))

            story.append(Paragraph(ar_text("المرجع التنظيمي المرتبط:"), normal_style))
            story.append(Paragraph(ar_text(item["regulation_reference"]), small_style))
            story.append(Spacer(1, 4))

            story.append(Paragraph(ar_text("نص المتطلب التنظيمي المرتبط:"), normal_style))
            story.append(Paragraph(ar_text(item["regulation_text"]), small_style))
            story.append(Spacer(1, 6))

            story.append(Paragraph(ar_text("المشكلة:"), normal_style))
            story.append(Paragraph(ar_text(item["problem"]), small_style))
            story.append(Spacer(1, 6))

            story.append(Paragraph(ar_text("العواقب المحتملة:"), normal_style))
            story.append(Paragraph(ar_text(item["consequence"]), small_style))
            story.append(Spacer(1, 6))

            story.append(Paragraph(ar_text("الإجراء المقترح:"), normal_style))
            story.append(Paragraph(ar_text(item["suggested_fix"]), small_style))
            story.append(Spacer(1, 14))

    story.append(Spacer(1, 16))
    story.append(Paragraph(ar_text("تنبيه مهم"), heading_style))
    story.append(Paragraph(
        ar_text("هذا التقرير يمثل فحص امتثال أولي آلي، ولا يعد رأيًا قانونيًا نهائيًا. يجب مراجعته من مختص قانوني أو مسؤول امتثال قبل الاعتماد."),
        small_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


# =========================
# واجهة المستخدم
# =========================

st.markdown("""
<div class="main-card">
    <h1>ممتثل</h1>
    <p>
    افحص عقدك أو سياستك مقابل متطلبات البنك المركزي السعودي SAMA.
    ارفع الملف، واضغط فحص، وسيظهر لك تقرير يوضح البنود غير المتوافقة
    ونص المتطلب التنظيمي المرتبط بها.
    </p>
</div>
""", unsafe_allow_html=True)

st.info("نطاق الديمو الحالي: الفحص مقابل متطلبات البنك المركزي السعودي SAMA فقط.")

uploaded_file = st.file_uploader(
    "ارفع ملف العقد أو السياسة",
    type=["txt", "pdf"]
)

show_text = st.checkbox("عرض النص المستخرج من الملف للتأكد", value=False)

analyze = st.button("ابدأ الفحص")


# =========================
# النتائج
# =========================

if analyze and not uploaded_file:
    st.warning("ارفع ملف TXT أو PDF أولًا عشان يبدأ الفحص.")

if uploaded_file and analyze:
    contract_text = extract_text_from_file(uploaded_file)

    if show_text:
        st.text_area("النص المستخرج من الملف", contract_text, height=220)

    if not contract_text.strip():
        st.error("لم يتمكن النظام من قراءة النص من الملف. جرّب ملف TXT أو PDF يحتوي على نص قابل للنسخ.")
    else:
        results = analyze_contract_against_sama(contract_text)
        risk_score, compliance_score, high_count, medium_count, low_count = calculate_scores(results)
        final_message, message_type = get_final_message(risk_score, len(results))

        st.markdown("""
        <div class="result-card">
            <h2>نتيجة الفحص</h2>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("نسبة الخطورة", f"{risk_score}%")

        with c2:
            st.metric("درجة الامتثال", f"{compliance_score}/100")

        with c3:
            st.metric("عدد المخاطر", len(results))

        if message_type == "success":
            st.success(final_message)
        elif message_type == "error":
            st.error(final_message)
        elif message_type == "warning":
            st.warning(final_message)
        else:
            st.info(final_message)

        pdf_report = create_pdf_report(
            results=results,
            risk_score=risk_score,
            compliance_score=compliance_score,
            high_count=high_count,
            medium_count=medium_count,
            final_message=final_message
        )

        st.download_button(
            label="تحميل تقرير PDF",
            data=pdf_report,
            file_name="mumtathil_sama_report.pdf",
            mime="application/pdf"
        )

        if not results:
            st.markdown("""
            <div class="green-box">
            لم يتم اكتشاف بنود غير متوافقة مع متطلبات SAMA بناءً على قاعدة البيانات الحالية.
            هذه النتيجة لا تعتبر رأيًا قانونيًا نهائيًا.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.subheader("البنود غير المتوافقة مع متطلبات SAMA")

            for i, item in enumerate(results, start=1):
                with st.expander(f"الخطر رقم {i}: {item['topic']} - {item['risk_level']}"):
                    st.write("الكلمات المكتشفة:", item["matched_keywords"])

                    st.markdown("**المرجع التنظيمي المرتبط:**")
                    st.info(item["regulation_reference"])

                    st.markdown(f"""
                    <div class="blue-box">
                    <b>نص المتطلب التنظيمي:</b><br>
                    {item["regulation_text"]}
                    </div>
                    """, unsafe_allow_html=True)

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

        st.caption("ملاحظة: النصوص التنظيمية في نسخة الديمو صياغات مبسطة لأغراض الاختبار، ويمكن لاحقًا استبدالها بنصوص رسمية من SAMA Rulebook.")
