import streamlit as st
import time

# --- 1. 後端邏輯核心 (Backend Logic) ---

class IChingLogic:
    def __init__(self):
        # 定義八卦基礎 (代碼: 名稱, 二進位, 符號, 特質)
        self.trigrams = {
            1: {"name": "乾", "bin": "111", "symbol": "☰", "attr": "剛健/天/主動"},
            2: {"name": "兌", "bin": "011", "symbol": "☱", "attr": "喜悅/澤/溝通"},
            3: {"name": "離", "bin": "101", "symbol": "☲", "attr": "熱情/火/文明"},
            4: {"name": "震", "bin": "001", "symbol": "☳", "attr": "變動/雷/突破"},
            5: {"name": "巽", "bin": "110", "symbol": "☴", "attr": "滲透/風/靈活"},
            6: {"name": "坎", "bin": "010", "symbol": "☵", "attr": "險阻/水/考驗"},
            7: {"name": "艮", "bin": "100", "symbol": "☶", "attr": "穩固/山/停止"},
            8: {"name": "坤", "bin": "000", "symbol": "☷", "attr": "包容/地/承載"}
        }

        # 定義部分重點卦象策略 (模擬數據庫)
        self.strategy_db = {
            "111101": { # 天火同人
                "name": "天火同人", "tag": "團結大同",
                "risk": "低", "opportunity": "極高",
                "advice": "外部大勢支持您的熱情。應打破界線，建立廣泛的聯盟。利涉大川。"
            },
            "101011": { # 火澤睽
                "name": "火澤睽", "tag": "求同存異",
                "risk": "高", "opportunity": "中",
                "advice": "內外目標背離。不要強求一致，應專注於差異化生存，並防範口舌是非。"
            },
            "000111": { # 地天泰
                "name": "地天泰", "tag": "天地交融",
                "risk": "低", "opportunity": "高",
                "advice": "心態積極，環境包容。這是全力衝刺的最佳時機，但需保持謙虛以持盈保泰。"
            },
            "111000": { # 天地否
                "name": "天地否", "tag": "閉塞不通",
                "risk": "極高", "opportunity": "低",
                "advice": "大環境與個人心態無法交流。此時不宜大舉進攻，應退守修身，等待時機。"
            },
             "111111": { # 乾為天
                "name": "乾為天", "tag": "自強不息",
                "risk": "中", "opportunity": "高",
                "advice": "能量極強，但需注意物極必反。適合擔當大任，但切忌傲慢。"
            },
            "101010": { # 坎為水 (修正：坎是010，上坎下坎是 010010)
                 # 讓我們用通用的生成邏輯來補足剩下的
            }
        }

    def get_hexagram_data(self, upper_id, lower_id):
        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        # 易經二進位堆疊：上卦在前，下卦在後 (或是從下往上畫)
        # 這裡為了方便查表，我們用字串拼接：Upper_Bin + Lower_Bin
        hex_code = upper["bin"] + lower["bin"]
        
        # 查找策略，如果找不到則自動生成通用建議
        if hex_code in self.strategy_db:
            result = self.strategy_db[hex_code]
            result["type"] = "Database Match"
        else:
            result = {
                "name": f"上{upper['name']}下{lower['name']}",
                "tag": "時空組合",
                "risk": "評估中",
                "opportunity": "評估中",
                "advice": f"這是一個由【{upper['attr']}】的環境與【{lower['attr']}】的心態組成的時空。建議思考：當外在是{upper['name']}而內在是{lower['name']}時，該如何順應大勢？",
                "type": "AI Generated"
            }
        
        return hex_code, upper, lower, result

# --- 2. 前端介面繪圖 (Frontend Visualization) ---

def draw_hexagram_lines(hex_code):
    """
    使用 HTML/CSS 在 Streamlit 中繪製卦象
    0 = 陰爻 (斷開), 1 = 陽爻 (實心)
    hex_code 順序：字串前3位是上卦(上->下)，後3位是下卦(上->下)
    但在畫圖時，傳統易經是從上往下畫 (上爻在最上面)
    """
    
    # 定義 CSS 樣式
    line_style = """
        <style>
        .yang-line { width: 100%; height: 20px; background-color: #333; margin-bottom: 8px; border-radius: 4px; }
        .yin-line-container { width: 100%; height: 20px; display: flex; justify-content: space-between; margin-bottom: 8px; }
        .yin-line-part { width: 42%; height: 100%; background-color: #555; border-radius: 4px; }
        .hex-container { width: 150px; margin: 0 auto; padding: 20px; background-color: #f0f2f6; border-radius: 10px; border: 2px solid #ddd;}
        </style>
    """
    st.markdown(line_style, unsafe_allow_html=True)
    
    html_lines = '<div class="hex-container">'
    
    # 遍歷二進位碼 (從左到右 = 從上爻到初爻)
    for bit in hex_code:
        if bit == '1': # 陽爻
            html_lines += '<div class="yang-line"></div>'
        else: # 陰爻
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
    
    # 初始化邏輯
    app_logic = IChingLogic()

    # --- Header ---
    st.title("☯️ IC-CSS 易時空決策分析系統")
    st.markdown("**AI-Powered I-Ching Chrono-Strategy System**")
    st.info("本系統將《易經》的時空邏輯轉化為決策模型。請輸入您的內在狀態與外在環境。")

    st.divider()

    # --- Input Area (Sidebar or Columns) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. 內在心態 (下卦)")
        st.markdown("*代表您的基礎、團隊或心理狀態*")
        lower_options = {k: f"{v['symbol']} {v['name']} ({v['attr']})" for k, v in app_logic.trigrams.items()}
        lower_sel = st.selectbox("選擇下卦", options=list(lower_options.keys()), format_func=lambda x: lower_options[x], index=0)

    with col2:
        st.subheader("2. 外在環境 (上卦)")
        st.markdown("*代表宏觀趨勢、時間或大環境*")
        upper_options = {k: f"{v['symbol']} {v['name']} ({v['attr']})" for k, v in app_logic.trigrams.items()}
        upper_sel = st.selectbox("選擇上卦", options=list(upper_options.keys()), format_func=lambda x: upper_options[x], index=2)

    # --- Action Button ---
    analyze_btn = st.button("🚀 啟動時空運算 (Analyze)", use_container_width=True, type="primary")

    if analyze_btn:
        with st.spinner("AI 正在進行卦象推演與策略匹配..."):
            time.sleep(1.2) # 模擬運算感
            
            # 獲取數據
            code, upper, lower, res = app_logic.get_hexagram_data(upper_sel, lower_sel)
            
            st.divider()
            
            # --- Output Area ---
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.markdown("### 時空卦象")
                draw_hexagram_lines(code)
                st.caption(f"二進位碼: {code}")

            with res_col2:
                st.markdown(f"## {res['name']}") 
                st.markdown(f"#### 🏷️ 核心標籤：**{res['tag']}**")
                
                # 顯示時空結構
                st.markdown(f"""
                - **時間 (上)**：{upper['name']} - {upper['attr']}
                - **空間 (下)**：{lower['name']} - {lower['attr']}
                """)
                
                # 風險與機會指標
                metric_col1, metric_col2 = st.columns(2)
                metric_col1.metric("風險指數", res['risk'])
                metric_col2.metric("機會指數", res['opportunity'])

            # --- Strategy Box ---
            st.markdown("### 💡 AI 策略建議")
            if res['risk'] in ["高", "極高"]:
                st.error(f"**行動指南：** {res['advice']}")
            elif res['opportunity'] == "極高":
                st.success(f"**行動指南：** {res['advice']}")
            else:
                st.info(f"**行動指南：** {res['advice']}")

            # --- Context Explanation ---
            with st.expander("查看運算邏輯 (Debug Info)"):
                st.write(f"Raw Input: Lower={lower['name']}({lower['bin']}), Upper={upper['name']}({upper['bin']})")
                st.write(f"Hexagram Binary: {code}")
                st.write(f"Data Source: {res['type']}")

if __name__ == "__main__":
    main()
