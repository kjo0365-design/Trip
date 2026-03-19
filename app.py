import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import base64
import random
from io import BytesIO
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌸 도쿄 벚꽃 여행 2026",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background: linear-gradient(160deg,#fff5f7 0%,#fdf0f5 40%,#f8f0ff 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

/* petal rain */
.petal-wrap { position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:0;overflow:hidden; }
.petal { position:absolute;top:-40px;opacity:0;animation:petalFall linear infinite; }
@keyframes petalFall {
  0%   { transform:translateY(0) rotate(0deg); opacity:0; }
  10%  { opacity:0.55; }
  90%  { opacity:0.25; }
  100% { transform:translateY(110vh) rotate(720deg) translateX(60px); opacity:0; }
}

/* hero */
.hero { text-align:center; padding:2rem 1rem 1rem; }
.hero-title {
  font-family:'Noto Serif KR',serif; font-size:2.6rem; font-weight:600;
  background:linear-gradient(135deg,#d4608a,#a855c8,#d4608a);
  background-size:200% auto; -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; animation:shimmer 4s linear infinite;
}
@keyframes shimmer { to { background-position:200% center; } }
.hero-sub  { font-size:0.95rem; color:#b07090; letter-spacing:0.08em; margin-top:4px; }
.hero-date { font-size:0.82rem; color:#c890b0; letter-spacing:0.12em; }

/* sakura banner */
.sakura-banner {
  background:linear-gradient(135deg,#ffe4ef,#f8d7fa);
  border:1.5px solid #f0b8d8; border-radius:16px;
  padding:0.8rem 1.2rem; text-align:center;
  margin:0.5rem 0 1.2rem; font-size:0.88rem; color:#9a3060;
  animation:pulse 3s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { box-shadow:0 0 0 0 rgba(212,96,138,.15); }
  50%      { box-shadow:0 0 0 8px rgba(212,96,138,0); }
}

/* flight bar */
.flight-row { display:flex; gap:10px; margin-bottom:1.2rem; }
.flight-card {
  flex:1; background:white; border:1px solid #f0d0e8; border-radius:14px;
  padding:0.9rem 1rem; position:relative; overflow:hidden;
  transition:transform .2s,box-shadow .2s;
}
.flight-card:hover { transform:translateY(-3px); box-shadow:0 8px 24px rgba(212,96,138,.15); }
.flight-card::before { content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#f0a0c8,#c890e8); }
.fc-label { font-size:0.7rem; color:#c890b0; letter-spacing:.1em; margin-bottom:3px; }
.fc-route { font-size:1rem; font-weight:500; color:#5a2040; }
.fc-time  { font-size:0.78rem; color:#9a7090; margin-top:2px; }

/* pink divider */
.pink-div { height:1px; background:linear-gradient(90deg,transparent,#f0c0d8,transparent); margin:1.2rem 0; border:none; }

/* section label */
.sec-label { font-family:'Noto Serif KR',serif; font-size:1rem; color:#9a3060; text-align:center; margin-bottom:0.8rem; }

/* day header */
.day-hdr {
  display:flex; align-items:center; gap:12px; padding:0.9rem 1.2rem;
  border-radius:14px; margin-bottom:1rem; background:white; border:1px solid #f0d0e8;
}
.day-hdr-emoji { font-size:1.8rem; }
.day-hdr-title { font-family:'Noto Serif KR',serif; font-size:1.05rem; font-weight:600; }
.day-hdr-sub   { font-size:0.78rem; color:#b07090; margin-top:2px; }

/* timeline */
.timeline { position:relative; padding-left:22px; }
.timeline::before {
  content:''; position:absolute; left:6px; top:6px; bottom:6px; width:1.5px;
  background:linear-gradient(180deg,#f0a0c8,#c890e8,#90b0e8); border-radius:2px;
}
.ev { position:relative; margin-bottom:12px; }
.ev-dot { position:absolute; left:-19px; top:10px; width:10px; height:10px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 2px rgba(212,96,138,.25); }
.ev-card { background:white; border:1px solid #f0d8e8; border-radius:12px; padding:11px 14px; transition:transform .2s,box-shadow .2s; }
.ev-card:hover { transform:translateX(4px); box-shadow:0 4px 18px rgba(212,96,138,.12); }
.ev-time  { font-size:0.68rem; color:#c8a0b8; letter-spacing:.08em; margin-bottom:2px; }
.ev-title { font-size:0.92rem; font-weight:500; color:#5a2040; }
.ev-desc  { font-size:0.8rem; color:#907080; margin-top:3px; line-height:1.5; }
.ev-tip   { margin-top:5px;padding:5px 9px;background:#f0f5ff;border-radius:7px;font-size:0.74rem;color:#506090;line-height:1.5; }
.ev-pink  { margin-top:5px;padding:5px 9px;background:#fff0f5;border-radius:7px;font-size:0.74rem;color:#a04060;line-height:1.5; }
.ev-teal  { margin-top:5px;padding:5px 9px;background:#f0faf8;border-radius:7px;font-size:0.74rem;color:#2a6058;line-height:1.5; }
.ev-night { margin-top:5px;padding:5px 9px;background:#f5f0ff;border-radius:7px;font-size:0.74rem;color:#6040a0;line-height:1.5; }
.done-badge { display:inline-block;font-size:0.63rem;padding:2px 7px;border-radius:20px;margin-left:6px;background:#e8f8f0;color:#2a7050;font-weight:500; }

/* photo grid */
.photo-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin:8px 0; }
.photo-item { border-radius:9px; overflow:hidden; aspect-ratio:1; background:#f8f0f5; }
.photo-item img { width:100%; height:100%; object-fit:cover; }

/* map label */
.map-lbl { font-size:0.76rem; color:#c890b0; text-align:center; margin-bottom:5px; letter-spacing:.08em; }

/* vibe card */
.vibe-card { margin-top:0.9rem; border-radius:14px; padding:0.9rem 1.1rem; }
.vibe-label { font-size:0.72rem; font-weight:500; margin-bottom:5px; letter-spacing:.08em; }
.vibe-text  { font-size:0.8rem; color:#7a5060; line-height:1.6; }

/* Streamlit button override */
div[data-testid="stButton"] > button {
  background:white; border:1.5px solid #f0c8dc; color:#9a5080;
  border-radius:50px; font-family:'Noto Sans KR',sans-serif;
  font-size:0.82rem; padding:6px 0; transition:all 0.2s; width:100%;
}
div[data-testid="stButton"] > button:hover {
  background:linear-gradient(135deg,#f0a8c8,#d890e0); color:white;
  border-color:transparent; transform:translateY(-2px); box-shadow:0 4px 14px rgba(212,96,138,.3);
}

/* footer */
.footer { text-align:center; padding:1.5rem 1rem; font-size:0.78rem; color:#c890b0; letter-spacing:.06em; }
</style>
""", unsafe_allow_html=True)

# ── Petal rain ────────────────────────────────────────────────────────────────
petals_html = '<div class="petal-wrap">'
for _ in range(20):
    left     = random.randint(0, 98)
    delay    = random.uniform(0, 12)
    duration = random.uniform(7, 15)
    size     = random.randint(13, 21)
    icon     = random.choice(["🌸","🌸","🌸","🌼","🌺"])
    petals_html += (
        f'<span class="petal" style="left:{left}%;font-size:{size}px;'
        f'animation-delay:{delay:.1f}s;animation-duration:{duration:.1f}s;">{icon}</span>'
    )
petals_html += '</div>'
st.markdown(petals_html, unsafe_allow_html=True)

# ── Default schedule data ─────────────────────────────────────────────────────
DEFAULT_DAYS = [
    {
        "label":"Day 1\n3/27 금","emoji":"🛬","color":"#e8849a",
        "title":"Day 1 · 3/27 (금) — 상봉의 기쁨",
        "subtitle":"나리타 도착 → 아키하바라 → 우에노 → 니혼바시 라이트업",
        "vibe":"나리타에서 만나는 순간부터 설레는 첫날 🌸 우에노 공원의 벚꽃 아래 첫 사진도 꼭 남겨요!",
        "events":[
            {"time":"11:50","icon":"✈️","title":"나리타 공항 도착","desc":"입국 심사 + 수하물 수취 후 스카이라이너 탑승","tip":"💡 스카이라이너 닛포리역 하차 → JR 야마노테선 아키하바라 환승 (약 1시간 15분)","done":False},
            {"time":"14:00","icon":"👩‍❤️‍👨","title":"아키하바라 — 수퍼호텔 체크인","desc":"미리 와 있던 남자친구와 상봉! 짐 맡기고 가볍게 출발 🎉","pink":"🏨 숙소: 수퍼호텔 아키하바라 (3/27~31)","done":False},
            {"time":"15:00","icon":"🌸","title":"우에노 공원 산책","desc":"해 질 녘 벚꽃 감상 · 아메요코 상점가 구경","pink":"🍺 야키토리 꼬치 + 생맥주로 첫날 건배!","done":False},
            {"time":"18:30","icon":"✨","title":"니혼바시 벚꽃 라이트업 — Sakura Fes","desc":"에도 벚꽃 거리 핑크빛 조명 & 팝업 스토어","night":"아키하바라에서 전철 5~10분 · 첫날 야경 산책 최적!","done":False},
        ],
        "map_center":[35.6982,139.7731],
        "markers":[
            {"lat":35.6982,"lon":139.7731,"name":"수퍼호텔 아키하바라 (숙소)","color":"red"},
            {"lat":35.7141,"lon":139.7740,"name":"우에노 공원 🌸","color":"pink"},
            {"lat":35.6813,"lon":139.7713,"name":"니혼바시 벚꽃 라이트업 ✨","color":"purple"},
        ],
    },
    {
        "label":"Day 2\n3/28 토","emoji":"💍","color":"#c47bb8",
        "title":"Day 2 · 3/28 (토) — 커플링 & 시부야",
        "subtitle":"하라주쿠 nane tokyo → 오모테산도 쇼핑 → 시부야 벚꽃 축제",
        "vibe":"반지 만드는 3시간이 평생 기억에 남을 거예요 💍 손가락에 반지를 끼는 순간을 잊지 말아요!",
        "events":[
            {"time":"10:15","icon":"🚃","title":"아키하바라 → 하라주쿠 이동","desc":"JR 야마노테선 · 환승 없이 약 30분","tip":"💡 아이폰이면 지갑 앱 Suica로 바로 탑승!","done":False},
            {"time":"11:00–14:00","icon":"💍","title":"nane tokyo 캣스트리트점 — 커플링 제작","desc":"세상에 하나뿐인 반지 만들기 · 3시간 소요 · 평점 5.0 ⭐","pink":"⚠️ 사전 예약 필수! 인스타 DM 또는 공식 홈페이지로 미리 예약","done":False},
            {"time":"14:00","icon":"🍽️","title":"늦은 점심","desc":"돈카츠 마이센 아오야마 본점 OR 루크스 랍스터 하라주쿠점 추천","done":False},
            {"time":"15:30","icon":"🛍️","title":"오모테산도 & 캣스트리트 쇼핑","desc":"편집샵 · 빈티지샵 · 반지 끼고 산책하며 시부야 방향으로","done":False},
            {"time":"18:30","icon":"✨","title":"시부야 벚꽃 축제 — 사쿠라가오카초","desc":"핑크 초롱불 라이트업 · 벚꽃 언덕 골목 감성","night":"🌆 스크램블 교차로 야경 → 파르코 지하 카오스 키친 저녁","done":False},
        ],
        "map_center":[35.6653,139.7090],
        "markers":[
            {"lat":35.6667,"lon":139.7063,"name":"💍 nane tokyo 캣스트리트점","color":"purple"},
            {"lat":35.6653,"lon":139.7127,"name":"오모테산도 힐즈 🛍️","color":"blue"},
            {"lat":35.6566,"lon":139.7024,"name":"시부야 벚꽃 축제 ✨","color":"pink"},
        ],
    },
    {
        "label":"Day 3\n3/29 일","emoji":"🌷","color":"#3d9b8c",
        "title":"Day 3 · 3/29 (일) — 꽃의 하루",
        "subtitle":"나카메구로 벚꽃 축제 → 요코하마 가든 네클리스",
        "vibe":"나카메구로 강가에서 샴페인 한 잔 🥂 요코하마 바다 뷰는 도쿄와 전혀 다른 낭만이 있어요!",
        "events":[
            {"time":"10:30–13:30","icon":"🌸","title":"나카메구로 벚꽃 축제","desc":"메구로강 벚꽃 터널 · 10:00~17:00 · 야타이 포장마차 운영","teal":"🥂 샴페인 & 딸기 탕후루 먹으며 강변 산책 · 스타벅스 리저브 인생샷!","done":False},
            {"time":"14:00","icon":"🚃","title":"나카메구로 → 요코하마 이동","desc":"도큐 도요코선 특급 · 환승 없이 35~40분","tip":"💡 미나토미라이 역 하차 — 가든 네클리스 바로 걸어서 이동 가능","done":False},
            {"time":"15:00","icon":"🌷","title":"가든 네클리스 요코하마 2026","desc":"3/19~6/14 개최 · 야마시타 공원 · 수만 송이 튤립 & 벚꽃","teal":"📸 아카렌가 창고 봄 한정 플리마켓 · 바다 뷰 배경 인생샷","done":False},
            {"time":"18:30","icon":"🌃","title":"요코하마 야경 & 저녁","desc":"항구 야경 감상 · 코스모월드 대관람차 · 차이나타운 저녁 식사","done":False},
        ],
        "map_center":[35.5500,139.6700],
        "markers":[
            {"lat":35.6359,"lon":139.7086,"name":"나카메구로 벚꽃 축제 🌸","color":"pink"},
            {"lat":35.4573,"lon":139.6330,"name":"가든 네클리스 요코하마 🌷","color":"green"},
            {"lat":35.4437,"lon":139.6380,"name":"요코하마 차이나타운 🌃","color":"orange"},
        ],
    },
    {
        "label":"Day 4\n3/30 월","emoji":"🛍️","color":"#c89b5a",
        "title":"Day 4 · 3/30 (월) — 쇼핑 & 롯폰기",
        "subtitle":"긴자 집중 쇼핑 → 롯폰기 힐즈 벚꽃 라이트업",
        "vibe":"쇼핑하고 지쳐도 롯폰기 라이트업은 꼭! 🗼 도쿄 타워 배경 사진은 이날이 유일한 기회예요.",
        "events":[
            {"time":"오전","icon":"😴","title":"늦잠 & 여유로운 브런치","desc":"전날 요코하마 많이 걸었으니 푹 쉬고 느지막이 출발 ☕","done":False},
            {"time":"오후","icon":"🛍️","title":"긴자 집중 쇼핑","desc":"돈키호테 · 미츠코시 백화점 · 도버 스트리트 마켓","tip":"💡 긴자에서 히비야선 타면 롯폰기까지 한 번에! 동선 최적","done":False},
            {"time":"18:30","icon":"✨","title":"롯폰기 힐즈 라이트업","desc":"모리 정원 · 사쿠라자카 벚꽃 터널","night":"🗼 연못에 비친 벚꽃 + 도쿄 타워 배경 포토존 · 여행 클라이맥스!","done":False},
            {"time":"20:00","icon":"🍷","title":"롯폰기 레스토랑 저녁","desc":"두 분만의 근사한 만찬으로 여행 4일차 마무리 🥂","pink":"✨ 오늘이 마지막 밤! 특별한 레스토랑 예약 추천","done":False},
        ],
        "map_center":[35.6660,139.7480],
        "markers":[
            {"lat":35.6716,"lon":139.7640,"name":"긴자 쇼핑 🛍️","color":"orange"},
            {"lat":35.6603,"lon":139.7305,"name":"롯폰기 힐즈 모리 정원 ✨","color":"purple"},
        ],
    },
    {
        "label":"Day 5\n3/31 화","emoji":"⛩️","color":"#6b7ab8",
        "title":"Day 5 · 3/31 (화) — 아쉬운 마지막",
        "subtitle":"아사쿠사 센소지 → 아키하바라 짐 찾기 → 나리타 출발",
        "vibe":"마지막 날이라 아쉽지만 아사쿠사의 전통 감성으로 마무리 ⛩️ 또 오고 싶어질 거예요! 🥹",
        "events":[
            {"time":"10:00","icon":"🏨","title":"체크아웃","desc":"수퍼호텔 아키하바라 체크아웃 · 큰 짐은 호텔에 맡기고 출발","done":False},
            {"time":"10:30","icon":"⛩️","title":"아사쿠사 · 센소지","desc":"나카미세도리 기념품 쇼핑 · 전통 간식 탐방","pink":"🌸 스미다 공원 벚꽃을 마지막으로 눈에 담기","done":False},
            {"time":"16:00","icon":"🧳","title":"아키하바라 · 짐 수령","desc":"호텔에서 짐 찾은 후 스카이라이너 탑승 → 나리타 공항으로","tip":"💡 16:30 공항 도착 목표 · 스카이라이너 약 1시간 소요","done":False},
            {"time":"20:10","icon":"✈️","title":"나리타 출발 → 인천 22:50 도착","desc":"RS704 · 또 다시 도쿄 오자구 🥹","night":"두 분의 벚꽃 여행이 평생 기억에 남기를 바라요 🌸💕","done":False},
        ],
        "map_center":[35.7060,139.7840],
        "markers":[
            {"lat":35.7148,"lon":139.7967,"name":"아사쿠사 센소지 ⛩️","color":"red"},
            {"lat":35.7077,"lon":139.8019,"name":"스미다 공원 벚꽃 🌸","color":"pink"},
            {"lat":35.6982,"lon":139.7731,"name":"수퍼호텔 아키하바라 🧳","color":"blue"},
        ],
    },
]

# ── Session state init ────────────────────────────────────────────────────────
if "days" not in st.session_state:
    st.session_state.days = json.loads(json.dumps(DEFAULT_DAYS))
if "selected_day" not in st.session_state:
    st.session_state.selected_day = 0
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "photos" not in st.session_state:
    # photos[day_idx][event_idx] = [b64, ...]
    st.session_state.photos = {i: {j: [] for j in range(len(d["events"]))} for i, d in enumerate(DEFAULT_DAYS)}
if "day_photos" not in st.session_state:
    st.session_state.day_photos = {i: [] for i in range(len(DEFAULT_DAYS))}
if "day_memo" not in st.session_state:
    st.session_state.day_memo = {i: "" for i in range(len(DEFAULT_DAYS))}
if "checklist" not in st.session_state:
    st.session_state.checklist = [False] * 8

# ── Helpers ───────────────────────────────────────────────────────────────────
def img_to_b64(uploaded_file) -> str:
    img = Image.open(uploaded_file)
    img.thumbnail((700, 700))
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()

def render_photo_grid(b64_list: list, cols: int = 3):
    if not b64_list:
        return
    grid_cols = st.columns(cols)
    for idx, b64 in enumerate(b64_list):
        with grid_cols[idx % cols]:
            st.markdown(
                f'<div class="photo-item"><img src="data:image/jpeg;base64,{b64}"/></div>',
                unsafe_allow_html=True,
            )

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🌸 도쿄 벚꽃 여행 2026</div>
  <div class="hero-sub">지은 & 남자친구의 로맨틱 도쿄 투어</div>
  <div class="hero-date">2026년 3월 27일 (금) — 3월 31일 (화) · 4박 5일</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sakura-banner">
  🌸 &nbsp;<strong>벚꽃 개화 예보</strong>&nbsp;·&nbsp;개화 3/20~23 예상&nbsp;·&nbsp;
  <strong style="color:#c04070;">만개 3/28~29</strong> — 여행 기간이 딱 절정! 🌸
</div>
""", unsafe_allow_html=True)

# ── Flight cards ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="flight-row">
  <div class="flight-card"><div class="fc-label">✈️ 출국 · 지은</div>
    <div class="fc-route">인천 → 나리타</div><div class="fc-time">3/27 (금) RS701 09:20 → 11:50</div></div>
  <div class="flight-card"><div class="fc-label">✈️ 출국 · 남자친구</div>
    <div class="fc-route">인천 → 나리타</div><div class="fc-time">3/24 (화) RS701 09:20 → 11:50</div></div>
  <div class="flight-card"><div class="fc-label">✈️ 귀국 · 둘 다</div>
    <div class="fc-route">나리타 → 인천</div><div class="fc-time">3/31 (화) RS704 20:10 → 22:50</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

# ── Day tabs ──────────────────────────────────────────────────────────────────
day_cols = st.columns(5)
days = st.session_state.days
for i, d in enumerate(days):
    with day_cols[i]:
        if st.button(d["label"], key=f"daybtn_{i}", use_container_width=True):
            st.session_state.selected_day = i
            st.session_state.edit_mode = False
            st.rerun()

st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

# ── Edit toggle ───────────────────────────────────────────────────────────────
di  = st.session_state.selected_day
day = days[di]

_, toggle_col = st.columns([5, 1])
with toggle_col:
    toggle_label = "🔒 편집 끄기" if st.session_state.edit_mode else "✏️ 일정 편집"
    if st.button(toggle_label, key="edit_toggle"):
        st.session_state.edit_mode = not st.session_state.edit_mode
        st.rerun()

# ── Two-column layout ─────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════════
# LEFT — Schedule
# ════════════════════════════════════════════════════════════════════
with col_left:

    # Day header
    if st.session_state.edit_mode:
        st.markdown("##### 📋 날짜 정보 편집")
        day["title"]    = st.text_input("날짜 제목",   value=day["title"],    key=f"t_{di}")
        day["subtitle"] = st.text_input("날짜 부제목", value=day["subtitle"], key=f"s_{di}")
        day["vibe"]     = st.text_input("오늘의 바이브", value=day["vibe"],   key=f"v_{di}")
        st.markdown("---")
    else:
        st.markdown(f"""
        <div class="day-hdr" style="border-color:{day['color']}40;">
          <div class="day-hdr-emoji">{day['emoji']}</div>
          <div>
            <div class="day-hdr-title" style="color:{day['color']};">{day['title']}</div>
            <div class="day-hdr-sub">{day['subtitle']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Events ────────────────────────────────────────────────────────
    # Ensure photo slots exist for all events
    for ei in range(len(day["events"])):
        if ei not in st.session_state.photos.get(di, {}):
            if di not in st.session_state.photos:
                st.session_state.photos[di] = {}
            st.session_state.photos[di][ei] = []

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    events_to_delete = []
    for ei, ev in enumerate(day["events"]):

        if st.session_state.edit_mode:
            # ── Edit card ──────────────────────────────────────────────
            with st.expander(f"✏️ {ev.get('icon','📍')} {ev.get('title','일정')}", expanded=False):
                c1, c2 = st.columns([1, 3])
                with c1:
                    ev["icon"] = st.text_input("아이콘", value=ev.get("icon","📍"), key=f"ico_{di}_{ei}")
                with c2:
                    ev["time"] = st.text_input("시간", value=ev.get("time",""), key=f"etm_{di}_{ei}")
                ev["title"] = st.text_input("제목", value=ev.get("title",""), key=f"eti_{di}_{ei}")
                ev["desc"]  = st.text_area("설명", value=ev.get("desc",""), key=f"ede_{di}_{ei}", height=80)
                ev["done"]  = st.checkbox("✅ 완료 표시", value=ev.get("done",False), key=f"edn_{di}_{ei}")

                st.markdown("**배지 (선택 입력 — 비우면 숨김)**")
                bc1, bc2 = st.columns(2)
                with bc1:
                    tip_val = st.text_input("💡 팁", value=ev.get("tip",""), key=f"etip_{di}_{ei}")
                    ev["tip"] = tip_val if tip_val else ""
                    pk_val = st.text_input("📌 핑크 메모", value=ev.get("pink",""), key=f"epk_{di}_{ei}")
                    ev["pink"] = pk_val if pk_val else ""
                with bc2:
                    tl_val = st.text_input("🌿 민트 메모", value=ev.get("teal",""), key=f"etl_{di}_{ei}")
                    ev["teal"] = tl_val if tl_val else ""
                    nt_val = st.text_input("✨ 보라 메모", value=ev.get("night",""), key=f"ent_{di}_{ei}")
                    ev["night"] = nt_val if nt_val else ""

                # Per-event photo upload
                st.markdown("**📷 이 일정 사진 추가**")
                ev_ups = st.file_uploader(
                    "", type=["jpg","jpeg","png","webp"],
                    accept_multiple_files=True, key=f"evup_{di}_{ei}",
                    label_visibility="collapsed",
                )
                if ev_ups:
                    for f in ev_ups:
                        b64 = img_to_b64(f)
                        if b64 not in st.session_state.photos[di].get(ei, []):
                            st.session_state.photos[di].setdefault(ei, []).append(b64)

                ev_photos = st.session_state.photos.get(di, {}).get(ei, [])
                if ev_photos:
                    render_photo_grid(ev_photos, cols=4)
                    if st.button("🗑️ 사진 전체 삭제", key=f"clrev_{di}_{ei}"):
                        st.session_state.photos[di][ei] = []
                        st.rerun()

                # Delete event
                st.markdown("---")
                if st.button(f"🗑️ 이 일정 삭제", key=f"del_{di}_{ei}", type="secondary"):
                    events_to_delete.append(ei)

        else:
            # ── View card ──────────────────────────────────────────────
            done_badge = '<span class="done-badge">✅ 완료</span>' if ev.get("done") else ""
            card = f"""
            <div class="ev">
              <div class="ev-dot" style="background:{day['color']};"></div>
              <div class="ev-card">
                <div class="ev-time">{ev.get('time','')}</div>
                <div class="ev-title">{ev.get('icon','📍')} {ev.get('title','')}{done_badge}</div>
                <div class="ev-desc">{ev.get('desc','')}</div>
            """
            for bk, bc in [("tip","ev-tip"),("pink","ev-pink"),("teal","ev-teal"),("night","ev-night")]:
                if ev.get(bk):
                    card += f'<div class="{bc}">{ev[bk]}</div>'
            card += "</div></div>"
            st.markdown(card, unsafe_allow_html=True)

            # Inline event photos (view mode)
            ev_photos = st.session_state.photos.get(di, {}).get(ei, [])
            if ev_photos:
                render_photo_grid(ev_photos, cols=4)

    st.markdown('</div>', unsafe_allow_html=True)  # close .timeline

    # Apply deletions (reverse to keep indices stable)
    for ei in sorted(events_to_delete, reverse=True):
        day["events"].pop(ei)
        st.session_state.photos.get(di, {}).pop(ei, None)
    if events_to_delete:
        st.rerun()

    # Add new event
    if st.session_state.edit_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ 새 일정 추가", key=f"addEv_{di}"):
            day["events"].append({
                "time":"00:00","icon":"📍",
                "title":"새로운 일정","desc":"설명을 입력하세요","done":False,
            })
            new_ei = len(day["events"]) - 1
            st.session_state.photos.setdefault(di, {})[new_ei] = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════
# RIGHT — Map + Vibe + Memo + Album
# ════════════════════════════════════════════════════════════════════
with col_right:

    # Map
    st.markdown('<div class="map-lbl">📍 오늘의 동선 지도</div>', unsafe_allow_html=True)
    m = folium.Map(location=day["map_center"], zoom_start=13, tiles="CartoDB positron")
    valid_colors = {"red","blue","green","orange","purple","gray","darkred","darkblue","darkgreen","cadetblue"}
    for mk in day["markers"]:
        fc = mk["color"] if mk["color"] in valid_colors else "gray"
        folium.Marker(
            location=[mk["lat"], mk["lon"]],
            popup=folium.Popup(mk["name"], max_width=200),
            tooltip=mk["name"],
            icon=folium.Icon(color=fc, icon="star", prefix="fa"),
        ).add_to(m)
    if len(day["markers"]) >= 2:
        folium.PolyLine(
            [[mk["lat"], mk["lon"]] for mk in day["markers"]],
            color=day["color"], weight=2.5, opacity=0.6, dash_array="6 4",
        ).add_to(m)
    st_folium(m, width=None, height=330, returned_objects=[])

    # Vibe card
    st.markdown(f"""
    <div class="vibe-card" style="background:linear-gradient(135deg,{day['color']}18,{day['color']}08);
         border:1px solid {day['color']}40;">
      <div class="vibe-label" style="color:{day['color']};">💕 TODAY'S VIBE</div>
      <div class="vibe-text">{day.get('vibe','')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

    # ── Memo ──────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">📝 오늘의 메모</div>', unsafe_allow_html=True)
    memo_val = st.text_area(
        "메모", value=st.session_state.day_memo.get(di, ""),
        height=110, key=f"memo_{di}",
        placeholder="오늘 여행에서 느낀 것, 맛있었던 음식, 다음에 또 오고 싶은 곳 등 자유롭게 적어봐요 💕",
        label_visibility="collapsed",
    )
    st.session_state.day_memo[di] = memo_val

    st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

    # ── Day album ──────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">📸 오늘의 사진 앨범</div>', unsafe_allow_html=True)

    day_ups = st.file_uploader(
        "사진 업로드 (여러 장 가능)", type=["jpg","jpeg","png","webp"],
        accept_multiple_files=True, key=f"dayup_{di}",
        label_visibility="collapsed",
    )
    if day_ups:
        for f in day_ups:
            b64 = img_to_b64(f)
            if b64 not in st.session_state.day_photos.get(di, []):
                st.session_state.day_photos.setdefault(di, []).append(b64)

    day_album = st.session_state.day_photos.get(di, [])
    if day_album:
        render_photo_grid(day_album, cols=3)
        col_dl, col_clr = st.columns(2)
        with col_clr:
            if st.button("🗑️ 앨범 전체 삭제", key=f"clrAlbum_{di}"):
                st.session_state.day_photos[di] = []
                st.rerun()
    else:
        st.markdown(
            '<div style="text-align:center;padding:1.5rem;color:#d8a0c0;font-size:0.82rem;'
            'background:white;border:1px dashed #f0c0d8;border-radius:12px;">'
            '📷 사진을 업로드하면 여기에 예쁘게 모여요 🌸</div>',
            unsafe_allow_html=True,
        )

# ── Checklist ─────────────────────────────────────────────────────────────────
st.markdown("<hr class='pink-div' style='margin:2rem 0 1rem;'>", unsafe_allow_html=True)
st.markdown('<div class="sec-label">✅ 여행 전 체크리스트</div>', unsafe_allow_html=True)

CHECK_ITEMS = [
    ("💍","nane tokyo 반지 공방 사전 예약 (인스타 DM)"),
    ("📱","아이폰 지갑 앱에 Suica 추가 & 충전"),
    ("✈️","스카이라이너 편도 티켓 클룩 예매"),
    ("🌸","나카메구로 축제 날짜 확인 (3/29 10:00~17:00)"),
    ("🌷","가든 네클리스 요코하마 2026 일정 확인"),
    ("📸","카메라 / 보조배터리 준비"),
    ("💴","엔화 환전 (카드도 대부분 가능)"),
    ("🧴","드럭스토어 쇼핑 리스트 미리 작성"),
]

ck_cols = st.columns(2)
for idx, (icon, text) in enumerate(CHECK_ITEMS):
    with ck_cols[idx % 2]:
        checked = st.checkbox(f"{icon} {text}", value=st.session_state.checklist[idx], key=f"chk_{idx}")
        st.session_state.checklist[idx] = checked

done_cnt = sum(st.session_state.checklist)
total    = len(CHECK_ITEMS)
st.markdown(f"""
<div style="margin:0.8rem 0 0.3rem;font-size:0.78rem;color:#c890b0;text-align:center;">
  준비 완료 {done_cnt}/{total} · {int(done_cnt/total*100)}%
</div>
""", unsafe_allow_html=True)
st.progress(done_cnt / total)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  🌸 &nbsp;만개 예상 3/28~29 &nbsp;·&nbsp; 💍 nane tokyo 사전 예약 필수 &nbsp;·&nbsp; ✨ 라이트업 3곳 예약 불필요 &nbsp; 🌸
  <br><br>
  <span style="font-size:0.74rem;">두 분의 벚꽃 여행이 평생 기억에 남기를 💕</span>
</div>
""", unsafe_allow_html=True)
