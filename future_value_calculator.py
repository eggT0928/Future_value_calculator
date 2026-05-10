import streamlit as st
import pandas as pd


# =========================================================
# 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="오늘 소비의 미래 기회비용 계산기",
    page_icon="💸",
    layout="centered"
)


# =========================================================
# 계산 함수
# =========================================================

def format_won(value: float) -> str:
    """금액을 원화 형식 문자열로 변환한다."""
    return f"{value:,.0f}원"


def calc_future_value(present_value: float, annual_return: float, years: int) -> float:
    """현재 금액을 연복리 수익률로 굴렸을 때의 명목 미래가치를 계산한다."""
    return present_value * ((1 + annual_return) ** years)


def calc_real_value(future_value: float, inflation_rate: float, years: int) -> float:
    """명목 미래가치를 물가상승률로 할인해 현재가치로 환산한다."""
    return future_value / ((1 + inflation_rate) ** years)


def calc_inflation_adjusted_price(present_value: float, inflation_rate: float, years: int) -> float:
    """현재 소비금액이 물가상승률만큼 오른다고 가정했을 때 미래 가격을 계산한다."""
    return present_value * ((1 + inflation_rate) ** years)


def calc_real_return_rate(annual_return: float, inflation_rate: float) -> float:
    """물가상승률을 반영한 실질 기대수익률을 계산한다."""
    if inflation_rate <= -1:
        return 0
    return ((1 + annual_return) / (1 + inflation_rate)) - 1


def calc_periodic_future_value(
    payment: float,
    annual_return: float,
    years: int,
    periods_per_year: int
) -> float:
    """
    반복 지출을 매 기간 말마다 투자했다고 가정했을 때의 미래가치를 계산한다.
    예: 매달 5만 원 지출을 줄여 매달 말 투자하는 경우
    """
    total_periods = years * periods_per_year

    if total_periods <= 0:
        return 0

    periodic_rate = (1 + annual_return) ** (1 / periods_per_year) - 1

    if periodic_rate == 0:
        return payment * total_periods

    return payment * (((1 + periodic_rate) ** total_periods - 1) / periodic_rate)


# =========================================================
# 제목 영역
# =========================================================

st.title("💸 오늘 소비의 미래 기회비용 계산기")

st.markdown(
    """
    오늘 쓰는 돈은 그냥 사라지는 돈이 아닐 수 있습니다.  
    같은 돈을 소비하지 않고 투자했다면, 미래에는 얼마가 되었을까요?

    워런 버핏이 이발비를 쓸 때도  
    “이 돈을 투자했으면 나중에 얼마가 됐을까?”를 생각했다는 일화처럼,  
    이 계산기는 **소비를 죄책감으로 보자는 도구가 아니라**  
    **소비의 기회비용을 한 번 숫자로 바라보는 도구**입니다.
    """
)

st.info(
    "핵심 질문: 지금 쓰려는 이 돈을 투자했다면, 미래에는 얼마가 되었을까?"
)

st.divider()


# =========================================================
# 입력 영역
# =========================================================

st.subheader("1️⃣ 기본 입력")

col1, col2 = st.columns(2)

with col1:
    expense = st.number_input(
        "현재 소비금액",
        min_value=0,
        value=10000,
        step=1000,
        help="지금 소비하려는 금액을 입력하세요. 예: 커피값, 배달비, 구독료, 쇼핑비"
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
        help="투자했을 때 기대하는 연평균 수익률입니다. 기본값은 7%입니다."
    )

with col4:
    inflation_percent = st.number_input(
        "물가상승률 (%)",
        min_value=0.0,
        max_value=20.0,
        value=2.5,
        step=0.1,
        help="미래 돈의 구매력을 현재가치로 환산하기 위한 물가상승률입니다. 기본값은 2.5%입니다."
    )

annual_return = annual_return_percent / 100
inflation_rate = inflation_percent / 100
real_return_rate = calc_real_return_rate(annual_return, inflation_rate)

st.divider()


# =========================================================
# 핵심 계산 결과
# =========================================================

future_value = calc_future_value(expense, annual_return, years)
real_value = calc_real_value(future_value, inflation_rate, years)
inflation_only_price = calc_inflation_adjusted_price(expense, inflation_rate, years)

st.subheader("2️⃣ 계산 결과")

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="오늘 소비금액",
        value=format_won(expense)
    )

with metric_col2:
    st.metric(
        label=f"투자했다면 {years}년 뒤",
        value=format_won(future_value)
    )

with metric_col3:
    st.metric(
        label="오늘 가치로 환산하면",
        value=format_won(real_value)
    )

st.markdown(
    f"""
    ### 해석

    지금 **{format_won(expense)}**을 소비하지 않고  
    연 **{annual_return_percent:.1f}%**로 **{years}년간 투자**했다고 가정하면,

    - 미래의 명목금액은 약 **{format_won(future_value)}**
    - 물가상승률 **{inflation_percent:.1f}%**를 반영한 현재가치는 약 **{format_won(real_value)}**
    - 물가를 뺀 실질 기대수익률은 약 **연 {real_return_rate * 100:.2f}%**

    로 볼 수 있습니다.
    """
)

st.warning(
    f"즉, 오늘의 {format_won(expense)} 소비는 "
    f"{years}년 뒤 기준으로 약 {format_won(future_value)}의 기회비용을 가진 선택일 수 있습니다."
)

with st.expander("참고: 물가만 반영하면 이 소비는 미래에 얼마일까?"):
    st.markdown(
        f"""
        이 부분은 투자 기회비용이 아니라 **물가만 반영한 참고값**입니다.

        현재 **{format_won(expense)}**짜리 소비가  
        매년 물가상승률 **{inflation_percent:.1f}%**만큼 오른다고 가정하면,

        **{years}년 뒤에는 약 {format_won(inflation_only_price)}** 정도의 가격이 됩니다.

        예를 들어 오늘 만 원짜리 소비가  
        30년 뒤에는 물가 때문에 2만 원대 소비가 될 수 있다는 의미입니다.
        """
    )

st.divider()


# =========================================================
# 기간별 비교표
# =========================================================

st.subheader("3️⃣ 기간별 비교")

comparison_years = [1, 5, 10, 20, 30, 40]

rows = []

for y in comparison_years:
    nominal = calc_future_value(expense, annual_return, y)
    real = calc_real_value(nominal, inflation_rate, y)
    inflation_price = calc_inflation_adjusted_price(expense, inflation_rate, y)

    rows.append({
        "기간": f"{y}년 뒤",
        "투자했다면 미래금액": round(nominal),
        "오늘 가치로 환산": round(real),
        "물가만 반영한 소비가격": round(inflation_price)
    })

df = pd.DataFrame(rows)

st.dataframe(
    df.style.format({
        "투자했다면 미래금액": "{:,.0f}원",
        "오늘 가치로 환산": "{:,.0f}원",
        "물가만 반영한 소비가격": "{:,.0f}원"
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "※ '물가만 반영한 소비가격'은 핵심 결과가 아니라 참고용입니다. "
    "이 계산기의 핵심은 '소비하지 않고 투자했다면 얼마가 되었을까?'입니다."
)

st.divider()


# =========================================================
# 그래프
# =========================================================

st.subheader("4️⃣ 그래프로 보기")

chart_years = list(range(1, years + 1))

chart_rows = []

for y in chart_years:
    nominal = calc_future_value(expense, annual_return, y)
    real = calc_real_value(nominal, inflation_rate, y)

    chart_rows.append({
        "연도": y,
        "투자했다면 미래금액": nominal,
        "오늘 가치로 환산": real
    })

chart_df = pd.DataFrame(chart_rows).set_index("연도")

st.line_chart(chart_df)

st.caption(
    "명목금액은 실제 미래의 숫자이고, 현재가치 환산금액은 물가상승률을 고려해 오늘 돈의 감각으로 바꾼 값입니다."
)

st.divider()


# =========================================================
# 반복 지출 계산
# =========================================================

st.subheader("5️⃣ 반복 지출까지 계산해보기")

st.markdown(
    """
    한 번의 소비보다 더 무서운 것은 **반복되는 소비**일 수 있습니다.  
    매일 커피값, 매주 배달비, 매달 구독료처럼 반복되는 지출이  
    장기적으로 어떤 기회비용을 만드는지도 계산해볼 수 있습니다.
    """
)

repeat_type = st.selectbox(
    "반복 주기",
    ["계산하지 않음", "매일", "매주", "매달", "매년"]
)

periods_map = {
    "매일": 365,
    "매주": 52,
    "매달": 12,
    "매년": 1
}

if repeat_type != "계산하지 않음":
    repeat_expense = st.number_input(
        "반복 지출 1회 금액",
        min_value=0,
        value=5000,
        step=1000,
        help="예: 매일 커피값 5,000원, 매달 구독료 15,000원"
    )

    periods_per_year = periods_map[repeat_type]
    annual_expense = repeat_expense * periods_per_year

    accumulated_future_value = calc_periodic_future_value(
        payment=repeat_expense,
        annual_return=annual_return,
        years=years,
        periods_per_year=periods_per_year
    )

    accumulated_real_value = calc_real_value(
        accumulated_future_value,
        inflation_rate,
        years
    )

    total_paid = repeat_expense * periods_per_year * years

    st.markdown(
        f"""
        ### 반복 지출 결과

        **{repeat_type} {format_won(repeat_expense)}**의 지출은  
        1년 기준으로 약 **{format_won(annual_expense)}**입니다.

        이 금액을 소비하지 않고 같은 주기로 투자했다고 단순 가정하면,

        - {years}년 동안 줄일 수 있었던 총 지출 원금: **{format_won(total_paid)}**
        - {years}년 뒤 명목 미래가치: **{format_won(accumulated_future_value)}**
        - 물가 반영 현재가치: **{format_won(accumulated_real_value)}**

        입니다.
        """
    )

    st.warning(
        f"{repeat_type} {format_won(repeat_expense)}의 반복 소비는 "
        f"{years}년 뒤 약 {format_won(accumulated_future_value)}의 기회비용을 만들 수 있습니다."
    )

    repeat_chart_rows = []

    for y in range(1, years + 1):
        fv = calc_periodic_future_value(
            payment=repeat_expense,
            annual_return=annual_return,
            years=y,
            periods_per_year=periods_per_year
        )
        rv = calc_real_value(fv, inflation_rate, y)

        repeat_chart_rows.append({
            "연도": y,
            "반복 지출 투자 시 미래금액": fv,
            "오늘 가치로 환산": rv
        })

    repeat_chart_df = pd.DataFrame(repeat_chart_rows).set_index("연도")

    st.line_chart(repeat_chart_df)

st.divider()


# =========================================================
# 공유용 문구 생성
# =========================================================

st.subheader("6️⃣ 공유용 한 줄 요약")

summary_text = (
    f"오늘 {format_won(expense)}을 소비하지 않고 "
    f"연 {annual_return_percent:.1f}%로 {years}년 투자했다면, "
    f"미래에는 약 {format_won(future_value)}이 될 수 있습니다. "
    f"물가를 반영한 오늘 가치로는 약 {format_won(real_value)}입니다."
)

st.code(summary_text, language="text")

st.divider()


# =========================================================
# 하단 안내
# =========================================================

st.caption(
    """
    ※ 이 계산기는 투자 권유가 아니라 소비의 기회비용을 이해하기 위한 교육용 도구입니다.  
    실제 수익률, 물가상승률, 세금, 수수료, 투자손실 가능성은 반영되지 않았습니다.  
    소비를 무조건 줄이라는 뜻이 아니라, 내가 정말 원하는 소비인지 한 번 더 생각해보자는 취지입니다.
    """
)
