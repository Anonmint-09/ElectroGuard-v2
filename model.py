import pickle
import numpy as np

data = pickle.load(open("model.pkl", "rb"))

model = data["model"]
scaler = data["scaler"]
features = data["features"]
MODEL_ACCURACY = data.get("accuracy", 99.5)

THEFT_TYPES = {
    "direct_hook": "Direct Hooking (Bypass Meter)",
    "tamper": "Meter Tampering",
    "bypass": "Illegal Line Bypass",
    "overload": "Unauthorized Overloading"
}

def predict_theft(voltage, current, power, time, meter_diff):
    """
    Predict electricity theft with confidence score and detailed reasons.
    Returns: (result_label, confidence_pct, reasons_list, theft_type_guess)
    """
    # Engineered features
    power_per_current = power / (current + 0.001)
    meter_efficiency = meter_diff / ((power * time / 1000) + 0.001)
    current_voltage_ratio = current / (voltage + 0.001)

    input_data = {
        "Voltage": voltage,
        "Current": current,
        "Power": power,
        "Time": time,
        "MeterDiff": meter_diff,
        "PowerPerCurrent": power_per_current,
        "MeterEfficiency": meter_efficiency,
        "CurrentVoltageRatio": current_voltage_ratio
    }

    input_values = [input_data[f] for f in features]
    input_scaled = scaler.transform([input_values])

    prediction = model.predict(input_scaled)[0]
    proba = model.predict_proba(input_scaled)[0]
    confidence = round(max(proba) * 100, 1)

    reasons = []
    severity_score = 0

    # Rule-based analysis
    if power > 4000:
        reasons.append(f"⚡ Extremely high power consumption ({power}W — normal max ~3500W)")
        severity_score += 3
    elif power > 3000:
        reasons.append(f"⚠️ High power consumption ({power}W)")
        severity_score += 1

    if current > 18:
        reasons.append(f"🔴 Dangerous current level ({current}A — safe max ~15A)")
        severity_score += 3
    elif current > 12:
        reasons.append(f"⚠️ Elevated current ({current}A)")
        severity_score += 1

    if voltage < 200 or voltage > 250:
        reasons.append(f"📉 Abnormal voltage ({voltage}V — normal: 210–240V)")
        severity_score += 2

    if meter_efficiency < 0.3:
        reasons.append(f"🔧 Possible meter tampering (meter efficiency: {meter_efficiency:.2f})")
        severity_score += 3
    elif meter_efficiency < 0.6:
        reasons.append(f"⚠️ Low meter reading efficiency ({meter_efficiency:.2f})")
        severity_score += 1

    if time < 2:
        reasons.append(f"⏱️ Very short usage duration ({time}h — suspicious high usage)")
        severity_score += 2

    expected_meter = round(power * time / 1000, 2)
    if meter_diff < expected_meter * 0.4:
        reasons.append(f"📊 Meter reading far below expected (got {meter_diff} kWh, expected ~{expected_meter} kWh)")
        severity_score += 3

    # Guess theft type
    theft_type = None
    if prediction == 1:
        if voltage < 205 and current > 15:
            theft_type = THEFT_TYPES["direct_hook"]
        elif meter_efficiency < 0.3:
            theft_type = THEFT_TYPES["tamper"]
        elif power > 5000:
            theft_type = THEFT_TYPES["bypass"]
        else:
            theft_type = THEFT_TYPES["overload"]

    if prediction == 1:
        if severity_score >= 6:
            severity = "CRITICAL"
        elif severity_score >= 3:
            severity = "HIGH"
        else:
            severity = "MODERATE"
        result = "THEFT_DETECTED"
    else:
        severity = "NONE"
        result = "SAFE"

    return result, confidence, reasons, theft_type, severity
