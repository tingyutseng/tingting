import streamlit as st
import time

# --- 1. 數據核心與邏輯引擎 (Backend Data & Logic) ---

class IChingLogic:
    """
    核心邏輯引擎：負責數據定義、五行/世應分析及 AI 決策洞察生成。
    """
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
        
        # 五行相生相剋關係表 (用於氣場警示)
        self.element_relations = {
            ('金', '木'): '相剋 (衝突)', ('木', '土'): '相剋 (衝突)', ('土', '水'): '相剋 (衝突)', 
            ('水', '火'): '相剋 (衝突)', ('火', '金'): '相剋 (衝突)', 
            ('金', '水'): '相生 (助力)', ('水', '木'): '相生 (助力)', ('木', '火'): '相生 (助力)', 
            ('火', '土'): '相生 (助力)', ('土', '金'): '相生 (助力)', 
            ('金', '金'): '相同 (疊加)', ('木', '木'): '相同 (疊加)', ('水', '水'): '相同 (疊加)', 
            ('火', '火'): '相同 (疊加)', ('土', '土'): '相同 (疊加)'
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
        
        # C. 128 個精確決策因子 (V4.1 要求: 填入「事業策略」，其餘使用通用定義)
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
            # 其餘 7 個主題的數據庫使用通用定義
            "2_財務與投資": {k: {'upper': "外部財務狀況", 'lower': "個人投資心態"} for k in range(1, 9)},
            "3_核心關係": {k: {'upper': "外部情感環境", 'lower': "個人情感狀態"} for k in range(1, 9)},
            "4_社交與貴人": {k: {'upper': "外部人脈圈", 'lower': "個人社交主動性"} for k in range(1, 9)},
            "5_個人成長": {k: {'upper': "外部學習資源", 'lower': "個人學習心態"} for k in range(1, 9)},
            "6_健康與福祉": {k: {'upper': "外部環境影響", 'lower': "個人身體狀況"} for k in range(1, 9)},
            "7_危機與風險": {k: {'upper': "外部風險程度", 'lower': "個人應對準備"} for k in range(1, 9)},
            "8_環境與變動": {k: {'upper': "外部大環境趨勢", 'lower': "個人適應能力"} for k in range(1, 9)},
        }

        # D. 64 卦完整靜態數據庫 (V4.1 要求: 乾為天/坤為地完整)
        self.hexagram_data = {
            "111111": { 
                "name": "乾為天", "tag": "自強不息", "gua_ci": "乾：元亨利貞。",
                "yao_ci": {
                    1: "初九：潛龍勿用。 (【事業解讀】: 應沉潛學習、秘密籌備，不宜公開行動。)", 
                    2: "九二：見龍在田，利見大人。 (【事業解讀】: 實力已展現，應尋求外部支持，與業界領袖合作交流。)", 
                    3: "九三：君子終日乾乾，夕惕若，厲，無咎。 (【事業解讀】: 處於內外轉換壓力點，必須整日勤奮不懈，保持警惕才能化解危險。)", 
                    4: "九四：或躍在淵，無咎。 (【事業解讀】: 進退兩難的過渡期，可選擇躍升或退守觀望，保持彈性準備，進退皆無咎。)", 
                    5: "九五：飛龍在天，利見大人。 (【事業解讀】: 事業的最高成就點，領導力被市場認可，利於大規模行動，鞏固地位。)", 
                    6: "上九：亢龍有悔。 (【事業解讀】: 能量過度，已無路可退。必須學會急流勇退，主動放權或修正方向，否則將導致失敗和懊悔。)"
                },
                "sec_dec_focus": 5 
            },
            "000000": { 
                "name": "坤為地", "tag": "厚德載物", "gua_ci": "坤：元亨，利牝馬之貞。君子有攸往，先迷後得主，利。",
                "yao_ci": {1: "初六：履霜，堅冰至。", 2: "六二：直方大，不習，無不利。", 3: "六三：含章可貞。", 4: "六四：括囊，無咎。", 5: "六五：黃裳，元吉。", 6: "上六：戰龍於野，其血玄黃。"},
                "sec_dec_focus": 2 
            },
            # --- Pro 模型應在此處補齊其他 62 卦的數據 ---
        }

    # --- 核心邏輯函數 ---

    def get_hexagram_data(self, theme, upper_id, lower_id):
        """主邏輯調度函數：執行三維分析並匯總結果。"""
        # 確保 theme 變數在函數範圍內穩定 (V4.1 修正點)
        current_theme = theme 
        
        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        hex_code = upper["bin"] + lower["bin"]
        
        # 情境因子（時空定性）
        context_data = self.contextual_factors.get(current_theme, {})
        u_ctx = context_data.get(upper_id, {}).get('upper', f"【{upper['name']}】抽象定義")
        l_ctx = context_data.get(lower_id, {}).get('lower', f"【{lower['name']}】抽象定義")
        
        hex_data = self.hexagram_data.get(hex_code, {"name": f"上{upper['name']}下{lower['name']}", "tag": "數據缺失", "gua_ci": "此卦辭數據缺失。", "yao_ci": {}, "sec_dec_focus": 1})
        
        # A. 氣場警示 (五行協調度)
        risk_score, risk_desc, risk_color, elem_relation = self._evaluate_static_risk(upper['element'], lower['element'])
        
        # B. 關係建議 (世應關係)
        is_se_ying_conflict = self._check_se_ying(hex_code)
        
        # C. 哲理總結生成
        ai_insight = self._generate_ai_decision_insight(hex_data, upper, lower, risk_desc, current_theme, u_ctx, l_ctx, is_se_ying_conflict, elem_relation)

        return hex_code, upper, lower, hex_data, u_ctx, l_ctx, risk_score, risk_desc, risk_color, is_se_ying_conflict, ai_insight, elem_relation

    def _evaluate_static_risk(self, u_elem, l_elem):
        """分析上/下卦五行關係，輸出風險分類和描述。"""
        relation_pair = (u_elem, l_elem)
        reverse_relation_pair = (l_elem, u_elem)
        
        relation = self.element_relations.get(relation_pair)
        if relation is None:
             relation = self.element_relations.get(reverse_relation_pair)

        if relation is None:
             if u_elem == l_elem:
                 relation = '相同 (疊加)'
             else:
                 return "穩定中性", "穩定中性 (萬物靜觀皆自得)", "info", "穩定中性"
                 
        if relation.startswith('相生'):
            return "高度協調", "高度協調 (天助自助，能量流動順暢)", "success", relation
        elif relation.startswith('相剋'):
            return "結構衝突", "結構衝突 (時與我爭，充滿挑戰和摩擦)", "error", relation
        elif relation.startswith('相同'):
            return "能量疊加", "能量疊加 (專注如一，力量集中但易趨於極端)", "warning", relation
        else:
            return "穩定中性", "穩定中性 (萬物靜觀皆自得)", "info", "穩定中性"


    def _check_se_ying(self, hex_code):
        """分析世應爻位 (3爻 vs 6爻) 的陰陽關係。"""
        se_yao = hex_code[2] 
        ying_yao = hex_code[5] 
        
        if se_yao != ying_yao:
            return "世應相吸：內外狀態形成對比，有利於吸引資源或建立互補關係。"
        else:
            return "世應相斥/重疊：內外狀態相似，可能產生摩擦或力量難以借用，需靠自身力量。"

    def _generate_ai_decision_insight(self, hex_data, upper, lower, risk_desc, theme, u_ctx, l_ctx, is_se_ying_conflict, elem_relation):
        """生成 V4.1 要求的精煉 HTML 決策洞察總結。"""
        tag = hex_data['tag']
        name = hex_data['name']
        
        # 1. 時空定性開場 (基於氣場警示)
        if risk_desc.startswith("高度協調"):
            opening = f"**「天助自助，相生共榮。」** 您處於【{tag}】的順流時空，內在與外在的氣場高度協調。此時機利於把握順流，事半功倍，但仍需智慧引導。"
        elif risk_desc.startswith("結構衝突"):
            opening = f"**「時與我爭，逆境方顯真英雄。」** 您正處於【{name}】的考驗。環境與心態存在本質牴觸，充滿挑戰和摩擦，需耗費大量心力來平衡，務必採取保守策略。"
        elif risk_desc.startswith("能量疊加"):
            opening = f"**「專注如一，勢可捲起千堆雪。」** 【{tag}】的能量極強，內外一致，力量集中是優勢，但也暗藏『亢龍有悔』的風險。請謹記，致中和，避免行動過激。"
        else:
            opening = f"**「萬物靜觀皆自得。」** 在【{theme}】主題下，局勢相對穩定。此時的勝敗完全取決於您的穩健和細節的把握，專注於您的基礎，以不變應萬變。"
            
        # 2. 氣場與情境分析 (核心參數列表)
        element_line = f"外在 **{upper['element']}** ({upper['name']}) 與內在 **{lower['element']}** ({lower['name']}) 呈 **{elem_relation}**。"
        context_line = f"當前您的外在趨勢為：*{u_ctx}*；內在心態為：*{l_ctx}*。"
        
        # 3. 核心行動原則 (基於氣場和世應的組合)
        if risk_desc.startswith("結構衝突"):
            action_principle = "面對結構衝突，核心原則應是：**先求止損，後謀變通。** 採取守勢，避免正面硬碰硬，積蓄力量以待時機。"
        elif risk_desc.startswith("能量疊加"):
            action_principle = "您的行動力極強，核心原則應是：**在行動前多加審視，知進知退，方能持盈保泰。** 謹防過度膨脹。"
        elif '相斥' in is_se_ying_conflict and risk_desc.startswith("高度協調"):
            action_principle = "雖然氣場順暢，但世應相斥，您必須主動與外部建立互補，不能單憑一己之力。核心原則：**尋求合作，借力使力。**"
        else:
            action_principle = "在鎖定此時空後，您的核心行動原則應是：**保持自覺，遵循卦象爻辭的階段性指引。**"

        # 最終總結的 HTML 格式 (符合 V4.1 輸出要求)
        final_insight = f"""
        <div style="background-color: #f0f8ff; border-radius: 10px; padding: 20px; border: 1px solid #cceeff;">
            <h4 style="margin-top: 0; color: #007bff;">【時空決策洞察】 (核心標籤: {tag})</h4>
            <p style="font-size: 1.1em; line-height: 1.6;">{opening}</p>
            
            <hr style="border-top: 1px solid #cceeff;">
            
            <p><strong>五行協調度：</strong> {element_line}</p>
            <p><strong>情境分析：：</strong> {context_line}</p>
            <p><strong>世應關係：</strong> {is_se_ying_conflict}</p>
            
            <hr style="border-top: 1px solid #cceeff;">
            
            <p style="font-size: 1.1em; font-weight: bold; color: #dc3545;">核心行動原則：</p>
            <p>{action_principle}</p>
        </div>
        """
        return final_insight


# --- 2. 前端介面繪圖 (Frontend Visualization) ---

def draw_hexagram_lines(hex_code):
    """繪製六爻圖 (符合報告結構要求)"""
    # 
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

    st.title("☯️ IC-CSS 易時空決策分析系統 V4.1 (Pro Model)")
    st.caption("核心分析精煉化：融合五行、世應與情境因子的策略輸出。")
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
        st.markdown("#### 🚀 外在環境 (上卦 / 時)")
        upper_sel = st.selectbox("選擇上卦：", options=trigram_keys, format_func=format_trigram_option_upper, index=0)

    with col2:
        st.markdown("#### 🧠 內在心態 (下卦 / 空)")
        lower_sel = st.selectbox("選擇下卦：", options=trigram_keys, format_func=format_trigram_option_lower, index=0)

    # C. 啟動按鈕
    analyze_btn = st.button("🔮 鎖定時空，生成決策報告", use_container_width=True, type="primary")

    if analyze_btn:
        with st.spinner(f"正在分析主題【{theme_sel}】下的時空組合..."):
            time.sleep(1) 
            
            code, upper, lower, hex_data, u_ctx, l_ctx, risk_score, risk_desc, risk_color, is_se_ying_conflict, ai_insight, elem_relation = app_logic.get_hexagram_data(theme_sel, upper_sel, lower_sel)
            
            st.markdown("---")
            
            # --- 報告區 ---
            st.header(f"📜 決策分析報告：{hex_data['name']}")
            
            # V4.1 核心總結：【時空決策洞察】
            st.markdown(ai_insight, unsafe_allow_html=True)
            
            st.markdown("---")

            # 結構展示 (符合報告結構要求)
            col_struct, col_info = st.columns([1, 2])
            
            with col_struct:
                st.markdown("##### 卦象結構")
                draw_hexagram_lines(code)
                st.caption(f"上卦: {upper['name']} / 下卦: {lower['name']} ({code})")
                
            with col_info:
                 st.markdown(f"#### 🏷️ 核心標籤：**{hex_data['tag']}**")
                 st.metric("時空氣場協調度", risk_score, elem_relation) 
                 st.markdown("##### 卦象簡述 (周易卦辭)")
                 st.info(hex_data.get('gua_ci', "此卦辭數據缺失。"))

            st.markdown("---")

            # 4. 行動建議 (高亮決策焦點)
            st.subheader("〽️ 行動建議：決策焦點與六爻全覽")
            
            yao_ci = hex_data.get('yao_ci', {})
            
            if yao_ci:
                dec_focus = hex_data.get("sec_dec_focus")
                
                # CSS 樣式 (高亮決策焦點)
                st.markdown("""
                <style>
                .yao-line { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 8px; border-left: 5px solid #007bff; }
                .focus-yao-line { background-color: #fff3cd; padding: 12px; border-radius: 6px; margin-bottom: 10px; border: 3px solid #ffc107; font-weight: bold; }
                </style>
                """, unsafe_allow_html=True)
                
                # 倒序顯示六爻
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
