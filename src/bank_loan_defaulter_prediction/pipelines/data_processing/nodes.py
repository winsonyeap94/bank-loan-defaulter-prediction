import re

import pandas as pd


# ============================== Auxiliary Functions ==============================
def _standardise_column_names(data_df: pd.DataFrame) -> pd.DataFrame:
    data_df.columns = [re.sub(r'[\s-]+', '_', x).upper() for x in data_df.columns]
    
    # There is a correction whereby the 'EMPLOYMENT_DURATION' column is wrongly labelled. The data contained within is 
    # actually the 'HOME_OWNERSHIP' column.
    data_df['__HOME_OWNERSHIP__'] = data_df['HOME_OWNERSHIP']  # NOTE: Still unsure what this column represents
    data_df['HOME_OWNERSHIP'] = data_df['EMPLOYMENT_DURATION']
    data_df = data_df.drop(columns=['EMPLOYMENT_DURATION'])
    
    return data_df


def _preprocess_categorical_variables(data_df: pd.DataFrame, reference_df: pd.DataFrame=None) -> pd.DataFrame:
    # Text cleanup
    data_df['LOAN_TITLE'] = data_df['LOAN_TITLE'].str.upper().str.strip()  # Standardise all titles to uppercase
    data_df['LOAN_TITLE'] = data_df['LOAN_TITLE'].replace({
        'BATHROOM': 'HOME IMPROVEMENT LOAN',
        'POOL': 'HOME IMPROVEMENT LOAN',
        'BILL PAYOFF': 'BILLS',
        'CAR LOAN': 'CAR FINANCING',
        'CARDS': 'CREDIT CARD', 
        'CARD CONSOLIDATION': 'CREDIT CARD CONSOLIDATION',
        'CC': 'CREDIT CARD',
        'CC CONSOLIDATION': 'CREDIT CARD CONSOLIDATION',
        'CC LOAN': 'CREDIT CARD',
        'CC REFI': 'CREDIT CARD REFINANCE',
        'CC REFINANCE': 'CREDIT CARD REFINANCE',
        'CC-REFINANCE': 'CREDIT CARD REFINANCE',
        'CONSO': 'CONSOLIDATION',
        'CONSOLIDATE': 'CONSOLIDATION',
        'CONSOLIDATED': 'CONSOLIDATION',
        'CONSOLIDATION LOAN': 'CONSOLIDATION',
        'CREDIT': 'CREDIT LOAN',
        'CREDIT CARD PAY OFF': 'CREDIT CARD PAYOFF',
        'CREDIT CARD REFI': 'CREDIT CARD REFINANCE',
        'CREDIT CARD REFINANCE LOAN': 'CREDIT CARD REFINANCE',
        'CREDIT CARD REFINANCING': 'CREDIT CARD REFINANCE',
        'CREDIT CARDS': 'CREDIT CARD',
        'CREDIT PAY OFF': 'CREDIT PAYOFF',
        'DEBT': 'DEBT LOAN',
        'DEBT CONSOLIDATION 2013': 'DEBT CONSOLIDATION',
        'DEBT CONSOLIDATION LOAN': 'DEBT CONSOLIDATION',
        'DEPT CONSOLIDATION': 'DEBT CONSOLIDATION',
        'GET DEBT FREE': 'GET OUT OF DEBT',
        'HOME': 'HOME LOAN',
        'HOME BUYING': 'HOME LOAN',
        'HOME IMPROVEMENT': 'HOME IMPROVEMENT LOAN',
        'HOUSE': 'HOME LOAN',
        'LOAN 1': 'LOAN',
        'LOAN1': 'LOAN',
        'LENDING CLUB': 'LOAN',
        'LENDING LOAN': 'LOAN',
        'MEDICAL EXPENSES': 'MEDICAL',
        'MEDICAL LOAN': 'MEDICAL',
        'MY LOAN': 'LOAN',
        'MYLOAN': 'LOAN',
        'PAY OFF': 'PAYOFF',
        'PAY OFF BILLS': 'PAYOFF',
        'PERSONAL': 'LOAN',
        'PERSONAL LOAN': 'LOAN',
        'REFI': 'REFINANCE',
        'REFINANCE LOAN': 'REFINANCE',
    })
    
    # Managing strings so that they are in Categorical format
    if reference_df is None:
        reference_df = data_df.copy()
    data_df['ID'] = data_df['ID'].astype(str)
    data_df['BATCH_ENROLLED'] = data_df['BATCH_ENROLLED'].astype(str)
    data_df['GRADE'] = pd.Categorical(data_df['GRADE'], categories=sorted(set(reference_df['GRADE'])), ordered=True)
    data_df['SUB_GRADE'] = pd.Categorical(data_df['SUB_GRADE'], categories=sorted(set(reference_df['SUB_GRADE'])), ordered=True)
    data_df['LOAN_TITLE'] = pd.Categorical(data_df['LOAN_TITLE'], categories=sorted(set(reference_df['LOAN_TITLE'])), ordered=False)
    data_df['INITIAL_LIST_STATUS'] = pd.Categorical(data_df['INITIAL_LIST_STATUS'].replace({'f': 'FORWARDED', 'w': 'WAITING'}), categories=['FORWARDED', 'WAITING'], ordered=False)
    data_df['APPLICATION_TYPE'] = pd.Categorical(data_df['APPLICATION_TYPE'], categories=sorted(set(reference_df['APPLICATION_TYPE'])), ordered=False)
    return data_df


def _preprocess_numerical_variables(data_df: pd.DataFrame, reference_df: pd.DataFrame=None) -> pd.DataFrame:
    numerical_vars = [
        'LOAN_AMOUNT', 'FUNDED_AMOUNT', 'FUNDED_AMOUNT_INVESTOR', 'TERM', 'INTEREST_RATE', 'DEBIT_TO_INCOME',
        'DELINQUENCY_TWO_YEARS', 'INQUIRES_SIX_MONTHS', 'OPEN_ACCOUNT', 'PUBLIC_RECORD', 'REVOLVING_BALANCE',
        'REVOLVING_UTILITIES', 'TOTAL_ACCOUNTS', 'TOTAL_RECEIVED_INTEREST', 'TOTAL_RECEIVED_LATE_FEE', 'RECOVERIES',
        'COLLECTION_RECOVERY_FEE', 'COLLECTION_12_MONTHS_MEDICAL', 'LAST_WEEK_PAY', 'TOTAL_COLLECTION_AMOUNT',
        'TOTAL_CURRENT_BALANCE', 'TOTAL_REVOLVING_CREDIT_LIMIT', 
    ]
    for var in numerical_vars:
        data_df[var] = pd.to_numeric(data_df[var], errors='coerce')
    return data_df


# ============================== Main Functions ==============================
def preprocess_dataset(data_df: pd.DataFrame, reference_df: pd.DataFrame=None) -> pd.DataFrame:
    """
    Preprocess the dataset by standardising column names, preprocessing categorical variables, and preprocessing numerical variables.
    """
    data_df = _standardise_column_names(data_df)
    data_df = _preprocess_categorical_variables(data_df, reference_df)
    data_df = _preprocess_numerical_variables(data_df, reference_df)
    return data_df


def feature_engineering(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature engineering for the dataset.
    """
    # ============================== Numerical ==============================
    # Ratio of funded amounts to the total loan amount
    data_df['FUNDED_AMOUNT_TO_PRINCIPAL'] = data_df['FUNDED_AMOUNT'] / data_df['LOAN_AMOUNT']
    data_df['FUNDED_AMOUNT_INVESTOR_TO_PRINCIPAL'] = data_df['FUNDED_AMOUNT_INVESTOR'] / data_df['LOAN_AMOUNT']
    
    # Ratio of interests collected to the total loan amount
    data_df['RECEIVED_INTEREST_TO_PRINCIPAL'] = data_df['TOTAL_RECEIVED_INTEREST'] / data_df['LOAN_AMOUNT']

    # Ratio of late fees collected to the total loan amount
    data_df['RECEIVED_LATE_FEE_TO_PRINCIPAL'] = data_df['TOTAL_RECEIVED_LATE_FEE'] / data_df['LOAN_AMOUNT']

    # ============================== Categorical ==============================
    # Whether a loan is part of consolidation
    data_df['IS_CONSOLIDATION'] = data_df['LOAN_TITLE'].str.contains('CONSOLIDATION', case=False).astype(int)

    return data_df

