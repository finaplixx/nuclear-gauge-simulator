# Nuclear Gauge Simulator

A simulation tool for nuclear density gauge testing used in soil compaction assessment.

## Features

- Simulates density and moisture counts based on soil properties
- Supports all UCSC soil classification types
- Provides detailed soil information for each classification
- Generates realistic test data with proper randomization
- Allows for exporting results to CSV

## Getting Started

### Online Usage

Visit the deployed Streamlit app at: [Nuclear Gauge Simulator](https://your-app-url.streamlit.app)

### Local Installation

1. Clone this repository
```bash
git clone https://github.com/your-username/nuclear-gauge-simulator.git
cd nuclear-gauge-simulator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run streamlit_app.py
```

## How to Use

1. Enter gauge information (optional)
2. Set test parameters:
   - Maximum dry density
   - Optimum moisture content
   - Soil type
   - Depth mode and gauge depth
   - Number of tests
3. Click "Generate Sample Tests"
4. View results in the table
5. Mark tests as done by checking the boxes
6. Export results to CSV for further analysis

## Background

Nuclear density gauges are used in construction to measure soil compaction. This simulator helps users:
- Understand how soil type affects test results
- Prepare for field testing by generating theoretical counts
- Learn about different soil classifications and their properties
- Generate realistic test reports for training purposes

## Science Behind the Simulation

The simulator uses calibrated linear equations to calculate theoretical density and moisture counts:
- Density Count = Intercept + (Slope × Dry Density)
- Each soil type has unique intercept and slope values
- Additional factors are applied for test depth, measurement time, and gauge calibration
- Randomization is applied to simulate real-world variations in readings

## Technical Details

- Built with Python, using Streamlit for the web interface
- Uses numpy for numerical calculations
- Implements pandas for data handling
- Free to use for educational and planning purposes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on field data collected from real nuclear gauge readings
- Soil classification information from UCSC soil classification system
