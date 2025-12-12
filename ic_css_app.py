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
        
        # C. 128 個精確決策因子 (僅完整填入「事業策略」主題)
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
            # 為了程式碼簡潔，其餘 7 個主題使用通用定義
            "2_財務與投資": {k: {'upper': "外部財務狀況", 'lower': "個人投資心態"} for k in range(1, 9)},
            "3_核心關係": {k: {'upper': "外部情感環境", 'lower': "個人情感狀態"} for k in range(1, 9)},
            "4_社交與貴人": {k: {'upper': "外部人脈圈", 'lower': "個人社交主動性"} for k in range(1, 9)},
            "5_個人成長": {k: {'upper': "外部學習資源", 'lower': "個人學習心態"} for k in range(1, 9)},
            "6_健康與福祉": {k: {'upper': "外部環境影響", 'lower': "個人身體狀況"} for k in range(1, 9)},
            "7_危機與風險": {k: {'upper': "外部風險程度", 'lower': "個人應對準備"} for k in range(1, 9)},
            "8_環境與變動": {k: {'upper': "外部大環境趨勢", 'lower': "個人適應能力"} for k in range(1, 9)},
        }

        # D. 64 卦完整靜態數據庫 (包含乾為天完整的卦辭與爻辭)
        self.hexagram_data = {
            "111111": { # 乾為天 (完整的數據)
                "name": "乾為天", "tag": "自強不息", "risk_type": "疊加",
                "gua_ci": "乾：元亨利貞。",
                "yao_ci": {
                    1: "初九：潛龍勿用。 (【事業解讀】: 應沉潛學習、秘密籌備，不宜公開行動。)", 
                    2: "九二：見龍在田，利見大人。 (【事業解讀】: 實力已展現，應尋求外部支持，與業界領袖合作交流。)", 
                    3: "九三：君子終日乾乾，夕惕若，厲，無咎。 (【事業解讀】: 處於內外轉換壓力點，必須整日勤奮不懈，保持警惕才能化解危險。)", 
                    4: "九四：或躍在淵，無咎。 (【事業解讀】: 進退兩難的過渡期，可選擇躍升或退守觀望，保持彈性準備，進退皆無咎。)", 
                    5: "九五：飛龍在天，利見大人。 (【事業解讀】: 事業的最高成就點，領導力被市場認可，利於大規模行動，鞏固地位。)", 
                    6: "上九：亢龍有悔。 (【事業解讀】: 能量過度，已無路可退。必須學會急流勇退，主動放權或修正方向，否則將導致失敗和懊悔。)"
                },
                "sec_dec_focus": 5 # 決策焦點設定為 九五
            },
            "000000": { # 坤為地 (簡化數據)
                "name": "坤為地", "tag": "厚德載物", "risk_type": "疊加",
                "gua_ci": "坤：元亨，利牝馬之貞。君子有攸往，先迷後得主，利。",
                "yao_ci": {1: "初六：履霜，堅冰至。", 2: "六二：直方大，不習，無不利。", 3: "六三：含章可貞。", 4: "六四：括囊，無咎。", 5: "六五：黃裳，元吉。", 6: "上六：戰龍於野，其血玄黃。"},
                "sec_dec_focus": 2 # 決策焦點設定為 六二
            },
            # ... (其餘 62 卦的數據庫需要您後續補全)
        }

    def get_hexagram_data(self, theme, upper_id, lower_id):
        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        hex_code = upper["bin"] + lower["bin"]
        
        context_data = self.contextual_factors.get(theme, {})
        upper_ctx = context_data.get(upper_id, {}).get('upper', f"【{upper['name']}】抽象定義")
        lower_ctx = context_data.get(lower_id, {}).get('lower', f"【{lower['name']}】抽象定義")
        
        hex_data = self.hexagram_data.get(hex_code, {"name": f"上{upper['name']}下{lower['name']}", "tag": "數據缺失", "gua_ci": "此卦辭數據缺失。", "yao_ci": {}, "sec_dec_focus": 1})
        
        # --- 新增邏輯：氣場協調度 ---
        risk_score, risk_desc, risk_color = self._evaluate_static_risk(upper['element'], lower['element'])
        
        # --- 新增邏輯：世應關係解讀 ---
        # 世爻為下卦三爻，應爻為上卦三爻（六爻）
        is_se_ying_conflict = self._check_se_ying(hex_code)
        
        # --- 新增邏輯：AI 哲理總結 ---
        ai_summary = self._generate_ai_summary(hex_data, upper, lower, risk_desc, theme)

        return hex_code, upper, lower, hex_data, upper_ctx, lower_ctx, risk_score, risk_desc, risk_color, is_se_ying_conflict, ai_summary

    def _evaluate_static_risk(self, u_elem, l_elem):
        # 五行相生相剋簡化判斷 -> 轉換為氣場協調度
        conflict = {('金', '木'), ('木', '土'), ('土', '水'), ('水', '火'), ('火', '金')}
        synergy = {('金', '水'), ('水', '木'), ('木', '火'), ('火', '土'), ('土', '金')}
        
        if (u_elem, l_elem) in conflict or (l_elem, u_elem) in conflict:
            return "結構衝突", "結構衝突 (時與我爭，充滿挑戰和摩擦)", "error"
        elif (u_elem, l_elem) in synergy or (l_elem, u_elem) in synergy:
            return "高度協調", "高度協調 (天助自助，能量流動順暢)", "success"
        elif u_elem == l_elem:
            return "能量疊加", "能量疊加 (專注如一，力量集中但易趨於極端)", "warning"
        else:
            return "穩定中性", "穩定中性 (萬物靜觀皆自得，策略成功關鍵在穩健)", "info"

    def _check_se_ying(self, hex_code):
        # 世爻: 3爻 (hex_code[2]) 應爻: 6爻 (hex_code[5])
        se_yao = hex_code[2] # 0 for Yin, 1 for Yang
        ying_yao = hex_code[5] # 0 for Yin, 1 for Yang
        
        if se_yao != ying_yao:
            return "世應相吸：內外狀態形成對比，有利於吸引資源或建立互補關係。"
        else:
            return "世應相斥/重疊：內外狀態相似，可能產生摩擦或力量難以借用，需靠自身力量。"

    def _generate_ai_summary(self, hex_data, upper, lower, risk_desc, theme):
        # 簡單的 AI 哲理總結
        tag = hex_data['tag']
        name = hex_data['name']
        
        if risk_desc.startswith("高度協調"):
            return f"**決策的藝術：** 您處於【{tag}】的時空，內在與外在的氣場高度協調。成功並非是無盡的奔跑，而是知道如何順應這股協調之力，**讓天助自助。** 此時，應把握時機，大膽前行。"
        elif risk_desc.startswith("結構衝突"):
            return f"**決策的哲理：** 您正處於【{name}】的考驗。衝突本身就是轉機的開端。當環境與心態產生本質牴觸時，真正的勇氣並非硬碰硬，而是**在逆境中調整自身，方顯真英雄。** 務必採取保守策略。"
        elif risk_desc.startswith("能量疊加"):
            return f"**決策的提醒：** 【{tag}】的能量極強，勢可捲起千堆雪。力量集中是優勢，但也暗藏『亢龍有悔』的風險。請謹記，**致中和，守恆常，** 避免自滿或行動過激。"
        else:
            return f"**決策的穩健：** 在【{theme}】主題下，局勢相對穩定。此時的勝敗完全取決於您的穩健和細節的把握。**萬物靜觀皆自得，** 專注於您的基礎，以不變應萬變。"


# --- 2. 前端介面繪圖 (Frontend Visualization) (保持不變) ---
# ... (draw_hexagram_lines 函數保持不變)
def draw_hexagram_lines(hex_code):
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
        if bit == '1': 
            html_lines += '<div class="yang-line"></div>'
        else: 
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

    st.title("☯️ IC-CSS 易時空決策分析系統 V3.0")
    st.caption("引入氣場協調度、世應解讀與決策焦點")
    st.markdown("---")

    # A. 步驟 1: 選擇主題情境
    st.subheader("1. 選擇決策主題情境")
    theme_options = {k: f"{k} ({v})" for k, v in app_logic.themes.items()}
    theme_list = list(theme_options.keys())
    default_theme_index = theme_list.index("1_事業策略") if "1_事業策略" in theme_list else 0
    theme_sel = st.selectbox("請選擇您當前最關注的領域：", options=theme_list, format_func=lambda x: theme_options[x], index=default_theme_index)

    st.markdown("---")

    # B. 步驟 2/3: 選擇上下卦
    st.subheader(f"2. 選擇「時空」要素 (主題: **{theme_sel}**)")
    col1, col2 = st.columns(2)
    
    context_data = app_logic.contextual_factors.get(theme_sel, {})
    trigram_keys = list(app_logic.trigrams.keys()) 

    def format_trigram_option_upper(idx):
        base_name = app_logic.trigrams[idx]['name']
        upper_desc = context_data.get(idx, {}).get('upper', f"【{base_name}】抽象定義")
        return f"{app_logic.trigrams[idx]['symbol']} {base_name} - {upper_desc}"
    
    def format_trigram_option_lower(idx):
        base_name = app_logic.trigrams[idx]['name']
        lower_desc = context_data.get(idx, {}).get('lower', f"【{base_name}】抽象定義")
        return f"{app_logic.trigrams[idx]['symbol']} {base_name} - {lower_desc}"

    with col1:
        st.markdown("#### 🚀 外在環境 (上卦)")
        upper_sel = st.selectbox("選擇上卦：", options=trigram_keys, format_func=format_trigram_option_upper, index=0)

    with col2:
        st.markdown("#### 🧠 內在心態 (下卦)")
        lower_sel = st.selectbox("選擇下卦：", options=trigram_keys, format_func=format_trigram_option_lower, index=0)

    # C. 啟動按鈕
    analyze_btn = st.button("🔮 鎖定時空，生成決策報告", use_container_width=True, type="primary")

    if analyze_btn:
        with st.spinner(f"正在分析主題【{theme_sel}】下的時空組合..."):
            time.sleep(1) 
            
            # 獲取所有新的分析結果
            code, upper, lower, hex_data, u_ctx, l_ctx, risk_score, risk_desc, risk_color, is_se_ying_conflict, ai_summary = app_logic.get_hexagram_data(theme_sel, upper_sel, lower_sel)
            
            st.markdown("---")
            
            # --- 報告區 ---
            st.header(f"📜 決策分析報告：{hex_data['name']}")
            
            # 氣場總結區
            if risk_color == "success": st.success(ai_summary)
            elif risk_color == "warning": st.warning(ai_summary)
            else: st.info(ai_summary)
            
            st.markdown("---")

            # 結構與情境解讀
            res_c1, res_c2 = st.columns([1, 2])
            
            with res_c1:
                st.markdown("##### 卦象結構")
                draw_hexagram_lines(code)
                st.caption(f"上卦: {upper['name']} / 下卦: {lower['name']} ({code})")

            with res_c2:
                st.markdown(f"#### 🏷️ 核心標籤：**{hex_data['tag']}**")
                st.metric("時空氣場協調度", risk_score, risk_desc)
                
                st.markdown("##### 🔍 關係與時空因子")
                st.markdown(f"- **外在環境**：*{u_ctx}*")
                st.markdown(f"- **內在心態**：*{l_ctx}*")
                st.markdown(f"- **世應關係**：**{is_se_ying_conflict}**") # 新增世應解讀

            st.markdown("---")

            # 4. 周易原文輸出
            st.subheader("📚 周易經典原文與行動指引")
            
            # 卦辭
            st.markdown("##### 📜 卦辭 (對整體時空的定性)")
            st.info(hex_data.get('gua_ci', "此卦辭數據缺失。"))
            
            # 爻辭
            st.markdown("##### 〽️ 行動建議：決策焦點與六爻全覽")
            yao_ci = hex_data.get('yao_ci', {})
            
            if yao_ci:
                dec_focus = hex_data.get("sec_dec_focus")
                
                st.markdown("""
                <style>
                .yao-line { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 8px; border-left: 5px solid #007bff; }
                .focus-yao-line { background-color: #fff3cd; padding: 12px; border-radius: 6px; margin-bottom: 10px; border: 3px solid #ffc107; font-weight: bold; }
                </style>
                """, unsafe_allow_html=True)
                
                # 倒序顯示六爻，並高亮決策焦點
                for i in range(6, 0, -1):
                    yao_text = yao_ci.get(i, f"第 {i} 爻數據缺失。")
                    yao_pos = "上爻" if i == 6 else ("初爻" if i == 1 else f"第 {i} 爻")
                    pos_name = upper['name'] if i > 3 else lower['name']
                    
                    line_class = "focus-yao-line" if i == dec_focus else "yao-line"

                    st.markdown(
                        f'<div class="{line_class}">**[{pos_name} - {yao_pos}]** {yao_text}</div>', 
                        unsafe_allow_html=True
                    )
            else:
                st.warning("此卦的爻辭數據庫尚未補全。")

# --- 執行區 ---
if __name__ == "__main__":
    main()
