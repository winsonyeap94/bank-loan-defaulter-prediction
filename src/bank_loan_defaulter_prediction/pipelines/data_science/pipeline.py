from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model, predict_on_test_dataset


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["feature_engineered_train_dataset", "params:model_options"],
                outputs=["model_input_train", "model_input_validation"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["model_input_train", "params:model_options"],
                outputs="classifier_model",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["classifier_model", "model_input_train", "model_input_validation", "params:model_options"],
                outputs="evaluation_metrics",
                name="evaluate_model_node",
            ),
            node(
                func=predict_on_test_dataset,
                inputs=["classifier_model", "feature_engineered_test_dataset", "params:model_options"],
                outputs="test_predictions",
                name="predict_on_test_node",
            ),
        ]
    )
