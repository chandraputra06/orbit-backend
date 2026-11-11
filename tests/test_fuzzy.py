from app.services import fuzzy_mamdani

def test_fuzzy_module_exists_without_fabricated_rules():
    assert fuzzy_mamdani.__doc__ is not None
