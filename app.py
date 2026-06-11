
from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# Dashboard BI Modul 6
# Studi Kasus: Dampak Penggunaan AI Generatif terhadap
# Performa Akademik dan Kesejahteraan Mahasiswa
# =========================================================

st.set_page_config(
    page_title="AI Student Impact BI Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual identity tokens ----------
COLORS = {
    "ink": "#EEF4FF",
    "muted": "#9AA8C7",
    "panel": "#141A2B",
    "panel_2": "#19213A",
    "line": "rgba(238,244,255,.13)",
    "violet": "#8B5CF6",
    "cyan": "#38BDF8",
    "mint": "#2DD4BF",
    "amber": "#F59E0B",
    "coral": "#FB7185",
    "green": "#22C55E",
    "red": "#EF4444",
}
PLOTLY_SEQUENCE = [COLORS["violet"], COLORS["cyan"], COLORS["mint"], COLORS["amber"], COLORS["coral"], "#A78BFA", "#67E8F9"]
BURNOUT_ORDER = ["Low", "Medium", "High"]
SEGMENT_ORDER = ["Light User", "Moderate User", "Heavy User"]
YEAR_ORDER = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
MAJOR_ORDER = ["STEM", "Business", "Humanities", "Medical", "Arts"]
POLICY_ORDER = ["Allowed_With_Citation", "Actively_Encouraged", "Strict_Ban"]

# ---------- CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 10% 8%, rgba(139,92,246,.24), transparent 34%),
            radial-gradient(circle at 92% 14%, rgba(45,212,191,.16), transparent 30%),
            linear-gradient(135deg, #0A0F1E 0%, #0E1324 48%, #10182B 100%);
        color: #EEF4FF;
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    [data-testid="stHeader"] { background: rgba(10, 15, 30, .55); backdrop-filter: blur(16px); }
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(20,26,43,.97) 0%, rgba(10,15,30,.98) 100%);
        border-right: 1px solid rgba(238,244,255,.10);
    }

    .block-container { padding-top: 1.25rem; padding-bottom: 3rem; max-width: 1480px; }

    h1, h2, h3 { font-family: 'Space Grotesk', 'Inter', sans-serif; letter-spacing: -.02em; }
    h1 { font-size: clamp(2rem, 3vw, 3.6rem) !important; line-height: 1.02 !important; }
    h2 { margin-top: 1.6rem !important; }

    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(238,244,255,.12);
        border-radius: 28px;
        padding: 28px 30px;
        margin-bottom: 18px;
        background:
            linear-gradient(135deg, rgba(139,92,246,.18), rgba(56,189,248,.08)),
            rgba(20,26,43,.84);
        box-shadow: 0 24px 80px rgba(0,0,0,.28);
    }
    .hero:after {
        content: "";
        position: absolute; inset: -60px -40px auto auto;
        width: 280px; height: 280px;
        background: conic-gradient(from 60deg, rgba(45,212,191,.45), rgba(139,92,246,.28), rgba(251,113,133,.24), rgba(45,212,191,.45));
        filter: blur(26px); opacity: .45; border-radius: 50%;
    }
    .hero-grid { display: grid; grid-template-columns: 1.2fr .8fr; gap: 20px; align-items: end; position: relative; z-index: 1; }
    .eyebrow { color: #2DD4BF; font-size: .76rem; text-transform: uppercase; letter-spacing: .18em; font-weight: 800; margin-bottom: 8px; }
    .hero p { color: #B9C4DF; max-width: 820px; font-size: 1.02rem; line-height: 1.65; }
    .thesis-card {
        border-radius: 22px;
        border: 1px solid rgba(238,244,255,.12);
        background: rgba(10,15,30,.58);
        padding: 18px;
    }
    .thesis-card .label { color: #9AA8C7; font-size: .78rem; text-transform: uppercase; letter-spacing: .15em; font-weight: 700; }
    .thesis-card .value { color: #EEF4FF; font-size: 1rem; line-height: 1.55; margin-top: 8px; }

    .kpi-card {
        border: 1px solid rgba(238,244,255,.12);
        background: linear-gradient(180deg, rgba(25,33,58,.92), rgba(20,26,43,.9));
        border-radius: 22px;
        padding: 18px 18px 15px 18px;
        min-height: 132px;
        box-shadow: 0 18px 50px rgba(0,0,0,.20);
    }
    .kpi-label { color: #9AA8C7; font-size: .76rem; text-transform: uppercase; letter-spacing: .14em; font-weight: 800; }
    .kpi-value { font-family: 'Space Grotesk', 'Inter', sans-serif; font-size: 2.1rem; margin-top: 8px; font-weight: 700; color: #EEF4FF; }
    .kpi-foot { color: #B9C4DF; font-size: .86rem; margin-top: 6px; line-height: 1.45; }

    .note {
        border: 1px solid rgba(45,212,191,.22);
        background: linear-gradient(135deg, rgba(45,212,191,.12), rgba(139,92,246,.08));
        border-radius: 18px;
        padding: 15px 16px;
        margin: 10px 0 18px 0;
        color: #DCE8FF;
        line-height: 1.6;
    }
    .note strong { color: #FFFFFF; }

    .ethical-note {
        border-left: 4px solid #F59E0B;
        background: rgba(245,158,11,.10);
        border-radius: 14px;
        padding: 12px 14px;
        color: #FFEED0;
        margin-bottom: 12px;
        line-height: 1.55;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(25,33,58,.7);
        border: 1px solid rgba(238,244,255,.10);
        border-radius: 999px;
        color: #B9C4DF;
        padding: 10px 16px;
    }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, rgba(139,92,246,.62), rgba(56,189,248,.34)) !important; color: white !important; }

    div[data-testid="stDataFrame"] { border: 1px solid rgba(238,244,255,.10); border-radius: 16px; overflow: hidden; }
    .small-muted { color: #9AA8C7; font-size: .86rem; line-height: 1.5; }
    .footer { margin-top: 28px; color: #9AA8C7; font-size: .85rem; text-align: center; }

    @media (max-width: 900px) { .hero-grid { grid-template-columns: 1fr; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Data loading and preparation ----------
DATA_PATHS = [
    Path("data/clean_dataset_ai_student_impact.csv"),
    Path("clean_dataset_ai_student_impact.csv"),
    Path("modul_3_4_5_final_outputs/clean_dataset_ai_student_impact_modul_4.csv"),
]
LOG_PATHS = [Path("data/data_cleaning_log.csv"), Path("data_cleaning_log.csv")]

NUMERIC_COLUMNS = [
    "Pre_Semester_GPA", "Weekly_GenAI_Hours", "Tool_Diversity", "Traditional_Study_Hours",
    "Perceived_AI_Dependency", "Anxiety_Level_During_Exams", "Post_Semester_GPA", "Skill_Retention_Score",
]
CATEGORICAL_COLUMNS = [
    "Major_Category", "Year_of_Study", "Primary_Use_Case", "Prompt_Engineering_Skill",
    "Institutional_Policy", "Burnout_Risk_Level",
]


def first_existing(paths: Iterable[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def normalize_paid_subscription(series: pd.Series) -> pd.Series:
    mapping = {
        True: True, False: False,
        "True": True, "False": False,
        "true": True, "false": False,
        "1": True, "0": False,
        1: True, 0: False,
        "Yes": True, "No": False,
        "yes": True, "no": False,
    }
    return series.map(mapping).astype("boolean")


@st.cache_data(show_spinner=False)
def load_data(uploaded_file=None) -> pd.DataFrame:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        path = first_existing(DATA_PATHS)
        if path is None:
            raise FileNotFoundError("Dataset tidak ditemukan. Letakkan file di data/clean_dataset_ai_student_impact.csv")
        df = pd.read_csv(path)
    return prepare_data(df)


@st.cache_data(show_spinner=False)
def load_cleaning_log() -> pd.DataFrame:
    path = first_existing(LOG_PATHS)
    if path is None:
        return pd.DataFrame()
    return pd.read_csv(path)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Identifier diperlakukan sebagai teks agar tidak digunakan untuk agregasi statistik.
    if "Student_ID" in df.columns:
        df["Student_ID"] = df["Student_ID"].astype(str).str.strip()

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().replace({"": pd.NA})

    if "Paid_Subscription" in df.columns:
        df["Paid_Subscription"] = normalize_paid_subscription(df["Paid_Subscription"])

    if "Primary_Use_Case" in df.columns:
        df["Primary_Use_Case"] = df["Primary_Use_Case"].fillna("Unknown")

    if {"Post_Semester_GPA", "Pre_Semester_GPA"}.issubset(df.columns) and "GPA_Change" not in df.columns:
        df["GPA_Change"] = df["Post_Semester_GPA"] - df["Pre_Semester_GPA"]

    if "Burnout_Risk_Level" in df.columns:
        df["High_Burnout_Flag"] = (df["Burnout_Risk_Level"] == "High").astype(int)

    if "Weekly_GenAI_Hours" in df.columns:
        bins = [-0.001, 5, 15, np.inf]
        labels = SEGMENT_ORDER
        df["AI_Usage_Segment"] = pd.cut(df["Weekly_GenAI_Hours"], bins=bins, labels=labels).astype("string")

    if "Perceived_AI_Dependency" in df.columns:
        df["Dependency_Band"] = pd.cut(
            df["Perceived_AI_Dependency"],
            bins=[0, 3, 6, 10],
            labels=["Low dependency", "Moderate dependency", "High dependency"],
            include_lowest=True,
        ).astype("string")

    return df


def filter_data(df: pd.DataFrame, majors: list[str], years: list[str], policies: list[str]) -> pd.DataFrame:
    if not majors or not years or not policies:
        return df.iloc[0:0].copy()
    mask = (
        df["Major_Category"].isin(majors)
        & df["Year_of_Study"].isin(years)
        & df["Institutional_Policy"].isin(policies)
    )
    return df.loc[mask].copy()


def fmt_num(value: float, decimals: int = 2) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(value: float, decimals: int = 1) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.{decimals}f}%".replace(".", ",")


def kpi_card(label: str, value: str, foot: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def note(text: str) -> None:
    st.markdown(f"<div class='note'>{text}</div>", unsafe_allow_html=True)


def ethical_note() -> None:
    st.markdown(
        """
        <div class="ethical-note">
        Dashboard ini membaca hubungan sebagai <strong>pola/asosiasi</strong>, bukan bukti sebab-akibat. Variabel burnout dan anxiety digunakan sebagai indikator risiko agregat, bukan diagnosis individual.
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig: go.Figure, height: int = 440) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["ink"], family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=54, b=40),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, title_font=dict(color=COLORS["muted"]), tickfont=dict(color=COLORS["muted"]))
    fig.update_yaxes(gridcolor="rgba(238,244,255,.12)", zeroline=False, title_font=dict(color=COLORS["muted"]), tickfont=dict(color=COLORS["muted"]))
    return fig


def make_gpa_by_major(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("Major_Category", observed=True)[["Pre_Semester_GPA", "Post_Semester_GPA"]].mean().reindex(MAJOR_ORDER).dropna(how="all").reset_index()
    long = g.melt(id_vars="Major_Category", var_name="GPA_Type", value_name="Average_GPA")
    long["GPA_Type"] = long["GPA_Type"].replace({"Pre_Semester_GPA": "Pre GPA", "Post_Semester_GPA": "Post GPA"})
    fig = px.bar(
        long, x="Major_Category", y="Average_GPA", color="GPA_Type", barmode="group",
        color_discrete_sequence=[COLORS["cyan"], COLORS["mint"]],
        labels={"Major_Category": "Bidang studi", "Average_GPA": "Rata-rata GPA", "GPA_Type": "Jenis GPA"},
        title="GPA Pre vs Post per Major Category",
        text_auto=".2f",
    )
    return style_figure(fig, 430)


def make_burnout_by_policy(df: pd.DataFrame) -> go.Figure:
    counts = pd.crosstab(df["Institutional_Policy"], df["Burnout_Risk_Level"], normalize="index") * 100
    counts = counts.reindex(POLICY_ORDER).dropna(how="all")
    for col in BURNOUT_ORDER:
        if col not in counts.columns:
            counts[col] = 0
    counts = counts[BURNOUT_ORDER].reset_index().melt(id_vars="Institutional_Policy", var_name="Burnout", value_name="Percentage")
    fig = px.bar(
        counts, x="Institutional_Policy", y="Percentage", color="Burnout", barmode="stack",
        category_orders={"Burnout": BURNOUT_ORDER, "Institutional_Policy": POLICY_ORDER},
        color_discrete_map={"Low": COLORS["mint"], "Medium": COLORS["amber"], "High": COLORS["coral"]},
        labels={"Institutional_Policy": "Kebijakan institusi", "Percentage": "Persentase mahasiswa", "Burnout": "Risiko burnout"},
        title="Distribusi Burnout Risk Level per Institutional Policy",
    )
    fig.update_traces(hovertemplate="%{x}<br>%{legendgroup}: %{y:.1f}%<extra></extra>")
    return style_figure(fig, 430)


def make_ai_segment_by_year(df: pd.DataFrame) -> go.Figure:
    tab = pd.crosstab(df["Year_of_Study"], df["AI_Usage_Segment"], normalize="index") * 100
    tab = tab.reindex(YEAR_ORDER).dropna(how="all")
    for col in SEGMENT_ORDER:
        if col not in tab.columns:
            tab[col] = 0
    tab = tab[SEGMENT_ORDER].reset_index().melt(id_vars="Year_of_Study", var_name="AI segment", value_name="Percentage")
    fig = px.bar(
        tab, x="Year_of_Study", y="Percentage", color="AI segment", barmode="stack",
        category_orders={"Year_of_Study": YEAR_ORDER, "AI segment": SEGMENT_ORDER},
        color_discrete_map={"Light User": COLORS["mint"], "Moderate User": COLORS["cyan"], "Heavy User": COLORS["coral"]},
        labels={"Year_of_Study": "Tahun studi", "Percentage": "Persentase mahasiswa"},
        title="Komposisi penggunaan AI per Year of Study",
    )
    return style_figure(fig, 430)


def make_hours_vs_gpa(df: pd.DataFrame) -> go.Figure:
    sample = df.sample(min(len(df), 6000), random_state=42) if len(df) else df
    fig = px.scatter(
        sample, x="Weekly_GenAI_Hours", y="Post_Semester_GPA", color="AI_Usage_Segment",
        category_orders={"AI_Usage_Segment": SEGMENT_ORDER},
        color_discrete_map={"Light User": COLORS["mint"], "Moderate User": COLORS["cyan"], "Heavy User": COLORS["coral"]},
        labels={"Weekly_GenAI_Hours": "Jam AI/minggu", "Post_Semester_GPA": "Post Semester GPA", "AI_Usage_Segment": "Segmentasi AI"},
        title="Weekly GenAI Hours vs Post Semester GPA",
        opacity=.58,
        hover_data=["Major_Category", "Year_of_Study", "Institutional_Policy"],
    )
    return style_figure(fig, 450)


def make_hours_vs_skill(df: pd.DataFrame) -> go.Figure:
    sample = df.sample(min(len(df), 6000), random_state=7) if len(df) else df
    fig = px.scatter(
        sample, x="Weekly_GenAI_Hours", y="Skill_Retention_Score", color="AI_Usage_Segment",
        category_orders={"AI_Usage_Segment": SEGMENT_ORDER},
        color_discrete_map={"Light User": COLORS["mint"], "Moderate User": COLORS["cyan"], "Heavy User": COLORS["coral"]},
        labels={"Weekly_GenAI_Hours": "Jam AI/minggu", "Skill_Retention_Score": "Skill Retention Score", "AI_Usage_Segment": "Segmentasi AI"},
        title="Weekly GenAI Hours vs Skill Retention Score",
        opacity=.58,
        hover_data=["Major_Category", "Year_of_Study", "Primary_Use_Case"],
    )
    return style_figure(fig, 450)


def make_dependency_box(df: pd.DataFrame) -> go.Figure:
    fig = px.box(
        df, x="Burnout_Risk_Level", y="Perceived_AI_Dependency", color="Burnout_Risk_Level",
        category_orders={"Burnout_Risk_Level": BURNOUT_ORDER},
        color_discrete_map={"Low": COLORS["mint"], "Medium": COLORS["amber"], "High": COLORS["coral"]},
        labels={"Burnout_Risk_Level": "Risiko burnout", "Perceived_AI_Dependency": "Perceived AI dependency"},
        title="Perceived AI Dependency vs Burnout Risk Level",
    )
    fig.update_layout(showlegend=False)
    return style_figure(fig, 430)


def make_risk_heatmap(df: pd.DataFrame) -> go.Figure:
    tab = df.pivot_table(
        index="Dependency_Band", columns="AI_Usage_Segment", values="High_Burnout_Flag",
        aggfunc="mean", observed=True,
    ) * 100
    tab = tab.reindex(["Low dependency", "Moderate dependency", "High dependency"])
    for segment in SEGMENT_ORDER:
        if segment not in tab.columns:
            tab[segment] = np.nan
    tab = tab[SEGMENT_ORDER]
    fig = px.imshow(
        tab,
        text_auto=".1f",
        color_continuous_scale="RdPu",
        labels=dict(x="Segmentasi penggunaan AI", y="Tingkat dependency", color="High burnout (%)"),
        title="Profil risiko mahasiswa berdasarkan AI dependency dan burnout risk",
        aspect="auto",
    )
    return style_figure(fig, 430)


def make_segment_summary(df: pd.DataFrame) -> go.Figure:
    seg = df.groupby("AI_Usage_Segment", observed=True).agg(
        Student_Count=("Student_ID", "count"),
        Avg_Post_GPA=("Post_Semester_GPA", "mean"),
        Avg_Skill=("Skill_Retention_Score", "mean"),
        High_Burnout_Rate=("High_Burnout_Flag", "mean"),
    ).reindex(SEGMENT_ORDER).reset_index()
    seg["High_Burnout_Rate"] *= 100
    fig = go.Figure()
    fig.add_bar(x=seg["AI_Usage_Segment"], y=seg["Avg_Post_GPA"], name="Avg Post GPA", marker_color=COLORS["cyan"], yaxis="y")
    fig.add_scatter(x=seg["AI_Usage_Segment"], y=seg["High_Burnout_Rate"], name="High Burnout (%)", mode="lines+markers", marker=dict(size=10), line=dict(width=3, color=COLORS["coral"]), yaxis="y2")
    fig.update_layout(
        title="Perbandingan GPA dan High Burnout Risk per AI Usage Segment",
        yaxis=dict(title="Avg Post GPA", range=[0, 4.2]),
        yaxis2=dict(title="High Burnout (%)", overlaying="y", side="right", range=[0, max(100, seg["High_Burnout_Rate"].max() * 1.15)]),
    )
    return style_figure(fig, 440)


def validation_table(df: pd.DataFrame, filtered_df: pd.DataFrame) -> pd.DataFrame:
    invalid_year = int((~df["Year_of_Study"].isin(YEAR_ORDER)).sum()) if "Year_of_Study" in df else None
    invalid_pre_gpa = int(((df["Pre_Semester_GPA"] < 0) | (df["Pre_Semester_GPA"] > 4)).sum()) if "Pre_Semester_GPA" in df else None
    invalid_post_gpa = int(((df["Post_Semester_GPA"] < 0) | (df["Post_Semester_GPA"] > 4)).sum()) if "Post_Semester_GPA" in df else None
    invalid_tool = int(((df["Tool_Diversity"] < 1) | (df["Tool_Diversity"] > 5)).sum()) if "Tool_Diversity" in df else None
    duplicate_id = int(df["Student_ID"].duplicated().sum()) if "Student_ID" in df else None
    missing_total = int(df.isna().sum().sum())

    rows = [
        ("Missing values", missing_total, "Lulus" if missing_total == 0 else "Perlu cek", "Clean dataset seharusnya tidak memiliki missing value kritis."),
        ("Year_of_Study invalid", invalid_year, "Lulus" if invalid_year == 0 else "Perlu cleaning", "Kategori valid: Freshman, Sophomore, Junior, Senior, Graduate."),
        ("Pre_Semester_GPA di luar 0–4", invalid_pre_gpa, "Lulus" if invalid_pre_gpa == 0 else "Perlu cleaning", "GPA harus berada pada rentang 0,00–4,00."),
        ("Post_Semester_GPA di luar 0–4", invalid_post_gpa, "Lulus" if invalid_post_gpa == 0 else "Perlu cleaning", "GPA akhir harus berada pada rentang 0,00–4,00."),
        ("Tool_Diversity di luar 1–5", invalid_tool, "Lulus" if invalid_tool == 0 else "Perlu cleaning", "Nilai di atas 5 dianggap outlier tidak logis."),
        ("Duplikat Student_ID", duplicate_id, "Lulus" if duplicate_id == 0 else "Perlu cek", "Satu Student_ID hanya boleh mewakili satu mahasiswa."),
        ("Filter ekstrem / kosong", len(filtered_df), "Tertangani", "Dashboard menampilkan pesan khusus jika kombinasi filter tidak menghasilkan data."),
    ]
    return pd.DataFrame(rows, columns=["Pemeriksaan", "Jumlah / Hasil", "Status", "Catatan"])


# ---------- Sidebar ----------
st.sidebar.markdown("### Ruang Analisis")
st.sidebar.caption("Gunakan filter untuk melihat perubahan KPI dan risiko pada kelompok mahasiswa tertentu.")
uploaded = st.sidebar.file_uploader("Opsional: unggah CSV clean dataset", type=["csv"], help="Biarkan kosong untuk menggunakan dataset bawaan di folder data/.")

try:
    df_all = load_data(uploaded)
except Exception as exc:
    st.error(f"Data belum dapat dimuat: {exc}")
    st.stop()

majors_available = [x for x in MAJOR_ORDER if x in df_all["Major_Category"].dropna().unique().tolist()]
years_available = [x for x in YEAR_ORDER if x in df_all["Year_of_Study"].dropna().unique().tolist()]
policies_available = [x for x in POLICY_ORDER if x in df_all["Institutional_Policy"].dropna().unique().tolist()]

selected_majors = st.sidebar.multiselect("Major Category", majors_available, default=majors_available)
selected_years = st.sidebar.multiselect("Year of Study", years_available, default=years_available)
selected_policies = st.sidebar.multiselect("Institutional Policy", policies_available, default=policies_available)

st.sidebar.divider()
st.sidebar.markdown("### Ambang Segmentasi AI")
st.sidebar.markdown("<span class='small-muted'>Light ≤ 5 jam/minggu · Moderate > 5–15 jam/minggu · Heavy > 15 jam/minggu</span>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.download_button(
    "Download clean dataset",
    df_all.to_csv(index=False).encode("utf-8"),
    file_name="clean_dataset_ai_student_impact.csv",
    mime="text/csv",
)

filtered_df = filter_data(df_all, selected_majors, selected_years, selected_policies)

# ---------- Hero ----------
st.markdown(
    """
    <section class="hero">
      <div class="hero-grid">
        <div>
          <div class="eyebrow">Modul 6 · BI dashboard</div>
          <h1>AI Student Impact Decision Dashboard</h1>
          <p>Dashboard ini merangkum hubungan penggunaan AI generatif dengan performa akademik, retensi keterampilan, dan risiko burnout mahasiswa. Fokusnya bukan melarang AI, melainkan membantu stakeholder melihat segmen risiko dan menentukan kebijakan penggunaan AI yang lebih bertanggung jawab.</p>
        </div>
        <div class="thesis-card">
          <div class="label">Prinsip interpretasi</div>
          <div class="value">Hasil dashboard dibaca pada level agregat. Pola yang muncul menunjukkan indikasi dan asosiasi, bukan diagnosis individu atau kesimpulan sebab-akibat.</div>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.warning("Kombinasi filter tidak menghasilkan data. Ini adalah kondisi filter ekstrem yang sudah ditangani: dashboard tidak memaksakan visualisasi kosong dan meminta pengguna memperluas pilihan filter.")
    st.dataframe(validation_table(df_all, filtered_df), use_container_width=True, hide_index=True)
    st.stop()

# ---------- KPI ----------
student_count = len(filtered_df)
avg_post_gpa = filtered_df["Post_Semester_GPA"].mean()
avg_skill = filtered_df["Skill_Retention_Score"].mean()
high_burnout_rate = filtered_df["High_Burnout_Flag"].mean() * 100
avg_ai_hours = filtered_df["Weekly_GenAI_Hours"].mean()

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Mahasiswa terfilter", f"{student_count:,.0f}".replace(",", "."), "Jumlah record setelah filter aktif.")
with k2:
    kpi_card("Avg Post GPA", fmt_num(avg_post_gpa, 2), "Rata-rata GPA akhir semester.")
with k3:
    kpi_card("Avg Skill Retention", fmt_num(avg_skill, 1), "Rata-rata skor retensi keterampilan.")
with k4:
    kpi_card("High Burnout Risk", fmt_pct(high_burnout_rate, 1), "Persentase mahasiswa kategori burnout tinggi.")

ethical_note()

# ---------- Tabs ----------
tabs = st.tabs(["Executive overview", "Akademik & retensi", "Burnout & kebijakan", "Segmentasi risiko", "Kualitas data & uji"])

with tabs[0]:
    st.subheader("Ringkasan kondisi utama")
    col_a, col_b = st.columns([1.1, .9])
    with col_a:
        st.plotly_chart(make_gpa_by_major(filtered_df), use_container_width=True)
        note("<strong>Insight:</strong> Perbandingan Pre GPA dan Post GPA membantu melihat apakah performa akademik akhir cenderung lebih tinggi atau lebih rendah di setiap bidang studi. Grafik ini menjadi dasar untuk melihat dampak akademik secara agregat, bukan untuk menilai individu.")
    with col_b:
        st.plotly_chart(make_segment_summary(filtered_df), use_container_width=True)
        dominant_segment = filtered_df["AI_Usage_Segment"].value_counts().idxmax()
        note(f"<strong>Insight:</strong> Segmen terbesar pada filter saat ini adalah <strong>{dominant_segment}</strong>. Perbandingan segmentasi membantu stakeholder memahami apakah penggunaan AI yang lebih intensif disertai perubahan pada GPA dan burnout risk.")

    st.markdown("### Ringkasan segmentasi")
    seg_summary = filtered_df.groupby("AI_Usage_Segment", observed=True).agg(
        Student_Count=("Student_ID", "count"),
        Avg_Weekly_GenAI_Hours=("Weekly_GenAI_Hours", "mean"),
        Avg_Post_GPA=("Post_Semester_GPA", "mean"),
        Avg_Skill_Retention=("Skill_Retention_Score", "mean"),
        High_Burnout_Rate=("High_Burnout_Flag", "mean"),
    ).reindex(SEGMENT_ORDER).reset_index()
    seg_summary["High_Burnout_Rate"] = seg_summary["High_Burnout_Rate"] * 100
    st.dataframe(seg_summary, use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Dampak akademik dan retensi keterampilan")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_hours_vs_gpa(filtered_df), use_container_width=True)
        corr_gpa = filtered_df[["Weekly_GenAI_Hours", "Post_Semester_GPA"]].corr().iloc[0, 1]
        note(f"<strong>Interpretasi:</strong> Korelasi jam penggunaan AI dengan Post GPA pada data terfilter adalah <strong>{corr_gpa:.3f}</strong>. Nilai ini perlu dibaca sebagai asosiasi statistik awal, bukan bukti bahwa AI langsung menaikkan atau menurunkan GPA.")
    with col2:
        st.plotly_chart(make_hours_vs_skill(filtered_df), use_container_width=True)
        corr_skill = filtered_df[["Weekly_GenAI_Hours", "Skill_Retention_Score"]].corr().iloc[0, 1]
        note(f"<strong>Interpretasi:</strong> Korelasi jam penggunaan AI dengan Skill Retention Score adalah <strong>{corr_skill:.3f}</strong>. Jika arahnya negatif, hal ini menjadi sinyal perlunya desain pembelajaran yang menjaga retensi, misalnya refleksi proses dan asesmen berbasis pemahaman.")

    st.plotly_chart(make_dependency_box(filtered_df), use_container_width=True)
    note("<strong>Insight:</strong> Boxplot dependency membantu membaca apakah mahasiswa dengan risiko burnout lebih tinggi juga cenderung memiliki persepsi ketergantungan AI yang lebih tinggi. Temuan ini relevan untuk edukasi penggunaan AI sehat, bukan untuk memberi stigma pada kelompok tertentu.")

with tabs[2]:
    st.subheader("Burnout risk dan kebijakan institusi")
    col1, col2 = st.columns([1.1, .9])
    with col1:
        st.plotly_chart(make_burnout_by_policy(filtered_df), use_container_width=True)
        policy_rate = filtered_df.groupby("Institutional_Policy", observed=True)["High_Burnout_Flag"].mean().mul(100).sort_values(ascending=False)
        if not policy_rate.empty:
            top_policy = policy_rate.index[0]
            top_rate = policy_rate.iloc[0]
            note(f"<strong>Insight:</strong> Pada filter saat ini, kebijakan dengan proporsi High Burnout Risk tertinggi adalah <strong>{top_policy}</strong> sebesar <strong>{top_rate:.1f}%</strong>. Informasi ini membantu membandingkan pendekatan kebijakan, tetapi tetap perlu dibaca bersama faktor lain seperti major, tahun studi, dan intensitas penggunaan AI.")
    with col2:
        risk_by_major_year = filtered_df.pivot_table(
            index="Major_Category", columns="Year_of_Study", values="High_Burnout_Flag", aggfunc="mean", observed=True
        ).reindex(MAJOR_ORDER)[[y for y in YEAR_ORDER if y in filtered_df["Year_of_Study"].unique()]] * 100
        fig = px.imshow(
            risk_by_major_year,
            text_auto=".1f",
            color_continuous_scale="RdPu",
            labels=dict(x="Tahun studi", y="Bidang studi", color="High burnout (%)"),
            title="High Burnout Risk per Major dan Year of Study",
            aspect="auto",
        )
        st.plotly_chart(style_figure(fig, 430), use_container_width=True)
        note("<strong>Insight:</strong> Heatmap ini membantu menemukan kombinasi bidang studi dan tahun studi yang memerlukan perhatian lebih. Prioritas intervensi sebaiknya berbasis risiko agregat, bukan pelabelan individu.")

with tabs[3]:
    st.subheader("Segmentasi penggunaan AI dan profil risiko")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_ai_segment_by_year(filtered_df), use_container_width=True)
        note("<strong>Insight:</strong> Komposisi AI per tahun studi membantu melihat kelompok akademik mana yang lebih banyak berada pada Light, Moderate, atau Heavy User. Visualisasi ini mendukung desain literasi AI yang lebih spesifik per jenjang studi.")
    with col2:
        st.plotly_chart(make_risk_heatmap(filtered_df), use_container_width=True)
        note("<strong>Insight:</strong> Profil risiko mempertemukan dua indikator penting: intensitas penggunaan AI dan tingkat dependency. Area dengan High Burnout Rate tinggi menjadi prioritas edukasi, pendampingan, dan pengaturan beban belajar.")

    st.markdown("### Kelompok prioritas intervensi")
    priority = filtered_df.groupby(["AI_Usage_Segment", "Dependency_Band", "Burnout_Risk_Level"], observed=True).agg(
        Student_Count=("Student_ID", "count"),
        Avg_Post_GPA=("Post_Semester_GPA", "mean"),
        Avg_Skill_Retention=("Skill_Retention_Score", "mean"),
        Avg_Anxiety=("Anxiety_Level_During_Exams", "mean"),
    ).reset_index().sort_values(["Burnout_Risk_Level", "Student_Count"], ascending=[True, False])
    priority_high = priority[priority["Burnout_Risk_Level"] == "High"].sort_values("Student_Count", ascending=False).head(12)
    st.dataframe(priority_high, use_container_width=True, hide_index=True)
    note("<strong>Catatan kebijakan:</strong> Tabel prioritas tidak digunakan untuk menyalahkan mahasiswa, melainkan untuk menentukan kelompok yang paling membutuhkan panduan penggunaan AI, dukungan akademik, dan pencegahan burnout.")

with tabs[4]:
    st.subheader("Kualitas data, validasi, dan uji filter ekstrem")
    st.markdown("Dashboard menggunakan clean dataset hasil Modul 4. Halaman ini menunjukkan bahwa data sudah diuji terhadap nilai tidak valid dan dashboard tetap stabil saat filter menghasilkan data sangat sedikit atau kosong.")

    val = validation_table(df_all, filtered_df)
    st.dataframe(val, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Cleaning log")
        cleaning_log = load_cleaning_log()
        if cleaning_log.empty:
            st.info("Cleaning log tidak ditemukan di folder data. Jika tersedia, letakkan sebagai data/data_cleaning_log.csv.")
        else:
            st.dataframe(cleaning_log, use_container_width=True, hide_index=True)
    with c2:
        st.markdown("### Data terfilter")
        st.dataframe(filtered_df.head(200), use_container_width=True, hide_index=True)
        st.download_button(
            "Download data terfilter",
            filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="filtered_ai_student_impact.csv",
            mime="text/csv",
        )

st.markdown(
    """
    <div class="footer">© 2026 · AI Student Impact BI Dashboard · Modul 6 Skema Sertifikasi Data Analyst</div>
    """,
    unsafe_allow_html=True,
)
