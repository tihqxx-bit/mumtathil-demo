import html
from io import BytesIO

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ممتثل",
    page_icon="⚖️",
    layout="centered"
)


# =========================
# تصميم الواجهة
# =========================

st.markdown("""
<style>
.stApp {
    background: #0f172a;
    color: white;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

.main-card {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 20px;
}

.main-card h1 {
    color: white;
    font-size: 44px;
    margin-bottom: 8px;
}

.main-card p {
    color: #cbd5e1;
    font-size: 17px;
    line-height: 1.8;
}

.note-box {
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
    color: #e2e8f0;
}

.issue-box {
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 14px;
}

.blue-box {
    background: rgba(37, 99, 235, 0.18);
    border: 1px solid rgba(96, 165, 250, 0.45);
    border-radius: 14px;
    padding: 14px;
    margin-top: 10px;
}

.yellow-box {
    background: rgba(245, 158, 11, 0.18);
    border: 1px solid rgba(251, 191, 36, 0.45);
    border-radius: 14px;
    padding: 14px;
    margin-top: 10px;
}

.red-box {
    background: rgba(239, 68, 68, 0.18);
    border: 1px solid rgba(248, 113, 113, 0.45);
    border-radius: 14px;
    padding: 14px;
    margin-top: 10px;
}

.green-box {
    background: rgba(34, 197, 94, 0.18);
    border: 1px solid rgba(74, 222, 128, 0.45);
    border-radius: 14px;
    padding: 14px;
    margin-top: 10px;
}

.stButton > button {
    width: 100%;
    height: 54px;
    border-radius: 14px;
    background: linear-gradient(90deg, #2563eb, #14b8a6);
    color: white;
    border: none;
    font-size: 18px;
    font-weight: bold;
}

.stDownloadButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    background: #16a34a;
    color: white;
    border: none;
    font-size: 17px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# =========================
# قاعدة SAMA للديمو
# =========================

def load_sama_rules():
    """
    داتا تجريبية للـ MVP.
    الفكرة: لا نبحث عن كلمات عامة مثل رسوم وبيانات.
    نبحث فقط عن عبارات خطرة تدل على مخالفة أو ضعف امتثال.
    """
    data = {
        "topic": [
            "الإفصاح عن الرسوم",
            "شكاوى العملاء",
            "مشاركة بيانات العميل",
            "إيقاف الخدمة أو الحساب",
            "الإسناد الخارجي"
        ],
        "risk_phrases": [
            "دون إشعار,بدون إشعار,دون إبلاغ,بدون إبلاغ,تعديل الرسوم في أي وقت,تغيير الرسوم في أي وقت,دون الحاجة إلى موافقته",
            "لا تتحمل الشركة مسؤولية استقبال أي شكوى,لا يوجد حق اعتراض,قبول نهائي بجميع قرارات الشركة,لا يحق للعميل الاعتراض,أي شكوى أو اعتراض أو تظلم",
            "مشاركة البيانات مع طرف ثالث دون موافقة,مشاركة البيانات دون موافقة,دون توضيح أسباب المشاركة,دون موافقة منفصلة,مشاركة بيانات العميل مع طرف ثالث",
            "إيقاف الخدمة دون توضيح السبب,تعليق الحساب دون إشعار,إغلاق الحساب دون إشعار,في أي وقت دون توضيح السبب,في أي وقت دون إشعار",
            "إسناد خارجي دون ضوابط,تعهيد الخدمة دون التزام,مزود خارجي دون رقابة,دون توضيح ضوابط حماية البيانات,دون أي التزام إضافي"
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
            "البند قد يضعف حق العميل في تقديم الشكوى أو الاعتراض.",
            "البند قد يسمح بمشاركة بيانات العميل مع أطراف خارجية دون ضوابط واضحة.",
            "البند قد يمنح الشركة صلاحية إيقاف الخدمة أو الحساب دون سبب أو إشعار واضح.",
            "غياب ضوابط واضحة عند الاستعانة بطرف خارجي قد يسبب خطرًا تنظيميًا وتشغيليًا."
        ],
        "consequence": [
            "قد يؤدي إلى شكاوى عملاء أو إلزام الشركة بتعديل البند أو إجراء رقابي.",
            "قد يؤدي إلى ضعف حماية العميل وتصعيد الشكاوى للجهات المختصة.",
            "قد يؤدي إلى مخاطر خصوصية ومساءلة تنظيمية وفقدان ثقة العملاء.",
            "قد يؤدي إلى شكاوى عملاء أو اعتبار البند غير متوازن.",
            "قد يؤدي إلى مخاطر تشغيلية أو مساءلة تنظيمية عند فشل مزود الخدمة أو تسرب البيانات."
        ],
        "suggested_fix": [
            "إضافة نص يلزم الشركة بإشعار العميل قبل تغيير الرسوم بمدة واضحة، مع توضيح حقه في الاعتراض أو إنهاء الخدمة.",
            "إضافة بند يوضح طريقة تقديم الشكاوى، مدة الرد، آلية التوثيق، وآلية التصعيد عند الحاجة.",
            "توضيح متى ولماذا تتم مشاركة البيانات ومع من، مع اشتراط وجود موافقة أو أساس نظامي مناسب.",
            "تحديد حالات الإيقاف بوضوح مثل الاحتيال أو مخالفة الشروط أو المتطلبات النظامية، مع إشعار العميل متى ما أمكن.",
            "إضافة بند يحدد مسؤوليات مزود الخدمة، حماية البيانات، استمرارية الخدمة، وآلية الرقابة والمتابعة."
        ]
    }

    return pd.DataFrame(data)


# =========================
# قراءة الملف
# =========================

def extract_text_from_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if file_name.endswith(".pdf"):
        file_bytes = uploaded_file.read()
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""

        for page in pdf:
            text += page.get_text() + "\n"

        return text

    return ""


# =========================
# استخراج الجملة/البند من المستند
# =========================

def get_document_snippet(contract_text, phrase, window=170):
    text_lower = contract_text.lower()
    phrase_lower = phrase.lower()

    index = text_lower.find(phrase_lower)

    if index == -1:
        return "لم يتمكن النظام من استخراج نص البند من المستند."

    start = max(index - window, 0)
    end = min(index + len(phrase) + window, len(contract_text))

    snippet = contract_text[start:end].strip()
    snippet = snippet.replace("\n", " ")

    return snippet


# =========================
# التحليل
# =========================

def analyze_contract_against_sama(contract_text):
    rules = load_sama_rules()
    results = []
    contract_text_lower = contract_text.lower()

    for _, row in rules.iterrows():
        phrases = str(row["risk_phrases"]).split(",")
        matched_phrases = []

        for phrase in phrases:
            phrase = phrase.strip()
            if phrase and phrase.lower() in contract_text_lower:
                matched_phrases.append(phrase)

        if matched_phrases:
            first_phrase = matched_phrases[0]
            document_snippet = get_document_snippet(contract_text, first_phrase)

            results.append({
                "authority": "SAMA",
                "topic": row["topic"],
                "risk_level": row["risk_level"],
                "matched_phrases": "، ".join(matched_phrases),
                "document_snippet": document_snippet,
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

    risk_score = min((high_count * 25) + (medium_count * 12), 100)
    compliance_score = max(100 - risk_score, 0)

    return risk_score, compliance_score, high_count, medium_count


def get_final_message(risk_score, results_count):
    if results_count == 0:
        return "لم يتم اكتشاف بنود غير متوافقة مع متطلبات SAMA بناءً على قاعدة بيانات الديمو الحالية.", "success"

    if risk_score >= 75:
        return "المستند عالي الخطورة ويحتوي على بنود لا تتماشى مع متطلبات SAMA. ينصح بعدم اعتماده قبل المراجعة والتعديل.", "error"

    if risk_score >= 40:
        return "المستند يحتوي على مخاطر متوسطة مرتبطة بمتطلبات SAMA. يفضل تعديل البنود المشار إليها قبل الاعتماد.", "warning"

    return "المستند يحتوي على ملاحظات محدودة، ويحتاج مراجعة نهائية حسب حساسية المستند.", "info"


# =========================
# إنشاء PDF واضح بالعربي
# =========================

def safe_html(text):
    return html.escape(str(text))


def add_html_page(doc, body_html):
    page = doc.new_page(width=595, height=842)  # A4
    rect = fitz.Rect(40, 40, 555, 802)

    full_html = f"""
    <html>
    <body dir="rtl">
        <div class="page">
            {body_html}
        </div>
    </body>
    </html>
    """

    css = """
    body {
        direction: rtl;
        font-family: sans-serif;
        color: #0f172a;
        line-height: 1.7;
        font-size: 13px;
    }

    h1 {
        color: #1e3a8a;
        font-size: 24px;
        text-align: center;
        margin-bottom: 16px;
    }

    h2 {
        color: #1e40af;
        font-size: 17px;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    h3 {
        color: #0f172a;
        font-size: 14px;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    p {
        margin: 5px 0;
    }

    .summary {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 14px;
    }

    .safe {
        background: #ecfdf5;
        border: 1px solid #86efac;
        border-radius: 12px;
        padding: 14px;
        margin-top: 12px;
    }

    .issue {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }

    .reg {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 10px;
        padding: 10px;
        margin-top: 8px;
    }

    .problem {
        background: #fef3c7;
        border: 1px solid #fcd34d;
        border-radius: 10px;
        padding: 10px;
        margin-top: 8px;
    }

    .danger {
        background: #fee2e2;
        border: 1px solid #fca5a5;
        border-radius: 10px;
        padding: 10px;
        margin-top: 8px;
    }

    .fix {
        background: #dcfce7;
        border: 1px solid #86efac;
        border-radius: 10px;
        padding: 10px;
        margin-top: 8px;
    }

    .footer {
        color: #475569;
        font-size: 11px;
        margin-top: 20px;
        border-top: 1px solid #cbd5e1;
        padding-top: 10px;
    }
    """

    page.insert_htmlbox(rect, full_html, css=css)


def create_pdf_report(results, risk_score, compliance_score, high_count, medium_count, final_message):
    doc = fitz.open()

    summary_html = f"""
    <h1>تقرير فحص الامتثال مقابل متطلبات SAMA</h1>

    <div class="summary">
        <p><b>المنصة:</b> ممتثل</p>
        <p><b>مصدر المطابقة:</b> البنك المركزي السعودي SAMA</p>
        <p><b>نسبة الخطورة:</b> {risk_score}%</p>
        <p><b>درجة الامتثال:</b> {compliance_score}/100</p>
        <p><b>عدد المخاطر العالية:</b> {high_count}</p>
        <p><b>عدد المخاطر المتوسطة:</b> {medium_count}</p>
        <p><b>النتيجة النهائية:</b> {safe_html(final_message)}</p>
    </div>
    """

    if not results:
        summary_html += """
        <div class="safe">
            <h2>حالة المستند</h2>
            <p>لم يتم اكتشاف بنود غير متوافقة مع متطلبات SAMA بناءً على قاعدة بيانات الديمو الحالية.</p>
        </div>
        """
    else:
        summary_html += """
        <h2>البنود التي لا تتماشى مع متطلبات SAMA</h2>
        <p>يحتوي هذا التقرير على كل بند تم اكتشافه، والنص التنظيمي المرتبط به، والمشكلة، والعواقب، والإجراء المقترح.</p>
        """

    summary_html += """
    <div class="footer">
        هذا التقرير يمثل فحص امتثال أولي آلي لأغراض الديمو، ولا يعد رأيًا قانونيًا نهائيًا.
        يجب مراجعته من مختص قانوني أو مسؤول امتثال قبل الاعتماد.
    </div>
    """

    add_html_page(doc, summary_html)

    for i, item in enumerate(results, start=1):
        issue_html = f"""
        <h1>تفصيل الخطر رقم {i}</h1>

        <div class="issue">
            <h2>{safe_html(item["topic"])}</h2>
            <p><b>الجهة المرتبطة:</b> SAMA</p>
            <p><b>مستوى الخطورة:</b> {safe_html(item["risk_level"])}</p>
            <p><b>العبارات الخطرة المكتشفة:</b> {safe_html(item["matched_phrases"])}</p>
        </div>

        <h2>النص الموجود في المستند</h2>
        <div class="problem">
            <p>{safe_html(item["document_snippet"])}</p>
        </div>

        <h2>المرجع التنظيمي المرتبط</h2>
        <div class="reg">
            <p><b>{safe_html(item["regulation_reference"])}</b></p>
            <p>{safe_html(item["regulation_text"])}</p>
        </div>

        <h2>المشكلة</h2>
        <div class="problem">
            <p>{safe_html(item["problem"])}</p>
        </div>

        <h2>العواقب المحتملة</h2>
        <div class="danger">
            <p>{safe_html(item["consequence"])}</p>
        </div>

        <h2>الإجراء المقترح</h2>
        <div class="fix">
            <p>{safe_html(item["suggested_fix"])}</p>
        </div>

        <div class="footer">
            هذا التقرير يمثل فحص امتثال أولي آلي، ولا يعد رأيًا قانونيًا نهائيًا.
        </div>
        """

        add_html_page(doc, issue_html)

    pdf_bytes = doc.tobytes()
    doc.close()

    return BytesIO(pdf_bytes)


# =========================
# الواجهة
# =========================

st.markdown("""
<div class="main-card">
    <h1>ممتثل</h1>
    <p>
    ارفع عقد أو سياسة، وسيقوم ممتثل بفحصها مقابل متطلبات البنك المركزي السعودي SAMA.
    النتيجة تعرض البنود عالية الخطورة، والنص التنظيمي المرتبط بها، مع تقرير PDF واضح.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
نطاق الديمو الحالي: البنك المركزي السعودي SAMA فقط.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "ارفع ملف PDF أو TXT",
    type=["pdf", "txt"]
)

show_text = st.checkbox("عرض النص المستخرج من الملف", value=False)

analyze_button = st.button("ابدأ الفحص")


if analyze_button and not uploaded_file:
    st.warning("ارفع ملف PDF أو TXT أولًا.")

if uploaded_file and analyze_button:
    contract_text = extract_text_from_file(uploaded_file)

    if not contract_text.strip():
        st.error("لم يتمكن النظام من قراءة النص من الملف. جرّب ملف PDF يحتوي على نص قابل للنسخ أو ملف TXT.")
    else:
        if show_text:
            st.text_area("النص المستخرج", contract_text, height=220)

        results = analyze_contract_against_sama(contract_text)
        risk_score, compliance_score, high_count, medium_count = calculate_scores(results)
        final_message, message_type = get_final_message(risk_score, len(results))

        st.subheader("نتيجة الفحص")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("نسبة الخطورة", f"{risk_score}%")

        with col2:
            st.metric("درجة الامتثال", f"{compliance_score}/100")

        with col3:
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
                لم يتم اكتشاف بنود غير متوافقة مع متطلبات SAMA بناءً على قاعدة بيانات الديمو الحالية.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.subheader("البنود غير المتوافقة")

            for i, item in enumerate(results, start=1):
                with st.expander(f"الخطر رقم {i}: {item['topic']} - {item['risk_level']}"):
                    st.markdown(f"""
                    <div class="yellow-box">
                        <b>النص الموجود في المستند:</b><br>
                        {item["document_snippet"]}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="blue-box">
                        <b>المرجع التنظيمي المرتبط:</b><br>
                        {item["regulation_reference"]}<br><br>
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

st.caption("تنبيه: النصوص التنظيمية في الديمو صياغات مبسطة لأغراض الاختبار، ويمكن لاحقًا استبدالها بنصوص رسمية معتمدة من SAMA.")
