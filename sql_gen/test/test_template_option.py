from sql_gen.sql_gen.environment_selection import TemplateOption

def test_is_removes_main_folder_from_name():
    option = TemplateOption(1,"menu/template_1.sql")
    assert "template_1.sql" == option.name

def test_it_remove_windows_link_from_name():
    #when creating windos links it adds '.lnk'. 
    option = TemplateOption(1,"menu/template_1.sql.lnk")
    assert "template_1.sql" == option.name
