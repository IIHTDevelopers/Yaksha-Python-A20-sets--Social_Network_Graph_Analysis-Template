import pytest
import inspect
import importlib
from test.TestUtils import TestUtils
from social_network_graph_analysis import *

@pytest.fixture
def test_obj():
   return TestUtils()

def test_variable_naming(test_obj):
   """Test that the required variable names and structure are used"""
   try:
       # Import the module
       module = importlib.import_module("social_network_graph_analysis")

       # Check set initialization
       init_source = inspect.getsource(module.initialize_data)
       assert "network_a = {" in init_source or "network_a = set" in init_source, "Initialize data must create network_a set"
       assert "network_b = {" in init_source or "network_b = set" in init_source, "Initialize data must create network_b set"
       assert "tech_group = {" in init_source or "tech_group = set" in init_source, "Initialize data must create tech_group set"
       assert "gaming_group = {" in init_source or "gaming_group = set" in init_source, "Initialize data must create gaming_group set"
       assert "connections = {" in init_source, "Initialize data must create connections dictionary"
       
       # Check main function uses required data
       main_source = inspect.getsource(module.main)
       assert "network_a, network_b, tech_group, gaming_group, arts_group, connections" in main_source, "main() must initialize network data correctly"
       
       # Check set operation functions use correct parameter names
       assert "def find_mutual_connections(user_a, user_b, connections)" in inspect.getsource(module), "find_mutual_connections() must use correct parameters"
       assert "def find_exclusive_connections(user_a, user_b, connections)" in inspect.getsource(module), "find_exclusive_connections() must use correct parameters"
       assert "def identify_bridge_users(communities)" in inspect.getsource(module), "identify_bridge_users() must use correct parameters"
       
       # Verify predefined sets in initialize_data
       network_a, network_b, tech_group, gaming_group, arts_group, connections, _, _ = initialize_data()
       assert "user1" in network_a and "user7" in network_a, "network_a must contain correct users"
       assert "user5" in network_b and "user10" in network_b, "network_b must contain correct users"
       assert "user1" in tech_group and "user10" in tech_group, "tech_group must contain correct users"
       assert "user2" in gaming_group and "user9" in gaming_group, "gaming_group must contain correct users"
       
       # Check connections dictionary
       assert "user1" in connections and "user2" in connections["user1"], "connections must have correct user mappings"
       assert "user5" in connections and "user8" in connections["user5"], "connections must have correct user mappings"
       
       test_obj.yakshaAssert("test_variable_naming", True, "functional")
   except Exception as e:
       test_obj.yakshaAssert("test_variable_naming", False, "functional")
       pytest.fail(f"Variable naming test failed: {str(e)}")

def test_set_operations(test_obj):
   """Test all set operations"""
   try:
       # Test all filtering operations
       network_a, network_b, tech_group, gaming_group, arts_group, connections, new_users, influencers = initialize_data()

       # Test find_mutual_connections
       mutual = find_mutual_connections("user1", "user3", connections)
       assert mutual == {"user5"}, "user1 and user3 should share user5 as a mutual connection"
       
       # Test find_exclusive_connections
       exclusive = find_exclusive_connections("user1", "user2", connections)
       assert "user3" in exclusive and "user4" in exclusive, "exclusive connections should contain non-shared connections"
       
       # Test find_common_group_members
       common = find_common_group_members(tech_group, arts_group)
       assert "user3" in common and "user5" in common, "tech_group and arts_group should share user3 and user5"
       assert "user1" not in common, "user1 should not be in both tech_group and arts_group"
       
       # Test find_users_in_any_group
       any_users = find_users_in_any_group(tech_group, gaming_group)
       assert len(any_users) == len(tech_group) + len(gaming_group) - len(find_common_group_members(tech_group, gaming_group))
       assert "user1" in any_users and "user2" in any_users, "any_users should contain members from both groups"
       
       # Test direct connection check
       assert is_direct_connection("user1", "user2", connections), "user1 and user2 should be directly connected"
       assert not is_direct_connection("user1", "user4", connections), "user1 and user4 should not be directly connected"
       
       # Test second degree connection
       assert is_second_degree_connection("user1", "user4", connections), "user1 and user4 should be connected through user2"
       assert not is_second_degree_connection("user1", "user2", connections), "Direct connections should not be second-degree"
       
       # Test bridge user identification
       communities = {
           "tech": tech_group,
           "gaming": gaming_group,
           "arts": arts_group
       }
       bridges = identify_bridge_users(communities)
       assert "user8" in bridges, "user8 should be identified as a bridge user (in tech and gaming)"
       assert len(bridges["user3"]) >= 2, "user3 should connect at least 2 communities"
       
       # Test network density calculation
       density = calculate_network_density(network_a, connections)
       assert 0 <= density <= 1, "Network density should be between 0 and 1"
       
       # Test isolated users
       all_users = network_a.union(network_b)
       isolated = find_isolated_users(all_users, connections)
       assert isinstance(isolated, set), "isolated_users should be a set"
       
       # Test recommendation system
       recommendations = recommend_connections("user1", connections)
       assert isinstance(recommendations, set), "recommendations should be a set"
       assert "user2" not in recommendations, "Direct connections should not be in recommendations"
       
       test_obj.yakshaAssert("test_set_operations", True, "functional")
   except Exception as e:
       test_obj.yakshaAssert("test_set_operations", False, "functional")
       pytest.fail(f"Set operations test failed: {str(e)}")

def test_implementation_techniques(test_obj):
   """Test implementation of set operation techniques"""
   try:
       # Check set operation syntax
       source = inspect.getsource(find_mutual_connections)
       assert "&" in source or ".intersection" in source, "find_mutual_connections must use set intersection"
       
       source = inspect.getsource(find_exclusive_connections)
       assert "^" in source or ".symmetric_difference" in source, "find_exclusive_connections must use symmetric difference"
       
       source = inspect.getsource(find_common_group_members)
       assert "&" in source or ".intersection" in source, "find_common_group_members must use set intersection"
       
       source = inspect.getsource(find_users_in_any_group)
       assert "|" in source or ".union" in source, "find_users_in_any_group must use set union"
       
       # Check set comprehension
       source = inspect.getsource(identify_bridge_users)
       assert "{" in source and "for" in source, "identify_bridge_users should use set comprehension"
       
       # Check set methods
       source = inspect.getsource(find_isolated_users)
       assert ".update" in source or ".add" in source or ".difference" in source, "find_isolated_users should use set methods"
       
       # Check immutability
       network_a, network_b, _, _, _, _, _, _ = initialize_data()
       original_network_a = network_a.copy()
       
       # Test immutability in union operation
       union_result = network_a | network_b
       assert network_a == original_network_a, "Original set should not be modified by union operation"
       
       test_obj.yakshaAssert("test_implementation_techniques", True, "functional")
   except Exception as e:
       test_obj.yakshaAssert("test_implementation_techniques", False, "functional")
       pytest.fail(f"Implementation techniques test failed: {str(e)}")

if __name__ == '__main__':
   pytest.main(['-v'])