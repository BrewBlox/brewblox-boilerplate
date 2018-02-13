"""
Tests whether boilerplate package name was removed correctly.
Serves as a quick example for pytest tests
"""


def test_boilerplate(app):
    # Check whether boilerplate was updated correctly
    # Feel free to remove this test after having done so
    assert app.name != 'YOUR_PACKAGE', 'Please change the package name from the default "YOUR_PACKAGE"'
