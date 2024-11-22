import random
from datetime import datetime

import numpy as np
import pandas as pd
import wandb
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.logging_config import get_logger

wandb.Settings(quiet=True)
wandb.login()


def set_seeds(seed: int):
    """ Set seeds for reproducibility. """
    random.seed(seed)
    np.random.seed(seed)


if __name__ == "__main__":
    logger = get_logger('train')
    logger.setLevel('INFO')

    random_seed = 42
    set_seeds(random_seed)

    logger.info("📥 Loading dataset...")
    df = pd.read_csv("../data/data_2024-11-22_14:49:31.csv")
    logger.info(f"📊 Dataset shape: {df.shape}")

    logger.info("📦 Preparing dataset...")
    df = df.dropna()
    X = df.drop(columns=["url", "is_phishing", "domain", "tld"])
    y = df["is_phishing"]
    logger.info(f"📊 X shape: {X.shape}, y shape: {y.shape}")

    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler()),
    ])

    num_attribs = list(X)

    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
    ])

    X_prepared = full_pipeline.fit_transform(X)

    logger.info("✂️ Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X_prepared, y, test_size=0.1, random_state=random_seed)

    logger.info("⏳ Starting hyperparameter tuning...")
    wandb.init(
        project='phishing-url-detection',
        config={
            "model": "Random Forest",
        }
    )

    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None]
    }

    rf_clf = RandomForestClassifier(random_state=random_seed)
    grid_search = GridSearchCV(estimator=rf_clf, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    logger.info("✨ Best hyperparameters found:")
    logger.info(grid_search.best_params_)

    best_rf = grid_search.best_estimator_
    logger.info("✅ Hyperparameter tuning finished.")

    logger.info("⏱️ Computing metrics...")
    y_pred = best_rf.predict(X_test)
    overall_metrics = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    matrix = confusion_matrix(y_test, y_pred)

    metrics = {
        "accuracy": best_rf.score(X_test, y_test),
        "precision": overall_metrics[0],
        "recall": overall_metrics[1],
        "f1": overall_metrics[2],
        "false_positive_rate": matrix[0, 1] / y_test.value_counts()[0],
        "false_negative_rate": matrix[1, 0] / y_test.value_counts()[1]
    }

    wandb.log(metrics)
    wandb.finish()

    logger.info("💾 Saving model...")
    pipeline = Pipeline([
        ('preparation', full_pipeline),
        ('model', best_rf)
    ])

    output_file = f"../models/random_forest_with_pipeline_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.joblib"
    dump(pipeline, output_file)
    logger.info(f"✅ Model saved to {output_file}")

    logger.info("✅ Training finished.")
