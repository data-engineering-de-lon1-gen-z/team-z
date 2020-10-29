import unittest
from src.extract import read_csv
from unittest.mock import patch, Mock
from src.transform import get_raw_transactions, get_uuid, _basket

fake_uuid = "208e6031-3e31-4c4c-97b9-11413439d044"
sample_data = [
    {
        "Timestamp": "2020-10-01 09:00:00",
        "Location": "Isle of Wight",
        "Name": "John Whitmire",
        "Orders": ",Mocha,2.3,,Speciality Tea - Fruit,1.3,,Flavoured iced latte - Vanilla,2.75,,Frappes - Chocolate Cookie,2.75,Large,Filter coffee,1.8",
        "Payment Type": "CARD",
        "Cost": "10.90",
        "Card Details": "americanexpress,379663269694145",
    },
    {
        "Timestamp": "2020-10-01 09:01:00",
        "Location": "Isle of Wight",
        "Name": "Sarah Perea",
        "Orders": "Large,Americano,2.25,Regular,Americano,1.95,,Flavoured iced latte - Caramel,2.75",
        "Payment Type": "CASH",
        "Cost": "6.95",
        "Card Details": "None",
    },
    {
        "Timestamp": "2020-10-01 09:02:00",
        "Location": "Isle of Wight",
        "Name": "Patrick Young",
        "Orders": ",Smoothies - Carrot Kick,2.0,Large,Flavoured latte - Gingerbread,2.85,,Speciality Tea - Darjeeling,1.3",
        "Payment Type": "CARD",
        "Cost": "6.15",
        "Card Details": "visa13,4823964727912",
    },
]
expected_first_row_basket = [
    {"name": "Mocha", "flavour": "", "size": "", "price": 2.3, "iced": False},
    {"name": "Tea", "flavour": "Fruit", "size": "", "price": 1.3, "iced": False},
    {"name": "Latte", "flavour": "Vanilla", "size": "", "price": 2.75, "iced": True},
    {
        "name": "Frappes",
        "flavour": "Chocolate Cookie",
        "size": "",
        "price": 2.75,
        "iced": False,
    },
    {
        "name": "Filter Coffee",
        "flavour": "",
        "size": "Large",
        "price": 1.8,
        "iced": False,
    },
]
# TODO What should the first transaction look like when transformed?
expected_first_row_transaction = {}


def test_get_transactions(self):
    # get_uuid will always return fake_uuid
    with patch("src.transform.get_uuid", return_value=fake_uuid) as mock_get_uuid:
        mocked_transactions = get_raw_transactions(sample_data)
        assert mock_get_uuid.call_count == 3
        # Ensure we get back exactly 3 transactions
        assert len(mocked_transactions) == 3
        # Check the first item basket
        assert mocked_transactions[0]["basket"] == expected_first_row_basket
        # TODO
        assert mocked_transactions[0] == expected_first_row_transaction


def test__basket():
    # arrange - gets a basket of just the first line of the csv
    order_first_row_csv = sample_data[0]["Orders"].split(",")
    # act
    actual_first_row_basket = _basket(order_first_row_csv)
    # assert - are the two the same? Does the function work as we want it to? Yes!
    assert actual_first_row_basket == expected_first_row_basket
