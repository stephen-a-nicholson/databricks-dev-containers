"""
Tests for simple_pipeline.py

Demonstrates how to test PySpark code using pytest and chispa.
"""

import pytest
from pyspark.sql import SparkSession
from chispa.dataframe_comparer import assert_df_equality
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType


@pytest.fixture(scope="session")
def spark():
    """Create a local Spark session for testing."""
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("test")
        .getOrCreate()
    )
    yield spark
    spark.stop()


def test_basic_aggregation(spark):
    """Test basic groupBy and aggregation."""
    # Create test data
    data = [
        ("zone_a", 100.0),
        ("zone_a", 150.0),
        ("zone_b", 200.0),
    ]
    
    schema = StructType([
        StructField("zone", StringType(), True),
        StructField("fare", DoubleType(), True),
    ])
    
    df = spark.createDataFrame(data, schema)
    
    # Perform aggregation
    from pyspark.sql import functions as F
    result = (
        df.groupBy("zone")
        .agg(
            F.count("*").alias("count"),
            F.sum("fare").alias("total")
        )
    )
    
    # Expected result
    expected_data = [
        ("zone_a", 2, 250.0),
        ("zone_b", 1, 200.0),
    ]
    
    expected_schema = StructType([
        StructField("zone", StringType(), True),
        StructField("count", LongType(), False),
        StructField("total", DoubleType(), True),
    ])
    
    expected_df = spark.createDataFrame(expected_data, expected_schema)
    
    # Compare using chispa
    assert_df_equality(result, expected_df, ignore_row_order=True)


def test_filtering(spark):
    """Test DataFrame filtering."""
    data = [
        ("2024-01-01", 100.0),
        ("2024-01-02", 50.0),
        ("2024-01-03", 200.0),
    ]
    
    schema = StructType([
        StructField("date", StringType(), True),
        StructField("amount", DoubleType(), True),
    ])
    
    df = spark.createDataFrame(data, schema)
    
    # Filter for amounts > 75
    result = df.filter("amount > 75")
    
    # Should have 2 rows
    assert result.count() == 2
    
    # Check values
    amounts = [row.amount for row in result.collect()]
    assert 100.0 in amounts
    assert 200.0 in amounts


def test_column_operations(spark):
    """Test column transformations."""
    from pyspark.sql import functions as F
    
    data = [
        ("item_a", 10, 5.0),
        ("item_b", 20, 3.0),
    ]
    
    schema = StructType([
        StructField("item", StringType(), True),
        StructField("quantity", LongType(), True),
        StructField("price", DoubleType(), True),
    ])
    
    df = spark.createDataFrame(data, schema)
    
    # Add calculated column
    result = df.withColumn("total", F.col("quantity") * F.col("price"))
    
    # Verify calculation
    totals = {row.item: row.total for row in result.collect()}
    assert totals["item_a"] == 50.0
    assert totals["item_b"] == 60.0
