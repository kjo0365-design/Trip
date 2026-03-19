import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌸 도쿄 벚꽃 여행 2026",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;500&display=swap');

/* ─── Global ─────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #fff5f7 0%, #fdf0f5 40%, #f8f0ff 100%);
    min-height: 100vh;
}

/* ─── Hide default Streamlit chrome ─────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; }

/* ─── Petal rain ─────────────────────────── */
.petal-container {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.petal {
    position: absolute;
    top: -40px;
    font-size: 18px;
    opacity: 0;
    animation: petalFall linear infinite;
}
@keyframes petalFall {
    0%   { transform: translateY(0px) rotate(0deg) translateX(0px);  opacity: 0; }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.3; }
    100% { transform: translateY(110vh) rotate(720deg) translateX(80px); opacity: 0; }
}

/* ─── Hero section ───────────────────────── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-title {
    font-family: 'Noto Serif KR', serif;
    font-size: 2.8rem;
    font-weight: 600;
    background: linear-gradient(135deg, #d4608a, #a855c8, #d4608a);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
    margin-bottom: 0.3rem;
}
@keyframes shimmer { to { background-position: 200% center; } }
.hero-sub {
    font-size: 1rem;
    color: #b07090;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}
.hero-date {
    font-size: 0.85rem;
    color: #c890b0;
    letter-spacing: 0.12em;
}

/* ─── Sakura banner ──────────────────────── */
.sakura-banner {
    background: linear-gradient(135deg, #ffe4ef, #f8d7fa);
    border: 1.5px solid #f0b8d8;
    border-radius: 16px;
    padding: 0.9rem 1.4rem;
    text-align: center;
    margin: 0.5rem 0 1.5rem;
    font-size: 0.92rem;
    color: #9a3060;
    animation: bannerPulse 3s ease-in-out infinite;
}
@keyframes bannerPulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(212,96,138,0.15); }
    50%      { box-shadow: 0 0 0 8px rgba(212,96,138,0); }
}

/* ─── Flight cards ───────────────────────── */
.flight-row { display: flex; gap: 12px; margin-bottom: 1.5rem; }
.flight-card {
    flex: 1;
    background: white;
    border: 1px solid #f0d0e8;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.flight-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(212,96,138,0.15); }
.flight-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #f0a0c8, #c890e8);
}
.fc-label { font-size: 0.72rem; color: #c890b0; letter-spacing: 0.1em; margin-bottom: 4px; text-transform: uppercase; }
.fc-route { font-size: 1.05rem; font-weight: 500; color: #5a2040; }
.fc-time  { font-size: 0.8rem; color: #9a7090; margin-top: 2px; }

/* ─── Day nav tabs ───────────────────────── */
.day-nav {
    display: flex; gap: 8px;
    justify-content: center;
    margin: 1.5rem 0 1rem;
    flex-wrap: wrap;
}
.day-btn {
    padding: 8px 18px;
    border-radius: 50px;
    border: 1.5px solid #f0c8dc;
    background: white;
    font-size: 0.82rem;
    font-family: 'Noto Sans KR', sans-serif;
    color: #9a5080;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}
.day-btn:hover, .day-btn.active {
    color: white;
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(212,96,138,0.3);
}
.day-btn-0.active, .day-btn-0:hover { background: linear-gradient(135deg, #e8849a, #d46080); }
.day-btn-1.active, .day-btn-1:hover { background: linear-gradient(135deg, #c47bb8, #a055a0); }
.day-btn-2.active, .day-btn-2:hover { background: linear-gradient(135deg, #3d9b8c, #2a7a6c); }
.day-btn-3.active, .day-btn-3:hover { background: linear-gradient(135deg, #c89b5a, #a07840); }
.day-btn-4.active, .day-btn-4:hover { background: linear-gradient(135deg, #6b7ab8, #4a5a98); }

/* ─── Day header ─────────────────────────── */
.day-header {
    display: flex; align-items: center; gap: 14px;
    padding: 1rem 1.4rem;
    border-radius: 16px;
    margin-bottom: 1.2rem;
    background: white;
    border: 1px solid #f0d0e8;
}
.day-emoji { font-size: 2rem; }
.day-title-text { font-family: 'Noto Serif KR', serif; font-size: 1.15rem; font-weight: 600; color: #5a2040; }
.day-subtitle-text { font-size: 0.8rem; color: #b07090; margin-top: 2px; }

/* ─── Timeline ───────────────────────────── */
.timeline { position: relative; padding-left: 24px; }
.timeline::before {
    content: '';
    position: absolute;
    left: 7px; top: 8px; bottom: 8px;
    width: 1.5px;
    background: linear-gradient(180deg, #f0a0c8, #c890e8, #90b0e8);
    border-radius: 2px;
}

.event {
    position: relative;
    margin-bottom: 14px;
}
.event-dot {
    position: absolute;
    left: -21px; top: 10px;
    width: 10px; height: 10px;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 0 0 2px rgba(212,96,138,0.25);
}
.event-card {
    background: white;
    border: 1px solid #f0d8e8;
    border-radius: 14px;
    padding: 12px 16px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.event-card:hover { transform: translateX(4px); box-shadow: 0 4px 18px rgba(212,96,138,0.12); }
.ev-time  { font-size: 0.7rem; color: #c8a0b8; letter-spacing: 0.08em; margin-bottom: 3px; }
.ev-title { font-size: 0.95rem; font-weight: 500; color: #5a2040; display: flex; align-items: center; gap: 6px; }
.ev-desc  { font-size: 0.82rem; color: #907080; margin-top: 4px; line-height: 1.55; }

.ev-tip {
    margin-top: 6px; padding: 6px 10px;
    background: #f0f5ff; border-radius: 8px;
    font-size: 0.76rem; color: #506090; line-height: 1.5;
}
.ev-pink {
    margin-top: 6px; padding: 6px 10px;
    background: #fff0f5; border-radius: 8px;
    font-size: 0.76rem; color: #a04060; line-height: 1.5;
}
.ev-teal {
    margin-top: 6px; padding: 6px 10px;
    background: #f0faf8; border-radius: 8px;
    font-size: 0.76rem; color: #2a6058; line-height: 1.5;
}
.ev-night {
    margin-top: 6px; padding: 6px 10px;
    background: #f5f0ff; border-radius: 8px;
    font-size: 0.76rem; color: #6040a0; line-height: 1.5;
}

/* ─── Map section ────────────────────────── */
.map-label {
    font-size: 0.78rem; color: #c890b0;
    text-align: center;
    margin-bottom: 6px;
    letter-spacing: 0.08em;
}

/* ─── Bottom note ────────────────────────── */
.bottom-note {
    text-align: center;
    padding: 1.5rem 1rem;
    font-size: 0.8rem;
    color: #c890b0;
    letter-spacing: 0.06em;
}

/* ─── Divider ────────────────────────────── */
.pink-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #f0c0d8, transparent);
    margin: 1.5rem 0;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ── Petal rain ────────────────────────────────────────────────────────────────
petal_html = '<div class="petal-container">'
for i in range(18):
    left = random.randint(0, 98)
    delay = random.uniform(0, 10)
    duration = random.uniform(6, 14)
    size = random.randint(14, 22)
    p = random.choice(["🌸", "🌸", "🌸", "🌼", "🌺"])
    petal_html += (
        f'<span class="petal" style="left:{left}%;'
        f'animation-delay:{delay:.1f}s;'
        f'animation-duration:{duration:.1f}s;'
        f'font-size:{size}px;"></span>'
    )
petal_html += '</div>'
st.markdown(petal_html.replace('></span>', f'>{random.choice(["🌸","🌼","🌺"])}</span>'), unsafe_allow_html=True)

# Actually replace properly
petals = []
for i in range(18):
    left = random.randint(0, 98)
    delay = random.uniform(0, 10)
    duration = random.uniform(6, 14)
    size = random.randint(14, 22)
    p = random.choice(["🌸", "🌸", "🌸", "🌼", "🌺"])
    petals.append(
        f'<span class="petal" style="left:{left}%;'
        f'animation-delay:{delay:.1f}s;'
        f'animation-duration:{duration:.1f}s;'
        f'font-size:{size}px;">{p}</span>'
    )
st.markdown(f'<div class="petal-container">{"".join(petals)}</div>', unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🌸 도쿄 벚꽃 여행</div>
  <div class="hero-sub">지은 & 남자친구의 로맨틱 도쿄 투어</div>
  <div class="hero-date">2026년 3월 27일 (금) — 3월 31일 (화) · 4박 5일</div>
</div>
""", unsafe_allow_html=True)

# ── Sakura banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sakura-banner">
  🌸 &nbsp; <strong>벚꽃 개화 예보</strong> &nbsp;·&nbsp;
  개화 3/20~23 예상 &nbsp;·&nbsp;
  <strong style="color:#c04070;">만개 3/28~29</strong> — 여행 기간이 딱 절정! &nbsp; 🌸
</div>
""", unsafe_allow_html=True)

# ── Flight cards ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="flight-row">
  <div class="flight-card">
    <div class="fc-label">✈️ 출국 · 지은</div>
    <div class="fc-route">인천 → 나리타</div>
    <div class="fc-time">3/27 (금) &nbsp; RS701 &nbsp; 09:20 → 11:50</div>
  </div>
  <div class="flight-card">
    <div class="fc-label">✈️ 출국 · 남자친구</div>
    <div class="fc-route">인천 → 나리타</div>
    <div class="fc-time">3/24 (화) &nbsp; RS701 &nbsp; 09:20 → 11:50</div>
  </div>
  <div class="flight-card">
    <div class="fc-label">✈️ 귀국 · 둘 다</div>
    <div class="fc-route">나리타 → 인천</div>
    <div class="fc-time">3/31 (화) &nbsp; RS704 &nbsp; 20:10 → 22:50</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Day data ──────────────────────────────────────────────────────────────────
DAYS = [
    {
        "label": "Day 1\n3/27 금",
        "emoji": "🛬",
        "title": "Day 1 · 3/27 (금) — 상봉의 기쁨",
        "subtitle": "나리타 도착 → 아키하바라 → 우에노 → 니혼바시 라이트업",
        "color": "#e8849a",
        "events": [
            {"time": "11:50", "icon": "✈️", "title": "나리타 공항 도착",
             "desc": "입국 심사 + 수하물 수취 후 스카이라이너 탑승",
             "tip": "💡 스카이라이너 닛포리역 하차 → JR 야마노테선으로 아키하바라 환승 (약 1시간 15분)"},
            {"time": "14:00", "icon": "👩‍❤️‍👨", "title": "아키하바라 — 수퍼호텔 체크인",
             "desc": "미리 와 있던 남자친구와 상봉! 짐 맡기고 가볍게 출발 🎉",
             "pink": "🏨 숙소: 수퍼호텔 아키하바라 (3/27~31)"},
            {"time": "15:00", "icon": "🌸", "title": "우에노 공원 산책",
             "desc": "해 질 녘 벚꽃 감상 · 아메요코 상점가 구경",
             "pink": "🍺 야키토리 꼬치 + 생맥주로 첫날 건배!"},
            {"time": "18:30", "icon": "✨", "title": "니혼바시 벚꽃 라이트업 — Sakura Fes",
             "desc": "에도 벚꽃 거리(Edo Sakura-dori) 핑크빛 조명 & 팝업 스토어",
             "night": "아키하바라에서 전철 5~10분 · 첫날 야경 산책 최적!"},
        ],
        "map_center": [35.6982, 139.7731],
        "markers": [
            {"lat": 35.6982, "lon": 139.7731, "name": "수퍼호텔 아키하바라 (숙소)", "color": "red"},
            {"lat": 35.7141, "lon": 139.7740, "name": "우에노 공원 🌸", "color": "pink"},
            {"lat": 35.6813, "lon": 139.7713, "name": "니혼바시 벚꽃 라이트업 ✨", "color": "purple"},
        ],
    },
    {
        "label": "Day 2\n3/28 토",
        "emoji": "💍",
        "title": "Day 2 · 3/28 (토) — 커플링 & 시부야",
        "subtitle": "하라주쿠 nane tokyo → 오모테산도 쇼핑 → 시부야 벚꽃 축제",
        "color": "#c47bb8",
        "events": [
            {"time": "10:15", "icon": "🚃", "title": "아키하바라 → 하라주쿠 이동",
             "desc": "JR 야마노테선 · 환승 없이 약 30분",
             "tip": "💡 아이폰이면 지갑 앱 Suica로 바로 탑승!"},
            {"time": "11:00–14:00", "icon": "💍", "title": "nane tokyo 캣스트리트점 — 커플링 제작",
             "desc": "세상에 하나뿐인 반지 만들기 · 3시간 소요 · 평점 5.0 ⭐",
             "pink": "⚠️ 사전 예약 필수! 인스타 DM 또는 공식 홈페이지로 미리 예약"},
            {"time": "14:00", "icon": "🍽️", "title": "늦은 점심",
             "desc": "돈카츠 마이센 아오야마 본점 OR 루크스 랍스터 하라주쿠점 추천"},
            {"time": "15:30", "icon": "🛍️", "title": "오모테산도 & 캣스트리트 쇼핑",
             "desc": "편집샵 · 빈티지샵 · 반지 끼고 산책하며 시부야 방향으로 내려가기"},
            {"time": "18:30", "icon": "✨", "title": "시부야 벚꽃 축제 — 사쿠라가오카초",
             "desc": "핑크 초롱불 라이트업 · 벚꽃 언덕(사쿠라자카) 골목 감성",
             "night": "🌆 스크램블 교차로 야경 → 파르코 지하 카오스 키친 저녁"},
        ],
        "map_center": [35.6653, 139.7090],
        "markers": [
            {"lat": 35.6667, "lon": 139.7063, "name": "💍 nane tokyo 캣스트리트점", "color": "purple"},
            {"lat": 35.6653, "lon": 139.7127, "name": "오모테산도 힐즈 🛍️", "color": "blue"},
            {"lat": 35.6566, "lon": 139.7024, "name": "시부야 벚꽃 축제 ✨", "color": "pink"},
        ],
    },
    {
        "label": "Day 3\n3/29 일",
        "emoji": "🌷",
        "title": "Day 3 · 3/29 (일) — 꽃의 하루",
        "subtitle": "나카메구로 벚꽃 축제 → 요코하마 가든 네클리스",
        "color": "#3d9b8c",
        "events": [
            {"time": "10:30–13:30", "icon": "🌸", "title": "나카메구로 벚꽃 축제",
             "desc": "메구로강 벚꽃 터널 · 10:00~17:00 · 야타이 포장마차 운영",
             "teal": "🥂 샴페인 & 딸기 탕후루 먹으며 강변 산책 · 스타벅스 리저브 인생샷!"},
            {"time": "14:00", "icon": "🚃", "title": "나카메구로 → 요코하마 이동",
             "desc": "도큐 도요코선 특급 · 환승 없이 35~40분",
             "tip": "💡 미나토미라이 역 하차 — 가든 네클리스 바로 걸어서 이동 가능"},
            {"time": "15:00", "icon": "🌷", "title": "가든 네클리스 요코하마 2026",
             "desc": "3/19~6/14 개최 · 야마시타 공원 · 수만 송이 튤립 & 벚꽃",
             "teal": "📸 아카렌가 창고 봄 한정 플리마켓 · 바다 뷰 배경 인생샷"},
            {"time": "18:30", "icon": "🌃", "title": "요코하마 야경 & 저녁",
             "desc": "항구 야경 감상 · 코스모월드 대관람차 · 차이나타운 저녁 식사"},
        ],
        "map_center": [35.5500, 139.6700],
        "markers": [
            {"lat": 35.6359, "lon": 139.7086, "name": "나카메구로 벚꽃 축제 🌸", "color": "pink"},
            {"lat": 35.4573, "lon": 139.6330, "name": "가든 네클리스 요코하마 🌷", "color": "green"},
            {"lat": 35.4437, "lon": 139.6380, "name": "요코하마 차이나타운 🌃", "color": "orange"},
        ],
    },
    {
        "label": "Day 4\n3/30 월",
        "emoji": "🛍️",
        "title": "Day 4 · 3/30 (월) — 쇼핑 & 롯폰기",
        "subtitle": "긴자 집중 쇼핑 → 롯폰기 힐즈 벚꽃 라이트업",
        "color": "#c89b5a",
        "events": [
            {"time": "오전", "icon": "😴", "title": "늦잠 & 여유로운 브런치",
             "desc": "전날 요코하마 많이 걸었으니 푹 쉬고 느지막이 출발 ☕"},
            {"time": "오후", "icon": "🛍️", "title": "긴자 집중 쇼핑",
             "desc": "돈키호테 · 미츠코시 백화점 · 도버 스트리트 마켓",
             "tip": "💡 긴자에서 히비야선 타면 롯폰기까지 한 번에! 동선 최적"},
            {"time": "18:30", "icon": "✨", "title": "롯폰기 힐즈 라이트업",
             "desc": "모리 정원 · 사쿠라자카 벚꽃 터널",
             "night": "🗼 연못에 비친 벚꽃 + 도쿄 타워 배경 포토존 · 여행 클라이맥스!"},
            {"time": "20:00", "icon": "🍷", "title": "롯폰기 레스토랑 저녁",
             "desc": "두 분만의 근사한 만찬으로 여행 4일차 마무리 🥂",
             "pink": "✨ 오늘이 마지막 밤! 특별한 레스토랑 예약 추천"},
        ],
        "map_center": [35.6660, 139.7480],
        "markers": [
            {"lat": 35.6716, "lon": 139.7640, "name": "긴자 쇼핑 🛍️", "color": "orange"},
            {"lat": 35.6603, "lon": 139.7305, "name": "롯폰기 힐즈 모리 정원 ✨", "color": "purple"},
        ],
    },
    {
        "label": "Day 5\n3/31 화",
        "emoji": "⛩️",
        "title": "Day 5 · 3/31 (화) — 아쉬운 마지막",
        "subtitle": "아사쿠사 센소지 → 아키하바라 짐 찾기 → 나리타 출발",
        "color": "#6b7ab8",
        "events": [
            {"time": "10:00", "icon": "🏨", "title": "체크아웃",
             "desc": "수퍼호텔 아키하바라 체크아웃 · 큰 짐은 호텔에 맡기고 출발"},
            {"time": "10:30", "icon": "⛩️", "title": "아사쿠사 · 센소지",
             "desc": "나카미세도리 기념품 쇼핑 · 전통 간식 탐방",
             "pink": "🌸 스미다 공원 벚꽃을 마지막으로 눈에 담기"},
            {"time": "16:00", "icon": "🧳", "title": "아키하바라 · 짐 수령",
             "desc": "호텔에서 짐 찾은 후 스카이라이너 탑승 → 나리타 공항으로",
             "tip": "💡 16:30 공항 도착 목표 · 스카이라이너 약 1시간 소요"},
            {"time": "20:10", "icon": "✈️", "title": "나리타 출발 → 인천 22:50 도착",
             "desc": "RS704 · 또 다시 도쿄 오자구 🥹",
             "night": "두 분의 벚꽃 여행이 평생 기억에 남기를 바라요 🌸💕"},
        ],
        "map_center": [35.7060, 139.7840],
        "markers": [
            {"lat": 35.7148, "lon": 139.7967, "name": "아사쿠사 센소지 ⛩️", "color": "red"},
            {"lat": 35.7077, "lon": 139.8019, "name": "스미다 공원 벚꽃 🌸", "color": "pink"},
            {"lat": 35.6982, "lon": 139.7731, "name": "수퍼호텔 아키하바라 🧳", "color": "blue"},
        ],
    },
]

DAY_COLORS = ["#e8849a", "#c47bb8", "#3d9b8c", "#c89b5a", "#6b7ab8"]

# ── Day selector ──────────────────────────────────────────────────────────────
if "selected_day" not in st.session_state:
    st.session_state.selected_day = 0

btn_html = '<div class="day-nav">'
for i, d in enumerate(DAYS):
    active = "active" if i == st.session_state.selected_day else ""
    btn_html += (
        f'<div class="day-btn day-btn-{i} {active}" '
        f'style="display:inline-block;">{d["label"].replace(chr(10),"<br>")}</div>'
    )
btn_html += '</div>'
st.markdown(btn_html, unsafe_allow_html=True)

cols = st.columns(5)
for i, d in enumerate(DAYS):
    if cols[i].button(d["label"], key=f"daybtn_{i}", use_container_width=True):
        st.session_state.selected_day = i
        st.rerun()

st.markdown("<hr class='pink-divider'>", unsafe_allow_html=True)

# ── Selected day content ──────────────────────────────────────────────────────
day = DAYS[st.session_state.selected_day]
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Day header
    st.markdown(f"""
    <div class="day-header" style="border-color:{day['color']}40;">
      <div class="day-emoji">{day['emoji']}</div>
      <div>
        <div class="day-title-text" style="color:{day['color']};">{day['title']}</div>
        <div class="day-subtitle-text">{day['subtitle']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Timeline events
    events_html = '<div class="timeline">'
    for ev in day["events"]:
        dot_color = day["color"]
        card = f"""
        <div class="event">
          <div class="event-dot" style="background:{dot_color};"></div>
          <div class="event-card">
            <div class="ev-time">{ev['time']}</div>
            <div class="ev-title">{ev['icon']} {ev['title']}</div>
            <div class="ev-desc">{ev['desc']}</div>
        """
        if "tip" in ev:
            card += f'<div class="ev-tip">{ev["tip"]}</div>'
        if "pink" in ev:
            card += f'<div class="ev-pink">{ev["pink"]}</div>'
        if "teal" in ev:
            card += f'<div class="ev-teal">{ev["teal"]}</div>'
        if "night" in ev:
            card += f'<div class="ev-night">{ev["night"]}</div>'
        card += "</div></div>"
        events_html += card
    events_html += "</div>"
    st.markdown(events_html, unsafe_allow_html=True)

with col_right:
    # Map
    st.markdown('<div class="map-label">📍 오늘의 동선 지도</div>', unsafe_allow_html=True)

    m = folium.Map(
        location=day["map_center"],
        zoom_start=13,
        tiles="CartoDB positron",
    )

    icon_colors = {
        "red": "red", "pink": "pink", "purple": "purple",
        "blue": "blue", "green": "green", "orange": "orange",
    }

    for mk in day["markers"]:
        fc = icon_colors.get(mk["color"], "gray")
        folium.Marker(
            location=[mk["lat"], mk["lon"]],
            popup=folium.Popup(mk["name"], max_width=200),
            tooltip=mk["name"],
            icon=folium.Icon(
                color=fc if fc in ["red","blue","green","orange","purple","gray"] else "pink",
                icon="heart" if "love" in mk["name"].lower() else "star",
                prefix="fa",
            ),
        ).add_to(m)

    # Draw route between markers
    if len(day["markers"]) >= 2:
        coords = [[mk["lat"], mk["lon"]] for mk in day["markers"]]
        folium.PolyLine(
            coords,
            color=day["color"],
            weight=2.5,
            opacity=0.6,
            dash_array="6 4",
        ).add_to(m)

    st_folium(m, width=None, height=400, returned_objects=[])

    # Cute memo card
    st.markdown(f"""
    <div style="
        margin-top: 1rem;
        background: linear-gradient(135deg, {day['color']}15, {day['color']}08);
        border: 1px solid {day['color']}40;
        border-radius: 14px;
        padding: 1rem 1.2rem;
    ">
      <div style="font-size:0.75rem; color:{day['color']}; font-weight:500; margin-bottom:6px; letter-spacing:0.08em;">
        💕 TODAY'S VIBE
      </div>
      <div style="font-size:0.82rem; color:#7a5060; line-height:1.6;">
        {["나리타에서 만나는 순간부터 설레는 첫날 🌸 우에노 공원의 벚꽃 아래 첫 사진도 꼭 남겨요!",
          "반지 만드는 3시간이 평생 기억에 남을 거예요 💍 손가락에 반지를 끼는 순간을 잊지 말아요!",
          "나카메구로 강가에서 샴페인 한 잔 🥂 요코하마 바다 뷰는 도쿄와 전혀 다른 낭만이 있어요!",
          "쇼핑하고 지쳐도 롯폰기 라이트업은 꼭! 🗼 도쿄 타워 배경 사진은 이날이 유일한 기회예요.",
          "마지막 날이라 아쉽지만 아사쿠사의 전통 감성으로 마무리 ⛩️ 또 오고 싶어질 거예요! 🥹"][st.session_state.selected_day]}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown("<hr class='pink-divider' style='margin:2rem 0 1rem;'>", unsafe_allow_html=True)

# ── Checklist section ─────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; font-family:'Noto Serif KR',serif; font-size:1.1rem;
     color:#9a3060; margin-bottom:1rem;">
  ✅ 여행 전 체크리스트
</div>
""", unsafe_allow_html=True)

check_col1, check_col2 = st.columns(2)
checks = [
    ("💍", "nane tokyo 반지 공방 사전 예약 (인스타 DM)", True),
    ("📱", "아이폰 지갑 앱에 Suica 추가 & 충전", False),
    ("✈️", "스카이라이너 편도 티켓 클룩 예매", False),
    ("🌸", "나카메구로 축제 날짜 확인 (3/29 10:00~17:00)", True),
    ("🌷", "가든 네클리스 요코하마 2026 일정 확인", True),
    ("📸", "카메라 / 보조배터리 준비", False),
    ("💴", "엔화 환전 (카드도 대부분 가능)", False),
    ("🧴", "드럭스토어 쇼핑 리스트 미리 작성", False),
]

for i, (icon, text, done) in enumerate(checks):
    col = check_col1 if i % 2 == 0 else check_col2
    style = "text-decoration:line-through; color:#c8a8b8;" if done else "color:#5a2040;"
    col.markdown(
        f'<div style="padding:8px 12px; margin-bottom:6px; background:white; '
        f'border:1px solid #f0d0e8; border-radius:10px; font-size:0.85rem; {style}">'
        f'{icon} {text}</div>',
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bottom-note">
  🌸 &nbsp; 만개 예상 3/28~29 &nbsp;·&nbsp;
  💍 nane tokyo 사전 예약 필수 &nbsp;·&nbsp;
  ✨ 라이트업 3곳 예약 불필요 &nbsp;·&nbsp;
  🌸
  <br><br>
  <span style="font-size:0.75rem;">두 분의 벚꽃 여행이 평생 기억에 남기를 💕</span>
</div>
""", unsafe_allow_html=True)
