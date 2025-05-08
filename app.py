import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="User Daily Amount Visualization",
    page_icon="📊",
    layout="wide"
)

# Set dark theme
st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        .stTitle {
            color: #ffffff;
        }
        .stSubheader {
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("User Daily Amount Visualization")

# Load data directly from users.json
try:
    with open('users.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create line chart with dark theme
    fig = px.line(
        df,
        x='date',
        y='daily_amount',
        color='username',
        title='Daily Amount by User',
        labels={
            'date': 'Date',
            'daily_amount': 'Daily Amount',
            'username': 'Username'
        },
        template='plotly_dark',  # Dark theme
        markers=True,
        line_shape='linear'
    )
    
    # Update layout with dark theme styling
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Daily Amount",
        hovermode='x unified',
        legend_title="Users",
        height=700,
        width=None,
        font=dict(size=14, color='white'),
        title=dict(
            font=dict(size=24, color='white'),
            y=0.95
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05,
            bgcolor="rgba(0, 0, 0, 0.8)"
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='black',
        paper_bgcolor='black'
    )
    
    # Update axes with dark theme
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#333333',
        tickangle=45,
        color='white'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#333333',
        color='white'
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Display raw data with dark theme styling
    st.subheader("Raw Data")
    st.dataframe(
        df.style.format({
            'daily_amount': '{:.4f}',
            'date': lambda x: x.strftime('%Y-%m-%d')
        }).set_properties(**{
            'background-color': 'black',
            'color': 'white'
        }),
        use_container_width=True
    )
except FileNotFoundError:
    st.error("users.json file not found. Please make sure the file exists in the same directory as the app.")
except json.JSONDecodeError:
    st.error("Error reading the JSON file. Please check if the file format is correct.") 