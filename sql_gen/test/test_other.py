from sql_gen.sqltask_jinja.filters.other import split_uppercase

def t(expected, string):
    assert expected  == split_uppercase(string)

def test_split_uppercase():
    t("Inline Search","inlineSearch")
    t("Inline Search","InlineSearch")
    t("Inlinesearch","Inlinesearch")
    t("Inlinesearch","inlinesearch")
