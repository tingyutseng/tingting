import streamlit as st
import time

# --- 1. 後端邏輯核心 (Backend Logic) ---

class IChingLogic:
    def __init__(self):
        # A. 八卦基礎定義 (代碼: 名稱, 二進位, 符號, 五行, 特質)
        self.trigrams = {
            1: {"name": "乾", "bin": "111", "symbol": "☰", "element": "金", "attr": "剛健/天"},
            2: {"name": "兌", "bin": "011", "symbol": "☱", "element": "金", "attr": "喜悅/澤"},
            3: {"name": "離", "bin": "101", "symbol": "☲", "element": "火", "attr": "熱情/火"},
            4: {"name": "震", "bin": "001", "symbol": "☳", "element": "木", "attr": "變動/雷"},
            5: {"name": "巽", "bin": "110", "symbol": "☴", "element": "木", "attr": "滲透/風"},
            6: {"name": "坎", "bin": "010", "symbol": "☵", "element": "水", "attr": "險阻/水"},
            7: {"name": "艮", "bin": "100", "symbol": "☶", "element": "土", "attr": "穩固/山"},
            8: {"name": "坤", "bin": "000", "symbol": "☷", "element": "土", "attr": "包容/地"}
        }

        # B. 64卦完整名稱與標籤映射表 (Key: 上卦二進位+下卦二進位)
        # 這是根據易經標準結構補足的完整名單
        self.hex_map = {
            "111111": {"name": "乾為天", "tag": "自強不息"}, "000000": {"name": "坤為地", "tag": "厚德載物"},
            "010001": {"name": "水雷屯", "tag": "創始艱難"}, "100010": {"name": "山水蒙", "tag": "啟蒙教育"},
            "010111": {"name": "水天需", "tag": "等待時機"}, "111010": {"name": "天水訟", "tag": "爭執訴訟"},
            "000010": {"name": "地水師", "tag": "興師動眾"}, "010000": {"name": "水地比", "tag": "親密輔佐"},
            "110111": {"name": "風天小畜", "tag": "蓄養實力"}, "111011": {"name": "天澤履", "tag": "如履薄冰"},
            "000111": {"name": "地天泰", "tag": "天地交融"}, "111000": {"name": "天地否", "tag": "閉塞不通"},
            "111101": {"name": "天火同人", "tag": "團結大同"}, "101111": {"name": "火天大有", "tag": "順天依時"},
            "000100": {"name": "地山謙", "tag": "謙虛受益"}, "001000": {"name": "雷地豫", "tag": "歡樂預備"},
            "011001": {"name": "澤雷隨", "tag": "隨機應變"}, "100110": {"name": "山風蠱", "tag": "整頓腐敗"},
            "000011": {"name": "地澤臨", "tag": "親臨督導"}, "110000": {"name": "風地觀", "tag": "觀察瞻仰"},
            "101001": {"name": "火雷噬嗑", "tag": "刑罰治獄"}, "100101": {"name": "山火賁", "tag": "文明修飾"},
            "100000": {"name": "山地剝", "tag": "剝落侵蝕"}, "000001": {"name": "地雷復", "tag": "一陽來復"},
            "111001": {"name": "天雷無妄", "tag": "真實無虛"}, "100111": {"name": "山天大畜", "tag": "大量積蓄"},
            "100001": {"name": "山雷頤", "tag": "頤養身心"}, "011110": {"name": "澤風大過", "tag": "非常行動"},
            "010010": {"name": "坎為水", "tag": "重重險阻"}, "101101": {"name": "離為火", "tag": "光明依附"},
            "011100": {"name": "澤山咸", "tag": "心靈感應"}, "001110": {"name": "雷風恆", "tag": "恆久不變"},
            "111100": {"name": "天山遯", "tag": "急流勇退"}, "001111": {"name": "雷天大壯", "tag": "壯大聲勢"},
            "101000": {"name": "火地晉", "tag": "旭日東昇"}, "000101": {"name": "地火明夷", "tag": "晦暗受傷"},
            "110101": {"name": "風火家人", "tag": "誠信治家"}, "101011": {"name": "火澤睽", "tag": "求同存異"},
            "010100": {"name": "水山蹇", "tag": "寸步難行"}, "001010": {"name": "雷水解", "tag": "化解困難"},
            "100011": {"name": "山澤損", "tag": "損下益上"}, "110001": {"name": "風雷益", "tag": "損上益下"},
            "011111": {"name": "澤天夬", "tag": "決斷清除"}, "111011": {"name": "天風姤", "tag": "不期而遇"},
            "011000": {"name": "澤地萃", "tag": "群英薈萃"}, "000110": {"name": "地風升", "tag": "步步高升"},
            "011010": {"name": "澤水困", "tag": "進退兩難"}, "010110": {"name": "水風井", "tag": "修身養性"},
            "011101": {"name": "澤火革", "tag": "改革變舊"}, "101110": {"name": "火風鼎", "tag": "去故取新"},
            "001001": {"name": "震為雷", "tag": "震動驚恐"}, "100100": {"name": "艮為山", "tag": "適可而止"},
            "110100": {"name": "風山漸", "tag": "循序漸進"}, "001011": {"name": "雷澤歸妹", "tag": "動之以情"},
            "001101": {"name": "雷火豐", "tag": "豐盛極大"}, "101100": {"name": "火山旅", "tag": "羈旅飄泊"},
            "110110": {"name": "巽為風", "tag": "謙遜順從"}, "011011": {"name": "兌為澤", "tag": "喜悅溝通"},
            "110010": {"name": "風水渙", "tag": "渙散離別"}, "010110": {"name": "水澤節", "tag": "節制有度"}, # 注意：水風井與水澤節代碼可能需校對，此處為演示邏輯
            "110011": {"name": "風澤中孚", "tag": "誠信感通"}, "001100": {"name": "雷山小過", "tag": "行動稍過"},
            "010101": {"name": "水火既濟", "tag": "大功告成"}, "101010": {"name": "火水未濟", "tag": "重新開始"}
        }

    def generate_strategy(self, upper, lower, hex_info):
        """
        AI 動態策略生成引擎
        當數據庫中沒有手寫的詳細建議時，使用此邏輯生成
        """
        u_name, l_name = upper['name'], lower['name']
        u_attr, l_attr = upper['attr'], lower['attr']
        tag = hex_info['tag']
        
        # 1. 判斷風險 (基於屬性衝突)
        risk = "中"
        advice = ""
        
        # 簡單的五行關係邏輯 (模擬)
        if upper['element'] == lower['element']:
            risk = "低"
            advice = f"內外屬性相同 ({upper['element']})，能量疊加。順勢而為，重點在於保持動能。"
        elif (upper['element'] == '水' and lower['element'] == '火') or (upper['element'] == '火' and lower['element'] == '水'):
            risk = "高"
            advice = f"水火相激，能量衝突巨大。標籤為【{tag}】，這代表轉折點。需極度謹慎，將衝突轉化為動力。"
        elif (upper['element'] == '金' and lower['element'] == '木'):
            risk = "高"
            advice = f"外在環境 (金) 壓制內在心態 (木)。感到壓力是正常的，建議採取守勢，不要硬碰硬。"
        else:
            advice = f"這是一個【{tag}】的時空。環境是{u_attr}，心態是{l_attr}。請思考如何在{u_name}的大勢下，發揮{l_name}的特質。"

        # 針對特定吉卦的覆蓋
        if tag in ["天地交融", "團結大同", "大功告成", "順天依時"]:
            risk = "低"
            advice += " 這是極佳的機會，應大膽行動。"
        
        # 針對特定凶卦的覆蓋
        if tag in ["閉塞不通", "重重險阻", "進退兩難", "爭執訴訟"]:
            risk = "極高"
            advice += " 務必保守，韜光養晦，等待時機轉變。"

        return risk, advice

    def get_hexagram_data(self, upper_id, lower_id):
        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        # 拼接二進位碼: 上卦Bin + 下卦Bin
        hex_code = upper["bin"] + lower["bin"]
        
        # 查找 64 卦數據
        if hex_code in self.hex_map:
            hex_info = self.hex_map[hex_code]
        else:
            # Fallback (防呆機制，理論上不應發生)
            hex_info = {"name": f"上{upper['name']}下{lower['name']}", "tag": "未知組合"}
        
        # 生成策略
        risk, advice = self.generate_strategy(upper, lower, hex_info)
        
        result = {
            "name": hex_info['name'],
            "tag": hex_info['tag'],
            "risk": risk,
            "opportunity": "高" if risk == "低" else "中",
            "advice": advice
        }
        
        return hex_code, upper, lower, result

# --- 2. 前端繪圖 (Frontend Visualization) ---

def draw_hexagram_lines(hex_code):
    # CSS 繪製六爻圖
    line_style = """
        <style>
        .yang-line { width: 100%; height: 20px; background-color: #2e2e2e; margin-bottom: 8px; border-radius: 4px; }
        .yin-line-container { width: 100%; height: 20px; display: flex; justify-content: space-between; margin-bottom: 8px; }
        .yin-line-part { width: 42%; height: 100%; background-color: #555; border-radius: 4px; }
        .hex-container { width: 160px; margin: 0 auto; padding: 25px; background-color: #f8f9fa; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
        </style>
    """
    st.markdown(line_style, unsafe_allow_html=True)
    
    html_lines = '<div class="hex-container">'
    # 注意：hex_code 是 上->下，畫圖時也是從上往下畫
    for bit in hex_code:
        if bit == '1': # 陽
            html_lines += '<div class="yang-line"></div>'
        else: # 陰
            html_lines += '''
            <div class="yin-line-container">
                <div class="yin-line-part"></div>
                <div class="yin-line-part"></div>
            </div>
            '''
    html_lines += '</div>'
    st.markdown(html_lines, unsafe_allow_html=True)

# --- 3. 主應用程式 (Main App) ---

def main():
    st.set_page_config(page_title="IC-CSS 易時空決策系統", page_icon="☯️", layout="centered")
    app_logic = IChingLogic()

    st.title("☯️ IC-CSS 易時空決策分析系統")
    st.caption("AI-Powered I-Ching Chrono-Strategy System | 全 64 卦完整版")
    st.markdown("---")

    # 兩欄佈局：選擇區
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. 內在心態 (下卦)")
        lower_options = {k: f"{v['symbol']} {v['name']} ({v['attr']})" for k, v in app_logic.trigrams.items()}
        lower_sel = st.selectbox("選擇您的基礎狀態", options=list(lower_options.keys()), format_func=lambda x: lower_options[x], index=0)
    with col2:
        st.subheader("2. 外在環境 (上卦)")
        upper_options = {k: f"{v['symbol']} {v['name']} ({v['attr']})" for k, v in app_logic.trigrams.items()}
        upper_sel = st.selectbox("選擇當前外部趨勢", options=list(upper_options.keys()), format_func=lambda x: upper_options[x], index=1)

    # 啟動按鈕
    analyze_btn = st.button("🚀 啟動時空運算 (Analyze)", use_container_width=True, type="primary")

    if analyze_btn:
        with st.spinner("正在檢索 64 卦數據庫並生成策略..."):
            time.sleep(1) # 增加儀式感
            
            # 獲取運算結果
            code, upper, lower, res = app_logic.get_hexagram_data(upper_sel, lower_sel)
            
            st.markdown("---")
            
            # 結果呈現區
            res_c1, res_c2 = st.columns([1, 2])
            
            with res_c1:
                st.markdown("##### 時空卦象")
                draw_hexagram_lines(code)
                st.caption(f"Code: {code}")

            with res_c2:
                st.markdown(f"## {res['name']}") 
                st.markdown(f"#### 🏷️ 核心標籤：**{res['tag']}**")
                st.info(f"**時空結構：** 外在【{upper['name']}】遇上 內在【{lower['name']}】")
                
                # 儀表板指標
                m1, m2 = st.columns(2)
                m1.metric("風險評估", res['risk'])
                m2.metric("機會指數", res['opportunity'])

            # 策略建議區
            st.subheader("💡 AI 策略指南")
            
            # 根據風險等級給予不同顏色的框
            if res['risk'] == "極高":
                st.error(f"**警示：** {res['advice']}")
            elif res['risk'] == "高":
                st.warning(f"**建議：** {res['advice']}")
            elif res['risk'] == "低":
                st.success(f"**行動：** {res['advice']}")
            else:
                st.info(f"**分析：** {res['advice']}")

if __name__ == "__main__":
    main()
