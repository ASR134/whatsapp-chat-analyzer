import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import matplotlib 
import seaborn as sns
import numpy as np


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChatPulse · WhatsApp Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #07080d !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(100,60,220,.22) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(20,180,160,.14) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 60% 40%, rgba(255,80,120,.07) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(13,12,20,.85) !important;
    border-right: 1px solid rgba(255,255,255,.06) !important;
    backdrop-filter: blur(24px);
}

[data-testid="stSidebar"] * { color: #e8e6f0 !important; }

[data-testid="stSidebar"] .stFileUploader > div {
    border: 1.5px dashed rgba(130,90,255,.55) !important;
    border-radius: 14px !important;
    background: rgba(130,90,255,.06) !important;
    transition: border-color .2s, background .2s;
}
[data-testid="stSidebar"] .stFileUploader > div:hover {
    border-color: rgba(130,90,255,.9) !important;
    background: rgba(130,90,255,.12) !important;
}

/* Sidebar logo / brand */
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.55rem;
    letter-spacing: -.02em;
    background: linear-gradient(135deg, #a78bfa, #38bdf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    padding: 0 0 6px 0;
    display: block;
}
.sidebar-sub {
    font-size: .75rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: rgba(200,195,230,.45) !important;
    font-family: 'Space Mono', monospace;
    margin-bottom: 28px;
    display: block;
}

/* Selectbox / button */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(167,139,250,.6) !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    letter-spacing: .04em !important;
    padding: 12px 24px !important;
    cursor: pointer !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 4px 24px rgba(124,58,237,.35) !important;
}
.stButton > button:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
}

/* ── Main headings ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -.03em;
    background: linear-gradient(90deg, #a78bfa 0%, #38bdf8 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 6px;
}
.page-subtitle {
    font-size: .85rem;
    color: rgba(200,195,230,.45);
    font-family: 'Space Mono', monospace;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 40px;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #e8e6f0;
    margin: 48px 0 20px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(167,139,250,.4), transparent);
}

/* ── Stat cards ── */
.stat-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 18px;
    padding: 28px 24px;
    text-align: center;
    transition: border-color .25s, transform .2s, box-shadow .25s;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, var(--accent-color, rgba(167,139,250,.15)) 0%, transparent 70%);
    opacity: 0;
    transition: opacity .3s;
}
.stat-card:hover { border-color: rgba(167,139,250,.35); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,.3); }
.stat-card:hover::before { opacity: 1; }
.stat-icon { font-size: 2rem; margin-bottom: 10px; display: block; }
.stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent-start, #a78bfa), var(--accent-end, #38bdf8));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 6px;
}
.stat-label {
    font-size: .72rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: rgba(200,195,230,.5);
    font-family: 'Space Mono', monospace;
}

/* ── Chart containers ── */
.chart-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 24px;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.07) !important;
}

/* ── Welcome state ── */
.welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
    gap: 20px;
}
.welcome-icon {
    font-size: 5rem;
    animation: pulse-icon 3s ease-in-out infinite;
}
@keyframes pulse-icon {
    0%, 100% { transform: scale(1) rotate(-3deg); }
    50% { transform: scale(1.08) rotate(3deg); }
}
.welcome-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: rgba(232,230,240,.7);
}
.welcome-hint {
    font-size: .85rem;
    color: rgba(200,195,230,.35);
    font-family: 'Space Mono', monospace;
    letter-spacing: .06em;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,.3), rgba(56,189,248,.3), transparent);
    margin: 40px 0;
    border: none;
}

/* ── Matplotlib global ── */
div[data-testid="stImage"] img { border-radius: 14px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,.3); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib theme ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0d0c14",
    "axes.facecolor":    "#0d0c14",
    "axes.edgecolor":    "#2a2840",
    "axes.labelcolor":   "#a09ec0",
    "axes.titlecolor":   "#e8e6f0",
    "xtick.color":       "#6b6890",
    "ytick.color":       "#6b6890",
    "grid.color":        "#1a1830",
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "text.color":        "#e8e6f0",
    "font.family":       "monospace",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

GRAD_COLORS = ["#a78bfa","#818cf8","#38bdf8","#34d399","#f472b6","#fb923c","#facc15"]

def styled_fig(figsize=(10,4)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor("#0d0c14")
    ax.set_facecolor("#0d0c14")
    return fig, ax

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="sidebar-brand">ChatPulse</span>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-sub">WhatsApp Analyzer</span>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop your exported chat (.txt)", type=["txt"])

    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode(encoding="utf-8")
        df = preprocessor.preprocess(data)

        users_list = df["user"].unique().tolist()
        if "group notification" in users_list:
            users_list.remove("group notification")
        users_list = sorted(users_list)
        users_list.insert(0, "Overall")

        st.markdown("---")
        selected_user = st.selectbox("👤  Analyze for", users_list)

        run = st.button("⚡  Run Analysis")
    else:
        selected_user = None
        run = False

# ── Main ──────────────────────────────────────────────────────────────────────
if not uploaded_file:
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-icon">💬</div>
        <div class="welcome-text">Drop your chat.<br>Discover the story.</div>
        <div class="welcome-hint">Export a WhatsApp chat → upload in the sidebar → hit Run</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Header
st.markdown('<div class="page-title">Chat Analytics</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">📂 {uploaded_file.name} &nbsp;·&nbsp; {df.shape[0]:,} messages</div>', unsafe_allow_html=True)

if not run:
    st.info("👈  Choose a user and click **Run Analysis** to get started.", icon="✨")
    st.stop()

# ─── 1. Top Stats ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Top Statistics</div>', unsafe_allow_html=True)

num_messages, words, media_elements, links = helper.fetch_stats(selected_user, df)

cards = [
    ("💬", num_messages,    "Messages",       "#a78bfa", "#818cf8"),
    ("📝", words,           "Words",          "#38bdf8", "#34d399"),
    ("🖼️", media_elements,  "Media Shared",   "#f472b6", "#fb923c"),
    ("🔗", links,           "Links Shared",   "#facc15", "#fb923c"),
]

cols = st.columns(4)
for col, (icon, val, label, c1, c2) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div class="stat-card" style="--accent-start:{c1};--accent-end:{c2};--accent-color:{c1}22;">
            <span class="stat-icon">{icon}</span>
            <div class="stat-value">{val:,}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── 2. Monthly Timeline ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">📅 Monthly Timeline</div>', unsafe_allow_html=True)
timeline = helper.monthly_timeline(selected_user, df)

fig, ax = styled_fig((12, 3.5))
x = range(len(timeline))
ax.fill_between(x, timeline["message"], alpha=0.18, color="#a78bfa")
ax.plot(x, timeline["message"], color="#a78bfa", linewidth=2.5, marker="o", markersize=4, markerfacecolor="#38bdf8")
ax.set_xticks(list(x))
ax.set_xticklabels(timeline["time"], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Messages", labelpad=10)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ─── 3. Activity Map ──────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗓️ Activity Map</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    day_series = helper.active_days(selected_user, df)
    fig, ax = styled_fig((6, 4))
    colors = [GRAD_COLORS[i % len(GRAD_COLORS)] for i in range(len(day_series))]
    bars = ax.barh(day_series.index, day_series.values, color=colors, height=0.6, edgecolor="none")
    ax.set_xlabel("Messages", labelpad=8)
    ax.set_title("By Day of Week", pad=12, fontsize=11, color="#e8e6f0")
    ax.grid(axis="x", alpha=0.3)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(day_series.values)*0.01, bar.get_y()+bar.get_height()/2,
                f"{int(w):,}", va="center", fontsize=8, color="#a09ec0")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    month_series = helper.active_months(selected_user, df)
    fig, ax = styled_fig((6, 4))
    colors2 = [GRAD_COLORS[(i+3) % len(GRAD_COLORS)] for i in range(len(month_series))]
    bars2 = ax.barh(month_series.index, month_series.values, color=colors2, height=0.6, edgecolor="none")
    ax.set_xlabel("Messages", labelpad=8)
    ax.set_title("By Month", pad=12, fontsize=11, color="#e8e6f0")
    ax.grid(axis="x", alpha=0.3)
    for bar in bars2:
        w = bar.get_width()
        ax.text(w + max(month_series.values)*0.01, bar.get_y()+bar.get_height()/2,
                f"{int(w):,}", va="center", fontsize=8, color="#a09ec0")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ─── 4. Heatmap ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔥 Hourly Activity Heatmap</div>', unsafe_allow_html=True)
mat_heatmap = helper.activity_heatmap(selected_user, df)

fig, ax = plt.subplots(figsize=(14, 4))
fig.set_facecolor("#0d0c14")
ax.set_facecolor("#0d0c14")
sns.heatmap(
    mat_heatmap, ax=ax,
    cmap=sns.color_palette("rocket", as_cmap=True),
    linewidths=0.4, linecolor="#07080d",
    cbar_kws={"shrink": 0.6, "pad": 0.01},
)
ax.tick_params(colors="#a09ec0", labelsize=8)
ax.set_xlabel("Hour Period", color="#a09ec0", labelpad=10)
ax.set_ylabel("Day", color="#a09ec0", labelpad=10)
plt.xticks(rotation=45, ha="right")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ─── 5. Most Busy Users ───────────────────────────────────────────────────────
if selected_user == "Overall":
    st.markdown('<div class="section-header">🏆 Most Active Users</div>', unsafe_allow_html=True)
    x_series, new_df = helper.most_busy_users(df)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig, ax = styled_fig((8, 4))
        bar_colors = GRAD_COLORS[:len(x_series)]
        ax.bar(x_series.index, x_series.values, color=bar_colors, edgecolor="none", width=0.6)
        ax.set_ylabel("Messages", labelpad=8)
        ax.grid(axis="y", alpha=0.3)
        plt.xticks(rotation=30, ha="right")
        for i, (idx, v) in enumerate(x_series.items()):
            ax.text(i, v + max(x_series.values)*0.01, f"{v:,}", ha="center", fontsize=8, color="#a09ec0")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    with col2:
        st.dataframe(new_df, use_container_width=True, hide_index=True)

# ─── 6. Word Cloud ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">☁️ Word Cloud</div>', unsafe_allow_html=True)
try:
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = styled_fig((10, 5))
    ax.imshow(df_wc, interpolation="bilinear")
    ax.axis("off")
    fig.tight_layout(pad=0)
    st.pyplot(fig)
    plt.close(fig)
except Exception as e:
    st.warning(f"Could not generate word cloud: {e}")

# ─── 7. Most Common Words ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔤 Most Common Words</div>', unsafe_allow_html=True)
most_common_df = helper.most_common_words(selected_user, df)

fig, ax = styled_fig((10, 5))
n = len(most_common_df)
grad = [GRAD_COLORS[i % len(GRAD_COLORS)] for i in range(n)]
ax.barh(most_common_df[0], most_common_df[1], color=grad[::-1], edgecolor="none", height=0.65)
ax.set_xlabel("Frequency", labelpad=8)
ax.grid(axis="x", alpha=0.3)
ax.invert_yaxis()
for i in range(n):
    ax.text(most_common_df[1].iloc[i] + most_common_df[1].max()*0.005,
            i, f"{most_common_df[1].iloc[i]:,}", va="center", fontsize=8, color="#a09ec0")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ─── 8. Emoji Analysis ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">😄 Emoji Analysis</div>', unsafe_allow_html=True)
emoji_df = helper.emoji_helper(selected_user, df)

if emoji_df.empty:
    st.info("No emojis found in this chat.")
else:
    col1, col2 = st.columns([2, 3])
    with col1:
        st.dataframe(emoji_df.rename(columns={0: "Emoji", 1: "Count"}), use_container_width=True, hide_index=True)
    with col2:
        top_n = min(6, len(emoji_df))
        fig, ax = styled_fig((7, 4.5))
        wedge_colors = GRAD_COLORS[:top_n]
        wedges, texts, autotexts = ax.pie(
            emoji_df[1].head(top_n),
            labels=emoji_df[0].head(top_n).tolist(),
            colors=wedge_colors,
            autopct="%0.1f%%",
            startangle=140,
            pctdistance=0.78,
            wedgeprops=dict(width=0.55, edgecolor="#07080d", linewidth=2),
        )
        for t in texts: t.set_color("#e8e6f0"); t.set_fontsize(13)
        for at in autotexts: at.set_color("#0d0c14"); at.set_fontsize(8); at.set_fontweight("bold")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:rgba(200,195,230,.25); font-family:'Space Mono',monospace; font-size:.7rem; letter-spacing:.08em; padding-bottom:20px;">
    CHATPULSE &nbsp;·&nbsp; WHATSAPP ANALYTICS &nbsp;·&nbsp; BUILT WITH STREAMLIT
</div>
""", unsafe_allow_html=True)