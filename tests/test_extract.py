from src.extract import read_csv

single_line_raw_csv = [
    '2020-10-01 16:59:00,Isle of Wight,Carol Field,"Regular,Chai latte,2.3,Large,Americano,2.25",CARD,4.55,"americanexpress,352673943791481"'
]


def test_read_csv():
    actual = read_csv(single_line_raw_csv)
    expected = {
        "Timestamp": "2020-10-01 16:59:00",
        "Location": "Isle of Wight",
        "Name": "Carol Field",
        "Orders": "Regular,Chai latte,2.3,Large,Americano,2.25",
        "Payment Type": "CARD",
        "Cost": "4.55",
        "Card Details": "americanexpress,352673943791481",
    }
    assert actual == expected
