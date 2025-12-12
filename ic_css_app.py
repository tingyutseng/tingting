import streamlit as st
import time

# --- 1. 數據核心與邏輯引擎 (Backend Data & Logic) ---

class IChingLogic:
    def __init__(self):
        # A. 八卦基礎定義 (Key: 1-8)
        self.trigrams = {
            1: {"name": "乾", "bin": "111", "symbol": "☰", "element": "金"},
            2: {"name": "兌", "bin": "011", "symbol": "☱", "element": "金"},
            3: {"name": "離", "bin": "101", "symbol": "☲", "element": "火"},
            4: {"name": "震", "bin": "001", "symbol": "☳", "element": "木"},
            5: {"name": "巽", "bin": "110", "symbol": "☴", "element": "木"},
            6: {"name": "坎", "bin": "010", "symbol": "☵", "element": "水"},
            7: {"name": "艮", "bin": "100", "symbol": "☶", "element": "土"},
            8: {"name": "坤", "bin": "000", "symbol": "☷", "element": "土"}
        }

        # B. 8 大情境決策主題
        self.themes = {
            "1_事業策略": "目標確立、專案推進、市場競爭",
            "2_財務與投資": "資金流動、風險控制、資產配置",
            "3_核心關係": "情感穩定、伴侶溝通、家庭和睦",
            "4_社交與貴人": "人脈拓展、合作辨識、社交活動",
            "5_個人成長": "學習精進、心態調整、自我實現",
            "6_健康與福祉": "身心狀態、能量平衡、長期保健",
            "7_危機與風險": "突發事件處理、法律訴訟、止損轉機",
            "8_環境與變動": "遷徙適應、宏觀趨勢、地域變動"
        }
        
        # C. 128 個精確決策因子 (主題 x 卦 x 上/下位)
        # 此處數據結構為 {主題ID: {卦ID: {'upper': 描述, 'lower': 描述}, ...}, ...}
        # 由於內容極長，僅示範一小部分，您需手動或用 AI 補全此表。
        self.contextual_factors = {
            "1_事業策略": {
                1: {'upper': "宏觀經濟/業界領袖/大勢有利", 'lower': "剛健意志/決斷力/主導資源"}, # 乾
                2: {'upper': "資源缺口/溝通障礙/協議協商", 'lower': "語言表達/喜悅期待/資源互惠"}, # 兌
                3: {'upper': "品牌曝光/公關熱度/熱門產業", 'lower': "專案熱情/明確目標/主動推廣"}, # 離
                4: {'upper': "突發衝擊/技術變革/競爭者發動", 'lower': "積極行動/主動爭取/缺乏穩重"}, # 震
                5: {'upper': "趨勢漸進/外來影響/計畫緩慢", 'lower': "彈性/循序漸進/計畫執行力"}, # 巽
                6: {'upper': "潛在危機/市場風險/資源陷阱", 'lower': "擔憂/準備不足/缺乏方向"}, # 坎
                7: {'upper': "專案停滯/目標不變/區域限制", 'lower': "專注/謹慎/不願變通"}, # 艮
                8: {'upper': "市場基礎/後勤供應/合作環境", 'lower': "執行力/包容性/耐心與準備"}, # 坤
            },
            "2_財務與投資": {
                1: {'upper': "雄厚資本/牛市趨勢/政策利好", 'lower': "投資膽識/掌握主動權/大筆資金"}, # 乾
                # ... 請在此處補齊其他 7 個主題 x 8 個卦象的精確描述
            }
            # ... 為了程式碼長度，其餘 6 個主題的數據需補全
        }

        # D. 64 卦完整靜態數據庫 (卦辭與爻辭)
        # 這裡僅以「乾為天」和「坤為地」為例，其他 62 卦需補全。
        self.hexagram_data = {
            "111111": { # 乾為天
                "name": "乾為天", "tag": "自強不息",
                "gua_ci": "乾：元亨利貞。",
                "yao_ci": {
                    1: "初九：潛龍勿用。", 2: "九二：見龍在田，利見大人。", 3: "九三：君子終日乾乾，夕惕若，厲，無咎。", 
                    4: "九四：或躍在淵，無咎。", 5: "九五：飛龍在天，利見大人。", 6: "上九：亢龍有悔。"
                }
            },
            "000000": { # 坤為地
                "name": "坤為地", "tag": "厚德載物",
                "gua_ci": "坤：元亨，利牝馬之貞。君子有攸往，先迷後得主，利。西南得朋，東北喪朋。安貞，吉。",
                "yao_ci": {
                    1: "初六：履霜，堅冰至。", 2: "六二：直方大，不習，無不利。", 3: "六三：含章可貞。或從王事，無成有終。",
                    4: "六四：括囊，無咎，無譽。", 5: "六五：黃裳，元吉。", 6: "上六：戰龍於野，其血玄黃。"
                }
            },
            # --- 請在此處補齊其他 62 卦的數據 ---
            "111101": { 
                "name": "天火同人", "tag": "團結大同",
                "gua_ci": "同人：同人於野，亨。利涉大川，利君子貞。",
                "yao_ci": {
                    1: "初九：同人於門，無咎。", 2: "六二：同人於宗，吝。", 3: "九三：伏戎於莽，升其高陵，三歲不興。",
                    4: "九四：乘其墉，弗克攻，吉。", 5: "九五：同人，先號啕而後笑，大師克相遇。", 6: "上九：同人於郊，無悔。"
                }
            },
            # ... (其餘 61 卦的數據庫)
        }

    def get_hexagram_data(self, theme, upper_id, lower_id):
        # 獲取上下卦基礎信息
        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        hex_code = upper["bin"] + lower["bin"]
        
        # 獲取情境定義
        context_data = self.contextual_factors.get(theme, {})
        upper_ctx = context_data.get(upper_id, {}).get('upper', upper['name'])
        lower_ctx = context_data.get(lower_id, {}).get('lower', lower['name'])
        
        # 獲取卦象文本
        hex_data = self.hexagram_data.get(hex_code, {"name": "組合卦", "tag": "未知", "gua_ci": "數據缺失", "yao_ci": {}})
        
        # 模擬靜態風險評估 (基於五行相生相剋)
        risk_score = self._evaluate_static_risk(upper['element'], lower['element'])

        return hex_code, upper, lower, hex_data, upper_ctx, lower_ctx, risk_score

    def _evaluate_static_risk(self, u_elem, l_elem):
        # 五行相生相剋簡化判斷
        conflict = {('金', '木'), ('木', '土'), ('土', '水'), ('水', '火'), ('火', '金')}
        synergy = {('金', '水'), ('水', '木'), ('木', '火'), ('火', '土'), ('土', '金')}
        
        if (u_elem, l_elem) in conflict or (l_elem, u_elem) in conflict:
            return "高風險 (五行相剋)"
        elif (u_elem, l_elem) in synergy or (l_elem, u_elem) in synergy:
            return "低風險 (五行相生)"
        elif u_elem == l_elem:
            return "中風險 (能量疊加)"
        else:
            return "中風險 (穩定)"

# --- 2. 前端介面繪圖 (Frontend Visualization) ---

def draw_hexagram_lines(hex_code):
    # 此函數與之前版本一致，用於繪製卦象
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
    st.caption("最終靜態版：8 大主題 x 64 卦 x 128 個決策因子")
    st.markdown("---")

    # A. 步驟 1: 選擇主題情境
    st.subheader("1. 選擇決策主題情境")
    theme_options = {k: f"{k} ({v})" for k, v in app_logic.themes.items()}
    theme_sel = st.selectbox("請選擇您當前最關注的領域：", options=list(theme_options.keys()), format_func=lambda x: theme_options[x], index=0)

    st.markdown("---")

    # B. 步驟 2/3: 選擇上下卦
    st.subheader(f"2. 選擇「時空」要素 (主題: **{theme_sel}**)")
    col1, col2 = st.columns(2)
    
    # 獲取情境描述
    context_data = app_logic.contextual_factors.get(theme_sel, {})
    
    # 動態創建選項列表
    def format_trigram_option(idx):
        base_name = app_logic.trigrams[idx]['name']
        upper_desc = context_data.get(idx, {}).get('upper', '抽象定義')
        return f"{base_name} - {upper_desc}"
    
    def format_trigram_option_lower(idx):
        base_name = app_logic.trigrams[idx]['name']
        lower_desc = context_data.get(idx, {}).get('lower', '抽象定義')
        return f"{base_name} - {lower_desc}"

    with col1:
        st.markdown("#### 🚀 外在環境 (上卦)")
        st.markdown("*代表無法掌控的外部趨勢、挑戰或機會*")
        upper_sel = st.selectbox("選擇上卦：", options=list(app_logic.trigrams.keys()), format_func=format_trigram_option, index=1)

    with col2:
        st.markdown("#### 🧠 內在心態 (下卦)")
        st.markdown("*代表您可以掌控的內在資源、心態或基礎*")
        lower_sel = st.selectbox("選擇下卦：", options=list(app_logic.trigrams.keys()), format_func=format_trigram_option_lower, index=7)

    # C. 啟動按鈕
    analyze_btn = st.button("🔮 鎖定時空，生成決策報告", use_container_width=True, type="primary")

    if analyze_btn:
        with st.spinner(f"正在分析主題【{theme_sel}】下的時空組合..."):
            time.sleep(1) 
            
            code, upper, lower, hex_data, u_ctx, l_ctx, risk = app_logic.get_hexagram_data(theme_sel, upper_sel, lower_sel)
            
            st.markdown("---")
            
            # --- 報告區 ---
            st.header(f"📜 決策分析報告：{hex_data['name']}")
            
            res_c1, res_c2 = st.columns([1, 2])
            
            with res_c1:
                st.markdown("##### 卦象結構")
                draw_hexagram_lines(code)
                st.caption(f"上卦: {upper['name']} / 下卦: {lower['name']}")

            with res_c2:
                st.markdown(f"#### 🏷️ 核心標籤：**{hex_data['tag']}**")
                st.markdown(f"**五行判斷風險：** {risk}")
                
                st.markdown("##### 情境解讀")
                st.info(f"**在【{theme_sel}】主題下：**")
                st.markdown(f"- **外在環境 (上卦)**：**{upper['name']}** - *{u_ctx}*")
                st.markdown(f"- **內在心態 (下卦)**：**{lower['name']}** - *{l_ctx}*")

            st.markdown("---")

            # 4. 周易原文輸出
            st.subheader("📚 周易經典原文")
            
            # 卦辭
            st.markdown("##### 📜 卦辭 (對整體時空的定性)")
            st.success(hex_data.get('gua_ci', "此卦辭數據缺失。"))

            # 爻辭 (靜態輸出所有六條，供使用者參考)
            st.markdown("##### 〽️ 爻辭 (六條行動建議)")
            yao_ci = hex_data.get('yao_ci', {})
            
            if yao_ci:
                for i in range(1, 7):
                    yao_text = yao_ci.get(i, f"第 {i} 爻數據缺失。")
                    st.markdown(f"**[{app_logic.trigrams[lower_sel]['name'] if i <= 3 else app_logic.trigrams[upper_sel]['name']} 爻位 {i}]** {yao_text}")
            else:
                st.warning("此卦的爻辭數據庫尚未補全。")

# --- 執行區 ---
if __name__ == "__main__":
    main()
    
