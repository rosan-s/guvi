def bank_a_summary() -> dict:
    return {
        "provider": "MockBank A",
        "accounts": 2,
        "average_balance": 125000.0,
        "monthly_inflows": 420000.0,
        "monthly_outflows": 395000.0,
        "note": "Replace with real banking API integration",
    }


def bank_b_summary() -> dict:
    return {
        "provider": "MockBank B",
        "upi_collections": 180000.0,
        "card_sales": 95000.0,
        "chargebacks": 1200.0,
        "note": "Replace with real payment API integration",
    }
