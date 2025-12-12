import streamlit as st
import hashlib
import textwrap

# ---- Data Definitions ----
TRIGRAMS = {
    "乾": {"name": "乾", "bin": "111", "symbol": "☰", "element": "金"},
    "兌": {"name": "兌", "bin": "110", "symbol": "☱", "element": "金"},
    "離": {"name": "離", "bin": "101", "symbol": "☲", "element": "火"},
    "震": {"name": "震", "bin": "100", "symbol": "☳", "element": "木"},
    "巽": {"name": "巽", "bin": "011", "symbol": "☴", "element": "木"},
    "坎": {"name": "坎", "bin": "010", "symbol": "☵", "element": "水"},
    "艮": {"name": "艮", "bin": "001", "symbol": "☶", "element": "土"},
    "坤": {"name": "坤", "bin": "000", "symbol": "☷", "element": "土"},
}

THEMES = [
    "事業策略",
    "財務投資",
    "產品設計",
    "人力資源/團隊",
    "市場/品牌",
    "危機管理",
    "個人決策/關係",
    "政策規劃/制度設計",
]

# Generate 128 contextual factors (8 themes x 8 gua x 2 positions)
CONTEXTUAL_FACTORS = {}
for t_idx, theme in enumerate(THEMES):
    for g_key, g_data in TRIGRAMS.items():
        for pos in ["上卦", "下卦"]:
            key = f"{theme}__{g_key}__{pos}"
            # modern, practical phrasing
            CONTEXTUAL_FACTORS[key] = (
                f"[{theme}] 當{pos}為 {g_key}（{g_data['element']}），常見情境："
                + {
                    "乾": "決策驅動、領導、資源整合的問題",
                    "兌": "溝通、客戶反饋與情感動態",
                    "離": "品牌/可視化表現與能見度的抉擇",
                    "震": "創新驅動、快速試錯的實驗文化",
                    "巽": "策略傳播、滲透性成長與滲透策略",
                    "坎": "資訊風險、財務流動性或安全疑慮",
                    "艮": "規範、邊界管理和慢速穩定成長",
                    "坤": "資源承載、支持系統與穩定性需求",
                }[g_key]
            )

# ---- Hexagram (64) generation scaffold ----
# We'll create 64 combinated hexagrams programmatically. For each, provide
# name, tag, gua_ci, yao_ci (six-level interpretations), sec_dec_focus (1-6).
HEXAGRAMS = {}

def make_hexagram_key(upper, lower):
    return f"{upper}-{lower}"

for u_key, u in TRIGRAMS.items():
    for l_key, l in TRIGRAMS.items():
        key = make_hexagram_key(u_key, l_key)
        # name convention: "上卦/下卦"
        name = f"{u_key}上/{l_key}下"
        # tag - short phrase for modern usage
        tag = f"{u['element']}→{l['element']} 節點分析"
        # gua_ci: brief modernised hexagram statement
        gua_ci = (
            f"當上卦為 {u_key}（{u['element']}），下卦為 {l_key}（{l['element']}）。"
            + "這代表資源、節奏與風險的組合需要被同時考量，"
            + "適用於需要在策略與操作間取得平衡的決策情境。"
        )
        # Determine sec_dec_focus deterministically for reproducibility
        h = hashlib.sha1(key.encode('utf-8')).hexdigest()
        sec_focus = (int(h, 16) % 6) + 1  # 1..6

        # Create six yao lines with modern applications and yin/yang attribute
        yao_ci = []
        for i in range(6):
            idx = i + 1
            # simple yin/yang: odd lines -> yang (1), even -> yin (0)
            yin_yang = 1 if idx % 2 == 1 else 0
            # create a short modern interpretation for each line
            yao_text = (
                f"第{idx}爻 ({'陽' if yin_yang==1 else '陰'})：在{THEMES[(hash(key + str(idx)) % len(THEMES))]}情境中，"
                + f"代表宜{'主動' if yin_yang==1 else '守勢'}行動，具體提醒：注意{u_key}->{l_key}的能量流向。"
            )
            yao_ci.append({
                "index": idx,
                "yin_yang": yin_yang,
                "text": yao_text,
            })

        HEXAGRAMS[key] = {
            "name": name,
            "tag": tag,
            "gua_ci": gua_ci,
            "yao_ci": yao_ci,
            "sec_dec_focus": sec_focus,
            # store upper/lower elements for quick lookup
            "upper": u_key,
            "lower": l_key,
        }

# ---- Five-element relation helper ----
# Simple map for generating relationship (相生/相剋/相同)
GENERATIVE = {
    '木': '火',
    '火': '土',
    '土': '金',
    '金': '水',
    '水': '木',
}

CONTROLLING = {
    '木': '土',
    '火': '金',
    '土': '水',
    '金': '木',
    '水': '火',
}

def five_element_relation(u_elem, l_elem):
    if u_elem == l_elem:
        return "相同"
    if GENERATIVE.get(u_elem) == l_elem:
        return "相生"
    if CONTROLLING.get(u_elem) == l_elem:
        return "相剋"
    # if none of the above, try reverse
    if GENERATIVE.get(l_elem) == u_elem:
        return "被相生"
    if CONTROLLING.get(l_elem) == u_elem:
        return "被相剋"
    return "中性"

# ---- Core logic: get_hexagram_data ----

def get_hexagram_data(upper_key, lower_key, theme):
    """
    Given upper and lower trigram keys and a theme, return a consolidated
    analysis including: five-element coordination (氣場警示), 世應關係,
    and a refined AI decision insight (HTML/Markdown string).
    """
    key = make_hexagram_key(upper_key, lower_key)
    if key not in HEXAGRAMS:
        raise ValueError("無效的卦組合")

    hex_data = HEXAGRAMS[key]

    # A. 氣場警示 (五行協調度)
    u_elem = TRIGRAMS[upper_key]['element']
    l_elem = TRIGRAMS[lower_key]['element']
    fe_relation = five_element_relation(u_elem, l_elem)

    if fe_relation in ("相生", "被相生"):
        fe_label = "高度協調（天助自助）"
        fe_comment = "資源與機會相互補充，傾向於主動擴展與整合。"
    elif fe_relation in ("相剋", "被相剋"):
        fe_label = "結構衝突（時與我爭）"
        fe_comment = "需求與阻力同時存在，採取防禦/調整策略以避免消耗。"
    elif fe_relation == "相同":
        fe_label = "能量疊加（專注如一/易趨極端）"
        fe_comment = "優勢集中但需警惕過度偏執或資源浪費。"
    else:
        fe_label = "中性（複合情況）"
        fe_comment = "局面平衡，需靠策略選擇來引導走向。"

    five_element = {
        "upper_element": u_elem,
        "lower_element": l_elem,
        "relation": fe_relation,
        "label": fe_label,
        "comment": fe_comment,
    }

    # B. 世應關係 (third yao vs sixth yao yin/yang)
    yao_list = hex_data['yao_ci']
    # third is index 2 (1-based 3)
    shi = yao_list[2]['yin_yang']
    ying = yao_list[5]['yin_yang']
    if shi != ying:
        relation_label = "不同（相吸）"
        relation_comment = "世應互補，有利建立合作或外部支持。"
    else:
        relation_label = "相同（相斥/重疊）"
        relation_comment = "需以自我調整為主，可能出現內部摩擦。"

    shiying = {
        "shi": shi,
        "ying": ying,
        "label": relation_label,
        "comment": relation_comment,
    }

    # C. 哲理總結生成
    insight_md = _generate_ai_decision_insight(hex_data, five_element, shiying, theme)

    return {
        "hexagram": hex_data,
        "five_element": five_element,
        "shiying": shiying,
        "insight_md": insight_md,
    }


def _generate_ai_decision_insight(hex_data, five_element, shiying, theme):
    """
    Create a compact HTML/Markdown block that contains:
    - A philosophical opening derived from the five-element label
    - Core parameters list
    - Core action principles based on combinations
    """
    # Philosophical opening based on five-element label
    fe_label = five_element['label']
    if "高度協調" in fe_label:
        opening = "時空有助，乘勢而行；秉持整合之智，以小步快驗證，再擴張。"
    elif "結構衝突" in fe_label:
        opening = "當下如風暴前夕：既非全然退場，也非莽撞前進。首重界面修補與能量重分配。"
    elif "能量疊加" in fe_label:
        opening = "能量集中，適合深耕；但勿忘外部校準，以免陷入過度自信的盲點。"
    else:
        opening = "局勢混合，策略先行；設定小目標與回饋機制以取得關鍵信息。"

    # Parameter list
    params = textwrap.dedent(f"""
    **核心參數清單**

    - 五行協調度：**{five_element['relation']}** — {five_element['label']}
    - 上卦（U）：{hex_data['upper']}（{TRIGRAMS[hex_data['upper']]['element']}）
    - 下卦（L）：{hex_data['lower']}（{TRIGRAMS[hex_data['lower']]['element']}）
    - 情境主題：{theme}
    - 上卦情境：{CONTEXTUAL_FACTORS.get(f'{theme}__{hex_data['upper']}__上卦','-')}
    - 下卦情境：{CONTEXTUAL_FACTORS.get(f'{theme}__{hex_data['lower']}__下卦','-')}
    - 世應關係：**{shiying['label']}** — {shiying['comment']}

    """)

    # Core action principles:
    # Combine five_element and shiying to produce tactical guidelines
    actions = []
    if "高度協調" in five_element['label'] and "不同（相吸）" in shiying['label']:
        actions.append("乘勢而進：利用互補關係快速取得外部資源或合作。")
        actions.append("保持快速回饋循環，確保整合效益可測量。")
    elif "高度協調" in five_element['label'] and "相同（相斥/重疊）" in shiying['label']:
        actions.append("重點內化：集中資源加速執行，同時設立內部審查機制以防偏差。")
    elif "結構衝突" in five_element['label']:
        actions.append("優先化緩解措施：減少摩擦，尋找短期替代路徑以保存核心勢能。")
        actions.append("若必要，分階段撤退並重整資源配置。")
    elif "能量疊加" in five_element['label']:
        actions.append("適度放大：將有限資源投入高概率回報的小域，避免資源分散。")
        actions.append("建立外部對照指標，強制檢驗盲點。")
    else:
        actions.append("分散風險並快速學習：採用小步試驗策略，逐步建立信息優勢。")

    # Generic final principle
    actions.append("最終行動準則：知進知退，方能持盈保泰。")

    action_md = "\n".join([f"- {a}" for a in actions])

    # Highlight which yao is the decision focus
    focus_idx = hex_data['sec_dec_focus']

    # Assemble as HTML/Markdown block
    md = textwrap.dedent(f"""
    <div class="iccss-insight">
    <h3>時空定性 — {fe_label}</h3>
    <p><em>{opening}</em></p>
    {params}
    **核心行動原則**

    {action_md}

    <p><small>決策焦點：第 {focus_idx} 爻（以六爻倒序顯示）</small></p>
    </div>
    """)

    return md

# ---- Streamlit Frontend ----

st.set_page_config(page_title="IC-CSS 易時空決策系統 - Pro (V4.1)", layout="centered")
st.title("IC-CSS 易時空決策系統 — Pro (V4.1 精煉版)")
st.caption("策略先行·時空定性 · AI 輔助決策報告")

with st.sidebar:
    st.header("輸入參數")
    upper = st.selectbox("選擇上卦（上三爻）", list(TRIGRAMS.keys()), index=0)
    lower = st.selectbox("選擇下卦（下三爻）", list(TRIGRAMS.keys()), index=7)
    theme = st.selectbox("情境主題", THEMES, index=0)
    show_raw = st.checkbox("顯示原始卦數據 (debug) ", value=False)

# Validate combination
try:
    analysis = get_hexagram_data(upper, lower, theme)
except Exception as e:
    st.error(f"分析失敗：{e}")
    st.stop()

hexagram = analysis['hexagram']

# Main report structure
st.header("時空決策洞察 (V4.1)")
# Insight block (HTML)
st.markdown(analysis['insight_md'], unsafe_allow_html=True)

# 卦象結構：簡單六爻圖與上/下卦標注
st.subheader("卦象結構")
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"**卦名**：{hexagram['name']}  ")
    st.markdown(f"**標籤**：{hexagram['tag']}  ")
    st.markdown(f"**卦辭**：{hexagram['gua_ci']}  ")

# Draw six lines (倒序顯示，六爻從上到下為 6..1) with CSS highlighting
focus = hexagram['sec_dec_focus']

yao_lines = list(reversed(hexagram['yao_ci']))  # reversed for display 6..1

line_html = "<div class='yao-wrap' style='font-family:monospace;'>"
for l in yao_lines:
    idx = l['index']
    is_focus = (idx == focus)
    yin_yang_char = '——' if l['yin_yang'] == 1 else '— —'
    style = "padding:8px;margin:4px 0;border-radius:6px;"
    if is_focus:
        style += "background:linear-gradient(90deg, rgba(250,250,210,0.9), rgba(240,240,200,0.6));border:1px solid #d0b84c;"
    else:
        style += "background:transparent;border:1px solid rgba(0,0,0,0.05);"
    line_html += f"<div style='{style}'><strong>第{idx}爻</strong> {yin_yang_char} — {l['text']}</div>"
line_html += "</div>"

with col2:
    st.markdown(line_html, unsafe_allow_html=True)

# 卦象簡述與行動建議（倒序顯示六爻）
st.subheader("卦象簡述與行動建議")
for l in yao_lines:
    idx = l['index']
    st.markdown(f"**第{idx}爻** — {'陽' if l['yin_yang']==1 else '陰'}： {l['text']}")

# Final summary
st.subheader("最終目標總結")
st.markdown("**綜合建議**：" + analysis['five_element']['comment'])

if show_raw:
    st.subheader("(Debug) 原始資料")
    st.json(analysis)

st.markdown("---")
st.caption("建立者：IC-CSS Project · 請將本工具用作策略輔助，而非嚴格決策替代")

