import streamlit as st
import folium
from streamlit_folium import st_folium
import json, base64, random
from io import BytesIO
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="🌸 도쿄 벚꽃 여행 2026", page_icon="🌸",
                   layout="wide", initial_sidebar_state="collapsed")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR',sans-serif;}
.stApp{background:linear-gradient(160deg,#fff5f7 0%,#fdf0f5 40%,#f8f0ff 100%);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.5rem;padding-bottom:3rem;}

.petal-wrap{position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:0;overflow:hidden;}
.petal{position:absolute;top:-40px;opacity:0;animation:pF linear infinite;}
@keyframes pF{0%{transform:translateY(0) rotate(0deg);opacity:0;}10%{opacity:.55;}90%{opacity:.25;}100%{transform:translateY(110vh) rotate(720deg) translateX(60px);opacity:0;}}

.hero{text-align:center;padding:2rem 1rem 1rem;}
.hero-title{font-family:'Noto Serif KR',serif;font-size:2.6rem;font-weight:600;
  background:linear-gradient(135deg,#d4608a,#a855c8,#d4608a);background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shim 4s linear infinite;}
@keyframes shim{to{background-position:200% center;}}
.hero-sub{font-size:.95rem;color:#b07090;letter-spacing:.08em;margin-top:4px;}
.hero-date{font-size:.82rem;color:#c890b0;letter-spacing:.12em;}

.sakura-banner{background:linear-gradient(135deg,#ffe4ef,#f8d7fa);border:1.5px solid #f0b8d8;
  border-radius:16px;padding:.8rem 1.2rem;text-align:center;margin:.5rem 0 1.2rem;
  font-size:.88rem;color:#9a3060;animation:pulse 3s ease-in-out infinite;}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(212,96,138,.15);}50%{box-shadow:0 0 0 8px rgba(212,96,138,0);}}

.flight-row{display:flex;gap:10px;margin-bottom:1.2rem;}
.flight-card{flex:1;background:white;border:1px solid #f0d0e8;border-radius:14px;padding:.9rem 1rem;
  position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s;}
.flight-card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(212,96,138,.15);}
.flight-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#f0a0c8,#c890e8);}
.fc-label{font-size:.7rem;color:#c890b0;letter-spacing:.1em;margin-bottom:3px;}
.fc-route{font-size:1rem;font-weight:500;color:#5a2040;}
.fc-time{font-size:.78rem;color:#9a7090;margin-top:2px;}

.pink-div{height:1px;background:linear-gradient(90deg,transparent,#f0c0d8,transparent);margin:1.2rem 0;border:none;}
.sec-label{font-family:'Noto Serif KR',serif;font-size:1rem;color:#9a3060;text-align:center;margin-bottom:.8rem;}

.day-hdr{display:flex;align-items:center;gap:12px;padding:.9rem 1.2rem;border-radius:14px;
  margin-bottom:1rem;background:white;border:1px solid #f0d0e8;}
.day-hdr-emoji{font-size:1.8rem;}
.day-hdr-title{font-family:'Noto Serif KR',serif;font-size:1.05rem;font-weight:600;}
.day-hdr-sub{font-size:.78rem;color:#b07090;margin-top:2px;}

.timeline{position:relative;padding-left:22px;}
.timeline::before{content:'';position:absolute;left:6px;top:6px;bottom:6px;width:1.5px;
  background:linear-gradient(180deg,#f0a0c8,#c890e8,#90b0e8);border-radius:2px;}
.ev{position:relative;margin-bottom:12px;}
.ev-dot{position:absolute;left:-19px;top:10px;width:10px;height:10px;border-radius:50%;
  border:2px solid white;box-shadow:0 0 0 2px rgba(212,96,138,.25);}
.ev-card{background:white;border:1px solid #f0d8e8;border-radius:12px;padding:11px 14px;
  transition:transform .2s,box-shadow .2s;}
.ev-card:hover{transform:translateX(4px);box-shadow:0 4px 18px rgba(212,96,138,.12);}
.ev-time{font-size:.68rem;color:#c8a0b8;letter-spacing:.08em;margin-bottom:2px;}
.ev-title{font-size:.92rem;font-weight:500;color:#5a2040;}
.ev-desc{font-size:.8rem;color:#907080;margin-top:3px;line-height:1.5;}
.ev-tip{margin-top:5px;padding:5px 9px;background:#f0f5ff;border-radius:7px;font-size:.74rem;color:#506090;line-height:1.5;}
.ev-pink{margin-top:5px;padding:5px 9px;background:#fff0f5;border-radius:7px;font-size:.74rem;color:#a04060;line-height:1.5;}
.ev-teal{margin-top:5px;padding:5px 9px;background:#f0faf8;border-radius:7px;font-size:.74rem;color:#2a6058;line-height:1.5;}
.ev-night{margin-top:5px;padding:5px 9px;background:#f5f0ff;border-radius:7px;font-size:.74rem;color:#6040a0;line-height:1.5;}
.done-badge{display:inline-block;font-size:.63rem;padding:2px 7px;border-radius:20px;margin-left:6px;background:#e8f8f0;color:#2a7050;font-weight:500;}

.photo-item{border-radius:9px;overflow:hidden;aspect-ratio:1;background:#f8f0f5;}
.photo-item img{width:100%;height:100%;object-fit:cover;}

.map-lbl{font-size:.76rem;color:#c890b0;text-align:center;margin-bottom:5px;letter-spacing:.08em;}
.vibe-card{margin-top:.9rem;border-radius:14px;padding:.9rem 1.1rem;}
.vibe-label{font-size:.72rem;font-weight:500;margin-bottom:5px;letter-spacing:.08em;}
.vibe-text{font-size:.8rem;color:#7a5060;line-height:1.6;}

/* ── Quick links ── */
.links-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:.5rem;}
.link-card{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 6px;
  background:white;border:1px solid #f0d0e8;border-radius:12px;text-decoration:none;
  transition:transform .18s,box-shadow .18s;cursor:pointer;}
.link-card:hover{transform:translateY(-3px);box-shadow:0 6px 18px rgba(212,96,138,.18);border-color:#e8a0c8;}
.link-icon{font-size:1.3rem;line-height:1;}
.link-name{font-size:.68rem;color:#9a5070;font-weight:500;text-align:center;line-height:1.3;}

/* ── Checklist edit ── */
.chk-edit-row{display:flex;align-items:center;gap:6px;background:white;
  border:1px solid #f0d0e8;border-radius:10px;padding:6px 10px;margin-bottom:5px;}
.chk-edit-icon{font-size:1rem;width:22px;text-align:center;flex-shrink:0;}

div[data-testid="stButton"]>button{background:white;border:1.5px solid #f0c8dc;color:#9a5080;
  border-radius:50px;font-family:'Noto Sans KR',sans-serif;font-size:.82rem;padding:6px 0;
  transition:all .2s;width:100%;}
div[data-testid="stButton"]>button:hover{background:linear-gradient(135deg,#f0a8c8,#d890e0);
  color:white;border-color:transparent;transform:translateY(-2px);box-shadow:0 4px 14px rgba(212,96,138,.3);}

.footer{text-align:center;padding:1.5rem 1rem;font-size:.78rem;color:#c890b0;letter-spacing:.06em;}
</style>
""", unsafe_allow_html=True)

# ── Petal rain ────────────────────────────────────────────────────────────────
ph = '<div class="petal-wrap">'
for _ in range(20):
    ph += (f'<span class="petal" style="left:{random.randint(0,98)}%;font-size:{random.randint(13,21)}px;'
           f'animation-delay:{random.uniform(0,12):.1f}s;animation-duration:{random.uniform(7,15):.1f}s;">'
           f'{random.choice(["🌸","🌸","🌸","🌼","🌺"])}</span>')
st.markdown(ph + '</div>', unsafe_allow_html=True)

# ── Default data ──────────────────────────────────────────────────────────────
DEFAULT_DAYS = [
    {"label":"Day 1\n3/27 금","emoji":"🛬","color":"#e8849a",
     "title":"Day 1 · 3/27 (금) — 상봉의 기쁨",
     "subtitle":"나리타 도착 → 아키하바라 → 우에노 → 니혼바시 라이트업",
     "vibe":"나리타에서 만나는 순간부터 설레는 첫날 🌸 우에노 공원의 벚꽃 아래 첫 사진도 꼭 남겨요!",
     "events":[
       {"time":"11:50","icon":"✈️","title":"나리타 공항 도착","desc":"입국 심사 + 수하물 수취 후 스카이라이너 탑승","tip":"💡 스카이라이너 닛포리역 하차 → JR 야마노테선 아키하바라 환승 (약 1시간 15분)","done":False,"lat":35.7653,"lon":140.3862},
       {"time":"14:00","icon":"👩‍❤️‍👨","title":"아키하바라 — 수퍼호텔 체크인","desc":"미리 와 있던 남자친구와 상봉! 짐 맡기고 출발 🎉","pink":"🏨 숙소: 수퍼호텔 아키하바라 (3/27~31)","done":False,"lat":35.6982,"lon":139.7731},
       {"time":"15:00","icon":"🌸","title":"우에노 공원 산책","desc":"해 질 녘 벚꽃 감상 · 아메요코 상점가 구경","pink":"🍺 야키토리 꼬치 + 생맥주로 첫날 건배!","done":False,"lat":35.7141,"lon":139.7740},
       {"time":"18:30","icon":"✨","title":"니혼바시 벚꽃 라이트업 — Sakura Fes","desc":"에도 벚꽃 거리 핑크빛 조명 & 팝업 스토어","night":"아키하바라에서 전철 5~10분 · 첫날 야경 산책 최적!","done":False,"lat":35.6813,"lon":139.7713},
     ]},
    {"label":"Day 2\n3/28 토","emoji":"💍","color":"#c47bb8",
     "title":"Day 2 · 3/28 (토) — 커플링 & 시부야",
     "subtitle":"하라주쿠 nane tokyo → 오모테산도 쇼핑 → 시부야 벚꽃 축제",
     "vibe":"반지 만드는 3시간이 평생 기억에 남을 거예요 💍 손가락에 반지를 끼는 순간을 잊지 말아요!",
     "events":[
       {"time":"10:15","icon":"🚃","title":"아키하바라 → 하라주쿠 이동","desc":"JR 야마노테선 · 환승 없이 약 30분","tip":"💡 아이폰이면 지갑 앱 Suica로 바로 탑승!","done":False,"lat":35.6982,"lon":139.7731},
       {"time":"11:00–14:00","icon":"💍","title":"nane tokyo 커플링 제작","desc":"세상에 하나뿐인 반지 만들기 · 3시간 소요 · 평점 5.0 ⭐","pink":"⚠️ 사전 예약 필수! 인스타 DM 또는 공식 홈페이지로 미리 예약","done":False,"lat":35.6667,"lon":139.7063},
       {"time":"14:00","icon":"🍽️","title":"늦은 점심","desc":"돈카츠 마이센 아오야마 본점 OR 루크스 랍스터 하라주쿠점 추천","done":False,"lat":35.6653,"lon":139.7127},
       {"time":"15:30","icon":"🛍️","title":"오모테산도 & 캣스트리트 쇼핑","desc":"편집샵 · 빈티지샵 · 반지 끼고 산책하며 시부야 방향으로","done":False,"lat":35.6680,"lon":139.7100},
       {"time":"18:30","icon":"✨","title":"시부야 벚꽃 축제 — 사쿠라가오카초","desc":"핑크 초롱불 라이트업 · 벚꽃 언덕 골목 감성","night":"🌆 스크램블 교차로 야경 → 파르코 지하 카오스 키친 저녁","done":False,"lat":35.6566,"lon":139.7024},
     ]},
    {"label":"Day 3\n3/29 일","emoji":"🌷","color":"#3d9b8c",
     "title":"Day 3 · 3/29 (일) — 꽃의 하루",
     "subtitle":"나카메구로 벚꽃 축제 → 요코하마 가든 네클리스",
     "vibe":"나카메구로 강가에서 샴페인 한 잔 🥂 요코하마 바다 뷰는 도쿄와 전혀 다른 낭만이 있어요!",
     "events":[
       {"time":"10:30–13:30","icon":"🌸","title":"나카메구로 벚꽃 축제","desc":"메구로강 벚꽃 터널 · 10:00~17:00 · 야타이 포장마차 운영","teal":"🥂 샴페인 & 딸기 탕후루 먹으며 강변 산책 · 스타벅스 리저브 인생샷!","done":False,"lat":35.6359,"lon":139.7086},
       {"time":"14:00","icon":"🚃","title":"나카메구로 → 요코하마 이동","desc":"도큐 도요코선 특급 · 환승 없이 35~40분","tip":"💡 미나토미라이 역 하차 — 가든 네클리스 바로 걸어서 이동","done":False,"lat":35.6359,"lon":139.7086},
       {"time":"15:00","icon":"🌷","title":"가든 네클리스 요코하마 2026","desc":"3/19~6/14 개최 · 야마시타 공원 · 수만 송이 튤립 & 벚꽃","teal":"📸 아카렌가 창고 봄 한정 플리마켓 · 바다 뷰 배경 인생샷","done":False,"lat":35.4573,"lon":139.6330},
       {"time":"18:30","icon":"🌃","title":"요코하마 야경 & 저녁","desc":"항구 야경 감상 · 코스모월드 대관람차 · 차이나타운 저녁 식사","done":False,"lat":35.4437,"lon":139.6380},
     ]},
    {"label":"Day 4\n3/30 월","emoji":"🛍️","color":"#c89b5a",
     "title":"Day 4 · 3/30 (월) — 쇼핑 & 롯폰기",
     "subtitle":"긴자 집중 쇼핑 → 롯폰기 힐즈 벚꽃 라이트업",
     "vibe":"쇼핑하고 지쳐도 롯폰기 라이트업은 꼭! 🗼 도쿄 타워 배경 사진은 이날이 유일한 기회예요.",
     "events":[
       {"time":"오전","icon":"😴","title":"늦잠 & 여유로운 브런치","desc":"전날 요코하마 많이 걸었으니 푹 쉬고 느지막이 출발 ☕","done":False,"lat":35.6982,"lon":139.7731},
       {"time":"오후","icon":"🛍️","title":"긴자 집중 쇼핑","desc":"돈키호테 · 미츠코시 백화점 · 도버 스트리트 마켓","tip":"💡 긴자에서 히비야선 타면 롯폰기까지 한 번에! 동선 최적","done":False,"lat":35.6716,"lon":139.7640},
       {"time":"18:30","icon":"✨","title":"롯폰기 힐즈 라이트업","desc":"모리 정원 · 사쿠라자카 벚꽃 터널","night":"🗼 연못에 비친 벚꽃 + 도쿄 타워 배경 포토존 · 여행 클라이맥스!","done":False,"lat":35.6603,"lon":139.7305},
       {"time":"20:00","icon":"🍷","title":"롯폰기 레스토랑 저녁","desc":"두 분만의 근사한 만찬으로 여행 4일차 마무리 🥂","pink":"✨ 오늘이 마지막 밤! 특별한 레스토랑 예약 추천","done":False,"lat":35.6580,"lon":139.7310},
     ]},
    {"label":"Day 5\n3/31 화","emoji":"⛩️","color":"#6b7ab8",
     "title":"Day 5 · 3/31 (화) — 아쉬운 마지막",
     "subtitle":"아사쿠사 센소지 → 아키하바라 짐 찾기 → 나리타 출발",
     "vibe":"마지막 날이라 아쉽지만 아사쿠사의 전통 감성으로 마무리 ⛩️ 또 오고 싶어질 거예요! 🥹",
     "events":[
       {"time":"10:00","icon":"🏨","title":"체크아웃","desc":"수퍼호텔 아키하바라 체크아웃 · 큰 짐은 호텔에 맡기고 출발","done":False,"lat":35.6982,"lon":139.7731},
       {"time":"10:30","icon":"⛩️","title":"아사쿠사 · 센소지","desc":"나카미세도리 기념품 쇼핑 · 전통 간식 탐방","pink":"🌸 스미다 공원 벚꽃을 마지막으로 눈에 담기","done":False,"lat":35.7148,"lon":139.7967},
       {"time":"16:00","icon":"🧳","title":"아키하바라 · 짐 수령","desc":"호텔에서 짐 찾은 후 스카이라이너 탑승 → 나리타 공항으로","tip":"💡 16:30 공항 도착 목표 · 스카이라이너 약 1시간 소요","done":False,"lat":35.6982,"lon":139.7731},
       {"time":"20:10","icon":"✈️","title":"나리타 출발 → 인천 22:50 도착","desc":"RS704 · 또 다시 도쿄 오자구 🥹","night":"두 분의 벚꽃 여행이 평생 기억에 남기를 바라요 🌸💕","done":False,"lat":35.7653,"lon":140.3862},
     ]},
]

DEFAULT_CHECKS = [
    {"icon":"💍","text":"nane tokyo 반지 공방 사전 예약 (인스타 DM)","done":False},
    {"icon":"📱","text":"아이폰 지갑 앱에 Suica 추가 & 충전","done":False},
    {"icon":"✈️","text":"스카이라이너 편도 티켓 클룩 예매","done":False},
    {"icon":"🌸","text":"나카메구로 축제 날짜 확인 (3/29 10:00~17:00)","done":False},
    {"icon":"🌷","text":"가든 네클리스 요코하마 2026 일정 확인","done":False},
    {"icon":"📸","text":"카메라 / 보조배터리 준비","done":False},
    {"icon":"💴","text":"엔화 환전 (카드도 대부분 가능)","done":False},
    {"icon":"🧴","text":"드럭스토어 쇼핑 리스트 미리 작성","done":False},
]

QUICK_LINKS = [
    {"name":"Google Maps","icon":"🗺️","url":"https://maps.google.com"},
    {"name":"Agoda","icon":"🏨","url":"https://www.agoda.com"},
    {"name":"NOL","icon":"🎫","url":"https://nol.jp"},
    {"name":"마이리얼트립","icon":"🌏","url":"https://www.myrealtrip.com"},
    {"name":"Klook","icon":"🎟️","url":"https://www.klook.com/ko"},
    {"name":"투어비스","icon":"🚌","url":"https://www.tourvis.com"},
    {"name":"KKday","icon":"🎪","url":"https://www.kkday.com/ko"},
    {"name":"Tabelog","icon":"🍜","url":"https://tabelog.com"},
    {"name":"핫페퍼","icon":"🍱","url":"https://www.hotpepper.jp"},
    {"name":"MATCHA","icon":"🍵","url":"https://matcha-jp.com/ko"},
]

# ── Session state ─────────────────────────────────────────────────────────────
if "days"        not in st.session_state: st.session_state.days = json.loads(json.dumps(DEFAULT_DAYS))
if "sel"         not in st.session_state: st.session_state.sel  = 0
if "edit_mode"   not in st.session_state: st.session_state.edit_mode = False
if "edit_checks" not in st.session_state: st.session_state.edit_checks = False
if "photos"      not in st.session_state:
    st.session_state.photos = {i:{j:[] for j in range(len(d["events"]))} for i,d in enumerate(DEFAULT_DAYS)}
if "day_photos"  not in st.session_state: st.session_state.day_photos = {i:[] for i in range(len(DEFAULT_DAYS))}
if "day_memo"    not in st.session_state: st.session_state.day_memo   = {i:"" for i in range(len(DEFAULT_DAYS))}
if "checks"      not in st.session_state: st.session_state.checks     = json.loads(json.dumps(DEFAULT_CHECKS))

# ── Helpers ───────────────────────────────────────────────────────────────────
def img_to_b64(f) -> str:
    img = Image.open(f); img.thumbnail((700,700))
    buf = BytesIO(); img.save(buf,format="JPEG",quality=82)
    return base64.b64encode(buf.getvalue()).decode()

def photo_grid(b64s, cols=3):
    if not b64s: return
    cs = st.columns(cols)
    for i, b in enumerate(b64s):
        with cs[i%cols]:
            st.markdown(f'<div class="photo-item"><img src="data:image/jpeg;base64,{b}"/></div>', unsafe_allow_html=True)

def build_map(day):
    """Build folium map using event lat/lon coords (filtered: skip Narita)."""
    NARITA = (35.7653, 140.3862)
    pts = []
    for ev in day["events"]:
        lat, lon = ev.get("lat"), ev.get("lon")
        if lat and lon and (lat, lon) != NARITA:
            pts.append((lat, lon, ev.get("title",""), ev.get("icon","📍")))

    if pts:
        avg_lat = sum(p[0] for p in pts) / len(pts)
        avg_lon = sum(p[1] for p in pts) / len(pts)
        center  = [avg_lat, avg_lon]
    else:
        center = day.get("map_center", [35.6895, 139.6917])

    m = folium.Map(location=center, zoom_start=13, tiles="CartoDB positron")

    valid_colors = {"red","blue","green","orange","purple","gray","darkred","darkblue","darkgreen","cadetblue"}
    day_color    = day.get("color","#e8849a")

    for idx, (lat, lon, name, icon_emoji) in enumerate(pts):
        num = idx + 1
        html_icon = f"""
        <div style="background:{day_color};color:white;width:26px;height:26px;border-radius:50%;
             display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;
             border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,.25);">{num}</div>"""
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(f"<b>{icon_emoji} {name}</b>", max_width=200),
            tooltip=f"{num}. {name}",
            icon=folium.DivIcon(html=html_icon, icon_size=(26,26), icon_anchor=(13,13)),
        ).add_to(m)

    if len(pts) >= 2:
        coords = [[p[0], p[1]] for p in pts]
        folium.PolyLine(coords, color=day_color, weight=2.5, opacity=0.65, dash_array="6 4").add_to(m)

    return m

# ═════════════════════════════════════════════════════════════════════════════
# RENDER
# ═════════════════════════════════════════════════════════════════════════════

# Hero
st.markdown("""
<div class="hero">
  <div class="hero-title">🌸 도쿄 벚꽃 여행 2026</div>
  <div class="hero-sub">지은 &amp; 남자친구의 로맨틱 도쿄 투어</div>
  <div class="hero-date">2026년 3월 27일 (금) — 3월 31일 (화) · 4박 5일</div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class="sakura-banner">
  🌸 &nbsp;<strong>벚꽃 개화 예보</strong>&nbsp;·&nbsp;개화 3/20~23 예상&nbsp;·&nbsp;
  <strong style="color:#c04070;">만개 3/28~29</strong> — 여행 기간이 딱 절정! 🌸
</div>""", unsafe_allow_html=True)

# Flights
st.markdown("""<div class="flight-row">
  <div class="flight-card"><div class="fc-label">✈️ 출국 · 지은</div>
    <div class="fc-route">인천 → 나리타</div><div class="fc-time">3/27 (금) RS701 09:20 → 11:50</div></div>
  <div class="flight-card"><div class="fc-label">✈️ 출국 · 남자친구</div>
    <div class="fc-route">인천 → 나리타</div><div class="fc-time">3/24 (화) RS701 09:20 → 11:50</div></div>
  <div class="flight-card"><div class="fc-label">✈️ 귀국 · 둘 다</div>
    <div class="fc-route">나리타 → 인천</div><div class="fc-time">3/31 (화) RS704 20:10 → 22:50</div></div>
</div>""", unsafe_allow_html=True)

# ── Quick links ───────────────────────────────────────────────────────────────
st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)
st.markdown('<div class="sec-label">🔗 여행 유용 사이트 바로가기</div>', unsafe_allow_html=True)

lnk_html = '<div class="links-grid">'
for lk in QUICK_LINKS:
    lnk_html += (f'<a class="link-card" href="{lk["url"]}" target="_blank" rel="noopener">'
                 f'<span class="link-icon">{lk["icon"]}</span>'
                 f'<span class="link-name">{lk["name"]}</span></a>')
lnk_html += '</div>'
st.markdown(lnk_html, unsafe_allow_html=True)

st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

# ── Day tabs ──────────────────────────────────────────────────────────────────
day_cols = st.columns(5)
days = st.session_state.days
for i, d in enumerate(days):
    with day_cols[i]:
        if st.button(d["label"], key=f"db_{i}", use_container_width=True):
            st.session_state.sel  = i
            st.session_state.edit_mode = False
            st.rerun()

st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

di  = st.session_state.sel
day = days[di]

# Edit toggle
_, etcol = st.columns([5,1])
with etcol:
    lbl = "🔒 편집 끄기" if st.session_state.edit_mode else "✏️ 일정 편집"
    if st.button(lbl, key="et"):
        st.session_state.edit_mode = not st.session_state.edit_mode
        st.rerun()

col_l, col_r = st.columns([1,1], gap="large")

# ════════════════════════════════════════════════════════════════════
# LEFT — schedule
# ════════════════════════════════════════════════════════════════════
with col_l:

    if st.session_state.edit_mode:
        st.markdown("##### 📋 날짜 정보 편집")
        day["title"]    = st.text_input("날짜 제목",   value=day["title"],    key=f"t_{di}")
        day["subtitle"] = st.text_input("날짜 부제목", value=day["subtitle"], key=f"s_{di}")
        day["vibe"]     = st.text_input("오늘의 바이브", value=day["vibe"],   key=f"v_{di}")
        st.markdown("---")
    else:
        st.markdown(f"""<div class="day-hdr" style="border-color:{day['color']}40;">
          <div class="day-hdr-emoji">{day['emoji']}</div>
          <div><div class="day-hdr-title" style="color:{day['color']};">{day['title']}</div>
          <div class="day-hdr-sub">{day['subtitle']}</div></div></div>""", unsafe_allow_html=True)

    # ensure photo slots
    for ei in range(len(day["events"])):
        st.session_state.photos.setdefault(di, {}).setdefault(ei, [])

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    to_del = []

    for ei, ev in enumerate(day["events"]):
        if st.session_state.edit_mode:
            with st.expander(f"✏️ {ev.get('icon','📍')} {ev.get('title','일정')}", expanded=False):
                c1,c2 = st.columns([1,3])
                with c1: ev["icon"] = st.text_input("아이콘", value=ev.get("icon","📍"), key=f"ico_{di}_{ei}")
                with c2: ev["time"] = st.text_input("시간",   value=ev.get("time",""),   key=f"etm_{di}_{ei}")
                ev["title"] = st.text_input("제목", value=ev.get("title",""), key=f"eti_{di}_{ei}")
                ev["desc"]  = st.text_area( "설명", value=ev.get("desc",""),  key=f"ede_{di}_{ei}", height=75)
                ev["done"]  = st.checkbox("✅ 완료 표시", value=ev.get("done",False), key=f"edn_{di}_{ei}")

                # location
                st.markdown("**📍 지도 위치 (위도 / 경도)**")
                lc1,lc2 = st.columns(2)
                with lc1:
                    ev["lat"] = st.number_input("위도 (lat)", value=float(ev.get("lat",35.6895)),
                                                format="%.4f", key=f"lat_{di}_{ei}")
                with lc2:
                    ev["lon"] = st.number_input("경도 (lon)", value=float(ev.get("lon",139.6917)),
                                                format="%.4f", key=f"lon_{di}_{ei}")

                st.markdown("**배지 (비우면 숨김)**")
                b1,b2 = st.columns(2)
                with b1:
                    ev["tip"]  = st.text_input("💡 팁",      value=ev.get("tip",""),   key=f"etip_{di}_{ei}") or ""
                    ev["pink"] = st.text_input("📌 핑크 메모", value=ev.get("pink",""), key=f"epk_{di}_{ei}")  or ""
                with b2:
                    ev["teal"] = st.text_input("🌿 민트 메모", value=ev.get("teal",""), key=f"etl_{di}_{ei}")  or ""
                    ev["night"]= st.text_input("✨ 보라 메모", value=ev.get("night",""),key=f"ent_{di}_{ei}")  or ""

                # per-event photos
                st.markdown("**📷 이 일정 사진**")
                evups = st.file_uploader("", type=["jpg","jpeg","png","webp"],
                                         accept_multiple_files=True, key=f"evup_{di}_{ei}",
                                         label_visibility="collapsed")
                if evups:
                    for f in evups:
                        b = img_to_b64(f)
                        if b not in st.session_state.photos[di].get(ei,[]):
                            st.session_state.photos[di].setdefault(ei,[]).append(b)

                evp = st.session_state.photos.get(di,{}).get(ei,[])
                if evp:
                    photo_grid(evp, cols=4)
                    if st.button("🗑️ 사진 삭제", key=f"clrev_{di}_{ei}"):
                        st.session_state.photos[di][ei]=[]
                        st.rerun()

                st.markdown("---")
                if st.button(f"🗑️ 이 일정 삭제", key=f"del_{di}_{ei}"):
                    to_del.append(ei)
        else:
            done_b = '<span class="done-badge">✅ 완료</span>' if ev.get("done") else ""
            card = (f'<div class="ev"><div class="ev-dot" style="background:{day["color"]};"></div>'
                    f'<div class="ev-card">'
                    f'<div class="ev-time">{ev.get("time","")}</div>'
                    f'<div class="ev-title">{ev.get("icon","📍")} {ev.get("title","")}{done_b}</div>'
                    f'<div class="ev-desc">{ev.get("desc","")}</div>')
            for bk,bc in [("tip","ev-tip"),("pink","ev-pink"),("teal","ev-teal"),("night","ev-night")]:
                if ev.get(bk): card += f'<div class="{bc}">{ev[bk]}</div>'
            card += "</div></div>"
            st.markdown(card, unsafe_allow_html=True)

            evp = st.session_state.photos.get(di,{}).get(ei,[])
            if evp: photo_grid(evp, cols=4)

    st.markdown('</div>', unsafe_allow_html=True)

    for ei in sorted(to_del, reverse=True):
        day["events"].pop(ei)
        st.session_state.photos.get(di,{}).pop(ei,None)
    if to_del: st.rerun()

    if st.session_state.edit_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ 새 일정 추가", key=f"addEv_{di}"):
            day["events"].append({"time":"00:00","icon":"📍","title":"새로운 일정",
                                   "desc":"설명을 입력하세요","done":False,
                                   "lat":day["events"][-1].get("lat",35.6895) if day["events"] else 35.6895,
                                   "lon":day["events"][-1].get("lon",139.6917) if day["events"] else 139.6917})
            new_ei = len(day["events"])-1
            st.session_state.photos.setdefault(di,{})[new_ei]=[]
            st.rerun()

# ════════════════════════════════════════════════════════════════════
# RIGHT — map + vibe + memo + album
# ════════════════════════════════════════════════════════════════════
with col_r:
    st.markdown('<div class="map-lbl">📍 오늘의 동선 지도 (일정 위치 수정 시 자동 반영)</div>', unsafe_allow_html=True)
    st_folium(build_map(day), width=None, height=340, returned_objects=[])

    st.markdown(f"""<div class="vibe-card" style="background:linear-gradient(135deg,{day['color']}18,{day['color']}08);
         border:1px solid {day['color']}40;">
      <div class="vibe-label" style="color:{day['color']};">💕 TODAY'S VIBE</div>
      <div class="vibe-text">{day.get('vibe','')}</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

    st.markdown('<div class="sec-label">📝 오늘의 메모</div>', unsafe_allow_html=True)
    mv = st.text_area("메모", value=st.session_state.day_memo.get(di,""),
                      height=100, key=f"memo_{di}",
                      placeholder="오늘 여행에서 느낀 것, 맛있었던 음식, 다음에 또 오고 싶은 곳 등 자유롭게 적어봐요 💕",
                      label_visibility="collapsed")
    st.session_state.day_memo[di] = mv

    st.markdown("<hr class='pink-div'>", unsafe_allow_html=True)

    st.markdown('<div class="sec-label">📸 오늘의 사진 앨범</div>', unsafe_allow_html=True)
    dup = st.file_uploader("사진 업로드", type=["jpg","jpeg","png","webp"],
                           accept_multiple_files=True, key=f"dayup_{di}",
                           label_visibility="collapsed")
    if dup:
        for f in dup:
            b = img_to_b64(f)
            if b not in st.session_state.day_photos.get(di,[]):
                st.session_state.day_photos.setdefault(di,[]).append(b)

    da = st.session_state.day_photos.get(di,[])
    if da:
        photo_grid(da, cols=3)
        _, clrcol = st.columns([3,1])
        with clrcol:
            if st.button("🗑️ 전체 삭제", key=f"clrA_{di}"):
                st.session_state.day_photos[di]=[]; st.rerun()
    else:
        st.markdown('<div style="text-align:center;padding:1.5rem;color:#d8a0c0;font-size:.82rem;'
                    'background:white;border:1px dashed #f0c0d8;border-radius:12px;">'
                    '📷 사진을 업로드하면 여기에 예쁘게 모여요 🌸</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHECKLIST (editable)
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr class='pink-div' style='margin:2rem 0 1rem;'>", unsafe_allow_html=True)

chk_hdr_l, chk_hdr_r = st.columns([4,1])
with chk_hdr_l:
    st.markdown('<div class="sec-label" style="text-align:left;margin-bottom:.3rem;">✅ 여행 전 체크리스트</div>', unsafe_allow_html=True)
with chk_hdr_r:
    clbl = "🔒 편집 끄기" if st.session_state.edit_checks else "✏️ 편집"
    if st.button(clbl, key="ckedit"):
        st.session_state.edit_checks = not st.session_state.edit_checks
        st.rerun()

checks = st.session_state.checks

if st.session_state.edit_checks:
    st.markdown("**항목 수정 / 추가 / 삭제**")
    chk_del = []
    for ci, ck in enumerate(checks):
        cc1,cc2,cc3,cc4 = st.columns([1,2,5,1])
        with cc1:
            ck["icon"] = st.text_input("아이콘", value=ck.get("icon","📌"), key=f"ckico_{ci}",
                                       label_visibility="collapsed")
        with cc2:
            ck["done"] = st.checkbox("완료", value=ck.get("done",False), key=f"ckdn_{ci}",
                                     label_visibility="collapsed")
        with cc3:
            ck["text"] = st.text_input("항목", value=ck.get("text",""), key=f"cktxt_{ci}",
                                       label_visibility="collapsed")
        with cc4:
            if st.button("🗑️", key=f"ckdel_{ci}"):
                chk_del.append(ci)

    for ci in sorted(chk_del, reverse=True):
        checks.pop(ci)
    if chk_del: st.rerun()

    if st.button("➕ 항목 추가", key="addChk"):
        checks.append({"icon":"📌","text":"새 항목","done":False})
        st.rerun()
else:
    ck_cols = st.columns(2)
    for ci, ck in enumerate(checks):
        with ck_cols[ci % 2]:
            checked = st.checkbox(f"{ck.get('icon','📌')} {ck.get('text','')}",
                                  value=ck.get("done",False), key=f"chk_{ci}")
            ck["done"] = checked

done_cnt = sum(c.get("done",False) for c in checks)
total    = len(checks) if checks else 1
st.markdown(f'<div style="margin:.8rem 0 .3rem;font-size:.78rem;color:#c890b0;text-align:center;">'
            f'준비 완료 {done_cnt}/{len(checks)} · {int(done_cnt/total*100)}%</div>', unsafe_allow_html=True)
st.progress(done_cnt / total)

# Footer
st.markdown("""<div class="footer">
  🌸 &nbsp;만개 예상 3/28~29 &nbsp;·&nbsp; 💍 nane tokyo 사전 예약 필수 &nbsp;·&nbsp; ✨ 라이트업 3곳 예약 불필요 &nbsp; 🌸
  <br><br><span style="font-size:.74rem;">두 분의 벚꽃 여행이 평생 기억에 남기를 💕</span>
</div>""", unsafe_allow_html=True)
