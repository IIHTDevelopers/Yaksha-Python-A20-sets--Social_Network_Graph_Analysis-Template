import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
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

    def test_variable_naming(self):
        """Test that the required variable names and structure are used"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
                return

            error_count = 0

            # Check set initialization
            if check_function_exists(self.module_obj, "initialize_data"):
                try:
                    init_source = inspect.getsource(self.module_obj.initialize_data)
                    if "network_a = {" not in init_source and "network_a = set" not in init_source:
                        error_count += 1
                    if "network_b = {" not in init_source and "network_b = set" not in init_source:
                        error_count += 1
                    if "tech_group = {" not in init_source and "tech_group = set" not in init_source:
                        error_count += 1
                    if "gaming_group = {" not in init_source and "gaming_group = set" not in init_source:
                        error_count += 1
                    if "connections = {" not in init_source:
                        error_count += 1
                except Exception as e:
                    error_count += 1
            else:
                error_count += 1

            # Check main function uses required data
            if check_function_exists(self.module_obj, "main"):
                try:
                    main_source = inspect.getsource(self.module_obj.main)
                    if "network_a, network_b, tech_group, gaming_group, arts_group, connections" not in main_source:
                        error_count += 1
                except Exception as e:
                    error_count += 1
            else:
                error_count += 1

            # Verify predefined sets in initialize_data
            if check_function_exists(self.module_obj, "initialize_data"):
                try:
                    init_result = safely_call_function(self.module_obj, "initialize_data")
                    if init_result is None or not isinstance(init_result, tuple) or len(init_result) < 6:
                        error_count += 1
                    else:
                        network_a, network_b, tech_group, gaming_group, arts_group, connections = init_result[:6]
                        
                        if not isinstance(network_a, set) or "user1" not in network_a or "user7" not in network_a:
                            error_count += 1
                        if not isinstance(network_b, set) or "user5" not in network_b or "user10" not in network_b:
                            error_count += 1
                        if not isinstance(tech_group, set) or "user1" not in tech_group or "user10" not in tech_group:
                            error_count += 1
                        if not isinstance(gaming_group, set) or "user2" not in gaming_group or "user9" not in gaming_group:
                            error_count += 1
                        if not isinstance(connections, dict) or "user1" not in connections or "user2" not in connections["user1"]:
                            error_count += 1
                        if "user5" not in connections or "user8" not in connections["user5"]:
                            error_count += 1
                except Exception as e:
                    error_count += 1

            if error_count > 0:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestVariableNaming", True, "functional")
            print("TestVariableNaming = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
            print("TestVariableNaming = Failed")

    def test_set_operations(self):
        """Test all set operations"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestSetOperations", False, "functional")
                print("TestSetOperations = Failed")
                return

            # Check required functions
            required_functions = [
                "initialize_data",
                "find_mutual_connections",
                "find_exclusive_connections",
                "find_common_group_members",
                "find_users_in_any_group",
                "is_direct_connection",
                "is_second_degree_connection",
                "identify_bridge_users",
                "calculate_network_density",
                "find_isolated_users",
                "recommend_connections"
            ]
            
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestSetOperations", False, "functional")
                    print("TestSetOperations = Failed")
                    return

            # Initialize data for testing
            init_result = safely_call_function(self.module_obj, "initialize_data")
            if init_result is None or not isinstance(init_result, tuple) or len(init_result) < 8:
                self.test_obj.yakshaAssert("TestSetOperations", False, "functional")
                print("TestSetOperations = Failed")
                return
            
            network_a, network_b, tech_group, gaming_group, arts_group, connections, new_users, influencers = init_result[:8]
            
            if not isinstance(network_a, set) or not network_a or not isinstance(connections, dict) or not connections:
                self.test_obj.yakshaAssert("TestSetOperations", False, "functional")
                print("TestSetOperations = Failed")
                return

            error_count = 0

            # Test find_mutual_connections
            mutual = safely_call_function(self.module_obj, "find_mutual_connections", "user1", "user3", connections)
            if mutual is None or not isinstance(mutual, set) or "user5" not in mutual:
                error_count += 1

            # Test find_exclusive_connections
            exclusive = safely_call_function(self.module_obj, "find_exclusive_connections", "user1", "user2", connections)
            if exclusive is None or not isinstance(exclusive, set) or ("user3" not in exclusive and "user4" not in exclusive):
                error_count += 1

            # Test find_common_group_members
            common = safely_call_function(self.module_obj, "find_common_group_members", tech_group, arts_group)
            if common is None or not isinstance(common, set) or "user3" not in common or "user5" not in common:
                error_count += 1

            # Test find_users_in_any_group
            any_users = safely_call_function(self.module_obj, "find_users_in_any_group", tech_group, gaming_group)
            if any_users is None or not isinstance(any_users, set):
                error_count += 1
            else:
                # Get the set of common members between tech_group and gaming_group
                common_members = safely_call_function(self.module_obj, "find_common_group_members", tech_group, gaming_group)
                if common_members is not None and isinstance(common_members, set):
                    expected_length = len(tech_group) + len(gaming_group) - len(common_members)
                    if len(any_users) != expected_length:
                        error_count += 1
                
                if "user1" not in any_users or "user2" not in any_users:
                    error_count += 1

            # Test direct connection check
            direct = safely_call_function(self.module_obj, "is_direct_connection", "user1", "user2", connections)
            if direct is None or not isinstance(direct, bool) or not direct:
                error_count += 1
            
            direct = safely_call_function(self.module_obj, "is_direct_connection", "user1", "user4", connections)
            if direct is None or not isinstance(direct, bool) or direct:
                error_count += 1

            # Test second degree connection
            second_degree = safely_call_function(self.module_obj, "is_second_degree_connection", "user1", "user4", connections)
            if second_degree is None or not isinstance(second_degree, bool) or not second_degree:
                error_count += 1
            
            second_degree = safely_call_function(self.module_obj, "is_second_degree_connection", "user1", "user2", connections)
            if second_degree is None or not isinstance(second_degree, bool) or second_degree:
                error_count += 1

            # Test bridge user identification
            communities = {
                "tech": tech_group,
                "gaming": gaming_group,
                "arts": arts_group
            }
            bridges = safely_call_function(self.module_obj, "identify_bridge_users", communities)
            if bridges is None or not isinstance(bridges, dict) or "user8" not in bridges:
                error_count += 1
            if "user3" not in bridges or len(bridges["user3"]) < 2:
                error_count += 1

            # Test network density calculation
            density = safely_call_function(self.module_obj, "calculate_network_density", network_a, connections)
            if density is None or not isinstance(density, (int, float)) or density < 0 or density > 1:
                error_count += 1

            # Test isolated users
            all_users = network_a.union(network_b)
            isolated = safely_call_function(self.module_obj, "find_isolated_users", all_users, connections)
            if isolated is None or not isinstance(isolated, set):
                error_count += 1

            # Test recommendation system
            recommendations = safely_call_function(self.module_obj, "recommend_connections", "user1", connections)
            if recommendations is None or not isinstance(recommendations, set) or "user2" in recommendations:
                error_count += 1

            if error_count > 0:
                self.test_obj.yakshaAssert("TestSetOperations", False, "functional")
                print("TestSetOperations = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestSetOperations", True, "functional")
            print("TestSetOperations = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestSetOperations", False, "functional")
            print("TestSetOperations = Failed")

    def test_implementation_techniques(self):
        """Test implementation of set operation techniques"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestImplementationTechniques", False, "functional")
                print("TestImplementationTechniques = Failed")
                return

            # Check required functions
            required_functions = [
                "find_mutual_connections",
                "find_exclusive_connections",
                "find_common_group_members",
                "find_users_in_any_group",
                "identify_bridge_users",
                "find_isolated_users",
                "initialize_data"
            ]
            
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestImplementationTechniques", False, "functional")
                    print("TestImplementationTechniques = Failed")
                    return

            error_count = 0

            # Check set operation syntax
            try:
                source = inspect.getsource(self.module_obj.find_mutual_connections)
                if "&" not in source and ".intersection" not in source:
                    error_count += 1
            except Exception as e:
                error_count += 1

            try:
                source = inspect.getsource(self.module_obj.find_exclusive_connections)
                if "^" not in source and ".symmetric_difference" not in source:
                    error_count += 1
            except Exception as e:
                error_count += 1

            try:
                source = inspect.getsource(self.module_obj.find_common_group_members)
                if "&" not in source and ".intersection" not in source:
                    error_count += 1
            except Exception as e:
                error_count += 1

            try:
                source = inspect.getsource(self.module_obj.find_users_in_any_group)
                if "|" not in source and ".union" not in source:
                    error_count += 1
            except Exception as e:
                error_count += 1

            # Check set comprehension
            try:
                source = inspect.getsource(self.module_obj.identify_bridge_users)
                if "{" not in source or "for" not in source:
                    error_count += 1
            except Exception as e:
                error_count += 1

            # Check set methods
            try:
                source = inspect.getsource(self.module_obj.find_isolated_users)
                if ".update" not in source and ".add" not in source and ".difference" not in source:
                    error_count += 1
            except Exception as e:
                error_count += 1

            # Check immutability
            try:
                init_result = safely_call_function(self.module_obj, "initialize_data")
                if init_result is not None and isinstance(init_result, tuple) and len(init_result) >= 2:
                    network_a, network_b = init_result[:2]
                    
                    if isinstance(network_a, set) and isinstance(network_b, set):
                        original_network_a = network_a.copy()
                        
                        # Test immutability in union operation
                        union_result = network_a | network_b
                        if network_a != original_network_a:
                            error_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1

            if error_count > 0:
                self.test_obj.yakshaAssert("TestImplementationTechniques", False, "functional")
                print("TestImplementationTechniques = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestImplementationTechniques", True, "functional")
            print("TestImplementationTechniques = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestImplementationTechniques", False, "functional")
            print("TestImplementationTechniques = Failed")

if __name__ == '__main__':
    unittest.main()