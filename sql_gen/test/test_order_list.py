import pytest

def test_order_list_by_list_b():
    list_a = [100, 1, 10]
    list_b = [1, 10, 100]
    #sorted_list_b_by_list_a
    result = sorted(list_b, key=lambda x: list_a.index(x))
    assert [100,1,10] == result 

def test_order_list_by_list_b_with_different_elements():
    list_a = [100, 1, 10, 500, 400]
    list_b = [1, 10, 100]
    #sorted_list_b_by_list_a
    result = sorted(list_b, key=lambda x: list_a.index(x))
    assert [100,1,10] == result 

def test_order_list_of_words_by_the_order_they_appear_in_a_text():
    list_a = "Hi Juan this is Antonio".split()
    list_b = ["Antonio", "Juan"]
    #sorted_list_b_by_list_a
    result = sorted(list_b, key=lambda x: list_a.index(x))
    assert ["Juan", "Antonio"] == result 
