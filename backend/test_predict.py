from ml.predict_model import predict_risk_hybrid


def tampilkan_hasil(judul, result):
    print("\n" + "=" * 50)
    print(judul)
    print("=" * 50)

    if not result["success"]:
        print("ERROR :", result["message"])
        return

    print("Status Kredit    :", result["status"])
    print("Probability      :", round(result["probability"], 4))

    if result["status"] == "LAYAK":
        print("Risk Level       :", result["risk_level"])
        print("Risk Probability :", round(result["risk_probability"], 4))
        print("Plafond          :", result["recommended_plafond"])

    print("Rekomendasi      :", result["recommendation"])


# ==================================================
# TEST 1 - NASABAH SANGAT AMAN
# ==================================================

result = predict_risk_hybrid(
    {
        "revolving_utilization": 0.10,
        "age": 45,
        "delinquency_30_59": 0,
        "debt_ratio": 0.15,
        "monthly_income": 25000000,
        "num_credit_lines": 12,
        "delinquency_90": 0,
        "real_estate_loans": 2,
        "delinquency_60_89": 0,
        "dependents": 1,
    }
)

tampilkan_hasil("TEST 1 - NASABAH SANGAT AMAN", result)


# ==================================================
# TEST 2 - NASABAH NORMAL
# ==================================================

result = predict_risk_hybrid(
    {
        "revolving_utilization": 0.45,
        "age": 35,
        "delinquency_30_59": 1,
        "debt_ratio": 0.40,
        "monthly_income": 8000000,
        "num_credit_lines": 6,
        "delinquency_90": 0,
        "real_estate_loans": 1,
        "delinquency_60_89": 0,
        "dependents": 2,
    }
)

tampilkan_hasil("TEST 2 - NASABAH NORMAL", result)


# ==================================================
# TEST 3 - NASABAH RISIKO TINGGI
# ==================================================

result = predict_risk_hybrid(
    {
        "revolving_utilization": 0.80,
        "age": 28,
        "delinquency_30_59": 2,
        "debt_ratio": 0.90,
        "monthly_income": 3500000,
        "num_credit_lines": 4,
        "delinquency_90": 1,
        "real_estate_loans": 0,
        "delinquency_60_89": 1,
        "dependents": 4,
    }
)

tampilkan_hasil("TEST 3 - NASABAH RISIKO TINGGI", result)


# ==================================================
# TEST 4 - NASABAH SANGAT BURUK
# ==================================================

result = predict_risk_hybrid(
    {
        "revolving_utilization": 1.00,
        "age": 22,
        "delinquency_30_59": 5,
        "debt_ratio": 1.50,
        "monthly_income": 300000,
        "num_credit_lines": 2,
        "delinquency_90": 4,
        "real_estate_loans": 0,
        "delinquency_60_89": 3,
        "dependents": 5,
    }
)

tampilkan_hasil("TEST 4 - NASABAH SANGAT BURUK", result)
