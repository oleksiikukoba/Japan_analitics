import streamlit as st
import math

# --- КОНСТАНТИ ТА НАЛАШТУВАННЯ ---
# Ви можете оновлювати ці значення за потреби
EXCHANGE_RATE_JPY_UAH = 0.27  # Курс єни до гривні
ZENMARKET_FEE_JPY = 300  # Комісія ZenMarket в єнах
JAPAN_SHIPPING_JPY = 1500  # Вартість доставки по Японії в єнах
DUTY_FREE_LIMIT_EUR = 150  # Безмитний ліміт в євро
EXCHANGE_RATE_EUR_UAH = 42.5  # Курс євро до гривні
EXCHANGE_RATE_JPY_EUR = 0.006  # Курс єни до євро

# Варіанти міжнародної доставки (вартість за 100 г в єнах)
DELIVERY_OPTIONS = [
    {"name": "EMS", "cost_per_100g_jpy": 500},
    {"name": "DHL", "cost_per_100g_jpy": 700},
    {"name": "FedEx", "cost_per_100g_jpy": 650},
    {"name": "ZenExpress", "cost_per_100g_jpy": 400},
]

# --- ІНТЕРФЕЙС ДОДАТКУ ---

st.set_page_config(page_title="Калькулятор вартості з Японії", page_icon="🎣")

st.title("🎣 Калькулятор кінцевої вартості снастей з Японії")
st.markdown(
    "Цей калькулятор допоможе вам розрахувати приблизну вартість покупки товарів з Японії з урахуванням усіх комісій, доставки та мита.")

# Поля для введення даних
url = st.text_input("Вставте посилання на товар (необов'язково)")
price = st.number_input("Ціна товару в єнах (JPY)", min_value=0, step=100)
weight = st.number_input("Приблизна вага товару в грамах", min_value=1, value=500, step=50)

# Кнопка для розрахунку
if st.button("Розрахувати вартість"):
    if price == 0:
        st.warning("Будь ласка, введіть ціну товару.")
    else:
        # --- ЛОГІКА РОЗРАХУНКУ ---

        # Базова вартість в різних валютах
        base_yen = price + ZENMARKET_FEE_JPY + JAPAN_SHIPPING_JPY
        base_uah = base_yen * EXCHANGE_RATE_JPY_UAH
        base_eur = base_yen * EXCHANGE_RATE_JPY_EUR

        # Розрахунок мита
        duty_uah = 0
        if base_eur > DUTY_FREE_LIMIT_EUR:
            # Мито = (Вартість - 150 євро) * 10% + ПДВ = (Вартість - 150 євро) * 20%
            # Формула спрощена до (Загальна вартість - Ліміт) * 32% (10% мито + 20% ПДВ)
            duty_uah = (base_eur - DUTY_FREE_LIMIT_EUR) * 0.32 * EXCHANGE_RATE_EUR_UAH

        st.subheader("📊 Результати розрахунку:")

        # Розрахунок для кожного способу доставки
        for option in DELIVERY_OPTIONS:
            intl_shipping_yen = option["cost_per_100g_jpy"] * math.ceil(weight / 100)
            intl_shipping_uah = intl_shipping_yen * EXCHANGE_RATE_JPY_UAH

            total_uah = base_uah + intl_shipping_uah + duty_uah

            # Вивід результатів у вигляді картки
            st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; margin-bottom: 12px;">
                <h4>{option['name']}</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li>🚚 Доставка по Японії: <strong>{JAPAN_SHIPPING_JPY * EXCHANGE_RATE_JPY_UAH:.2f} ₴</strong></li>
                    <li>🌏 Міжнародна доставка: <strong>{intl_shipping_uah:.2f} ₴</strong></li>
                    <li>🧾 Розмитнення (якщо потрібно): <strong>{duty_uah:.2f} ₴</strong></li>
                </ul>
                <hr style="margin: 8px 0;">
                <p style="font-size: 1.1em;">💰 <strong>Загалом: {total_uah:.2f} ₴</strong></p>
            </div>
            """, unsafe_allow_html=True)