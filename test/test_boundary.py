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

    def test_boundary_scenarios(self):
        """Consolidated test for boundary scenarios"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Test all required functions
            required_functions = [
                "find_mutual_connections",
                "find_exclusive_connections",
                "find_common_group_members",
                "find_users_in_any_group",
                "is_direct_connection",
                "is_second_degree_connection",
                "identify_bridge_users",
                "calculate_network_density",
                "initialize_data"
            ]
            
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                    print("TestBoundaryScenarios = Failed")
                    return

            # Test with empty connection data
            empty_connections = {}
            connections = {"user1": set(), "user2": set()}
            
            # Test mutual connections with empty sets
            mutual = safely_call_function(self.module_obj, "find_mutual_connections", "user1", "user2", connections)
            if mutual is None or not isinstance(mutual, set) or mutual != set():
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Test exclusive connections with empty sets
            exclusive = safely_call_function(self.module_obj, "find_exclusive_connections", "user1", "user2", connections)
            if exclusive is None or not isinstance(exclusive, set) or exclusive != set():
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Test with real network data if available
            init_result = safely_call_function(self.module_obj, "initialize_data")
            if init_result is None or not isinstance(init_result, tuple) or len(init_result) < 6:
                # Create fallback data for testing
                network_a = {"user1", "user2", "user3", "user4"}
                network_b = {"user5", "user6", "user7", "user8"}
                tech_group = {"user1", "user3", "user5", "user8", "user10"}
                gaming_group = {"user2", "user4", "user8", "user9"}
                arts_group = {"user3", "user5", "user7"}
                connections = {
                    "user1": {"user2", "user3", "user5"},
                    "user2": {"user1", "user4"},
                    "user3": {"user1", "user5"},
                    "user4": {"user2"},
                    "user5": {"user1", "user3", "user8"},
                    "user8": {"user5"}
                }
            else:
                network_a, network_b, tech_group, gaming_group, arts_group = init_result[:5]
                connections = init_result[5] if len(init_result) > 5 else {}
                
                if not isinstance(network_a, set) or not isinstance(tech_group, set):
                    # Create fallback data
                    network_a = {"user1", "user2", "user3", "user4"}
                    tech_group = {"user1", "user3", "user5", "user8", "user10"}

            # Test set operations with empty set
            empty_set = set()
            common = safely_call_function(self.module_obj, "find_common_group_members", tech_group, empty_set)
            if common is None or not isinstance(common, set) or common != set():
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            union = safely_call_function(self.module_obj, "find_users_in_any_group", tech_group, empty_set)
            if union is None or not isinstance(union, set) or union != tech_group:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Add valid users to connections if needed for testing
            if not connections or len(connections) < 2:
                connections = {
                    "user1": {"user2", "user3"},
                    "user2": {"user1", "user4"},
                    "user3": {"user1", "user5"},
                    "user4": {"user2"},
                    "user5": {"user3"}
                }

            # Test direct connection edge cases
            direct = safely_call_function(self.module_obj, "is_direct_connection", "user1", "user2", connections)
            if direct is None or not isinstance(direct, bool):
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Test with non-connected users
            direct = safely_call_function(self.module_obj, "is_direct_connection", "user1", "user9", connections)
            if direct is None or not isinstance(direct, bool):
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Test second-degree connection edge cases if user4 exists
            if "user4" in connections:
                second_degree = safely_call_function(self.module_obj, "is_second_degree_connection", "user1", "user4", connections)
                if second_degree is None or not isinstance(second_degree, bool):
                    self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                    print("TestBoundaryScenarios = Failed")
                    return

            # Test bridge user detection with isolated communities
            isolated_communities = {
                "group1": {"user1", "user2"},
                "group2": {"user3", "user4"}
            }
            bridges = safely_call_function(self.module_obj, "identify_bridge_users", isolated_communities)
            if bridges is None or not isinstance(bridges, dict) or bridges != {}:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Test network density bounds
            min_density = safely_call_function(self.module_obj, "calculate_network_density", {"user1", "user2"}, {"user1": set(), "user2": set()})
            if min_density is None or not isinstance(min_density, (int, float)) or min_density != 0:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            max_connections = {"user1": {"user2"}, "user2": {"user1"}}
            max_density = safely_call_function(self.module_obj, "calculate_network_density", {"user1", "user2"}, max_connections)
            if max_density is None or not isinstance(max_density, (int, float)) or max_density != 1:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
            print("TestBoundaryScenarios = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            print("TestBoundaryScenarios = Failed")

    def test_edge_case_filtering(self):
        """Test set operations with edge case inputs"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
                print("TestEdgeCaseFiltering = Failed")
                return

            # Test all required functions
            required_functions = [
                "find_common_group_members",
                "find_exclusive_connections",
                "initialize_data"
            ]
            
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
                    print("TestEdgeCaseFiltering = Failed")
                    return

            # Try to get test data
            init_result = safely_call_function(self.module_obj, "initialize_data")
            if init_result is None or not isinstance(init_result, tuple) or len(init_result) < 6:
                # Create fallback data
                tech_group = {"user1", "user3", "user5", "user8"}
                gaming_group = {"user2", "user8", "user9"}
                new_users = {"userX", "userY"}
            else:
                network_a, network_b, tech_group, gaming_group, arts_group, connections = init_result[:6]
                new_users = init_result[6] if len(init_result) > 6 else {"userX", "userY"}

            # Test set operations with identical sets
            common = safely_call_function(self.module_obj, "find_common_group_members", tech_group, tech_group)
            if common is None or not isinstance(common, set) or common != tech_group:
                self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
                print("TestEdgeCaseFiltering = Failed")
                return

            # Test exclusive connections with self
            exclusive = safely_call_function(self.module_obj, "find_exclusive_connections", "user1", "user1", 
                                           {"user1": {"user2", "user3"}, "user2": {"user1"}, "user3": {"user1"}})
            if exclusive is None or not isinstance(exclusive, set) or exclusive != set():
                self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
                print("TestEdgeCaseFiltering = Failed")
                return

            # Test with disjoint sets
            disjoint_set = {"userX", "userY", "userZ"}
            common = safely_call_function(self.module_obj, "find_common_group_members", tech_group, disjoint_set)
            if common is None or not isinstance(common, set) or common != set():
                self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
                print("TestEdgeCaseFiltering = Failed")
                return

            # Success case
            self.test_obj.yakshaAssert("TestEdgeCaseFiltering", True, "boundary")
            print("TestEdgeCaseFiltering = Passed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
            print("TestEdgeCaseFiltering = Failed")

if __name__ == '__main__':
    unittest.main()