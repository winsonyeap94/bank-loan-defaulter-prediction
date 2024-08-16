from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    plot_roc_curve,
    plot_confusion_matrix
)


def create_pipeline(**kwargs) -> Pipeline:
    """This is a simple pipeline which generates a pair of plots"""
    return pipeline(
        [
            node(
                func=plot_roc_curve,
                inputs=["train_predictions", "validation_predictions", "params:model_options"],
                outputs="viz_roc_curve",
            ),
            node(
                func=plot_confusion_matrix,
                inputs=["train_predictions", "validation_predictions", "params:model_options"],
                outputs="viz_confusion_matrix",
            )
        ]
    )
