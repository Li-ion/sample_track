import streamlit as st
import pickle

# 页面配置
st.set_page_config(page_title="实验室样品管理", layout="centered")

with open('sample_positions.pkl', 'rb') as f:
    sample_positions = pickle.load(f)

if 'current_lims' not in st.session_state:
    st.session_state.current_lims = None

st.markdown("""
<style>
    body {
        background-color: #f5f7fa;
        font-family: 'Microsoft YaHei', sans-serif;
    }

    .title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: #1a1a1a;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 16px;
        color: #666;
        text-align: center;
        margin-bottom: 20px;
    }
    .input-box {
        width: 100%;
        padding: 12px;
        border: 1px solid #d9d9d9;
        border-radius: 8px;
        font-size: 14px;
        box-sizing: border-box;
    }
    .btn-primary {
        background-color: #4078f2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        cursor: pointer;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
    }
    .btn-primary:hover {
        background-color: #3366cc;
    }
    .btn-secondary {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
    }
    .btn-secondary:hover {
        background-color: #3e8e3c;
    }
    .label {
        font-size: 16px;
        color: #333;
        margin-bottom: 8px;
    }
    .position-display {
        background-color: #f5f7fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #4078f2;
        margin-bottom: 20px;
    }
    .hint {
        font-size: 14px;
        color: #888;
        text-align: center;
        margin-top: 20px;
    }
    .sync-info {
        font-size: 12px;
        color: #4078f2;
        text-align: center;
        margin-top: 8px;
    }
    .scan-icon {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 18px;
        color: #999;
        cursor: pointer;
    }
    .input-group {
        position: relative;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.current_lims is None:
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="title">实验室样品追踪</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">请输入或扫描LIMS号查询样品位置</p>', unsafe_allow_html=True)

        # 输入框 + 扫码图标
        lims_input = st.text_input("LIMS号", placeholder="请输入LIMS号, 如SH-2025-1234", key="lims_input")
        

        # 查询按钮
        if st.button("🔍 查询"):
            if lims_input.strip():
                st.session_state.current_lims = lims_input.strip()
                st.rerun()  # 确保立即跳转
            else:
                st.warning("请输入LIMS编号")

        st.markdown('<p class="hint">输入LIMS号后点击查询按钮，或使用扫码功能快速输入</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # 详情页：更新位置
    lims = st.session_state.current_lims
    current_pos = sample_positions.get(lims, "")

    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown(f'<h1 class="title">位置</h1>', unsafe_allow_html=True)
        st.markdown('<div class="label">LIMS 号</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background-color: #e6f2ff; border-radius: 8px; padding: 10px; text-align: center; color: #4078f2; font-size: 18px; margin: 10px 0;">{lims}</div>', unsafe_allow_html=True)

        st.markdown('<div class="label">当前位置</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="position-display">{current_pos or "无"}</div>', unsafe_allow_html=True)

        locations = ["A1", "A2", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2"]
        new_pos = st.selectbox("更新位置", locations, index=locations.index(current_pos) if current_pos in locations else 0)

        if st.button("更新位置", type="primary"):
            sample_positions[lims] = new_pos
            st.success(f"已成功更新 {lims} 的位置为 {new_pos}")
            with open('sample_positions.pkl', 'wb') as f:
                pickle.dump(sample_positions, f)

        # 返回按钮
        if st.button("← 返回"):
            st.session_state.current_lims = None
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
