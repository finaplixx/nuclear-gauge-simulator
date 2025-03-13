import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Import your simulator classes from the main file
from nuclear_gauge_simulator import TroxlerGaugeSimulator, SoilDescriptions

st.set_page_config(page_title="Nuclear Gauge Simulator", layout="wide")

st.title("Nuclear Gauge Simulator")

# Create two columns for the main layout
col1, col2 = st.columns([3, 7])

with col1:
    st.header("Gauge Setup")
    
    with st.expander("Gauge Information", expanded=False):
        model = st.text_input("Model", value="3440")
        serial_number = st.text_input("Serial Number", value="12345")
        calibration_date = st.text_input("Calibration Date", value="2024-09-15")
    
    with st.expander("Daily Standard Count", expanded=False):
        std_density_count = st.number_input("Density Standard Count", value=1570, min_value=1000, max_value=2000)
        std_moisture_count = st.number_input("Moisture Standard Count", value=670, min_value=400, max_value=1000)
    
    st.header("Test Parameters")
    
    max_dry_density = st.number_input("Maximum Dry Density (pcf)", min_value=100.0, max_value=150.0, value=120.0)
    optimum_moisture = st.number_input("Optimum Moisture (%)", min_value=1.0, max_value=30.0, value=8.0)
    
    soil_types = [
        "GW (Well-graded gravel)",
        "GP (Poorly graded gravel)",
        "GM (Silty gravel)",
        "GC (Clayey gravel)",
        "SW (Well-graded sand)",
        "SP (Poorly graded sand)",
        "SM (Silty sand)",
        "SC (Clayey sand)",
        "ML (Silt)",
        "CL (Lean clay)",
        "OL (Organic silt/clay, low plasticity)",
        "MH (Elastic silt)",
        "CH (Fat clay)",
        "OH (Organic silt/clay, high plasticity)",
        "PT (Peat)",
        "Type II (Aggregate Base)",
        "Asphalt",
        "Concrete"
    ]
    
    soil_type = st.selectbox("Soil Type", soil_types, index=9)  # Default to CL (Lean clay)
    depth_mode = st.selectbox("Depth Mode", ["DS", "BS"], index=0)
    gauge_depth = st.number_input("Gauge Depth (inches)", min_value=4, max_value=12, value=8)
    test_duration = st.number_input("Test Duration (minutes)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)
    num_tests = st.number_input("Number of Tests", min_value=1, max_value=20, value=10, step=1)
    
    # Generate button
    generate_button = st.button("Generate Sample Tests", type="primary", use_container_width=True)

with col2:
    # Display soil descriptions
    st.header("Soil Classification")
    soil_info = SoilDescriptions()
    descriptions = soil_info.get_soil_descriptions(soil_type)
    
    desc_cols = st.columns(3)
    with desc_cols[0]:
        st.subheader("Basic Description")
        st.info(descriptions[0])
    with desc_cols[1]:
        st.subheader("Field Identification")
        st.info(descriptions[1])
    with desc_cols[2]:
        st.subheader("Typical Uses")
        st.info(descriptions[2])
    
    # Initialize session state to store results
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None
    
    if generate_button:
        # Create simulator instance
        simulator = TroxlerGaugeSimulator(
            model=model,
            serial_number=serial_number,
            std_density_count=std_density_count,
            std_moisture_count=std_moisture_count
        )
        
        # Show a spinner while generating
        with st.spinner("Generating test results..."):
            # Generate test results
            results_df = simulator.generate_sample_tests(
                max_dry_density=max_dry_density,
                optimum_moisture=optimum_moisture,
                num_tests=num_tests,
                depth_mode=depth_mode,
                test_duration=test_duration,
                soil_type=soil_type,
                gauge_depth=gauge_depth
            )
            
            st.session_state.results_df = results_df
            st.success(f"Generated {num_tests} sample tests!")
    
    # Display results if available
    if st.session_state.results_df is not None:
        st.header("Test Results")
        
        # Create a container with a border
        results_container = st.container()
        
        # Report header info
        st.subheader("Test Information")
        
        info_cols = st.columns(2)
        with info_cols[0]:
            st.markdown(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
            st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
            st.markdown(f"**Gauge Model:** {model}")
            st.markdown(f"**Serial Number:** {serial_number}")
        
        with info_cols[1]:
            st.markdown(f"**Max Dry Density:** {max_dry_density} pcf")
            st.markdown(f"**Optimum Moisture:** {optimum_moisture}%")
            st.markdown(f"**Soil Type:** {soil_type}")
            st.markdown(f"**Depth Mode:** {depth_mode}")
        
        # Format the DataFrame for display
        results_df = st.session_state.results_df.copy()
        
        # Create an editable dataframe with a "Done" column
        edited_df = st.data_editor(
            results_df,
            column_config={
                "Test #": st.column_config.NumberColumn(format="%d"),
                "Density Count": st.column_config.NumberColumn(format="%d"),
                "Moisture Count": st.column_config.NumberColumn(format="%d"),
                "Wet Density (pcf)": st.column_config.NumberColumn(format="%.1f"),
                "Dry Density (pcf)": st.column_config.NumberColumn(format="%.1f"),
                "Moisture (lbs/ft³)": st.column_config.NumberColumn(format="%.1f"),
                "Moisture (%)": st.column_config.NumberColumn(format="%.1f"),
                "Compaction (%)": st.column_config.NumberColumn(format="%.1f"),
                "Done": st.column_config.CheckboxColumn(default=False)
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Add export button
        if st.download_button(
            label="Export Results (CSV)",
            data=edited_df.to_csv(index=False).encode('utf-8'),
            file_name=f"gauge_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        ):
            st.success("Results exported successfully!")

# Add a footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center">
        <p>Nuclear Gauge Simulator | Created for educational and planning purposes</p>
    </div>
    """, 
    unsafe_allow_html=True
)
