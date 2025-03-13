import numpy as np
import random
from datetime import datetime

class SoilDescriptions:
    """Provides text descriptions for soil classifications"""
    
    def __init__(self):
        # Create descriptions for all soil types
        self.soil_descriptions = {
            "GW (Well-graded gravel)": "Wide range of particle sizes, good distribution, little or no fines.",
            "GP (Poorly graded gravel)": "Predominantly one size or missing some sizes, little or no fines.",
            "GM (Silty gravel)": "Gravel with significant silt content, low to no plasticity.",
            "GC (Clayey gravel)": "Gravel with significant clay content, plastic fines.",
            "SW (Well-graded sand)": "Wide range of sand sizes, good distribution, little or no fines.",
            "SP (Poorly graded sand)": "Predominantly one size or missing some sizes, little or no fines.",
            "SM (Silty sand)": "Sand with significant silt content, low to no plasticity.",
            "SC (Clayey sand)": "Sand with significant clay content, plastic fines.",
            "ML (Silt)": "Low plasticity silts, rock flour, silty or clayey fine sands.",
            "CL (Lean clay)": "Low to medium plasticity clays, gravelly/sandy/silty clays.",
            "OL (Organic silt/clay, low plasticity)": "Low plasticity organic silts and clays.",
            "MH (Elastic silt)": "High plasticity silts, micaceous or diatomaceous fine sands and silts.",
            "CH (Fat clay)": "High plasticity clays, high swelling potential.",
            "OH (Organic silt/clay, high plasticity)": "High plasticity organic clays.",
            "PT (Peat)": "Peat, humus, swamp soils with high organic content.",
            "Type II (Aggregate Base)": "Crushed aggregate base course meeting Type II specifications.",
            "Asphalt": "Asphalt concrete paving material, bituminous mixture.",
            "Concrete": "Portland cement concrete, hardened cementitious material."
        }
        
        self.field_characteristics = {
            "GW (Well-graded gravel)": "Field ID: No plasticity, coarse with varied sizes. Good compaction.",
            "GP (Poorly graded gravel)": "Field ID: No plasticity, uniform size. Moderate compaction.",
            "GM (Silty gravel)": "Field ID: Slight plasticity when wet, dusty when dry.",
            "GC (Clayey gravel)": "Field ID: Plasticity present, can roll thin threads when moist.",
            "SW (Well-graded sand)": "Field ID: Granular feel, varied grain sizes, no cohesion.",
            "SP (Poorly graded sand)": "Field ID: Uniform grain size, no cohesion.",
            "SM (Silty sand)": "Field ID: Slight plasticity when wet, dusty when dry.",
            "SC (Clayey sand)": "Field ID: Plasticity present, can form ribbons when moist.",
            "ML (Silt)": "Field ID: Low plasticity, feels smooth, slightly sticky. Dilatant reaction.",
            "CL (Lean clay)": "Field ID: Medium plasticity, can form ribbons 1\"-2\", moderate strength.",
            "OL (Organic silt/clay, low plasticity)": "Field ID: Dark color, organic odor, low plasticity.",
            "MH (Elastic silt)": "Field ID: Smooth, buttery feel. High dilatant reaction.",
            "CH (Fat clay)": "Field ID: High plasticity, can form ribbons >2\", high strength.",
            "OH (Organic silt/clay, high plasticity)": "Field ID: Dark color, organic odor, high plasticity.",
            "PT (Peat)": "Field ID: Very fibrous, organic odor, dark brown to black color.",
            "Type II (Aggregate Base)": "Field ID: Crushed stone mixture with fines, angular particles.",
            "Asphalt": "Field ID: Black color, petroleum odor, thermoplastic behavior.",
            "Concrete": "Field ID: Gray, very hard, composed of cement paste and aggregate."
        }
        
        self.typical_uses = {
            "GW (Well-graded gravel)": "Typical Uses: Road bases, backfill, drainage layers.",
            "GP (Poorly graded gravel)": "Typical Uses: Drainage material, filter material.",
            "GM (Silty gravel)": "Typical Uses: Road bases, embankments, structural fill.",
            "GC (Clayey gravel)": "Typical Uses: Liners, road bases with proper drainage.",
            "SW (Well-graded sand)": "Typical Uses: Structural fill, backfill, concrete sand.",
            "SP (Poorly graded sand)": "Typical Uses: Drainage material, bedding material.",
            "SM (Silty sand)": "Typical Uses: Fills, embankments, subgrades.",
            "SC (Clayey sand)": "Typical Uses: Liners, cores, fills with controlled permeability.",
            "ML (Silt)": "Typical Uses: General fill, embankments (with proper compaction).",
            "CL (Lean clay)": "Typical Uses: Liners, cores, fills with low permeability.",
            "OL (Organic silt/clay, low plasticity)": "Typical Uses: Not suitable for engineering use.",
            "MH (Elastic silt)": "Typical Uses: Not recommended for structural uses.",
            "CH (Fat clay)": "Typical Uses: Liners, slurry walls, barriers.",
            "OH (Organic silt/clay, high plasticity)": "Typical Uses: Not suitable for engineering use.",
            "PT (Peat)": "Typical Uses: Must be removed from construction areas.",
            "Type II (Aggregate Base)": "Typical Uses: Road bases, structural fill, foundation support.",
            "Asphalt": "Typical Uses: Pavements, waterproofing, roofing.",
            "Concrete": "Typical Uses: Structural elements, pavements, foundation support."
        }
    
    def get_soil_descriptions(self, soil_type):
        """Get descriptive text for a soil type"""
        # Default info if soil type not found
        if soil_type not in self.soil_descriptions:
            return [
                "No specific information available for this soil type.",
                "Please refer to UCSC classification guidelines.",
                "Consult field testing manual for identification guidelines."
            ]
        
        # Return descriptions
        return [
            self.soil_descriptions.get(soil_type, "Unknown soil type"),
            self.field_characteristics.get(soil_type, "Field identification details not available"),
            self.typical_uses.get(soil_type, "Typical usage information not available")
        ]

class TroxlerGaugeSimulator:
    """
    Simulates a nuclear density gauge providing theoretical density and moisture counts
    based on realistic parameters for soil testing.
    """
    
    def __init__(self, model="3440", serial_number="12345", std_density_count=1570, std_moisture_count=670):
        self.model = model
        self.serial_number = serial_number
        self.calibration_date = "2024-09-15"
        
        # Standard count values (calibrated based on user input)
        self.std_density_count = std_density_count
        self.std_moisture_count = std_moisture_count
        
        # UCSC soil classification with calibrated coefficients based on field data
        # Each soil type has intercept and slope for density count calculation
        # Formula: density_count = intercept + (slope * dry_density)
        self.soil_density_equations = {
            "GW (Well-graded gravel)": {"intercept": 3200, "slope": -18.5},
            "GP (Poorly graded gravel)": {"intercept": 3150, "slope": -18.0},
            "GM (Silty gravel)": {"intercept": 4000, "slope": -25.0},
            "GC (Clayey gravel)": {"intercept": 4100, "slope": -26.0},
            "SW (Well-graded sand)": {"intercept": 3150, "slope": -17.0},
            "SP (Poorly graded sand)": {"intercept": 3100, "slope": -16.5},
            "SM (Silty sand)": {"intercept": 5800, "slope": -42.0},  # Calibrated from field data
            "SC (Clayey sand)": {"intercept": 5000, "slope": -35.0},
            "ML (Silt)": {"intercept": 4500, "slope": -31.0},
            "CL (Lean clay)": {"intercept": 4200, "slope": -29.0},  # Calibrated from field data
            "OL (Organic silt/clay, low plasticity)": {"intercept": 4600, "slope": -32.0},
            "MH (Elastic silt)": {"intercept": 4400, "slope": -30.0},
            "CH (Fat clay)": {"intercept": 4300, "slope": -29.5},
            "OH (Organic silt/clay, high plasticity)": {"intercept": 4700, "slope": -33.0},
            "PT (Peat)": {"intercept": 5000, "slope": -35.0},
            "Type II (Aggregate Base)": {"intercept": 4000, "slope": -25.0},  # Added Type II material (similar to GM)
            "Asphalt": {"intercept": 3000, "slope": -16.0},
            "Concrete": {"intercept": 2800, "slope": -15.0}
        }
        
        # Moisture count calculation factors adjusted for 5-10% increase
        self.soil_moisture_factors = {
            "GW (Well-graded gravel)": 1.0,
            "GP (Poorly graded gravel)": 1.0,
            "GM (Silty gravel)": 1.1,
            "GC (Clayey gravel)": 1.1,
            "SW (Well-graded sand)": 1.0,
            "SP (Poorly graded sand)": 1.0,
            "SM (Silty sand)": 1.2,
            "SC (Clayey sand)": 1.2,
            "ML (Silt)": 1.3,
            "CL (Lean clay)": 1.3,
            "OL (Organic silt/clay, low plasticity)": 1.4,
            "MH (Elastic silt)": 1.35,
            "CH (Fat clay)": 1.35,
            "OH (Organic silt/clay, high plasticity)": 1.4,
            "PT (Peat)": 1.5,
            "Type II (Aggregate Base)": 1.1,  # Added Type II material (similar to GM)
            "Asphalt": 0.9,
            "Concrete": 0.8
        }
        
    def calculate_density_count(self, dry_density, wet_density, depth="DS", measurement_time=1, 
                               soil_type="CL (Lean clay)", gauge_depth=8):
        """
        Calculate simulated density count based on dry density and soil type
        """
        # Get soil parameters or use default if soil type not found
        soil_params = self.soil_density_equations.get(
            soil_type, 
            {"intercept": 4986, "slope": -34.6}  # Default from overall regression
        )
        
        intercept = soil_params["intercept"]
        slope = soil_params["slope"]
        
        # Calculate base count using the linear equation
        base_count = intercept + (slope * dry_density)
        
        # Adjust for depth mode
        if depth == "BS":
            # Backscatter generally gives higher counts than direct transmission
            base_count = base_count * 1.15
        else:  # Direct Transmission
            # Adjust based on gauge depth (deeper insertion = slightly different count)
            depth_factor = 1.0 + ((gauge_depth - 6) * 0.01)  # 1% adjustment per inch from standard 6"
            base_count = base_count * depth_factor
        
        # Adjust for measurement time (longer time = more counts, follows sqrt curve)
        base_count = base_count * (measurement_time ** 0.5)
        
        # Scale the count based on the standard count ratio
        # This adjusts for differences in gauge calibration
        std_count_factor = self.std_density_count / 1570  # Standard calibration value used is 1570
        base_count = base_count * std_count_factor
        
        # Enhanced randomization to prevent repeating values, especially at high densities
        # Use a combination of techniques to ensure uniqueness
        
        # 1. Base randomization with gaussian distribution
        cv = 0.06  # 6% coefficient of variation from field data
        # Add additional randomness factor based on density to prevent repetition at high densities
        cv_adjusted = cv * (1 + (dry_density / 1000))  # Slightly increase variation for higher densities
        
        # 2. Add a small unique factor based on the specific density value
        # This helps ensure different inputs get different outputs
        uniqueness_factor = np.sin(dry_density * 0.1) * 0.03
        
        # 3. Combine the randomizations
        randomization = np.random.normal(1.0, cv_adjusted) + uniqueness_factor
        
        # Ensure the randomization factor is within reasonable bounds
        randomization = max(0.85, min(1.15, randomization))
        
        # Apply randomization
        count = int(base_count * randomization)
        
        # Final touch - add a truly random +/-1 to eliminate any potential repeats
        count += random.choice([-1, 0, 1])
        
        # Ensure count is within reasonable bounds
        return max(500, min(count, 2000))
    
    def calculate_moisture_count(self, moisture_content, measurement_time=1, soil_type="CL (Lean clay)"):
        """
        Calculate simulated moisture count based on moisture content
        """
        # Get soil moisture factor (or default to 1.0)
        soil_factor = self.soil_moisture_factors.get(soil_type, 1.0)
        
        # Base calculation for moisture count - increased by 5-10% as requested
        base_count = 50 + (9.5 * moisture_content * soil_factor)
        
        # Adjust for measurement time
        base_count = base_count * (measurement_time ** 0.5)
        
        # Scale based on standard count
        std_count_factor = self.std_moisture_count / 670  # Standard calibration value is 670
        base_count = base_count * std_count_factor
        
        # Enhanced randomization to prevent repeating values
        # Use a combination of techniques to ensure uniqueness
        
        # 1. Base randomization with gaussian distribution
        cv = 0.08  # 8% coefficient of variation
        
        # 2. Add a small unique factor based on the specific moisture value
        # This helps ensure different inputs get different outputs
        uniqueness_factor = np.cos(moisture_content * 0.2) * 0.04
        
        # 3. Combine the randomizations
        randomization = np.random.normal(1.0, cv) + uniqueness_factor
        
        # Ensure the randomization factor is within reasonable bounds
        randomization = max(0.82, min(1.18, randomization))
        
        # Apply randomization
        count = int(base_count * randomization)
        
        # Final touch - add a truly random +/-1 to eliminate any potential repeats
        count += random.choice([-1, 0, 1])
        
        # Ensure count is within reasonable bounds
        return max(50, min(count, 500))
    
    def generate_sample_tests(self, max_dry_density, optimum_moisture, num_tests=10, 
                             depth_mode="DS", test_duration=1, soil_type="CL (Lean clay)", gauge_depth=8):
        """
        Generate sample test results based on max dry density and optimum moisture
        """
        import pandas as pd  # Import pandas here to avoid import issues
        
        results = []
        
        # Generate random compaction values that vary but remain in the 95-98% range
        # Use truncated normal distribution to avoid repeats but maintain range
        compactions = []
        for _ in range(num_tests):
            # Generate a random compaction value with normal distribution
            comp = np.random.normal(96.5, 0.8)  # mean 96.5%, stddev 0.8%
            # Truncate to the desired range
            comp = max(95.0, min(98.0, comp))
            # Round to 1 decimal place
            comp = round(comp, 1)
            compactions.append(comp)
        
        # Ensure we don't have duplicate compaction values
        used_values = set()
        for i in range(len(compactions)):
            while compactions[i] in used_values:
                # Add a small random adjustment to eliminate duplicates
                compactions[i] = round(compactions[i] + random.uniform(-0.2, 0.2), 1)
                # Ensure we stay in range
                compactions[i] = max(95.0, min(98.0, compactions[i]))
            used_values.add(compactions[i])
        
        # Generate random moisture contents that vary within +/- 2% of optimum
        # Use truncated normal distribution to avoid repeats
        moistures = []
        used_moisture_values = set()
        for _ in range(num_tests):
            # Generate a random moisture with normal distribution
            moist = np.random.normal(optimum_moisture, 0.8)  # mean at optimum, stddev 0.8%
            # Truncate to the desired range
            moist = max(optimum_moisture - 2.0, min(optimum_moisture + 2.0, moist))
            # Round to 1 decimal place
            moist = round(moist, 1)
            
            # Ensure we don't have duplicate moisture values
            while moist in used_moisture_values:
                # Add a small random adjustment to eliminate duplicates
                moist = round(moist + random.uniform(-0.2, 0.2), 1)
                # Ensure we stay in range
                moist = max(optimum_moisture - 2.0, min(optimum_moisture + 2.0, moist))
            
            used_moisture_values.add(moist)
            moistures.append(moist)
        
        for i in range(1, num_tests + 1):
            # Get the compaction and moisture values for this test
            compaction_percentage = compactions[i-1]
            moisture_content = moistures[i-1]
            
            # Calculate dry density based on compaction percentage
            dry_density = round((compaction_percentage / 100) * max_dry_density, 1)
            
            # Calculate wet density
            wet_density = round(dry_density * (1 + moisture_content / 100), 1)
            
            # Calculate moisture pounds per cubic foot
            moisture_lbs = round(wet_density - dry_density, 1)
            
            # Calculate density and moisture counts
            density_count = self.calculate_density_count(
                dry_density, 
                wet_density,
                depth_mode, 
                test_duration, 
                soil_type, 
                gauge_depth
            )
            
            moisture_count = self.calculate_moisture_count(
                moisture_content, 
                test_duration, 
                soil_type
            )
            
            results.append({
                "Test #": i,
                "Density Count": density_count,
                "Moisture Count": moisture_count,
                "Wet Density (pcf)": wet_density,
                "Dry Density (pcf)": dry_density,
                "Moisture (lbs/ft³)": moisture_lbs,
                "Moisture (%)": moisture_content,
                "Compaction (%)": compaction_percentage,
                "Done": False  # Added field to track completion status
            })
        
        return pd.DataFrame(results)

# This part will only run if the script is executed directly (not when imported)
if __name__ == "__main__":
    print("Nuclear Gauge Simulator module. Import this module to use its classes in other applications.")
