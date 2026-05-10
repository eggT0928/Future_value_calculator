import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="오늘 소비의 미래가격 계산기",
    page_icon="💸",
    layout="centered"
)

# -----------------------------
# 기본 함수
# -----------------------------

def format_won(value):
    """금액을 원화 형식으로 변환한다."""
    return f"{value:,.0f}원"


def calc_future_value(present_value, annual_return, years):
    """현재 금액을 연복리 수익률로 굴렸을 때의 명목 미래가치를 계산한다."""
    return present_value * ((1 + annual_return) ** years)


def calc_real_value(future_value, inflation_rate, years):
    """명목 미래가치를 물가상승률로 할인해 현재가치로 환산한다."""
    return future_value / ((1 + inflation_rate) ** years)


def calc_future_price_by_inflation(present_value, inflation_rate, years):
    """현재 소비금액과 같은 구매력을 유지하려면 미래에 필요한 금액을 계산한다."""
    return present_value * ((1 + inflation_rate) ** years)


# -----------------------------
# 제목 영역
# -----------------------------

st.title("💸 오늘 소비의 미래가격 계산기")

st.markdown(
    """
    오늘 쓰는 돈은 단순한 지출이 아닐 수 있습니다.  
    같은 돈을 투자했다면 미래에 얼마가 되었을지 계산해보세요.
    
    예를 들어 오늘의 **10,000원 소비**는  
    10년 뒤, 20년 뒤, 30년 뒤에는 전혀 다른 의미가 될 수 있습니다.
    """
)

st.divider()

# -----------------------------
# 입력 영역
# -----------------------------

st.subheader("1️⃣ 기본 입력")

col1, col2 = st.columns(2)

with col1:
    expense = st.number_input(
        "현재 지출금",
        min_value=0,
        value=10000,
        step=1000,
        help="지금 소비하려는 금액을 입력하세요."
    )

with col2:
    years = st.number_input(
        "계산 기간",
        min_value=1,
        max_value=100,
        value=30,
        step=1,
        help="몇 년 뒤의 가치를 계산할지 입력하세요."
    )

col3, col4 = st.columns(2)

with col3:
    annual_return_percent = st.number_input(
        "연복리 기대수익률 (%)",
        min_value=0.0,
        max_value=50.0,
        value=7.0,
        step=0.1,
        help="투자했을 때 기대하는 연평균 수익률입니다."
    )

with col4:
    inflation_percent = st.number_input(
        "물가상승률 (%)",
        min_value=0.0,
        max_value=20.0,
        value=2.5,
        step=0.1,
        help="미래 돈의 구매력을 현재가치로 환산하기 위한 물가상승률입니다."
    )

annual_return = annual_return_percent / 100
inflation_rate = inflation_percent / 100

st.divider()

# -----------------------------
# 핵심 계산
# -----------------------------

future_value = calc_future_value(expense, annual_return, years)
real_value = calc_real_value(future_value, inflation_rate, years)
future_price = calc_future_price_by_inflation(expense, inflation_rate, years)

st.subheader("2️⃣ 계산 결과")

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label=f"{years}년 뒤 명목 미래가치",
        value=format_won(future_value)
    )

with metric_col2:
    st.metric(
        label="현재가치 기준",
        value=format_won(real_value)
    )

with metric_col3:
    st.metric(
        label=f"{years}년 뒤 같은 소비의 예상 가격",
        value=format_won(future_price)
    )

st.markdown(
    f"""
    ### 해석
    
    지금 **{format_won(expense)}**을 소비하지 않고  
    연 **{annual_return_percent:.1f}%**로 {years}년간 투자했다면,
    
    - 명목 금액으로는 약 **{format_won(future_value)}**
    - 물가상승률 **{inflation_percent:.1f}%**를 반영한 현재가치로는 약 **{format_won(real_value)}**
    - 지금의 {format_won(expense)}와 같은 구매력을 가진 소비는 {years}년 뒤 약 **{format_won(future_price)}**
    
    정도로 볼 수 있습니다.
    """
)

st.divider()

# -----------------------------
# 10년, 20년, 30년 비교표
# -----------------------------

st.subheader("3️⃣ 기간별 비교")

comparison_years = [1, 5, 10, 20, 30, 40]

rows = []

for y in comparison_years:
    nominal = calc_future_value(expense, annual_return, y)
    real = calc_real_value(nominal, inflation_rate, y)
    inflation_price = calc_future_price_by_inflation(expense, inflation_rate, y)

    rows.append({
        "기간": f"{y}년 뒤",
        "명목 미래가치": round(nominal),
        "현재가치 기준": round(real),
        "같은 소비의 미래 예상 가격": round(inflation_price)
    })

df = pd.DataFrame(rows)

st.dataframe(
    df.style.format({
        "명목 미래가치": "{:,.0f}원",
        "현재가치 기준": "{:,.0f}원",
        "같은 소비의 미래 예상 가격": "{:,.0f}원"
    }),
    use_container_width=True
)

# -----------------------------
# 차트
# -----------------------------

chart_years = list(range(1, years + 1))

chart_rows = []

for y in chart_years:
    nominal = calc_future_value(expense, annual_return, y)
    real = calc_real_value(nominal, inflation_rate, y)
    inflation_price = calc_future_price_by_inflation(expense, inflation_rate, y)

    chart_rows.append({
        "연도": y,
        "명목 미래가치": nominal,
        "현재가치 기준": real,
        "같은 소비의 미래 예상 가격": inflation_price
    })

chart_df = pd.DataFrame(chart_rows).set_index("연도")

st.subheader("4️⃣ 그래프로 보기")
st.line_chart(chart_df)

st.divider()

# -----------------------------
# 반복 지출 계산
# -----------------------------

st.subheader("5️⃣ 반복 지출까지 계산해보기")

st.markdown(
    """
    한 번의 소비보다 더 무서운 것은 반복되는 소비입니다.  
    매일, 매주, 매달 반복되는 지출이 장기적으로 어떤 기회비용을 만드는지도 계산해볼 수 있습니다.
    """
)

repeat_type = st.selectbox(
    "반복 주기",
    ["계산하지 않음", "매일", "매주", "매달", "매년"]
)

if repeat_type != "계산하지 않음":
    repeat_expense = st.number_input(
        "반복 지출 1회 금액",
        min_value=0,
        value=5000,
        step=1000,
        help="예: 매일 커피값 5,000원"
    )

    if repeat_type == "매일":
        annual_expense = repeat_expense * 365
    elif repeat_type == "매주":
        annual_expense = repeat_expense * 52
    elif repeat_type == "매달":
        annual_expense = repeat_expense * 12
    else:
        annual_expense = repeat_expense

    # 매년 말 같은 금액을 투자한다고 단순 가정한다.
    accumulated_future_value = 0

    for i in range(years):
        remaining_years = years - i
        accumulated_future_value += annual_expense * ((1 + annual_return) ** remaining_years)

    accumulated_real_value = calc_real_value(
        accumulated_future_value,
        inflation_rate,
        years
    )

    st.markdown(
        f"""
        ### 반복 지출 결과
        
        **{repeat_type} {format_won(repeat_expense)}**의 지출은  
        1년 기준으로 약 **{format_won(annual_expense)}**입니다.
        
        이 금액을 매년 투자했다고 단순 가정하면,
        
        - {years}년 뒤 명목 미래가치: **{format_won(accumulated_future_value)}**
        - 물가 반영 현재가치: **{format_won(accumulated_real_value)}**
        
        입니다.
        """
    )

st.divider()

# -----------------------------
# 안내 문구
# -----------------------------

st.caption(
    """
    ※ 이 계산기는 투자 권유가 아니라 소비의 기회비용을 이해하기 위한 교육용 도구입니다.  
    실제 수익률, 물가상승률, 세금, 수수료, 투자손실 가능성은 반영되지 않았습니다.
    """
)