import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from dataclasses import dataclass
from src.ml_project.utils import save_obj
from src.ml_project.exception import CustomException
from src.ml_project.logger import logging


@dataclass
class DataTranformationConfig:
    obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTranformationConfig()
    
    def get_data_transformation_obj(self):
        try:
            numerical_columns=["reading_score","writing_score"]
            categorical_columns=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]

            num_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='median')),
                ("scalar",StandardScaler())
            ])
            cat_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='most_frequent')),
                ("one_hot_encoder",OneHotEncoder()),
                ("scalar",StandardScaler(with_mean=False))
            ])

            logging.info(f"Categorical Columns: {categorical_columns}")
            logging.info(f"Numerical Columns: {numerical_columns}")

            preprocessor=ColumnTransformer(transformers=[
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Train Test Data read as Dataframe.")

            preprocessor_obj=self.get_data_transformation_obj()

            target_column_name="math_score"
            numerical_columns=["reading_score","writing_score"]

            ## dividing train datasets into dependent and independent features

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            ## dividing train datasets into dependent and independent features
            
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying preprocessing on training and testing dataframe.")

            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)         # use transform because of Data Leakage Concept

            train_arr=np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saving preprocessing object file.")

            save_obj(
                file_path=self.data_transformation_config.obj_file_path,
                obj=preprocessor_obj
            )

            return(
                train_arr, test_arr, self.data_transformation_config.obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)