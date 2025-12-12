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

        # 五行相生相剋關係表 (用於氣場協調度判斷)
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

        # C. 主題 → 八卦對應敘述
        self.contextual_factors = {
            "1_事業策略": {
                1: {'upper': "宏觀經濟/業界領袖/大勢有利", 'lower': "剛健意志/決斷力/主導資源"},
                2: {'upper': "資源缺口/溝通障礙/協議協商", 'lower': "語言表達/喜悅期待/資源互惠"},
                3: {'upper': "品牌曝光/公關熱度/熱門產業", 'lower': "專案熱情/明確目標/主動推廣"},
                4: {'upper': "突發衝擊/技術變革/競爭者發動", 'lower': "積極行動/主動爭取/缺乏穩重"},
                5: {'upper': "趨勢漸進/外來影響/計畫緩慢", 'lower': "彈性/循序漸進/計畫執行力"},
                6: {'upper': "潛在危機/市場風險/資源陷阱", 'lower': "擔憂/準備不足/缺乏方向"},
                7: {'upper': "專案停滯/目標不變/區域限制", 'lower': "專注/謹慎/不願變通"},
                8: {'upper': "市場基礎/後勤供應/合作環境", 'lower': "執行力/包容性/耐心與準備"},
            },
            # 其餘主題共用
            "2_財務與投資": {k: {'upper': "外部財務狀況", 'lower': "個人投資心態"} for k in range(1, 9)},
            "3_核心關係": {k: {'upper': "外部情感環境", 'lower': "個人情感狀態"} for k in range(1, 9)},
            "4_社交與貴人": {k: {'upper': "外部人脈圈", 'lower': "個人社交主動性"} for k in range(1, 9)},
            "5_個人成長": {k: {'upper': "外部學習資源", 'lower': "個人學習心態"} for k in range(1, 9)},
            "6_健康與福祉": {k: {'upper': "外部環境影響", 'lower': "個人身體狀況"} for k in range(1, 9)},
            "7_危機與風險": {k: {'upper': "外部風險程度", 'lower': "個人應對準備"} for k in range(1, 9)},
            "8_環境與變動": {k: {'upper': "外部大環境趨勢", 'lower': "個人適應能力"} for k in range(1, 9)},
        }

        # D. 卦辭資料庫（示例）
        self.hexagram_data = {
            "111111": { 
                "name": "乾為天", "tag": "自強不息", 
                "gua_ci": "乾：元亨利貞。",
                "yao_ci": {
                    1: "初九：潛龍勿用。",
                    2: "九二：見龍在田，利見大人。",
                    3: "九三：君子終日乾乾，夕惕若，厲，無咎。",
                    4: "九四：或躍在淵，無咎。",
                    5: "九五：飛龍在天，利見大人。",
                    6: "上九：亢龍有悔。"
                },
                "sec_dec_focus": 5 
            },
            "000000": {
                "name": "坤為地", "tag": "厚德載物",
                "gua_ci": "坤：元亨，利牝馬之貞。",
                "yao_ci": {},
                "sec_dec_focus": 2
            }
        }

    # --- 核心邏輯函數 ---

    def get_hexagram_data(self, theme, upper_id, lower_id):
        current_theme = theme

        upper = self.trigrams[upper_id]
        lower = self.trigrams[lower_id]
        hex_code = upper["bin"] + lower["bin"]

        # 取得主題語境
        context_data = self.contextual_factors.get(current_theme, {})
        upper_ctx = context_data.get(upper_id, {}).get('upper', f"【{upper['name']}】抽象定義")
        lower_ctx = context_data.get(lower_id, {}).get('lower', f"【{lower['name']}】抽象定義")

        # 卦辭資料
        hex_data = self.hexagram_data.get(
            hex_code,
            {"name": f"上{upper['name']}下{lower['name']}", 
             "tag": "數據缺失", 
             "gua_ci": "此卦辭數據缺失。",
             "yao_ci": {},
             "sec_dec_focus": 1}
        )

        # 五行風險
        risk_score, risk_desc, risk_color, elem_relation = self._evaluate_static_risk(
            upper["element"], lower["element"]
        )

        # 世應
        is_se_ying_conflict = self._check_se_ying(hex_code)

        # AI 決策洞察
        ai_insight = self._generate_ai_decision_insight(
            hex_data, upper, lower, risk_desc,
            current_theme, upper_ctx, lower_ctx,
            is_se_ying_conflict, elem_relation
        )

        return (
            hex_code, upper, lower, hex_data,
            upper_ctx, lower_ctx,
            risk_score, risk_desc, risk_color,
            is_se_ying_conflict, ai_insight, elem_relation
        )

    def _evaluate_static_risk(self, u_elem, l_elem):
        relation_pair = (u_elem, l_elem)
        reverse_relation_pair = (l_elem, u_elem)

        relation = self.element_relations.get(relation_pair)
        if relation is None:
            relation = self.element_relations.get(reverse_relation_pair)

        if relation is None:
            if u_elem == l_elem:
                relation = "相同 (疊加)"
            else:
                return "穩定中性", "穩定中性 (萬物靜觀皆自得)", "info", "穩定中性"

        if relation.startswith("相生"):
            return "高度協調", "高度協調 (天助自助，能量順暢)", "success", relation
        elif relation.startswith("相剋"):
            return "結構衝突", "結構衝突 (時與我爭，挑戰提升)", "error", relation
        elif relation.startswith("相同"):
            return "能量疊加", "能量疊加 (力量集中但易極端)", "warning", relation

        return "穩定中性", "穩定中性 (萬物靜觀皆自得)", "info", "穩定中性"

    def _check_se_ying(self, hex_code):
        se_yao = hex_code[2]
        ying_yao = hex_code[5]

        if se_yao != ying_yao:
            return "世應相吸：互補、有利於合作。"
        else:
            return "世應相斥：內外同質，較難借力。"

    def _generate_ai_decision_insight(
        self, hex_data, upper, lower, risk_desc,
        theme, upper_ctx, lower_ctx,
        se_ying_desc, elem_relation
    ):
        name = hex_data["name"]
        tag = hex_data["tag"]

        opening = f"您目前位於 **{name}（{tag}）** 的時空格局中。"
        env = f"外在狀態（上卦 {upper['name']}）→ {upper_ctx}"
        inner = f"內在狀態（下卦 {lower['name']}）→ {lower_ctx}"
        risk = f"五行氣場：{elem_relation}，屬於 **{risk_desc}**。"
        seying = f"世應關係：{se_ying_desc}"

        return f"{opening}\n\n{env}\n\n{inner}\n\n{risk}\n\n{seying}"

