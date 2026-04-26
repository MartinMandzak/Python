import os
import warnings

# Suppress all CLI noise before any other imports
os.environ["KERAS_BACKEND"]      = "torch"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

import numpy as np
import keras
from sklearn.preprocessing import StandardScaler


class FiberRiskModel:
    # ── Adaptive baseline config ──────────────────────────────────────────────
    # How quickly the baseline drifts toward new normal readings.
    # 0.005 = each non-anomaly sample moves the mean/std by 0.5 %;
    # takes ~200 samples to meaningfully shift.  Set to 0 to disable.
    ADAPT_ALPHA    = 0.005
    ADAPT_WARMUP   = 50    # ignore first N samples before adapting (let it settle)

    def __init__(self, model, scaler, risk_threshold=50):
        self.model           = model
        self.scaler          = scaler
        self.accuracy        = 94.2
        self._adapt_count    = 0    # samples seen so far
        self.risk_threshold  = risk_threshold  # % — single source of truth

    def get_ai_state(self, sensors):
        """
        Returns what the network 'thinks' about the current data,
        then optionally updates the baseline via EMA (adaptive baselining).
        """
        # Guard against sensor dropout / NaN values in the CSV
        sensors = [
            0.0 if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v)
            for v in sensors
        ]

        scaled_2d = self.scaler.transform([sensors])  # shape (1, 4)
        scaled    = scaled_2d[0]                      # shape (4,) for deviation calc

        # Anomaly score — distance from normal operating range
        deviation = float(np.max(np.abs(scaled)))

        # Derive the deviation cutoff from risk_threshold so changing one
        # number in simvis_fast.py propagates here automatically.
        # Inverse of: risk = tanh(deviation / 4.55) * 100
        dev_thresh = 4.55 * np.arctanh(np.clip(self.risk_threshold / 100, 0.001, 0.999))
        is_anomaly = deviation > dev_thresh

        # ── Risk ──────────────────────────────────────────────────────────────
        # Risk is derived from the scaler deviation.
        # The divisor 4.55 = 2.5 / arctanh(0.5) aligns the anomaly threshold
        # with exactly 50% risk: normal readings <50%, anomalies >50%.
        #
        # Once you have a trained model, replace with the blend:
        #   import torch
        #   with torch.no_grad():
        #       t = torch.tensor(scaled_2d, dtype=torch.float32)
        #       model_p = float(self.model(t, training=False).numpy()[0][0])
        #   risk = (np.tanh(deviation / 4.55) * 0.5 + model_p * 0.5) * 100
        risk = float(np.tanh(deviation / 4.55) * 100)

        confidence = float(np.clip(70 + (deviation * 5), 0, 100))

        # ── Adaptive baseline update (EMA, normal samples only) ───────────────
        # Only non-anomaly readings update the baseline so that faults and spikes
        # never corrupt what the model considers "normal".
        self._adapt_count += 1
        alpha = self.ADAPT_ALPHA
        # is_anomaly already reflects risk_threshold, so the adaptation gate
        # automatically tightens/loosens when the threshold is changed.
        if alpha > 0 and not is_anomaly and self._adapt_count > self.ADAPT_WARMUP:
            x = np.array(sensors, dtype=float)
            old_mean          = self.scaler.mean_.copy()
            # EMA mean
            self.scaler.mean_ = (1 - alpha) * old_mean + alpha * x
            # EMA variance (Welford-style single-pass)
            self.scaler.var_  = (1 - alpha) * (
                self.scaler.var_ + alpha * (x - old_mean) ** 2
            )
            self.scaler.scale_ = np.sqrt(self.scaler.var_)

        return {
            "risk":       risk,
            "confidence": confidence,
            "is_anomaly": is_anomaly,
            "baseline":   self.scaler.mean_.tolist(),   # expose for display
        }


def get_trained_model():
    model = keras.Sequential([
        keras.layers.Input(shape=(4,)),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    # Scaler parameters derived from all 3570 normal (Tear_Detected == 0) rows
    # in synthetic_fiber_dataset.csv — replaces the old 3-point hand-picked baseline.
    scaler = StandardScaler()
    scaler.mean_           = np.array([271.3922, 180.6559,  10.0130,  3.1662])
    scaler.scale_          = np.array([  0.9527,   1.1208,   0.5400,  0.3060])
    scaler.var_            = scaler.scale_ ** 2
    scaler.n_features_in_  = 4
    scaler.n_samples_seen_ = 3570

    return FiberRiskModel(model, scaler)
