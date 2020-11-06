from unittest.mock import patch
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from src.load import _deduplicate_products, get_unique_products, get_locations
from src.models import Product, Location

sample_products_with_duplicates = [
    {"name": "Mocha", "flavour": "", "size": "", "price": 2.3, "iced": False},
    {"name": "Tea", "flavour": "Fruit", "size": "", "price": 1.3, "iced": False},
    {
        "name": "Latte",
        "flavour": "Vanilla",
        "size": "",
        "price": 2.75,
        "iced": True,
    },
    {
        "name": "Frappes",
        "flavour": "Chocolate Cookie",
        "size": "",
        "price": 2.75,
        "iced": False,
    },
    {"name": "Mocha", "flavour": "", "size": "", "price": 2.3, "iced": False},
    {
        "name": "Filter Coffee",
        "flavour": "",
        "size": "Large",
        "price": 1.8,
        "iced": False,
    },
    {
        "name": "Frappes",
        "flavour": "Chocolate Cookie",
        "size": "",
        "price": 2.75,
        "iced": False,
    },
]

expected_deduplicated_products = [
    {"name": "Mocha", "flavour": "", "size": "", "price": 2.3, "iced": False},
    {"name": "Tea", "flavour": "Fruit", "size": "", "price": 1.3, "iced": False},
    {
        "name": "Latte",
        "flavour": "Vanilla",
        "size": "",
        "price": 2.75,
        "iced": True,
    },
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


def test_deduplicate_products():
    actual = _deduplicate_products(sample_products_with_duplicates)
    # Lengths should be the same
    assert len(actual) == len(expected_deduplicated_products)
    # And should contain the same items
    for x in actual:
        assert x in expected_deduplicated_products


sample_raw_transaction = [
    {
        "id": "208e6031-3e31-4c4c-97b9-11413439d044",
        "basket": [
            {"name": "Mocha", "flavour": "", "size": "", "price": 2.3, "iced": False},
            {
                "name": "Tea",
                "flavour": "Fruit",
                "size": "",
                "price": 1.3,
                "iced": False,
            },
            {
                "name": "Latte",
                "flavour": "Vanilla",
                "size": "",
                "price": 2.75,
                "iced": True,
            },
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
        ],
        "datetime": 1601539200,
        "location": "Isle of Wight",
        "payment_type": "CARD",
        "transaction_total": "10.90",
        "card_details": "americanexpress",
    }
]

sample_uuid = "5070d6d7-41d8-44d9-89e1-063b4cbb0899"


@patch("src.load.get_uuid", return_value=sample_uuid)
@patch("src.load._deduplicate_products", return_value=expected_deduplicated_products)
def get_unique_products(mock_get_uuid, mock_deduplicate_products):
    actual = get_unique_products(sample_raw_transaction)

    assert mock_get_uuid.call_count == len(expected_deduplicated_products)
    assert mock_deduplicate_products.called_once()

    expected = [
        Product(
            id=sample_uuid, name="Mocha", flavour="", size="", price=2.3, iced=False
        ),
        Product(
            id=sample_uuid, name="Tea", flavour="Fruit", size="", price=1.3, iced=False
        ),
        Product(
            id=sample_uuid,
            name="Latte",
            flavour="Vanilla",
            size="",
            price=2.75,
            iced=True,
        ),
        Product(
            id=sample_uuid,
            name="Frappes",
            flavour="Chocolate Cookie",
            size="",
            price=2.75,
            iced=False,
        ),
        Product(
            id=sample_uuid,
            name="Filter Coffee",
            flavour="",
            size="Large",
            price=1.8,
            iced=False,
        ),
    ]
    assert actual == expected


@patch("src.load.get_uuid", return_value=sample_uuid)
def test_get_locations(mock_get_uuid):
    actual = get_locations(sample_raw_transaction)

    assert mock_get_uuid.called_once()
    assert actual == [Location(id=sample_uuid, name="Isle of Wight")]


def test_get_existing_product_id():
    pass


def get_basket_items():
    pass


def test_get_existing_location_id():
    pass


def test_ignore_duplicate():
    pass


def test_session_context_manager():
    pass


def test_init():
    pass


def test_insert_many():
    pass
