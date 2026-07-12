from ml.predict_model import predict_risk_hybrid

data = {
    "revolving_utilization": 0.25,
    "age": 35,
    "delinquency_30_59": 0,
    "debt_ratio": 0.45,
    "monthly_income": 8000000,
    "num_credit_lines": 6,
    "delinquency_90": 0,
    "real_estate_loans": 1,
    "delinquency_60_89": 0,
    "dependents": 2,
}

hasil = predict_risk_hybrid(data)

print(hasil)
