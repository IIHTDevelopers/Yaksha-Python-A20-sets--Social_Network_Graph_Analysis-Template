import unittest
import os
import importlib
import sys
import io
import contextlib
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning the result or None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        # Suppress stdout to prevent unwanted output
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_input_validation(self):
        """Consolidated test for input validation and error handling"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return

            # Test data for validation tests
            test_connections = {"user1": {"user2"}, "user2": {"user1"}}
            test_communities = {"group1": {"user1", "user2"}, "group2": {"user2", "user3"}}
            
            # List of functions to test with None inputs
            functions_to_test = [
                ("find_mutual_connections", ["user1", "user2", None]),
                ("find_exclusive_connections", ["user1", "user2", None]),
                ("find_all_connections", ["user1", None]),
                ("find_common_group_members", [None, {"user1", "user2"}]),
                ("find_common_group_members", [{"user1", "user2"}, None]),
                ("find_users_in_any_group", [None, {"user1", "user2"}]),
                ("find_users_in_any_group", [{"user1", "user2"}, None]),
                ("is_direct_connection", ["user1", "user2", None]),
                ("is_second_degree_connection", ["user1", "user2", None]),
                ("identify_bridge_users", [None]),
                ("calculate_network_density", [None, test_connections]),
                ("calculate_network_density", [set(), test_connections]),
                ("find_isolated_users", [None, test_connections]),
                ("recommend_connections", ["user1", None]),
                ("format_users_for_display", ["Group", None])
            ]
            
            # Test each function with None inputs
            error_count = 0
            for func_name, args in functions_to_test:
                if check_function_exists(self.module_obj, func_name):
                    func = getattr(self.module_obj, func_name)
                    result = check_raises(func, args, ValueError)
                    if not result:
                        error_count += 1
                else:
                    error_count += 1

            # Test with invalid parameter values
            
            # Test non-existent user
            if check_function_exists(self.module_obj, "find_mutual_connections"):
                result = check_raises(
                    self.module_obj.find_mutual_connections,
                    ["nonexistent", "user2", test_connections],
                    ValueError
                )
                if not result:
                    error_count += 1

            # Test invalid depth
            if check_function_exists(self.module_obj, "find_all_connections"):
                result = check_raises(
                    self.module_obj.find_all_connections,
                    ["user1", test_connections, 0],
                    ValueError
                )
                if not result:
                    error_count += 1

            # Test non-existent user in connections
            if check_function_exists(self.module_obj, "recommend_connections"):
                result = check_raises(
                    self.module_obj.recommend_connections,
                    ["nonexistent", test_connections],
                    ValueError
                )
                if not result:
                    error_count += 1

            if error_count > 0:
                self.test_obj.yakshaAssert("TestInputValidation", False, "exception")
                print("TestInputValidation = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestInputValidation", True, "exception")
            print("TestInputValidation = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestInputValidation", False, "exception")
            print("TestInputValidation = Failed")

    def test_error_handling(self):
        """Test specific error handling scenarios"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return

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
            
            error_count = 0
            
            # Check if find_mutual_connections exists
            if check_function_exists(self.module_obj, "find_mutual_connections"):
                # Should raise exception when dealing with invalid data types
                result = check_raises(
                    self.module_obj.find_mutual_connections,
                    ["user1", "user3", invalid_connections],
                    Exception
                )
                if not result:
                    error_count += 1
            else:
                error_count += 1

            # Test immutability - original connections should not change
            if check_function_exists(self.module_obj, "find_mutual_connections"):
                # Make a copy of the original connections for user1
                if "user1" in test_connections:
                    original_user1_connections = test_connections["user1"].copy()
                    
                    # Call the function
                    result = safely_call_function(self.module_obj, "find_mutual_connections", "user1", "user2", test_connections)
                    
                    # Check if the original data was modified
                    if test_connections["user1"] != original_user1_connections:
                        error_count += 1

            # Test community immutability
            communities = {
                "tech": {"user1", "user2", "user3"},
                "gaming": {"user2", "user4"}
            }
            
            # Make a deep copy of the original communities
            original_communities = {}
            for group, members in communities.items():
                original_communities[group] = members.copy()

            # Check if identify_bridge_users exists
            if check_function_exists(self.module_obj, "identify_bridge_users"):
                bridges = safely_call_function(self.module_obj, "identify_bridge_users", communities)
                
                # Check if the original data was modified
                modified = False
                for group in original_communities:
                    if group not in communities or communities[group] != original_communities[group]:
                        modified = True
                        break
                
                if modified:
                    error_count += 1
            else:
                error_count += 1

            if error_count > 0:
                self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestErrorHandling", True, "exception")
            print("TestErrorHandling = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
            print("TestErrorHandling = Failed")

if __name__ == '__main__':
    unittest.main()