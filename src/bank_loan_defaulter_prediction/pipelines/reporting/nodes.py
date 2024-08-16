from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, ConfusionMatrixDisplay


def plot_roc_curve(
    train_predictions: pd.DataFrame, validation_predictions: pd.DataFrame, parameters: Dict
):
    target_var = parameters["target"]
    train_auc = roc_auc_score(y_true=train_predictions[target_var], y_score=train_predictions[f"{target_var}_PRED_PROBA"])
    train_fpr, train_tpr, _ = roc_curve(y_true=train_predictions[target_var], y_score=train_predictions[f"{target_var}_PRED_PROBA"])
    validation_auc = roc_auc_score(y_true=validation_predictions[target_var], y_score=validation_predictions[f"{target_var}_PRED_PROBA"])
    validation_fpr, validation_tpr, _ = roc_curve(y_true=validation_predictions[target_var], y_score=validation_predictions[f"{target_var}_PRED_PROBA"])
    fig, ax = plt.subplots(figsize=(10, 8), constrained_layout=True)
    ax.plot(train_fpr, train_tpr, label=f"Train ROC Curve (AUC = {train_auc:.2f})")
    ax.plot(validation_fpr, validation_tpr, label=f"Validation ROC Curve (AUC = {validation_auc:.2f})")
    ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="black", label="Chance level (AUC=0.5)", alpha=0.8)
    ax.grid()
    ax.legend()
    ax.set_xlabel("False Positive Rate (FPR)")
    ax.set_ylabel("True Positive Rate (TPR)")
    fig.suptitle("ROC Curve", fontweight='bold')
    return fig


def plot_confusion_matrix(
    train_predictions: pd.DataFrame, validation_predictions: pd.DataFrame, parameters: Dict
):
    target_var = parameters["target"]
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8), constrained_layout=True)
    for col_id, normalize in enumerate([None, 'true']):
        ConfusionMatrixDisplay.from_predictions(
            y_true=train_predictions[target_var],
            y_pred=train_predictions[f"{target_var}_PRED"],
            ax=axes[0][col_id],
            normalize=normalize,
            values_format=",.0f" if normalize is None else ".2f",
            cmap=plt.cm.Blues,
            display_labels=["Non-Default", "Default"]
        )
        axes[0][col_id].set_title(f"Train Confusion Matrix (normalize={normalize})", fontweight='bold')
        ConfusionMatrixDisplay.from_predictions(
            y_true=validation_predictions[target_var],
            y_pred=validation_predictions[f"{target_var}_PRED"],
            ax=axes[1][col_id],
            normalize=normalize,
            values_format=",.0f" if normalize is None else ".2f",
            cmap=plt.cm.Blues,
            display_labels=["Non-Default", "Default"]
        )
        axes[1][col_id].set_title(f"Validation Confusion Matrix (normalize={normalize})", fontweight='bold')
    return fig
