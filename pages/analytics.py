import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from pathlib import Path
from utils.visualization import load_traffic_data

def show_analytics():
    st.title("Traffic Analytics 📊")
    
    # Load the data
    df = load_traffic_data()
    
    if df is None or df.empty:
        st.info("No traffic data available yet. Upload a video to start collecting data.")
        return
    
    # Mobile-friendly filters
    st.subheader("Filters")
    col1, col2 = st.columns(2)
    
    with col1:
        # Date range filter
        date_range = st.date_input(
            "Select Date Range",
            value=(df['timestamp'].min(), df['timestamp'].max()),
            min_value=df['timestamp'].min(),
            max_value=df['timestamp'].max()
        )
    
    with col2:
        # Vehicle type filter
        vehicle_types = ['All'] + list(df['vehicle_type'].unique())
        selected_type = st.selectbox("Vehicle Type", vehicle_types)
    
    # Filter data based on selections
    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['timestamp'].dt.date >= date_range[0]) &
            (filtered_df['timestamp'].dt.date <= date_range[1])
        ]
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['vehicle_type'] == selected_type]
    
    # Create mobile-friendly visualizations
    st.subheader("Traffic Overview")
    
    # Vehicle counts by type
    fig_counts = px.bar(
        filtered_df.groupby('vehicle_type').size().reset_index(name='count'),
        x='vehicle_type',
        y='count',
        title='Vehicle Counts by Type',
        labels={'vehicle_type': 'Vehicle Type', 'count': 'Count'}
    )
    st.plotly_chart(fig_counts, use_container_width=True)
    
    # Traffic flow over time
    fig_flow = px.line(
        filtered_df.groupby('timestamp').size().reset_index(name='count'),
        x='timestamp',
        y='count',
        title='Traffic Flow Over Time',
        labels={'timestamp': 'Time', 'count': 'Vehicle Count'}
    )
    st.plotly_chart(fig_flow, use_container_width=True)
    
    # Speed distribution
    if 'speed' in filtered_df.columns:
        fig_speed = px.histogram(
            filtered_df,
            x='speed',
            title='Vehicle Speed Distribution',
            labels={'speed': 'Speed (km/h)', 'count': 'Count'}
        )
        st.plotly_chart(fig_speed, use_container_width=True)
    
    # Summary statistics
    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Vehicles", len(filtered_df))
    with col2:
        st.metric("Average Speed", f"{filtered_df['speed'].mean():.1f} km/h" if 'speed' in filtered_df.columns else "N/A")
    with col3:
        st.metric("Peak Hour", filtered_df.groupby(filtered_df['timestamp'].dt.hour).size().idxmax())
    
    # Download data button
    st.download_button(
        label="Download Data",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f'traffic_data_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        use_container_width=True
    )

if __name__ == "__main__":
    show_analytics() 