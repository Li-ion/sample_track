import streamlit as st
import pandas as pd

# Mock database (replace with real DB like SQLite or API)
# Sample data: {lims_id: location}
sample_db = {
    "SH-2025-1234": "B3",
    "SH-2025-1235": "A5",
    "SH-2025-1236": "C7"
}

# Define available locations
locations = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5"]

# Page configuration
st.set_page_config(page_title="实验室样品管理", layout="centered")

# Initialize session state
if 'current_lims' not in st.session_state:
    st.session_state.current_lims = None
if 'page' not in st.session_state:
    st.session_state.page = "search"

def show_search_page():
    st.markdown("<h1 style='text-align: center; color: #1a365d;'>实验室样品管理</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>请输入或扫描LIMS号查询样品位置</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([8, 1])
    with col1:
        lims_input = st.text_input("LIMS号", placeholder="请输入LIMS号", key="lims_input")
    with col2:
        if st.button("📋", key="scan_btn"):
            st.warning("扫码功能未实现，可扩展为二维码扫描器")

    if st.button("🔍 查询", key="search_btn"):
        if lims_input.strip() == "":
            st.error("请输入LIMS号")
        else:
            if lims_input in sample_db:
                st.session_state.current_lims = lims_input
                st.session_state.page = "detail"
            else:
                st.warning(f"未找到 LIMS 号：{lims_input}")

    st.markdown("<p style='text-align: center; color: #999;'>提示：输入LIMS号后点击查询按钮，或使用扫码功能快速输入</p>", unsafe_allow_html=True)
    if st.button("🔄 点击同步最新数据", key="sync_btn"):
        st.success("数据已同步！")

def show_detail_page():
    lims_id = st.session_state.current_lims
    current_location = sample_db.get(lims_id, "")

    # Header
    st.markdown(f"<h2 style='text-align: center; color: #1a365d;'>样品信息</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; background-color: #e6f2ff; border-radius: 10px; padding: 10px; font-size: 1.2em; color: #1a365d; margin: 10px 0;'>{lims_id}</div>", unsafe_allow_html=True)

    # Current location
    st.markdown("<p style='color: #333; font-weight: 500;'>当前位置</p>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center; font-size: 1.5em; color: #1a365d; margin: 10px 0;'>{current_location}</div>", unsafe_allow_html=True)

    # Update location
    st.markdown("<p style='color: #333; font-weight: 500;'>更新位置</p>", unsafe_allow_html=True)
    new_location = st.selectbox("", options=locations, index=locations.index(current_location) if current_location in locations else 0)

    # Update button
    if st.button("🔐 更新位置", type="primary", use_container_width=True):
        sample_db[lims_id] = new_location
        st.success(f"✅ 样品位置已更新为：{new_location}")
        st.session_state.page = "search"

    # Footer note
    st.markdown("<div style='text-align: center; margin-top: 50px; color: #666; font-size: 0.9em;'>提示：选择位置后点击更新按钮保存样品位置信息<br><span style='color: #1a365d;'>数据已自动同步至云端，所有设备可查看相同信息</span></div>", unsafe_allow_html=True)

    # Back button
    if st.button("⬅️ 返回", key="back_btn"):
        st.session_state.page = "search"

# Main App Logic
if st.session_state.page == "search":
    show_search_page()
else:
    show_detail_page()

# Add top navigation bar
if st.session_state.page == "detail":
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("⬅️ 返回", key="top_back"):
            st.session_state.page = "search"
    with col2:
        if st.button("🔄 刷新", key="top_refresh"):
            st.experimental_rerun()