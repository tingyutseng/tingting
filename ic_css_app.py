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
        
        # 五行相生相剋關係表
        self.element_relations = {
            ('金', '木'): '相剋 (衝突)', ('木', '土'): '相剋 (衝突)', ('土', '水'): '相剋 (衝突)', 
            ('水', '火'): '相剋 (衝突)', ('火', '金'): '相剋 (衝突)', 
            ('金', '水'): '相生 (助力)', ('水', '木'): '相生 (助力)', ('木', '火'): '相生 (助力)', 
            ('火', '土'): '相生 (助力)', ('土', '金'): '相生 (助力)', 
            ('金', '金'): '相同 (疊加)', ('木', '木'): '相同 (疊加)', ('水', '水'): '相同 (疊加)', 
            ('火', '火'): '相同 (疊加)', ('土', '土'): '相同 (疊加)'
        }

        # B. 8 大情境決策主題 (不變)
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
        
        # C. 128 個精確決策因子 (不變)
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
            "2_財務與投資": {k: {'upper': "外部財務狀況", 'lower': "個人投資心態"} for k in range(1, 9)},
            "3_核心關係": {k: {'upper': "外部情感環境", 'lower': "個人情感狀態"} for k in range(1, 9)},
            "4_社交與貴人": {k: {'upper': "外部人脈圈", 'lower': "個人社交主動性"} for k in range(1, 9)},
            "5_個人成長": {k: {'upper': "外部學習資源", 'lower': "個人學習心態"} for k in range(1, 9)},
            "6_健康與福祉": {k: {'upper': "外部環境影響", 'lower': "個人身體狀況"} for k in range(1, 9)},
            "7_危機與風險": {k: {'upper': "外部風險程度", 'lower': "個人應對準備"} for k in range(1, 9)},
            "8_環境與變動": {k: {'upper': "外部大環境趨勢", 'lower': "個人適應能力"} for k in range(1, 9)},
        }

        # D. 64 卦完整靜態數據庫 (V5.2 增加水火既濟: 010101)
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
            # --- 新增 水火既濟 (Hexagram 63) ---
            "010101": { 
                "name": "水火既濟", "tag": "成功守成", "gua_ci": "既濟：亨，小利貞。初吉終亂。",
                "yao_ci": {
                    1: "初九：曳其輪，濡其尾，無咎。 (【事業解讀】: 剛開始需謹慎慢行，即使遇到小障礙也能化解，保持謙虛。)", 
                    2: "六二：婦喪其茀，勿逐，七日得。 (【事業解讀】: 遇到小挫折或失去重要輔助，不需急躁追趕，保持耐心最終能恢復。)", 
                    3: "九三：高宗伐鬼方，三年克之，小人勿用。 (【事業解讀】: 專案必須堅決執行，但過程漫長充滿挑戰，決策者應當果斷，但要避免任用小人或走捷徑。)", 
                    4: "六四：繻有衣袽，終日戒。 (【事業解讀】: 已經達成階段性成功，但風險仍存。必須時刻保持警惕，不斷修補漏洞。)", 
                    5: "九五：東鄰殺牛，不如西鄰之禴祭，實受其福。 (【事業解讀】: 專案應重實質、輕形式。不求盛大浮誇，務求實際成效和誠意，方能獲得真正的回報。)", 
                    6: "上六：濡其首，厲。 (【事業解讀】: 成功達到極點，但過度深入，面臨溺水之危。應立即收手、放權或急流勇退，否則有災難。)"
                },
                "sec_dec_focus": 5 
            },
            # --- Pro 模型應在此處補齊其他 61 卦的數據 ---
        }

    # --- 核心邏輯函數 ---

    def get_hexagram_data(self, theme, upper_id, lower_id):
        current_theme = theme 
        
        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        hex_code = upper["bin"] + lower["bin"]
        
        context_data = self.contextual_factors.get(current_theme, {})
        u_ctx = context_data.get(upper_id, {}).get('upper', f"【{upper['name']}】抽象定義")
        l_ctx = context_data.get(lower_id, {}).get('lower', f"【{lower['name']}】抽象定義")
        
        # 如果數據庫中沒有該卦，返回一個帶有明確提示的佔位符
        hex_data = self.hexagram_data.get(hex_code, {
            "name": f"上{upper['name']}下{lower['name']}", 
            "tag": "數據缺失", 
            "gua_ci": "此卦辭數據缺失。", 
            "yao_ci": {}, 
            "sec_dec_focus": 1
        })
        
        risk_score, risk_desc, risk_color, elem_relation = self._evaluate_static_risk(upper['element'], lower['element'])
        is_se_ying_conflict = self._check_se_ying(hex_code)
        
        ai_insight = self._generate_ai_decision_insight(hex_data, upper, lower, risk_desc, current_theme, u_ctx, l_ctx, is_se_ying_conflict, elem_relation, risk_score)
        full_translation = self._generate_full_translation(hex_data)

        return hex_code, upper, lower, hex_data, u_ctx, l_ctx, risk_score, risk_desc, risk_color, is_se_ying_conflict, ai_insight, elem_relation, full_translation

    def _evaluate_static_risk(self, u_elem, l_elem):
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
        se_yao = hex_code[2] 
        ying_yao = hex_code[5] 
        
        if se_yao != ying_yao:
            return "世應相吸：內外狀態形成對比，有利於吸引資源或建立互補關係。"
        else:
            return "世應相斥/重疊：內外狀態相似，可能產生摩擦或力量難以借用，需靠自身力量。"

    def _generate_full_translation(self, hex_data):
        """V5.2：合併周易原文及其現代解讀為一個區塊。"""
        gua_ci = hex_data.get('gua_ci', "此卦辭數據缺失。")
        yao_ci = hex_data.get('yao_ci', {})
        
        if not yao_ci:
            # 當數據庫缺失時，給出清晰的提示
            return f"""
            <div style="background-color: #fff0f0; padding: 20px; border-radius: 8px; border: 1px solid #dc3545;">
                <h4 style="margin-top: 0; color: #dc3545;">🚨 數據庫警報：周易原文解讀缺失</h4>
                <p><strong>【卦名】</strong> {hex_data['name']} / <strong>【卦辭】</strong> {gua_ci}</p>
                <p>此卦的六爻數據庫尚未補全。請先補齊 <code>IChingLogic</code> 類中的 <code>self.hexagram_data</code> 才能生成完整的專業解讀和行動建議。</p>
            </div>
            """

        yao_list = []
        for i in range(1, 7):
            yao_text = yao_ci.get(i, f"第 {i} 爻數據缺失。")
            clean_yao_text = yao_text.split('(')[0].strip()
            yao_list.append(f"**[{i} 爻]** {clean_yao_text}")
        
        combined_yao_text = "\n\n".join(yao_list)
        
        all_interpretations = [
            line.split('(')[-1].strip(')').replace('【事業解讀】:', '').strip() 
            for line in yao_ci.values() if '【事業解讀】' in line
        ]
        
        if all_interpretations:
            professional_summary = " ".join(all_interpretations)
        else:
            professional_summary = "該卦爻辭數據庫缺乏現代應用解讀，請檢查數據結構。"
        
        # 最終輸出 (周易原文與專業解讀區塊)
        translation_html = f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef;">
            <h4 style="margin-top: 0; color: #1e8449;">📜 專業解讀：總體趨勢與階段策略</h4>
            <p style="line-height: 1.6;">{professional_summary}</p>
            
            <hr style="border-top: 1px dashed #ced4da;">
            
            <h5 style="color: #495057;">📖 周易原文 (便於記憶與查閱)</h5>
            <p style="font-style: italic; margin-bottom: 5px;">**【卦辭】** {gua_ci}</p>
            <details style="padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;">
                <summary>點擊展開六爻原文</summary>
                <div style="white-space: pre-wrap; margin-top: 10px; font-family: 'Noto Sans TC', sans-serif;">{combined_yao_text}</div>
            </details>
        </div>
        """
        return translation_html


    def _generate_ai_decision_insight(self, hex_data, upper, lower, risk_desc, theme, u_ctx, l_ctx, is_se_ying_conflict, elem_relation, risk_score):
        """V5.2 核心洞察區塊"""
        tag = hex_data['tag']
        name = hex_data['name']
        
        # 1. 時空定性開場
        if risk_desc.startswith("高度協調"):
            opening_tone = "「天助自助，相生共榮。」"
        elif risk_desc.startswith("結構衝突"):
            opening_tone = "「時與我爭，逆境方顯真英雄。」"
        elif risk_desc.startswith("能量疊加"):
            opening_tone = "「專注如一，勢可捲起千堆雪。」"
        else:
            opening_tone = "「萬物靜觀皆自得。」"
            
        # 2. 核心參數列表
        element_line = f"外在 **{upper['element']}** ({upper['name']}) 與內在 **{lower['element']}** ({lower['name']}) 呈 **{elem_relation}**。"
        context_line = f"當前外在趨勢：*{u_ctx}*；內在心態：*{l_ctx}*。"
        
        # 3. 核心行動原則
        if risk_desc.startswith("結構衝突"):
            action_principle = "面對結構衝突，核心原則應是：**先求止損，後謀變通。** 採取守勢，積蓄力量。"
        elif risk_desc.startswith("能量疊加"):
            action_principle = "您的行動力極強，核心原則應是：**知進知退，致中和，持盈保泰。** 謹防過度膨脹。"
        elif '相斥' in is_se_ying_conflict and risk_desc.startswith("高度協調"):
            action_principle = "氣場順暢但世應相斥，必須主動尋求外部互補。核心原則：**尋求合作，借力使力。**"
        else:
            action_principle = "在鎖定此時空後，您的核心行動原則應是：**保持自覺，遵循卦象爻辭的階段性指引。**"

        # V5.2 最終總結的 HTML 格式：第一大區塊
        final_insight = f"""
        <div style="background-color: #e6f7ff; border-radius: 12px; padding: 25px; border: 2px solid #007bff; box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #007bff;">🔮 【核心決策洞察】 ({name})</h3>
                <span style="background-color: #ffc107; color: #343a40; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 1em;">TAG: {tag}</span>
            </div>
            
            <p style="font-size: 1.2em; line-height: 1.7; font-style: italic;">{opening_tone} 您處於【{risk_score}】的時空結構。</p>
            
            <hr style="border-top: 1px solid #007bff;">
            
            <h5 style="color: #007bff;">🧭 時空結構分析</h5>
            <p><strong>五行協調度：</strong> {element_line}</p>
            <p><strong>情境與心態：</strong> {context_line}</p>
            <p><strong>世應關係：</strong> {is_se_ying_conflict}</p>
            
            <hr style="border-top: 1px solid #007bff;">
            
            <p style="font-size: 1.2em; font-weight: bold; color: #dc3545;">🎯 總體行動原則：</p>
            <p style="font-size: 1.1em;">{action_principle}</p>
        </div>
        """
        return final_insight


# --- 2. 前端介面繪圖 (Frontend Visualization) ---

def draw_hexagram_lines(hex_code):
    """繪製六爻圖 (維持 V4.1 邏輯)"""
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

    st.title("☯️ IC-CSS 易時空決策分析系統 V5.2")
    st.caption("報告結構優化：核心洞察區域化，原文解讀集中化。")
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
    analyze_btn = st.button("卜算 🔮", use_container_width=True, type="primary")

    if analyze_btn:
        with st.spinner(f"正在分析主題【{theme_sel}】下的時空組合..."):
            time.sleep(1) 
            
            code, upper, lower, hex_data, u_ctx, l_ctx, risk_score, risk_desc, risk_color, is_se_ying_conflict, ai_insight, elem_relation, full_translation = app_logic.get_hexagram_data(theme_sel, upper_sel, lower_sel)
            
            st.markdown("---")
            
            # --- 報告區 1: 核心洞察 ---
            st.header(f"📜 決策分析報告：{hex_data['name']}")
            st.markdown(ai_insight, unsafe_allow_html=True) # 第一大區塊

            st.markdown("---")

            # 結構展示 (移到中間位置)
            col_struct, col_info = st.columns([1, 2])
            
            with col_struct:
                st.markdown("##### 卦象結構")
                draw_hexagram_lines(code)
                st.caption(f"上卦: {upper['name']} / 下卦: {lower['name']} ({code})")
                
            with col_info:
                 st.markdown(f"#### 簡要總結")
                 st.info(f"此局勢標籤為【**{hex_data['tag']}**】。外在（時）與內在（空）五行呈**{elem_relation}**關係。")
                 st.markdown("##### 情境因子細節")
                 st.markdown(f"* 外在環境（上卦）：{u_ctx}")
                 st.markdown(f"* 內在心態（下卦）：{l_ctx}")

            st.markdown("---")
            
            # --- 報告區 2: 周易原文與專業解讀 (現在即使數據缺失也會顯示清晰的警告) ---
            st.markdown(full_translation, unsafe_allow_html=True) # 第二大區塊

# --- 執行區 ---
if __name__ == "__main__":
    main()
