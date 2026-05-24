def get_trade_quality(confidence):

    if confidence >= 90:

        return "VERY HIGH"

    elif confidence >= 80:

        return "HIGH"

    elif confidence >= 70:

        return "MEDIUM"

    else:

        return "LOW"