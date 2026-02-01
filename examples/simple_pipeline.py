"""
Simple PySpark pipeline example.

This demonstrates basic PySpark operations that can be run locally
against a Databricks cluster using Databricks Connect.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def create_spark_session():
    """Create and return a Spark session."""
    return SparkSession.builder.appName("simple_pipeline").getOrCreate()


def process_sales_data(spark: SparkSession):
    """
    Process sales data and calculate revenue by region.
    
    Args:
        spark: Active Spark session
        
    Returns:
        DataFrame with aggregated results
    """
    # Read data from Databricks table
    # Replace 'samples.nyctaxi.trips' with your actual table
    df = spark.read.table("samples.nyctaxi.trips")
    
    # Simple aggregation
    result = (
        df.groupBy("pickup_zip")
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("fare_amount").alias("avg_fare"),
            F.sum("fare_amount").alias("total_revenue")
        )
        .orderBy(F.desc("total_revenue"))
        .limit(10)
    )
    
    return result


def main():
    """Main pipeline execution."""
    # Create Spark session (connects to Databricks via Databricks Connect)
    spark = create_spark_session()
    
    try:
        print("Processing sales data...")
        result = process_sales_data(spark)
        
        print("\nTop 10 Pickup Locations by Revenue:")
        result.show()
        
        print("\nPipeline completed successfully!")
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
        raise
    
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
