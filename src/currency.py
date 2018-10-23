import requests


class Money(object):
    ACCESS_KEY = "70aa40ebd553fc204640b4561204d6c8"
    RATES = {}

    @classmethod
    def exchange_rate(cls, currency="USD", source="USD"):
        if source == currency:
            rate = 1
        elif source == "USD" and \
                cls.RATES.get(source, {}).get(source + currency):
            rate = cls.RATES.get(source, {}).get(source + currency)
        elif cls.RATES.get("USD", {}).get("USD" + currency) and \
                cls.RATES.get("USD", {}).get("USD" + source):
            rate_c_u = cls.RATES.get("USD", {}).get("USD" + currency)
            rate_s_u = cls.RATES.get("USD", {}).get("USD" + source)
            rate = rate_s_u / rate_c_u
        else:
            params = {
                "access_key": cls.ACCESS_KEY,
                # "currencies": currency,
                "source": "USD",
            }
            json = requests.get("http://apilayer.net/api/live",
                                params=params).json()
            assert json.get("success", False), (params, json)
            response_rate = json.get("quotes", {})
            cls.RATES["USD"] = response_rate
            if source == "USD" and \
                    cls.RATES.get(source, {}).get(source + currency):
                rate = cls.RATES.get(source, {}).get(source + currency)
            elif cls.RATES.get("USD", {}).get("USD" + currency) and \
                    cls.RATES.get("USD", {}).get("USD" + source):
                rate_c_u = cls.RATES.get("USD", {}).get("USD" + currency)
                rate_s_u = cls.RATES.get("USD", {}).get("USD" + source)
                rate = rate_s_u / rate_c_u
        assert rate
        return rate

    @classmethod
    def purge_rates(cls):
        cls.RATES = {}

    def __str__(self):
        return "{0:.2f} {1}".format(self.value, self.currency)

    def __init__(self, value, currency="USD"):
        self.value = value
        self.currency = currency

    def __add__(self, other):
        if isinstance(other, type(self)):
            rate = type(self).exchange_rate(other.currency, self.currency)
            value = self.value + other.value / rate
            return type(self)(value, self.currency)
        elif other == 0:
            return self
        else:
            raise Exception("Operation not supported")

    __radd__ = __add__

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        value = self.value * other
        return type(self)(value, self.currency)

    __rmul__ = __mul__

    def __neg__(self):
        return type(self)(self.value * -1, self.currency)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __truediv__(self, other):
        return self * (1 / other)


if __name__ == '__main__':
    x = Money(10, "BYN")
    y = Money(11)  # define your own default value, e.g. “USD”
    z = Money(12.34, "EUR")
    print(z + 3.11 * x + y * 0.8)  # result in “EUR”
    # >>543.21 EUR

    lst = [Money(10, "BYN"), Money(11), Money(12.01, "JPY")]

    s = sum(lst)

    print(s)  # result in “BYN”
    # >>123.45 BYN
