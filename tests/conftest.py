# hoist fixtures into the pytest suite
# so that they are available to all tests

pytest_plugins = [
    "tests.fixtures",
]
