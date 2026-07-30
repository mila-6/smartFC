import streamlit as st
from main import app, MoneyState  # استيراد الـ agent والـ state من مشروعك

# إعدادات الواجهة
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

# صندوق إدخال المستخدم
user_input = st.text_input("اكتبي رسالتك هنا:", "")

# زر الإرسال
if st.button("إرسال"):
    if user_input.strip() != "":
        # تشغيل الـ agent
        state = MoneyState(messages=[], memory={}, query=user_input)
        result = app.invoke(state)

        # عرض رد المساعد
        st.subheader("رد المساعد:")
        st.write(result.messages[-1]["content"])
