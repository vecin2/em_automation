def test_some():
    assert "tit for tat" == "%s for %s" % ("tit", "tat")
    assert "chicken and waffles" == "{} and {}".format("chicken", "waffles")
    assert "Bond, James Bond" == "%(last)s, %(first)s %(last)s" % {
        "first": "James",
        "last": "Bond",
    }
    assert "Bond, James" == "{last}, {first}".format(first="James", last="Bond")
