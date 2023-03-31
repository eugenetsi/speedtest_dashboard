import time
import pandas as pd
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

from logger import get_logger
from db import create_table, print_db
from getter import get_data

DB_NAME = 'SPEEDTEST_DB'
TABLE_NAME = 'speedtest_data'

_logger = get_logger()

st.set_page_config(
    page_title="Speed of the internets",
    page_icon="✅",
    layout="wide",
)

# get first datapoint for init
df = pd.DataFrame(get_data(), columns=['Ping', 'Down', 'Up', 'Timestamp'])
# create table
conn, cursor = create_table()
# send data to table
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=True)
_logger.info('sent dataframe to db')
print_db(DB_NAME, TABLE_NAME)

# dashboard title
st.title("Speed of the internets")

# creating a single-element container
placeholder = st.empty()

prev = 0
prev_mean = 0
while True:
    with placeholder.container():
        # create three columns
        kpi1, kpi2 = st.columns(2)

        # average with delta
        kpi1.metric(
            label="Average Download",
            value=round(df.Down.astype('float').mean(), 2),
            delta=round(df.Down.astype('float').mean() - prev_mean, 2),)

        # current with delta
        kpi2.metric(
            label="Current Download",
            value=round(float(df.loc[len(df.index) - 1].Down), 2),
            delta=round(float(df.loc[len(df.index) - 1].Down) - prev, 2),)

        # down/up chart
        with kpi1:
            st.markdown("### Speed chart")
            fig = px.line(
                data_frame=df, y=[df.Down, df.Up], x=df.Timestamp)
            st.write(fig)
            
        # ping chart
        with kpi2:
            st.markdown("### Ping chart")
            fig = px.line(
                data_frame=df, y=df.Ping, x=df.Timestamp)
            st.write(fig)

        # all data
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)

        if len(df.index) > 1:
            prev = float(df.loc[len(df.index) - 2].Down)
        prev_mean = df.Down.astype('float').mean()
        df = df.append(pd.DataFrame(get_data(), columns=['Ping', 'Down', 'Up', 'Timestamp']), ignore_index=True)
        # update db
        df.to_sql(name=TABLE_NAME, if_exists='replace', con=conn)
        print_db(DB_NAME, TABLE_NAME)
