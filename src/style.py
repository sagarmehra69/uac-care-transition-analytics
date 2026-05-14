# style.py


import streamlit as st

def load_css():
  st.markdown("""
<style>

/*(GLOBAL STYLES)*/

html, body, [data-testid="stAppViewContainer"]{
    background:#0E1117;
    color:#FAFAFA;
    font-family:'Inter', Arial, sans-serif;
}

/*(SIDEBAR)*/

[data-testid="stSidebar"]{
    background:#13161F;
    border-right:1px solid #2D3150;
}

/*(KPI CARDS)*/

.kpi-card{
    background:linear-gradient(135deg,#1A1D2E 0%,#252842 100%);
    border:1px solid #2D3150;
    border-radius:14px;
    padding:22px 18px;
    text-align:center;
    margin-bottom:12px;
    margin-top:12px;
    transition:transform 0.3s ease, box-shadow 0.3s ease;
}

.kpi-card:nth-child(1){
    background:linear-gradient(135deg,#1A2E4A 0%,#2D4A6B 100%);
    border-left:4px solid #00D4FF;
}

.kpi-card:nth-child(2){
    background:linear-gradient(135deg,#2E1A3F 0%,#4A2D5E 100%);
    border-left:4px solid #B197FC;
}

.kpi-card:nth-child(3){
    background:linear-gradient(135deg,#2E3A1A 0%,#4A5E2D 100%);
    border-left:4px solid #6BCB77;
}

.kpi-card:nth-child(4){
    background:linear-gradient(135deg,#3F2E1A 0%,#5E4A2D 100%);
    border-left:4px solid #FFB347;
}

.kpi-card:nth-child(5){
    background:linear-gradient(135deg,#3F1A2E 0%,#5E2D4A 100%);
    border-left:4px solid #FF6B9D;
}

.kpi-card:hover{
    transform:translateY(-5px);
    box-shadow:0 10px 20px rgba(0,212,255,0.20);
}

.kpi-label{
    font-size:.78rem;
    color:#8A8FA8;
    text-transform:uppercase;
    letter-spacing:.08em;
}

.kpi-value{
    font-size:2rem;
    font-weight:700;
    margin:6px 0;
    color:#FFFFFF;
}

.kpi-sub{
    font-size:.75rem;
    color:#8A8FA8;
}

/*(SECTION HEADERS)*/
   
.section-header{
    font-size:2.0rem;
    font-weight:900;
    color:#FFFFFF;
    border-left:4px solid #00D4FF;
    padding-left:12px;
    margin:24px 0 16px;
    animation:fadeIn 1s ease-in;
}

/*(SUBHEADERS)*/

[data-testid="stHeading"] h2{
    font-size:2.2rem !important;
    font-weight:900 !important;
}

[data-testid="stHeading"] h3{
    font-size:2.0rem !important;
    font-weight:900 !important;
}

[data-testid="stHeading"] h4{
    font-size:1.8rem !important;
    font-weight:900 !important;
}

.stSubheader{
    font-weight:900 !important;
    font-size:1.8rem !important;
}

/*(INSIGHT CARDS)*/

.insight-card{
    background:#1A1D2E;
    border:1px solid #2D3150;
    border-radius:12px;
    padding:14px 16px;
    margin-bottom:10px;
    font-size:.92rem;
    line-height:1.6;
    animation:fadeIn 1.2s ease-in;
}

/*(RECOMMENDATION CARDS)*/

.rec-card{
    background:#13161F;
    border-left:4px solid #00D4FF;
    border-radius:10px;
    padding:12px 16px;
    margin-bottom:10px;
    font-size:.88rem;
    animation:fadeIn 1.5s ease-in;
}

/*(TABS)*/

button[data-baseweb="tab"]{
    padding:16px 30px;
    border-radius:14px;
    transition:all 0.3s ease;
    background:transparent;
}

/* TAB TEXT */
button[data-baseweb="tab"] p{
    font-size:20px !important;
    font-weight:700 !important;
    color:#FAFAFA !important;
}

/* HOVER */
button[data-baseweb="tab"]:hover{
    color:#00D4FF;
    transform:translateY(-2px);
}

/* ACTIVE TAB */
button[data-baseweb="tab"][aria-selected="true"]{
    background:linear-gradient(135deg,#00D4FF 0%,#0099CC 100%);
    color:#0E1117;
    box-shadow:0 4px 15px rgba(0,212,255,0.25);
}

/*(BUTTONS)*/

.stButton>button{
    background:linear-gradient(135deg,#00D4FF 0%,#0099CC 100%);
    color:#0E1117;
    border:none;
    border-radius:10px;
    padding:10px 22px;
    font-weight:700;
    cursor:pointer;
    transition:all 0.3s ease;
    margin-bottom:24px;
    margin-top:12px;
}

.stButton>button:hover{
    background:linear-gradient(135deg,#0099CC 0%,#00D4FF 100%);
    transform:scale(1.05);
}

/*(INPUTS)*/

.stSelectbox,
.stDateInput,
.stSlider{
    animation:fadeIn 1s ease-in;
}

/*(HERO IMAGE)*/

.hero-image{
    border-radius:14px;
    overflow:hidden;
    margin-bottom:20px;
}

.hero-image img{
    max-height:300px;
    object-fit:cover;
    object-position:center top;
    border-radius:14px;
}

/*(LOGO)*/

.logo-container{
    text-align:center;
    margin-bottom:20px;
}

/*(ANIMATIONS)*/

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(20px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

/*(METRICS & SPACING)*/

.stMetric{
    margin-bottom:8px;
    margin-top:8px;
}

.stMetricDelta{
    margin-top:4px;
}

</style>
""", unsafe_allow_html=True)
  

