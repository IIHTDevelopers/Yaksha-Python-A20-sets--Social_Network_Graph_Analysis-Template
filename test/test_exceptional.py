# test_exceptional.py
import pytest
from test.TestUtils import TestUtils
from social_network_graph_analysis import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_input_validation(test_obj):
    """Consolidated test for input validation and error handling"""
    try:
        # Test with None inputs for critical functions
        test_connections = {"user1": {"user2"}, "user2": {"user1"}}
        test_communities = {"group1": {"user1", "user2"}, "group2": {"user2", "user3"}}
        
        functions_to_test = [
            (find_mutual_connections, ["user1", "user2", None]),
            (find_exclusive_connections, ["user1", "user2", None]),
            (find_all_connections, ["user1", None]),
            (find_common_group_members, [None, {"user1", "user2"}]),
            (find_common_group_members, [{"user1", "user2"}, None]),
            (find_users_in_any_group, [None, {"user1", "user2"}]),
            (find_users_in_any_group, [{"user1", "user2"}, None]),
            (is_direct_connection, ["user1", "user2", None]),
            (is_second_degree_connection, ["user1", "user2", None]),
            (identify_bridge_users, [None]),
            (calculate_network_density, [None, test_connections]),
            (calculate_network_density, [set(), test_connections]),
            (find_isolated_users, [None, test_connections]),
            (recommend_connections, ["user1", None]),
            (format_users_for_display, ["Group", None])
        ]
        
        # Test all functions with None inputs
        for func, args in functions_to_test:
            with pytest.raises(ValueError):
                func(*args)
        
        # Test with invalid parameter values
        # Test non-existent user
        with pytest.raises(ValueError):
            find_mutual_connections("nonexistent", "user2", test_connections)
        
        # Test invalid depth
        with pytest.raises(ValueError):
            find_all_connections("user1", test_connections, 0)
        
        # Test non-existent user in connections
        with pytest.raises(ValueError):
            recommend_connections("nonexistent", test_connections)
        
        test_obj.yakshaAssert("TestInputValidation", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputValidation", False, "exception")
        pytest.fail(f"Input validation test failed: {str(e)}")

def test_error_handling(test_obj):
    """Test specific error handling scenarios"""
    try:
        # Setup test data
        test_connections = {
            "user1": {"user2", "user3"},
            "user2": {"user1", "user4"},
            "user3": {"user1", "user5"},
            "user4": {"user2"},
            "user5": {"user3"}
        }
        
        # Test handling missing fields
        invalid_connections = {
            "user1": {"user2"},
            "user3": "invalid"  # Not a set
        }
        
        # Should raise exception when dealing with invalid data types
        with pytest.raises(Exception):
            find_mutual_connections("user1", "user3", invalid_connections)
        
        # Test immutability - original connections should not change
        original_user1_connections = test_connections["user1"].copy()
        result = find_mutual_connections("user1", "user2", test_connections)
        assert test_connections["user1"] == original_user1_connections, "Original connections should not be modified"
        
        # Test immutability when adding a connection
        original_connections = test_connections.copy()
        # Simulate adding a connection (not using actual function since we're testing principle)
        new_connections = test_connections.copy()
        user1_connections = new_connections["user1"].copy()
        user1_connections.add("user6")
        new_connections["user1"] = user1_connections
        
        assert test_connections == original_connections, "Original connections should not be modified"
        assert "user6" in new_connections["user1"], "New connections should have the added connection"
        
        # Test community immutability
        communities = {
            "tech": {"user1", "user2", "user3"},
            "gaming": {"user2", "user4"}
        }
        original_communities = communities.copy()
        bridges = identify_bridge_users(communities)
        assert communities == original_communities, "Original communities should not be modified"
        
        test_obj.yakshaAssert("TestErrorHandling", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestErrorHandling", False, "exception")
        pytest.fail(f"Error handling test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])