import pytest
import unittest
from src.extract import read_csv, csv_import
from unittest.mock import patch, Mock
from src.transform import get_raw_transactions, get_uuid, _basket

#mock_dir = ['assert_any_call', 'assert_called', 'assert_called_once', 'assert_called_once_with', 'assert_called_with', 
#'assert_has_calls', 'assert_not_called', 'attach_mock', 'call_args', 'call_args_list', 'call_count', 'called', 'configure_mock', 
# 'method_calls', 'mock_add_spec', 'mock_calls', 'reset_mock', 'return_value', 'side_effect']

first_3_rows_csv = [{'Timestamp': '2020-10-01 09:00:00', 'Location': 'Isle of Wight', 'Name': 'John Whitmire', 'Orders': ',Mocha,2.3,,Speciality Tea - Fruit,1.3,,Flavoured iced latte - Vanilla,2.75,,Frappes - Chocolate Cookie,2.75,Large,Filter coffee,1.8', 'Payment Type': 'CARD', 'Cost': '10.90', 'Card Details': 'americanexpress,379663269694145'}, 
        {'Timestamp': '2020-10-01 09:01:00', 'Location': 'Isle of Wight', 'Name': 'Sarah Perea', 'Orders': 'Large,Americano,2.25,Regular,Americano,1.95,,Flavoured iced latte - Caramel,2.75', 'Payment Type': 'CASH', 'Cost': '6.95', 'Card Details': 'None'}, 
        {'Timestamp': '2020-10-01 09:02:00', 'Location': 'Isle of Wight', 'Name': 'Patrick Young', 'Orders': ',Smoothies - Carrot Kick,2.0,Large,Flavoured latte - Gingerbread,2.85,,Speciality Tea - Darjeeling,1.3', 'Payment Type': 'CARD', 'Cost': '6.15', 'Card Details': 'visa13,4823964727912'}]
fake_uuid = "0123456789"
fake_basket = [{'name': 'Mocha', 'flavour': '', 'size': '', 'price': 2.3, 'iced': False}, {'name': 'Tea', 'flavour': 'Fruit', 'size': '', 'price': 1.3, 'iced': False}, {'name': 'Latte', 'flavour': 'Vanilla', 'size': '', 'price': 2.75, 'iced': True}, {'name': 'Frappes', 'flavour': 'Chocolate Cookie', 'size': '', 'price': 2.75, 'iced': 
False}, {'name': 'Filter Coffee', 'flavour': '', 'size': 'Large', 'price': 1.8, 'iced': False}]
order_first_row_csv = first_3_rows_csv[0]["Orders"].split(",")



class Test_Get_Raw_Transactions(unittest.TestCase):
    # We use unittest mock patch for everything we will make into a stub or spy
    # Note that these patches are in reverse order in the arguments of the test
    @patch("src.transform._basket", return_value = fake_basket)
    @patch("src.transform.get_uuid", return_value = fake_uuid)
    def test_get_transactions(self, mock_get_uuid, mock_basket):
        #when get_uuid is called, it's made into a mock object with the @patch and its return value is the fake_uuid and when _basket is called, its made into a mock object
        #with the @patch and its return value is the fake basket
        mocked_transactions = get_raw_transactions(first_3_rows_csv)
        #print(mocked_transactions) - output = 3 rows of the result of get_raw_transactions() with the id and bakset for each transaction being the same - the fake uuid "0123456789" and the fake basket
        assert mock_get_uuid.call_count == 3
        assert mock_basket.call_count == 3
    
    def test__basket(self):
        #arrange - gets a basket of just the first line of the csv
        mocked_basket = _basket(order_first_row_csv)
        #act - comparing it to the basket which we pulled from the transactions list i.e. the end result of the _basket function
        expected_basket = fake_basket
        #assert - are the two the same? Does the function work as we want it to? Yes!
        assert mocked_basket == fake_basket


    
    
    

        
       
        

        

        
        
