import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="User $PRIME Payment Visualization",
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
        .metric-card {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("User $PRIME Payment Visualization")

# Load data directly from users.json
try:
    with open('users.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create two columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>Total Users</h3>
                <h2>{}</h2>
            </div>
        """.format(len(df['username'].unique())), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>Total Payments</h3>
                <h2>{:.4f}</h2>
            </div>
        """.format(df['daily_amount'].sum()), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>Average Payment</h3>
                <h2>{:.4f}</h2>
            </div>
        """.format(df['daily_amount'].mean()), unsafe_allow_html=True)
    
    # Create line chart with dark theme and smooth curves
    fig = px.line(
        df,
        x='date',
        y='daily_amount',
        color='username',
        title='Payment Amount by User',
        labels={
            'date': 'Date',
            'daily_amount': 'Payment Amount',
            'username': 'Username'
        },
        template='plotly_dark',
        markers=True,
        line_shape='spline'  # Using spline for smoother curves
    )
    
    # Update layout with dark theme styling
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Payment Amount",
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
        paper_bgcolor='black',
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_family="Arial",
            bordercolor="white",
        )
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
    
    # Calculate cumulative payments
    df_sorted = df.sort_values('date')
    df_sorted['cumulative_amount'] = df_sorted.groupby('username')['daily_amount'].cumsum()
    
    # Create cumulative payments chart
    fig_cumulative = px.line(
        df_sorted,
        x='date',
        y='cumulative_amount',
        color='username',
        title='Cumulative Payments by User',
        labels={
            'date': 'Date',
            'cumulative_amount': 'Cumulative Payment Amount',
            'username': 'Username'
        },
        template='plotly_dark',
        markers=True,
        line_shape='spline'
    )
    
    # Update layout for cumulative chart
    fig_cumulative.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Payment Amount",
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
        paper_bgcolor='black',
        hoverlabel=dict(
            bgcolor="black",
            font_size=12,
            font_family="Arial",
            bordercolor="white",
        )
    )
    
    # Update axes for cumulative chart
    fig_cumulative.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#333333',
        tickangle=45,
        color='white'
    )
    
    fig_cumulative.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#333333',
        color='white'
    )
    
    # Display the cumulative chart
    st.plotly_chart(fig_cumulative, use_container_width=True)
    
    # User Rankings Section
    st.subheader("User Prime Payment Rankings")
    
    # Calculate user statistics
    user_stats = df.groupby('username').agg({
        'daily_amount': ['sum', 'mean', 'max', 'count']
    }).round(4)
    user_stats.columns = ['Total Payments', 'Average Payment', 'Highest Payment', 'Number of Payments']
    user_stats = user_stats.sort_values('Total Payments', ascending=False)
    
    # Display user rankings
    st.dataframe(
        user_stats.style.format({
            'Total Payments': '{:.4f}',
            'Average Payment': '{:.4f}',
            'Highest Payment': '{:.4f}'
        }).set_properties(**{
            'background-color': 'black',
            'color': 'white'
        }),
        use_container_width=True
    )
    
    # Raw Data Section
    st.subheader("Payment Data")
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