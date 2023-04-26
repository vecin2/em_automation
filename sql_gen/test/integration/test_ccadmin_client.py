from sql_gen.emproject.ccadmin import CCAdmin
from sql_gen.exceptions import CCAdminException
import pytest

# test mark as skip becasue take too long to run as part o unit
@pytest.mark.skip
def test_run_ccadmin_succesful_returns_0():
    ccadmin = CCAdmin()
    result = ccadmin.show_config("-Dformat=txt")
    assert 0 == result


@pytest.mark.skip
def test_run_ccadmin_fail_throws_exception():
    with pytest.raises(CCAdminException) as e_info:
        ccadmin = CCAdmin()
        result = ccadmin.show_config("invalid_param")
    assert "Failed when running 'ccadmin" in str(e_info.value)
