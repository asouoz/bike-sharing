import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_clean_df = pd.read_csv("main_data.csv")
day_clean_df.head()

drop_col = ['windspeed']

for i in day_clean_df.columns:
  if i in drop_col:
    day_clean_df.drop(labels=i, axis=1, inplace=True)


def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df


def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df


def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    return weekday_rent_df


def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return workingday_rent_df


def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return holiday_rent_df


def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })
    return weather_rent_df



min_date = pd.to_datetime(day_clean_df['dteday']).dt.date.min()
max_date = pd.to_datetime(day_clean_df['dteday']).dt.date.max()
 
with st.sidebar:
    st.image("rentabike.jpeg")
    
    
    start_date, end_date = st.date_input(
        label='Time',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_clean_df[(day_clean_df['dteday'] >= str(start_date)) & 
                (day_clean_df['dteday'] <= str(end_date))]


daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)

weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)



st.header('Rent-a-Bike')


st.subheader('Rentals on Daily')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total', value= daily_rent_total)




st.subheader('Rentals based on the Weather')

fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:green", "tab:blue", "tab:red"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


st.subheader('Rentals on Workingday, Holiday, and Weekday')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors1=["tab:green", "tab:blue"]
colors2=["tab:green", "tab:blue"]
colors3=["tab:green", "tab:blue", "tab:red", "tab:pink", "tab:orange", "tab:purple", "tab:gray"]



sns.barplot(
    x='workingday',
    y='cnt',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Workingday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)



sns.barplot(
  x='holiday',
  y='cnt',
  data=holiday_rent_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_rent_df['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)



sns.barplot(
  x='weekday',
  y='cnt',
  data=weekday_rent_df,
  palette=colors3,
  ax=axes[2])

for index, row in enumerate(weekday_rent_df['cnt']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)