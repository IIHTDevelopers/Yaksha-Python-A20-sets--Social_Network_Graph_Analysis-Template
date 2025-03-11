# test_boundary.py
import pytest
from test.TestUtils import TestUtils
from social_network_graph_analysis import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_boundary_scenarios(test_obj):
    """Consolidated test for boundary scenarios"""
    try:
        # Test with empty connection data
        empty_connections = {}
        
        # Test edge cases with valid users but empty connections
        connections = {"user1": set(), "user2": set()}
        
        mutual = find_mutual_connections("user1", "user2", connections)
        assert mutual == set(), "Mutual connections of empty sets should be empty"
        
        exclusive = find_exclusive_connections("user1", "user2", connections)
        assert exclusive == set(), "Exclusive connections of empty sets should be empty"
        
        # Test with real network data
        network_a, network_b, tech_group, gaming_group, arts_group, connections, _, _ = initialize_data()
        
        # Test set operations with empty set
        empty_set = set()
        common = find_common_group_members(tech_group, empty_set)
        assert common == set(), "Intersection with empty set should be empty"
        
        union = find_users_in_any_group(tech_group, empty_set)
        assert union == tech_group, "Union with empty set should equal the non-empty set"
        
        # Test direct connection edge cases
        assert is_direct_connection("user1", "user2", connections), "User1 and user2 should be directly connected"
        assert not is_direct_connection("user1", "user9", connections), "User1 and user9 should not be directly connected"
        
        # Test second-degree connection edge cases
        assert is_second_degree_connection("user1", "user4", connections), "User1 and user4 should be 2nd degree connections"
        assert not is_second_degree_connection("user1", "user2", connections), "Direct connections should not be 2nd degree"
        
        # Test bridge user detection with isolated communities
        isolated_communities = {
            "group1": {"user1", "user2"},
            "group2": {"user3", "user4"}
        }
        bridges = identify_bridge_users(isolated_communities)
        assert bridges == {}, "No bridges between isolated communities"
        
        # Test network density bounds
        min_density = calculate_network_density({"user1", "user2"}, {"user1": set(), "user2": set()})
        assert min_density == 0, "Minimum density should be 0 for no connections"
        
        max_connections = {"user1": {"user2"}, "user2": {"user1"}}
        max_density = calculate_network_density({"user1", "user2"}, max_connections)
        assert max_density == 1, "Maximum density should be 1 for fully connected network"
        
        test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
        pytest.fail(f"Boundary scenarios test failed: {str(e)}")

def test_edge_case_filtering(test_obj):
    """Test set operations with edge case inputs"""
    try:
        network_a, network_b, tech_group, gaming_group, arts_group, connections, new_users, _ = initialize_data()
        
        # Test set operations with identical sets
        common = find_common_group_members(tech_group, tech_group)
        assert common == tech_group, "Intersection with self should equal self"
        
        exclusive = find_exclusive_connections("user1", "user1", {"user1": {"user2", "user3"}, "user2": {"user1"}, "user3": {"user1"}})
        assert exclusive == set(), "Exclusive connections with self should be empty"
        
        # Test with exact boundary cases
        tech_and_gaming = find_common_group_members(tech_group, gaming_group)
        assert "user8" in tech_and_gaming, "User8 should be in both tech and gaming groups"
        
        # Test with disjoint sets
        disjoint_set = {"userX", "userY", "userZ"}
        common = find_common_group_members(tech_group, disjoint_set)
        assert common == set(), "Intersection of disjoint sets should be empty"
        
        # Test with subset relationships
        subset = {"user1", "user3"}
        assert subset.issubset(tech_group), "Subset test should be true"
        
        # Test adding new users to existing network
        all_users = set()
        for group in [network_a, network_b, tech_group, gaming_group, arts_group]:
            all_users.update(group)
        
        assert all_users.isdisjoint(new_users) == False if any(user in all_users for user in new_users) else True, "Should correctly detect if new users overlap with existing users"
        
        test_obj.yakshaAssert("TestEdgeCaseFiltering", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
        pytest.fail(f"Edge case filtering test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])