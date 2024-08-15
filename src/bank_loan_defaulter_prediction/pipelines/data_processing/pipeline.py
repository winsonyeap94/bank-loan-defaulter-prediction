from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_dataset, feature_engineering


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_dataset,
                inputs={"data_df": "train_dataset"},
                outputs="preprocessed_train_dataset",
                name="preprocess_train_dataset",
            ),
            node(
                func=preprocess_dataset,
                inputs=["test_dataset", "preprocessed_train_dataset"],
                outputs="preprocessed_test_dataset",
                name="preprocess_test_dataset",
            ),
            node(
                func=feature_engineering,
                inputs=["preprocessed_train_dataset"],
                outputs="feature_engineered_train_dataset",
                name="feature_engineered_train_dataset",
            ),
            node(
                func=feature_engineering,
                inputs=["preprocessed_test_dataset"],
                outputs="feature_engineered_test_dataset",
                name="feature_engineered_test_dataset",
            ),
        ]
    )
