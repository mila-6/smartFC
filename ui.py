import streamlit as st
from main import app, MoneyState
import matplotlib.pyplot as plt

# إعدادات الصفحة
st.set_page_config(page_title="SmartFC Assistant", layout="wide")

# خلفية بنفسجي غامق + نص أبيض
page_bg = """
<style>
body {
    background-color: #2b0040;
    color: white;
}
div.stButton > button {
    background-color: #6a0dad;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
}
textarea, input {
    background-color: #3d0066 !important;
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# عنوان الواجهة
st.title("💜 SmartFC – مساعد إدارة المال")

# سجل المحادثات
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# إدخال المستخدم
user_input = st.text_input("اكتبي رسالتك هنا:")

# زر الإرسال
if st.button("إرسال"):
    if user_input.strip() != "":
        state = MoneyState(messages=[], memory={}, query=user_input)
        result = app.invoke(state)
        reply = result.messages[-1]["content"]

        # حفظ المحادثة
        st.session_state.chat_history.append(("أنتِ", user_input))
        st.session_state.chat_history.append(("SmartFC", reply))

# عرض سجل المحادثات
st.subheader("📜 سجل المحادثات")
for sender, msg in st.session_state.chat_history:
    st.write(f"**{sender}:** {msg}")

# تحليل المصاريف (رسومي)
st.subheader("📊 تحليل المصاريف")
expenses_input = st.text_area("اكتبي مصاريفك بهذا الشكل:\nطعام: 200\nملابس: 150\nترفيه: 100")

if st.button("تحليل المصاريف"):
    if expenses_input.strip() != "":
        categories = {}
        lines = expenses_input.split("\n")
        for line in lines:
            if ":" in line:
                cat, val = line.split(":")
                categories[cat.strip()] = float(val.strip())

        # رسم بياني
        fig, ax = plt.subplots()
        ax.bar(categories.keys(), categories.values(), color="#b366ff")
        ax.set_facecolor("#2b0040")
        fig.patch.set_facecolor("#2b0040")
        ax.tick_params(colors="white")
        ax.set_title("تحليل المصاريف", color="white")

        st.pyplot(fig)

# زر إعادة تشغيل الذاكرة
if st.button("🔄 إعادة تشغيل الذاكرة"):
    st.session_state.chat_history = []
    st.success("تم مسح الذاكرة وإعادة تشغيل النظام.")
