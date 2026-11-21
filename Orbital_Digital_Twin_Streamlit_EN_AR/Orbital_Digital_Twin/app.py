import streamlit as st
from models import orbit_trace, service_coverage, NODES

st.set_page_config(page_title="Orbital Digital Twin", layout="wide")
ar = st.radio("Language / اللغة", ("English", "العربية"), horizontal=True) == "العربية"


def t(en, arabic):
    return arabic if ar else en


direction = t("ltr", "rtl")
st.markdown(f"""
<style>
.stApp {{background:#edf4f2;color:#142d35}}
.stMarkdown,.stCaption {{direction:{direction};text-align:start}}
.space-hero {{background:linear-gradient(110deg,#142f46,#0a5352);
  color:#fff;padding:1.4rem 1.7rem;border-radius:18px;margin:.4rem 0 1.2rem}}
.space-hero h1 {{font-size:clamp(1.8rem,5vw,3rem);color:#fff;margin:.25rem 0}}
.space-hero strong {{color:#b1f0c4;font-size:.85rem}}
.orbit-svg {{width:100%;max-height:310px}}
.sat-live {{transform-box:fill-box;transform-origin:center;animation:signal 2.5s ease-in-out infinite}}
@keyframes signal {{50% {{opacity:.5}}}}
@media(prefers-reduced-motion:reduce) {{.sat-live {{animation:none}}}}
</style>
<div class="space-hero" lang="{t('en','ar')}">
<strong>{t('SYNTHETIC EXERCISE DATA','بيانات تمرين اصطناعية')}</strong>
<h1>{t('Orbital Digital Twin','التوأم الرقمي المداري')}</h1>
<p>{t('Standalone civilian simulation.',
      'محاكاة مدنية مستقلة.')}</p>
</div>
""", unsafe_allow_html=True)

st.caption(t("Conceptual orbit view. Positions and service dependencies are fictional.",
             "عرض مداري مبسط. المواقع واعتماد الخدمات افتراضيان."))
phase = st.slider(t("Exercise phase (%)", "مرحلة التمرين (%)"), 0, 100, 0, 5, key="phase")
offline = st.selectbox(t("Simulated relay outage", "انقطاع محاكى لقمر ترحيل"), (None, *NODES),
                       format_func=lambda node: node or t("None", "لا يوجد"), key="relay")
markers = []
for node, (x, y) in zip(NODES, orbit_trace(phase / 100)):
    live = node != offline
    colour = "#75edbb" if live else "#ffa996"
    markers.append(f'<circle class="{"sat-live" if live else ""}" cx="{x}" cy="{y}" r="8" fill="{colour}"/>'
                   f'<text x="{x}" y="{y-13}" text-anchor="middle" fill="#f9fcff">{node}</text>')
st.markdown(f"""
<svg class="orbit-svg" viewBox="0 0 500 220" role="img" aria-label="{t('Fictional orbit','مدار افتراضي')}">
  <rect width="500" height="220" rx="17" fill="#10283d"/>
  <ellipse cx="250" cy="110" rx="166" ry="66" fill="none" stroke="#6a9ba4" stroke-dasharray="5 6"/>
  <circle cx="250" cy="110" r="36" fill="#277f81" stroke="#9de5d1" stroke-width="3"/>
  {"".join(markers)}
</svg>""", unsafe_allow_html=True)
translated = {"Mapping": "الخرائط", "Weather reports": "تقارير الطقس", "Service notices": "إشعارات الخدمات"}
st.table([{t("Civil service", "الخدمة المدنية"): t(name, translated[name]),
           t("Available relays", "الأقمار المتاحة للترحيل"): total}
          for name, total in service_coverage(offline).items()])
