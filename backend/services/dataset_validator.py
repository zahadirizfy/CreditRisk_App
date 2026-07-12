import pandas as pd


# =====================================================
# DATASET YANG DIGUNAKAN MODEL
# =====================================================

REQUIRED_COLUMNS = [
    "No",
    "SeriousDlqin2yrs",
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfDependents",
]

NUMERIC_COLUMNS = [
    "SeriousDlqin2yrs",
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfDependents",
]


# =====================================================
# VALIDATE DATASET
# =====================================================


def validate_dataset(file_path):
    """
    Melakukan validasi dataset sebelum proses retraining.

    Validasi meliputi:
    1. File dapat dibaca.
    2. Dataset tidak kosong.
    3. Nama kolom harus sesuai.
    4. Urutan kolom harus sesuai.
    5. Seluruh kolom numerik bertipe numerik.
    """

    # =====================================================
    # LOAD CSV
    # =====================================================

    try:
        df = pd.read_csv(file_path, sep=None, engine="python")

    except Exception as e:
        return False, f"Gagal membaca file CSV. {str(e)}"

    # =====================================================
    # DATASET KOSONG
    # =====================================================

    if df.empty:
        return False, "Dataset kosong."

    # =====================================================
    # VALIDASI JUMLAH KOLOM
    # =====================================================

    uploaded_columns = list(df.columns)

    if len(uploaded_columns) != len(REQUIRED_COLUMNS):
        return (
            False,
            f"Jumlah kolom tidak sesuai. Seharusnya {len(REQUIRED_COLUMNS)} kolom.",
        )

    # =====================================================
    # VALIDASI NAMA KOLOM
    # =====================================================

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in uploaded_columns]

    if missing_columns:
        return (False, "Kolom berikut tidak ditemukan: " + ", ".join(missing_columns))

    extra_columns = [col for col in uploaded_columns if col not in REQUIRED_COLUMNS]

    if extra_columns:
        return (False, "Kolom tidak dikenali: " + ", ".join(extra_columns))

    # =====================================================
    # VALIDASI URUTAN KOLOM
    # =====================================================

    if uploaded_columns != REQUIRED_COLUMNS:
        return (False, "Urutan kolom dataset tidak sesuai dengan format sistem.")

    # =====================================================
    # VALIDASI TARGET
    # =====================================================

    unique_target = sorted(df["SeriousDlqin2yrs"].unique())

    if not set(unique_target).issubset({0, 1}):
        return (False, "Kolom target hanya boleh berisi nilai 0 dan 1.")

    # =====================================================
    # VALIDASI JUMLAH DATA
    # =====================================================

    if len(df) < 100:
        return (False, "Jumlah data minimal 100 baris untuk proses retraining.")

    # =====================================================
    # SUCCESS
    # =====================================================

    return True, {
        "message": "Dataset valid.",
        "rows": len(df),
        "columns": len(df.columns),
    }
