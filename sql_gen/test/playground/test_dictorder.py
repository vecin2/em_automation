my_dict = {}


def my_dict_list():
    return [k for k in my_dict]


def test_order_items():
    my_dict["one"] = 1
    my_dict["two"] = 2
    my_dict["a"] = "a"
    assert "one" == my_dict_list()[0]
    assert "two" == my_dict_list()[1]
    assert "a" == my_dict_list()[2]
    my_dict.pop(list(my_dict.keys())[-1])
    assert "one" == my_dict_list()[0]
    assert "two" == my_dict_list()[1]
    my_dict["b"] = "b"
    assert "b" == my_dict_list()[2]
    my_dict.pop(list(my_dict.keys())[-1])
    assert "one" == my_dict_list()[0]
    assert "two" == my_dict_list()[1]
