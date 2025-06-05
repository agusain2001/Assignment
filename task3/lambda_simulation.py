
import csv
import os
from datetime import datetime
from collections import defaultdict
import pandas as pd

# Simulate environment variables or context that Lambda might receive
# In a real Lambda, these might come from the event payload or environment variables
SIMULATED_S3_BUCKET_PATH = '/home/ubuntu/task3_aws_lambda/simulated_s3'
SIMULATED_S3_OUTPUT_PATH = '/home/ubuntu/task3_aws_lambda/simulated_s3_output'
TARGET_DATE_STR = os.getenv('TARGET_DATE', '2025-06-05') # Default to the date we created data for

def find_latest_trade_file(base_path, target_date):
    """Simulates finding the relevant trade file in S3 for a given date."""
    try:
        date_obj = datetime.strptime(target_date, '%Y-%m-%d')
        file_path = os.path.join(base_path, str(date_obj.year), f"{date_obj.month:02d}", f"{date_obj.day:02d}", 'trades.csv')
        
        # In a real scenario with multiple files per day (e.g., timestamped),
        # you would list objects and find the latest one.
        # For this simulation, we assume one file named 'trades.csv'.
        if os.path.exists(file_path):
            print(f"Found trade file: {file_path}")
            return file_path
        else:
            print(f"Trade file not found for date {target_date} at {file_path}")
            return None
    except ValueError:
        print(f"Invalid date format: {target_date}. Please use YYYY-MM-DD.")
        return None
    except Exception as e:
        print(f"Error finding trade file: {e}")
        return None

def analyze_trade_data(file_path):
    """Reads trade data from CSV and calculates volume and average price per stock."""
    if not file_path:
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"Read {len(df)} trades from {file_path}")

        # Ensure correct data types
        df['price'] = pd.to_numeric(df['price'])
        df['quantity'] = pd.to_numeric(df['quantity'])

        # Calculate total value for weighted average price
        df['total_value'] = df['price'] * df['quantity']

        # Group by ticker and aggregate
        analysis = df.groupby('ticker').agg(
            total_volume=('quantity', 'sum'),
            total_value=('total_value', 'sum')
        ).reset_index()

        # Calculate average price (weighted by quantity)
        analysis['average_price'] = analysis['total_value'] / analysis['total_volume']
        analysis['average_price'] = analysis['average_price'].round(2) # Round to 2 decimal places

        # Select and rename columns for the final report
        analysis_report = analysis[['ticker', 'total_volume', 'average_price']]
        print("Analysis complete:")
        print(analysis_report)
        return analysis_report

    except FileNotFoundError:
        print(f"Error: Input file not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error processing trade data: {e}")
        return None

def save_analysis_results(analysis_df, output_base_path, target_date):
    """Simulates saving the analysis results back to S3."""
    if analysis_df is None or analysis_df.empty:
        print("No analysis data to save.")
        return False

    try:
        date_obj = datetime.strptime(target_date, '%Y-%m-%d')
        output_dir = os.path.join(output_base_path, str(date_obj.year), f"{date_obj.month:02d}", f"{date_obj.day:02d}")
        os.makedirs(output_dir, exist_ok=True)
        
        output_filename = f"analysis_{target_date}.csv"
        output_file_path = os.path.join(output_dir, output_filename)
        
        analysis_df.to_csv(output_file_path, index=False)
        print(f"Analysis results saved to: {output_file_path}")
        return True
    except Exception as e:
        print(f"Error saving analysis results: {e}")
        return False

# Simulating the Lambda handler function
def lambda_handler(event, context):
    """Main function simulating the AWS Lambda execution flow."""
    print(f"Lambda simulation started for date: {TARGET_DATE_STR}")
    
    # 1. Find the trade data file (Simulated S3 List/Get)
    trade_file_path = find_latest_trade_file(SIMULATED_S3_BUCKET_PATH, TARGET_DATE_STR)
    
    if not trade_file_path:
        return {'statusCode': 404, 'body': f'Trade data not found for {TARGET_DATE_STR}'}
    
    # 2. Analyze the trade data
    analysis_results = analyze_trade_data(trade_file_path)
    
    if analysis_results is None:
        return {'statusCode': 500, 'body': 'Failed to analyze trade data'}
        
    # 3. Save the analysis results (Simulated S3 Put)
    success = save_analysis_results(analysis_results, SIMULATED_S3_OUTPUT_PATH, TARGET_DATE_STR)
    
    if success:
        print("Lambda simulation completed successfully.")
        return {'statusCode': 200, 'body': f'Analysis complete for {TARGET_DATE_STR}. Results saved.'}
    else:
        print("Lambda simulation failed during saving results.")
        return {'statusCode': 500, 'body': 'Failed to save analysis results'}

# --- Main execution block for local testing ---
if __name__ == "__main__":
    # Simulate calling the handler (like AWS would)
    # Pass dummy event and context (not used in this simple simulation)
    result = lambda_handler({}, {})
    print(f"\nLambda simulation finished with result: {result}")

