# tests/test_metaphor.py

import pytest
from main import hospital_search, drug_search, latest_info

# Test hospital_search function
def test_hospital_search():
    result = hospital_search("heart attack", "San Jose", "California", "95008")
    assert isinstance(result, list)  # Check if it returns a list of hyperlinks
    # Add more specific assertions based on the expected behavior

# Test drug_search function
def test_drug_search():
    result = drug_search("Tylenol", "San Francisco", "California", "94107")
    assert isinstance(result, list)  # Check if it returns a list of hyperlinks
    # Add more specific assertions based on the expected behavior

# Test latest_info function
def test_latest_info():
    result, summary = latest_info("Neuro Science")
    assert isinstance(result, list)  # Check if it returns a list of hyperlinks
    assert isinstance(summary, str)  # Check if it returns a summary as a string
    # Add more specific assertions based on the expected behavior

if __name__ == "__main__":
    pytest.main()
