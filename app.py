import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# ── PROFESSIONAL CSS ──
st.markdown("""
<style>
/* ── MAIN BACKGROUND ── */
.stApp {
    background: linear-gradient(160deg, #f0f4ff 0%, #faf5ff 50%, #f0fdf4 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* ── MAIN TITLE ── */
.main-title {
    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 50%, #0f766e 100%);
    color: white;
    padding: 35px 40px;
    border-radius: 20px;
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(124,58,237,0.3);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.main-subtitle {
    font-size: 1rem;
    font-weight: 400;
    color: #e0e7ff;
    margin-top: 8px;
    letter-spacing: 1px;
}

/* ── SECTION TITLES ── */
.section-title {
    background: linear-gradient(90deg, #1e40af, #7c3aed);
    color: white;
    padding: 14px 28px;
    border-radius: 12px;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 30px 0 15px 0;
    box-shadow: 0 4px 15px rgba(124,58,237,0.25);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── METRIC CARDS ── */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-top: 5px solid #7c3aed;
    transition: transform 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(124,58,237,0.2);
}

/* ── INFO BOXES ── */
.stAlert {
    border-radius: 14px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07) !important;
    font-weight: 600 !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 40%, #1e3a5f 100%) !important;
    padding: 20px 10px !important;
}

/* Sidebar heading */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* ── SELECTBOX SELECTED VALUE ── */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #f1f5f9 !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

/* ── DROPDOWN OPTIONS LIST ── */
div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 600 !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: #c7d2fe !important;
    color: #1e1b4b !important;
}

/* ── DATE INPUT ── */
section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="input"] * {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] input {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

/* ── CHECKBOX ── */
section[data-testid="stSidebar"] .stCheckbox label p {
    color: #cbd5e1 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

/* ── SIDEBAR DIVIDER ── */
section[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: 14px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    overflow: hidden !important;
}

/* ── FOOTER ── */
.footer {
    background: linear-gradient(135deg, #1e40af, #7c3aed, #0f766e);
    color: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    margin-top: 40px;
    font-size: 1rem;
    font-weight: 600;
    box-shadow: 0 6px 20px rgba(124,58,237,0.3);
    letter-spacing: 0.5px;
}

/* ── DIVIDER ── */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, #1e40af, #7c3aed, #0f766e) !important;
    margin: 25px 0 !important;
    border-radius: 5px !important;
    opacity: 0.3 !important;
}

/* ── PLOTLY CHART CONTAINER ── */
.stPlotlyChart {
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    overflow: hidden !important;
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TITLE
# ══════════════════════════════════════
st.markdown("""
<div class="main-title">
    📈 Stock Market Trend Analysis Dashboard
    <div class="main-subtitle">Real-Time Data • Technical Indicators • Professional Analytics</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
st.sidebar.markdown("## ⚙️ Control Panel")
st.sidebar.markdown("---")

stock = st.sidebar.selectbox(
    "🔍 Select Stock",
    ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "NFLX", "META"],
    index=0
)

st.sidebar.markdown("### 📅 Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Charts to Display")
show_ma     = st.sidebar.checkbox("📈 Moving Averages", value=True)
show_bb     = st.sidebar.checkbox("🎯 Bollinger Bands", value=True)
show_volume = st.sidebar.checkbox("📊 Volume Chart",    value=True)
show_rsi    = st.sidebar.checkbox("💹 RSI Indicator",   value=True)
show_macd   = st.sidebar.checkbox("📉 MACD Indicator",  value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; color:#94a3b8; font-size:0.85rem; padding:10px;'>
    📈 Stock Dashboard v2.0<br>
    <span style='color:#64748b;'>Data: Yahoo Finance</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# FETCH DATA
# ══════════════════════════════════════
with st.spinner(f"⏳ Fetching {stock} data..."):
    data = yf.download(stock, start=start_date, end=end_date, progress=False)
    data.columns = data.columns.droplevel(1)
    ticker = yf.Ticker(stock)
    info = ticker.info

# ══════════════════════════════════════
# COMPANY INFO
# ══════════════════════════════════════
st.markdown('<div class="section-title">🏢 Company Information</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info(f"**🏢 Company**\n\n{info.get('longName', stock)}")
with col2:
    st.info(f"**🏭 Sector**\n\n{info.get('sector', 'N/A')}")
with col3:
    st.info(f"**🏗️ Industry**\n\n{info.get('industry', 'N/A')}")
with col4:
    st.info(f"**🌍 Country**\n\n{info.get('country', 'N/A')}")

st.markdown("---")

# ══════════════════════════════════════
# KEY METRICS
# ══════════════════════════════════════
st.markdown('<div class="section-title">📊 Key Market Metrics</div>', unsafe_allow_html=True)

current_price = round(float(data['Close'].iloc[-1]), 2)
prev_price    = round(float(data['Close'].iloc[-2]), 2)
price_change  = round(current_price - prev_price, 2)
pct_change    = round((price_change / prev_price) * 100, 2)
high_52       = round(float(data['High'].max()), 2)
low_52        = round(float(data['Low'].min()), 2)
avg_volume    = round(float(data['Volume'].mean()), 0)
total_days    = len(data)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Current Price",  f"${current_price}", f"{price_change} ({pct_change}%)")
col2.metric("📈 52 Week High",   f"${high_52}")
col3.metric("📉 52 Week Low",    f"${low_52}")
col4.metric("📊 Avg Daily Volume", f"{avg_volume:,.0f}")

st.markdown("---")

# ══════════════════════════════════════
# CALCULATE INDICATORS
# ══════════════════════════════════════
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

rsi_ind = RSIIndicator(data['Close'])
data['RSI'] = rsi_ind.rsi()

macd_ind = MACD(data['Close'])
data['MACD']        = macd_ind.macd()
data['MACD_Signal'] = macd_ind.macd_signal()
data['MACD_Hist']   = macd_ind.macd_diff()

bb_ind = BollingerBands(data['Close'])
data['BB_Upper']  = bb_ind.bollinger_hband()
data['BB_Lower']  = bb_ind.bollinger_lband()
data['BB_Middle'] = bb_ind.bollinger_mavg()

# ── Chart base layout ──
def base_layout(title, y_title="Price (USD)", height=430):
    return dict(
        template='plotly_white',
        title=dict(text=title, font=dict(size=16, color='#1e40af', family='Segoe UI')),
        xaxis_title="Date",
        yaxis_title=y_title,
        paper_bgcolor='white',
        plot_bgcolor='#f8faff',
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False),
        margin=dict(l=50, r=30, t=70, b=50),
        hovermode='x unified'
    )

# ══════════════════════════════════════
# CHART 1 — LINE + MOVING AVERAGES
# ══════════════════════════════════════
if show_ma:
    st.markdown('<div class="section-title">📈 Stock Price with Moving Averages</div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=data.index, y=data['Close'],
        mode='lines', name='Close Price',
        line=dict(color='#1e40af', width=2.5),
        fill='tozeroy', fillcolor='rgba(30,64,175,0.05)'
    ))
    fig1.add_trace(go.Scatter(
        x=data.index, y=data['MA20'],
        mode='lines', name='MA 20 Days',
        line=dict(color='#f59e0b', width=2, dash='dot')
    ))
    fig1.add_trace(go.Scatter(
        x=data.index, y=data['MA50'],
        mode='lines', name='MA 50 Days',
        line=dict(color='#10b981', width=2, dash='dot')
    ))
    fig1.update_layout(**base_layout(f"{stock} — Closing Price with Moving Averages"))
    st.plotly_chart(fig1, use_container_width=True)

# ══════════════════════════════════════
# CHART 2 — CANDLESTICK + BOLLINGER
# ══════════════════════════════════════
if show_bb:
    st.markdown('<div class="section-title">🕯️ Candlestick Chart with Bollinger Bands</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'], high=data['High'],
        low=data['Low'],   close=data['Close'],
        name='OHLC',
        increasing_line_color='#10b981',
        decreasing_line_color='#ef4444'
    ))
    fig2.add_trace(go.Scatter(
        x=data.index, y=data['BB_Upper'],
        mode='lines', name='BB Upper',
        line=dict(color='#ef4444', width=1.5, dash='dash')
    ))
    fig2.add_trace(go.Scatter(
        x=data.index, y=data['BB_Middle'],
        mode='lines', name='BB Middle',
        line=dict(color='#f59e0b', width=1, dash='dot')
    ))
    fig2.add_trace(go.Scatter(
        x=data.index, y=data['BB_Lower'],
        mode='lines', name='BB Lower',
        line=dict(color='#10b981', width=1.5, dash='dash'),
        fill='tonexty', fillcolor='rgba(16,185,129,0.05)'
    ))
    fig2.update_layout(**base_layout(f"{stock} — Candlestick with Bollinger Bands"))
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════
# CHART 3 — VOLUME
# ══════════════════════════════════════
if show_volume:
    st.markdown('<div class="section-title">📊 Trading Volume Analysis</div>', unsafe_allow_html=True)
    colors = ['#059669' if data['Close'].iloc[i] >= data['Open'].iloc[i]
              else '#dc2626' for i in range(len(data))]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=data.index, y=data['Volume'],
        name='Volume',
        marker_color=colors,
        marker_line_color=colors,
        marker_line_width=0.5,
        opacity=1.0
    ))
    layout3 = base_layout(f"{stock} — Trading Volume", y_title="Volume", height=370)
    fig3.update_layout(**layout3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════
# CHART 4 — RSI
# ══════════════════════════════════════
if show_rsi:
    st.markdown('<div class="section-title">💹 RSI — Relative Strength Index</div>', unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_hrect(y0=70, y1=100, fillcolor="#fee2e2", opacity=0.4, line_width=0)
    fig4.add_hrect(y0=0,  y1=30,  fillcolor="#dcfce7", opacity=0.4, line_width=0)
    fig4.add_trace(go.Scatter(
        x=data.index, y=data['RSI'],
        mode='lines', name='RSI',
        line=dict(color='#7c3aed', width=2.5)
    ))
    fig4.add_hline(y=70, line_dash="dash", line_color="#ef4444", line_width=1.5,
                   annotation_text="Overbought (70)", annotation_position="right")
    fig4.add_hline(y=30, line_dash="dash", line_color="#10b981", line_width=1.5,
                   annotation_text="Oversold (30)", annotation_position="right")
    layout4 = base_layout(f"{stock} — RSI Indicator", y_title="RSI Value", height=370)
    fig4.update_layout(**layout4)
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════
# CHART 5 — MACD
# ══════════════════════════════════════
if show_macd:
    st.markdown('<div class="section-title">📉 MACD — Moving Average Convergence Divergence</div>', unsafe_allow_html=True)
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=data.index, y=data['MACD_Hist'],
        name='Histogram',
        marker_color=['#10b981' if v >= 0 else '#ef4444' for v in data['MACD_Hist']],
        opacity=0.6
    ))
    fig5.add_trace(go.Scatter(
        x=data.index, y=data['MACD'],
        mode='lines', name='MACD',
        line=dict(color='#1e40af', width=2.5)
    ))
    fig5.add_trace(go.Scatter(
        x=data.index, y=data['MACD_Signal'],
        mode='lines', name='Signal Line',
        line=dict(color='#ef4444', width=2)
    ))
    layout5 = base_layout(f"{stock} — MACD Indicator", y_title="MACD Value", height=370)
    fig5.update_layout(**layout5)
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════
# RAW DATA TABLE
# ══════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">📋 Recent Stock Data — Last 10 Trading Days</div>', unsafe_allow_html=True)
display_data = data[['Open','High','Low','Close','Volume','MA20','MA50','RSI']].tail(10).round(2)
st.dataframe(display_data, use_container_width=True)

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<div class="footer">
    📈 Stock Market Trend Analysis Dashboard &nbsp;|&nbsp;
    Stock: <b>{stock}</b> &nbsp;|&nbsp;
    Data Source: Yahoo Finance &nbsp;|&nbsp;
    Built with ❤️ using Python & Streamlit
</div>
""", unsafe_allow_html=True)
