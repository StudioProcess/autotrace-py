try:
    from autotrace import autotrace
    print("Successfully loaded autotrace")
except Exception as e:
    print("Error loading autotrace:")
    print(e)