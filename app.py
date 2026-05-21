import os
import tempfile
import streamlit as st
from flashcard_generator import generate_question
from utils.pdf_reader import extract_text_from_pdf

st.set_page_config(page_title="AI 闪卡生成器", layout="wide")
st.title("📚 AI 闪卡生成器")

# 侧边栏：填写 API Key
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input(
        "DeepSeek API Key",
        type="password",
        placeholder="sk-...",
        help="在 platform.deepseek.com 获取 API Key",
    )
    if api_key:
        os.environ["DEEPSEEK_API_KEY"] = api_key
        st.success("API Key 已设置")
    else:
        st.warning("请先填写 API Key")

# 保存文本到 session state
if "content" not in st.session_state:
    st.session_state.content = ""

mode = st.radio("输入方式：", ["粘贴文本", "上传 PDF"], index=0)

if mode == "粘贴文本":
    st.session_state.content = st.text_area(
        "粘贴文章内容：", value=st.session_state.content, height=300
    )
else:
    uploaded = st.file_uploader("上传 PDF 文件", type="pdf")
    if uploaded is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name
        with st.spinner("正在提取 PDF 文本…"):
            st.session_state.content = extract_text_from_pdf(tmp_path)
        os.remove(tmp_path)
        st.success("PDF 文本提取成功！")

keywords = st.text_input(
    "输入关键词（逗号分隔，例如：太阳，核聚变）："
).strip()
kw_list = [k.strip() for k in keywords.split(",") if k.strip()]

if st.button("生成闪卡"):
    if not os.environ.get("DEEPSEEK_API_KEY"):
        st.error("❌ 请先在左侧填写 DeepSeek API Key。")
    elif not st.session_state.content:
        st.warning("⚠️ 请提供文章内容（文本或 PDF）。")
    elif not kw_list:
        st.warning("⚠️ 请输入至少一个关键词。")
    else:
        with st.spinner("正在生成闪卡…"):
            for kw in kw_list:
                try:
                    card = generate_question(kw, st.session_state.content)
                    st.markdown(f"**Q：** {card['question']}")
                    st.markdown(f"**A：** {card['answer']}")
                    st.markdown("---")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"API 调用失败：{e}")
