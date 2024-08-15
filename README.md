# Bank Loan Defaulter Prediction #

## Overview ##

This is your new Kedro project with Kedro-Viz setup, which was generated using `kedro 0.19.7`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines ##

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies ##

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```shell
pip install -r requirements.txt
```

## How to run your Kedro pipeline ##

You can run your Kedro project with:

```shell
kedro run
```

## How to test your Kedro project ##

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```bash
pytest
```

To configure the coverage threshold, look at the `.coveragerc` file.

## Project dependencies ##

To see and update the dependency requirements for your project use `requirements.txt`. Install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## Package your Kedro project ##

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html).

## Data Dictionary ##

| No | Column Name | Description |
| --- | --- | --- |
| 1 | ID | Unique ID of representative. |
| 2 | Loan Amount | Loan amount applied. |
| 3 | Funded Amount | Loan amount funded. |
| 4 | Funded Amount Investor | Loan amount approved by the investors. |
| 5 | Term | Term of loan (in months). |
| 6 | Batch Enrolled | Batch number to representatives. |
| 7 | Interest Rate | Interest rate (%) on loan. |
| 8 | Grade | Grade by the bank. |
| 9 | Sub Grade | Sub-grade by the bank. |
| 10 | Employment Duration | Duration. |
| 11 | Home Ownership | Ownership of the home. |
| 12 | Verification Status | Income verification by the bank. |
| 13 | Payment Plan | If any payment plan has started against the loan. |
| 14 | Loan Title | Loan title provided. |
| 15 | Debit to Income | Ratio of preresentative's total monthly debt repayment divided by self-reported monthly income. |
| 16 | Delinquency - Two years | Number of 30+ days delinquency in past 2 years. |
| 17 | Inquires - Six months | Total number of inquiries in last 6 months. |
| 18 | Open Account | Number of open credit line in representative's credit line. |
| 19 | Public Record | Number of derogatory public records. |
| 20 | Revolving Balance | Total credit revolving balance. |
| 21 | Revolving Utilities | Amount of credit a representative is using relative to revolving balance. |
| 22 | Total Accounts | Total number of credit lines available in representative's credit line. |
| 23 | Initial List Status | Unique listing of the loan - W (Waiting), F (Forwarded). |
| 24 | Total Received Interest | Total interest received till date. |
| 25 | Total Received Late Fee | Total late fee received till date. |
| 26 | Recoveries | Post charge off gross recovery. |
| 27 | Collection Recovery Fee | Post charge off collection fee. |
| 28 | Collection 12 months Medical | Total collection in last 12 months excluding medical collections. |
| 29 | Application Type | Indicates whether the represenatative is an individual or joint. |
| 30 | Last Week Pay | Indicates how long (in weeks) a representtative has paid EMI after batch enrolled. |
| 31 | Accounts Delinquent | Number of accounts on which the representative is delinquent. |
| 32 | Total Collection Amount | Total current balance from all accounts. |
| 33 | Total Current Balance | Total current balance from all accounts. |
| 34 | Total Revolving Credit Limit | Total revolving credit limit. |
| 35 | Loan Status | 1 = Defaulter, 0 = Non-Defaulter. |
