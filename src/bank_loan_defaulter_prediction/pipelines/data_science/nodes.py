import logging
from typing import Dict, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    """
    Splits data into training and validation datasets.
    """
    train_df, validation_df = train_test_split(
        data, stratify=data[parameters['target']], test_size=parameters["validation_size"], random_state=parameters["random_state"]
    )
    train_df = train_df.reset_index(drop=True).assign(DATA_GROUP='Train')
    validation_df = validation_df.reset_index(drop=True).assign(DATA_GROUP='Validation')
    return train_df, validation_df


def train_model(train_df: pd.DataFrame, parameters: Dict) -> Pipeline:
    """
    Trains the classifier model.
    """
    # Setting up the Sklearn Pipeline
    # Preprocessing for numerical data
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    # Preprocessing for categorical data
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    # Combine preprocessing steps
    preprocessor_pipeline = ColumnTransformer(
        transformers=[
            ('numeric', numerical_transformer, parameters['features']['numeric']),
            ('categorical', categorical_transformer, parameters['features']['categorical'])
        ]
    )
    # Create the final pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor_pipeline),
        ('classifier', LogisticRegression(random_state=parameters['random_state']))
    ])
    
    input_features = parameters['features']['numeric'] + parameters['features']['categorical']
    model_pipeline.fit(train_df[input_features], train_df[parameters['target']])
    return model_pipeline


def evaluate_model(
    classifier_model: Pipeline, train_df: pd.DataFrame, validation_df: pd.DataFrame, parameters: Dict
) -> Tuple:
    """
    Calculates and logs the classification metrics.
    """
    target_var = parameters['target']
    input_features = parameters['features']['numeric'] + parameters['features']['categorical']
    train_df[f'{target_var}_PRED'] = classifier_model.predict(train_df[input_features])
    train_df[f'{target_var}_PRED_PROBA'] = classifier_model.predict_proba(train_df[input_features])[:, 1]
    validation_df[f'{target_var}_PRED'] = classifier_model.predict(validation_df[input_features])
    validation_df[f'{target_var}_PRED_PROBA'] = classifier_model.predict_proba(validation_df[input_features])[:, 1]
    
    def _calculate_metrics(y_true, y_pred, y_pred_proba):
        roc_value = roc_auc_score(y_true=y_true, y_score=y_pred_proba)
        accuracy_value = accuracy_score(y_true=y_true, y_pred=y_pred)
        f1_value = f1_score(y_true=y_true, y_pred=y_pred)
        return {
            "roc_auc": roc_value,
            "accuracy": accuracy_value,
            "f1": f1_value
        }
    
    train_metrics = _calculate_metrics(train_df[target_var], train_df[f'{target_var}_PRED'], train_df[f'{target_var}_PRED_PROBA'])
    validation_metrics = _calculate_metrics(validation_df[target_var], validation_df[f'{target_var}_PRED'], validation_df[f'{target_var}_PRED_PROBA'])
    combined_metrics = {
        "(Train) ROC AUC": train_metrics['roc_auc'],
        "(Train) Accuracy": train_metrics['accuracy'],
        "(Train) F1 Score": train_metrics['f1'],
        "(Validation) ROC AUC": validation_metrics['roc_auc'],
        "(Validation) Accuracy": validation_metrics['accuracy'],
        "(Validation) F1 Score": validation_metrics['f1']
    }
    
    _logger = logging.getLogger(__name__)
    _logger.info(f"============================== Train Metrics ==============================")
    _logger.info(f"ROC AUC: {train_metrics['roc_auc']:.3f}")
    _logger.info(f"Accuracy: {train_metrics['accuracy']:.3f}")
    _logger.info(f"F1 Score: {train_metrics['f1']:.3f}")
    _logger.info(f"============================== Validation Metrics ==============================")
    _logger.info(f"ROC AUC: {validation_metrics['roc_auc']:.3f}")
    _logger.info(f"Accuracy: {validation_metrics['accuracy']:.3f}")
    _logger.info(f"F1 Score: {validation_metrics['f1']:.3f}")
    
    return combined_metrics, train_df, validation_df


def predict_on_test_dataset(
    classifier_model: Pipeline, test_df: pd.DataFrame, parameters: Dict
) -> pd.DataFrame:
    """
    Predicts the target variable on the test dataset.
    """
    input_features = parameters['features']['numeric'] + parameters['features']['categorical']
    test_df[parameters['target']] = classifier_model.predict(test_df[input_features])
    return test_df
