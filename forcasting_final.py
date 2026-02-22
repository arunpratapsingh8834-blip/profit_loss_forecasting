# ==========================================
# LOSS & PROFIT ANALYSIS AND FORECASTING SYSTEM
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


# ------------------------------------------
# Page Configuration
# ------------------------------------------
st.set_page_config(
    page_title="Loss & Profit Analysis and Forecasting",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)
st.title("📈 Loss & Profit Analysis and Forecasting System")
st.markdown("upload your financial data to analyze past performance and forecast future trends.")
# ------------------------------------------
# File Upload
# ------------------------------------------
uploaded_file = st.file_uploader("Upload your financial data (CSV format)", type=["csv"])
if uploaded_file is None:
    st.warning("please uploade your csv file to  continue")
    st.stop()
#---------------
# Data Processing
#---------------    
df = pd.read_csv(uploaded_file)

#---------------
# clean column names
#---------------
df.columns = df.columns.str.strip()
#---------------
# rename common variations automatically
df.rename(columns={
    'cost_of_goods_sold': 'cost',
    'cogs': 'cost',
    'revenue': 'revenue',
    'marketring_expenses': 'marketing_expenses',
    'marketing': 'marketing_expenses'}, inplace=True)
#---------------
# Check for required columns
required_columns = ['date', 'revenue', 'cost', 'operating_expenses', 'marketing_expenses']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Missing required columns: {', '.join(missing_columns)}. Please upload a file with the correct format.")
    st.stop()
#---------------
# Ensure date column is in datetime format  
#---------------
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
df= df.dropna(subset=['date'])
#---------------
# Calculate profit
#---------------
df['profit'] = df['revenue'] - df['cost'] - df['operating_expenses']- df['marketing_expenses']

#---------------
# kpi section
#---------------
st.subheader("📌 Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
total_revenue = df['revenue'].sum()
total_cost = df['cost'].sum()
total_profit = df['profit'].sum()
col1.metric("Total Revenue", f"INR {total_revenue:,.2f}")
col2.metric("Total Cost", f"INR {total_cost:,.2f}")
col3.metric("Total Profit", f"INR {total_profit:,.2f}")
#---------------
# profit / loss explanation 
#---------------
st.subheader("📊 Profit & Loss Analysis")

if total_profit >= 0:
    st.success(f"Your business is profitable with a total profit of INR {total_profit:,.2f}. Keep up the good work!")
    st.write(""" profit occoured when the total revenue exceeds the total cost and expenses. This indicates that your business is generating more income than it is spending, which is a positive sign of financial health.""")
else:
    st.error(f"Your business is incurring a loss of INR {abs(total_profit):,.2f}.")
    st.write(""" loss occurs when the total cost and expenses exceed the total revenue. This indicates that your business is spending more than it is earning, which can be a sign of financial challenges.""")
#---------------
# interactive revenue and profit trend 
#---------------
st.subheader("📈 Revenue and Profit Trends")
fig1 = px.line(df, x='date', y=['revenue', 'profit'], title='Revenue and Profit Over Time' , markers=True)
st.plotly_chart(fig1, use_container_width=True)
#---------------
# expences breakdown
#---------------
st.subheader("📉 Expense Breakdown")
expense_fig = px.bar(df, x='date', y=['cost', 'operating_expenses', 'marketing_expenses'], title='Expense Breakdown Over Time', barmode='group')
st.plotly_chart(expense_fig, use_container_width=True)
#---------------
# forecasting section
#---------------
st.subheader("🔮 Forecasting profit ")
forecast_periods = st.slider("Select number of days (months) to forecast",30 ,365,90)


# Prepare data for Prophet
prophet_df = df[['date', 'profit']].rename(columns={'date': 'ds', 'profit': 'y'})
model = Prophet()
model.fit(prophet_df)
future = model.make_future_dataframe(periods=forecast_periods)
forecast = model.predict(future)
forecasr_fig = px.line(forecast, x='ds', y='yhat', title='Profit Forecast')
st.plotly_chart(forecasr_fig, use_container_width=True)
#---------------
# why forecast changes
#---------------
st.subheader("📊forecast interpretation")
st.write("""The forecast is generated using Facebook Prophet, a time-series forecasting model.

The model:
- Identifies historical trends
- Detects seasonality patterns
- Projects future profit based on past performance

If forecast shows decline:
→ Expenses may be increasing
→ Revenue growth may be slowing

If forecast shows growth:
→ Revenue trend is positive
→ Cost management is effective
""")
#---------------
# linear regression forecasting
st.subheader("🔮 Linear Regression Forecasting")
# Prepare data for Linear Regression
x = df[['revenue', 'cost', 'operating_expenses', 'marketing_expenses']]
y = df['profit']
# fit linear regression model
reg_model = LinearRegression()
reg_model.fit(x, y)
# get coefficients
coefficients = reg_model.coef_
features = x.columns

features_importance = pd.DataFrame({'Feature': features, 'impact on profit': coefficients})
st.write("Feature Impact on Profit:")
st.dataframe(features_importance)
#plot feature impact
feature_fig = px.bar(features_importance, x='Feature', y='impact on profit', title='Feature Impact on Profit', color='Feature', height=400)
st.plotly_chart(feature_fig, use_container_width=True)
#---------------
#footer
#---------------
st.markdown("---")
st.markdown("developed as a minor project to analyze and forecost profit and loss of any sales data of company .")
                


