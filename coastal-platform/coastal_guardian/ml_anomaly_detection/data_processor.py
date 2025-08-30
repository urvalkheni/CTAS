"""
Data Processing Module for Coastal Anomaly Detection

This module handles data preprocessing, cleaning, normalization, and feature
engineering for coastal monitoring data used in anomaly detection.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
from typing import Dict, List, Tuple, Optional, Union
import logging
from datetime import datetime, timedelta
import warnings
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore')


class CoastalDataProcessor:
    """
    Data processor for coastal monitoring data.
    
    Handles data cleaning, normalization, feature engineering, and
    preparation for machine learning models.
    """
    
    def __init__(self, scaling_method: str = "standard"):
        """
        Initialize the data processor.
        
        Args:
            scaling_method: Method for scaling data ('standard', 'minmax', 'robust')
        """
        self.scaling_method = scaling_method
        self.scaler = None
        self.imputer = None
        self.feature_columns = []
        self.is_fitted = False
        
        # Initialize scaler based on method
        if scaling_method == "standard":
            self.scaler = StandardScaler()
        elif scaling_method == "minmax":
            self.scaler = MinMaxScaler()
        elif scaling_method == "robust":
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Unsupported scaling method: {scaling_method}")
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the input data by handling missing values, outliers, and data quality issues.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning process")
        
        # Create a copy to avoid modifying original data
        cleaned_df = df.copy()
        
        # Remove duplicate rows
        initial_rows = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        logger.info(f"Removed {initial_rows - len(cleaned_df)} duplicate rows")
        
        # Handle missing values
        cleaned_df = self._handle_missing_values(cleaned_df)
        
        # Remove outliers
        cleaned_df = self._remove_outliers(cleaned_df)
        
        # Validate data types
        cleaned_df = self._validate_data_types(cleaned_df)
        
        logger.info(f"Data cleaning completed. Final shape: {cleaned_df.shape}")
        return cleaned_df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with handled missing values
        """
        logger.info("Handling missing values")
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        logger.info(f"Missing values per column:\n{missing_counts[missing_counts > 0]}")
        
        # For numerical columns, use forward fill then backward fill
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        df[numerical_cols] = df[numerical_cols].fillna(method='ffill').fillna(method='bfill')
        
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else "Unknown"
                df[col] = df[col].fillna(mode_value)
        
        # If still have missing values, use KNN imputation for numerical columns
        remaining_missing = df[numerical_cols].isnull().sum()
        if remaining_missing.sum() > 0:
            logger.info("Using KNN imputation for remaining missing values")
            imputer = KNNImputer(n_neighbors=5)
            df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
        """
        Remove outliers from numerical columns.
        
        Args:
            df: Input DataFrame
            method: Method for outlier detection ('iqr', 'zscore')
            
        Returns:
            DataFrame with outliers removed
        """
        logger.info(f"Removing outliers using {method} method")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        initial_rows = len(df)
        
        if method == "iqr":
            for col in numerical_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        elif method == "zscore":
            for col in numerical_cols:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < 3]  # Remove points with z-score > 3
        
        logger.info(f"Removed {initial_rows - len(df)} outlier rows")
        return df
    
    def _validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and convert data types as needed.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with validated data types
        """
        logger.info("Validating data types")
        
        # Convert timestamp columns if present
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        for col in timestamp_cols:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                logger.warning(f"Could not convert {col} to datetime")
        
        # Ensure numerical columns are numeric
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer new features from existing data.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering features")
        
        df_engineered = df.copy()
        
        # Time-based features
        timestamp_cols = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']
        for col in timestamp_cols:
            df_engineered[f'{col}_hour'] = df[col].dt.hour
            df_engineered[f'{col}_day'] = df[col].dt.day
            df_engineered[f'{col}_month'] = df[col].dt.month
            df_engineered[f'{col}_year'] = df[col].dt.year
            df_engineered[f'{col}_dayofweek'] = df[col].dt.dayofweek
        
        # Statistical features for numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            # Rolling statistics
            df_engineered[f'{col}_rolling_mean_3'] = df[col].rolling(window=3, min_periods=1).mean()
            df_engineered[f'{col}_rolling_std_3'] = df[col].rolling(window=3, min_periods=1).std()
            
            # Lag features
            df_engineered[f'{col}_lag_1'] = df[col].shift(1)
            df_engineered[f'{col}_lag_2'] = df[col].shift(2)
            
            # Difference features
            df_engineered[f'{col}_diff_1'] = df[col].diff(1)
            df_engineered[f'{col}_diff_2'] = df[col].diff(2)
        
        # Interaction features for coastal data
        if 'sea_level' in df.columns and 'wind_speed' in df.columns:
            df_engineered['sea_level_wind_interaction'] = df['sea_level'] * df['wind_speed']
        
        if 'temperature' in df.columns and 'ph' in df.columns:
            df_engineered['temp_ph_interaction'] = df['temperature'] * df['ph']
        
        # Environmental indices
        if all(col in df.columns for col in ['temperature', 'ph', 'dissolved_oxygen']):
            df_engineered['water_quality_index'] = (
                df['temperature'] * 0.3 + 
                df['ph'] * 0.4 + 
                df['dissolved_oxygen'] * 0.3
            )
        
        logger.info(f"Feature engineering completed. New shape: {df_engineered.shape}")
        return df_engineered
    
    def normalize_data(self, df: pd.DataFrame, feature_columns: List[str]) -> pd.DataFrame:
        """
        Normalize the data using the specified scaling method.
        
        Args:
            df: Input DataFrame
            feature_columns: List of columns to normalize
            
        Returns:
            Normalized DataFrame
        """
        logger.info(f"Normalizing data using {self.scaling_method} scaling")
        
        if not feature_columns:
            raise ValueError("Feature columns must be specified")
        
        # Store feature columns for later use
        self.feature_columns = feature_columns
        
        # Select only the feature columns
        data_to_scale = df[feature_columns].copy()
        
        # Fit and transform the data
        scaled_data = self.scaler.fit_transform(data_to_scale)
        
        # Create DataFrame with scaled data
        scaled_df = pd.DataFrame(
            scaled_data, 
            columns=feature_columns, 
            index=df.index
        )
        
        self.is_fitted = True
        logger.info("Data normalization completed")
        
        return scaled_df
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform new data using fitted scaler.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Transformed DataFrame
        """
        if not self.is_fitted:
            raise ValueError("Scaler must be fitted before transforming data")
        
        if not self.feature_columns:
            raise ValueError("Feature columns not set")
        
        # Select only the feature columns
        data_to_transform = df[self.feature_columns].copy()
        
        # Transform the data
        transformed_data = self.scaler.transform(data_to_transform)
        
        # Create DataFrame with transformed data
        transformed_df = pd.DataFrame(
            transformed_data, 
            columns=self.feature_columns, 
            index=df.index
        )
        
        return transformed_df
    
    def prepare_training_data(self, df: pd.DataFrame, feature_columns: List[str], 
                            target_column: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """
        Prepare data for training by cleaning, engineering features, and normalizing.
        
        Args:
            df: Input DataFrame
            feature_columns: List of feature columns
            target_column: Optional target column for supervised learning
            
        Returns:
            Tuple of (features, target) where target is None for unsupervised learning
        """
        logger.info("Preparing training data")
        
        # Clean the data
        cleaned_df = self.clean_data(df)
        
        # Engineer features
        engineered_df = self.engineer_features(cleaned_df)
        
        # Update feature columns to include engineered features
        available_features = [col for col in engineered_df.columns if col in feature_columns]
        if not available_features:
            raise ValueError("No feature columns found in the dataset")
        
        # Normalize the data
        normalized_df = self.normalize_data(engineered_df, available_features)
        
        # Prepare target if specified
        target = None
        if target_column and target_column in engineered_df.columns:
            target = engineered_df[target_column]
        
        logger.info(f"Training data prepared. Features: {len(available_features)}, Samples: {len(normalized_df)}")
        
        return normalized_df, target
    
    def get_feature_importance(self, df: pd.DataFrame, feature_columns: List[str]) -> Dict[str, float]:
        """
        Calculate feature importance based on variance and correlation.
        
        Args:
            df: Input DataFrame
            feature_columns: List of feature columns
            
        Returns:
            Dictionary of feature importance scores
        """
        logger.info("Calculating feature importance")
        
        # Select feature columns
        feature_data = df[feature_columns].copy()
        
        # Calculate variance for each feature
        variances = feature_data.var()
        
        # Calculate correlation with other features
        correlations = feature_data.corr().abs().mean()
        
        # Combine variance and correlation for importance score
        importance_scores = {}
        for feature in feature_columns:
            variance_score = variances[feature] / variances.sum()
            correlation_score = correlations[feature]
            importance_scores[feature] = (variance_score + correlation_score) / 2
        
        # Sort by importance
        importance_scores = dict(sorted(importance_scores.items(), key=lambda x: x[1], reverse=True))
        
        return importance_scores
    
    def save_processor(self, filepath: str) -> None:
        """
        Save the fitted processor to disk.
        
        Args:
            filepath: Path where to save the processor
        """
        import joblib
        
        if not self.is_fitted:
            raise ValueError("Processor must be fitted before saving")
        
        processor_data = {
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'scaling_method': self.scaling_method,
            'is_fitted': self.is_fitted
        }
        
        joblib.dump(processor_data, filepath)
        logger.info(f"Processor saved to {filepath}")
    
    def load_processor(self, filepath: str) -> None:
        """
        Load a fitted processor from disk.
        
        Args:
            filepath: Path to the saved processor
        """
        import joblib
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Processor file not found: {filepath}")
        
        processor_data = joblib.load(filepath)
        
        self.scaler = processor_data['scaler']
        self.feature_columns = processor_data['feature_columns']
        self.scaling_method = processor_data['scaling_method']
        self.is_fitted = processor_data['is_fitted']
        
        logger.info(f"Processor loaded from {filepath}")


class StormSurgeDataProcessor(CoastalDataProcessor):
    """
    Specialized data processor for storm surge data.
    """
    
    def __init__(self):
        super().__init__(scaling_method="robust")  # Robust scaling for weather data
        self.default_features = ["sea_level", "wind_speed", "atmospheric_pressure", "wave_height"]
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer storm surge specific features.
        """
        df_engineered = super().engineer_features(df)
        
        # Storm surge specific features
        if 'wind_speed' in df.columns:
            # Wind speed categories
            df_engineered['wind_speed_category'] = pd.cut(
                df['wind_speed'], 
                bins=[0, 10, 20, 30, 50, 100], 
                labels=['Calm', 'Light', 'Moderate', 'Strong', 'Very Strong']
            )
            
            # Wind speed squared (for non-linear relationships)
            df_engineered['wind_speed_squared'] = df['wind_speed'] ** 2
        
        if 'sea_level' in df.columns:
            # Sea level change rate
            df_engineered['sea_level_change_rate'] = df['sea_level'].diff(1)
            
            # Sea level acceleration
            df_engineered['sea_level_acceleration'] = df['sea_level'].diff(1).diff(1)
        
        if all(col in df.columns for col in ['wind_speed', 'atmospheric_pressure']):
            # Storm intensity index
            df_engineered['storm_intensity'] = (
                df['wind_speed'] * 0.6 + 
                (1013.25 - df['atmospheric_pressure']) * 0.4  # Pressure deficit
            )
        
        return df_engineered


class WaterQualityDataProcessor(CoastalDataProcessor):
    """
    Specialized data processor for water quality data.
    """
    
    def __init__(self):
        super().__init__(scaling_method="standard")
        self.default_features = ["ph", "turbidity", "dissolved_oxygen", "temperature", "conductivity"]
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer water quality specific features.
        """
        df_engineered = super().engineer_features(df)
        
        # Water quality specific features
        if 'ph' in df.columns:
            # pH categories
            df_engineered['ph_category'] = pd.cut(
                df['ph'], 
                bins=[0, 6.5, 7.5, 8.5, 14], 
                labels=['Acidic', 'Slightly Acidic', 'Neutral', 'Alkaline']
            )
            
            # pH deviation from neutral
            df_engineered['ph_deviation'] = abs(df['ph'] - 7.0)
        
        if 'temperature' in df.columns:
            # Temperature categories
            df_engineered['temperature_category'] = pd.cut(
                df['temperature'], 
                bins=[0, 10, 20, 30, 50], 
                labels=['Cold', 'Cool', 'Warm', 'Hot']
            )
        
        if all(col in df.columns for col in ['ph', 'temperature', 'dissolved_oxygen']):
            # Water quality index
            df_engineered['water_quality_index'] = (
                (df['ph'] - 6.5) * 0.3 +  # pH factor
                (df['dissolved_oxygen'] / 10) * 0.4 +  # Oxygen factor
                (25 - abs(df['temperature'] - 25)) / 25 * 0.3  # Temperature factor
            )
        
        if 'conductivity' in df.columns:
            # Conductivity categories
            df_engineered['conductivity_category'] = pd.cut(
                df['conductivity'], 
                bins=[0, 100, 500, 1000, 10000], 
                labels=['Low', 'Medium', 'High', 'Very High']
            )
        
        return df_engineered
