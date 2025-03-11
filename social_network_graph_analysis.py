"""
Social Network Graph Analysis
This program demonstrates set operations through social network analysis.
"""

def initialize_data():
   """
   Initialize the network data with predefined sets using sets.
   
   Returns:
       tuple: A tuple containing network data sets
   """
   # Create the main network sets
   network_a = {"user1", "user2", "user3", "user4", "user5", "user6", "user7"}
   network_b = {"user5", "user6", "user7", "user8", "user9", "user10"}
   tech_group = {"user1", "user3", "user5", "user8", "user10"}
   gaming_group = {"user2", "user4", "user6", "user8", "user9"}
   arts_group = {"user3", "user5", "user7", "user10"}
   
   # Create connection sets
   connections = {
       "user1": {"user2", "user3", "user5"},
       "user2": {"user1", "user4", "user6"},
       "user3": {"user1", "user5", "user7"},
       "user4": {"user2", "user6"},
       "user5": {"user1", "user3", "user7", "user8"},
       "user6": {"user2", "user4"},
       "user7": {"user3", "user5"},
       "user8": {"user5", "user9", "user10"},
       "user9": {"user8"},
       "user10": {"user8"}
   }
   
   # Create new network data sets
   new_users = {"user11", "user12", "user13"}
   influencers = {"user3", "user5", "user8", "user11"}
   
   return network_a, network_b, tech_group, gaming_group, arts_group, connections, new_users, influencers

def find_mutual_connections(user_a, user_b, connections):
    """
    Find mutual connections between two users.
    
    Args:
        user_a (str): First user
        user_b (str): Second user
        connections (dict): Dictionary of user connections
    
    Returns:
        set: Set of mutual connections
    """
    if connections is None:
        raise ValueError("Connections cannot be None")
        
    if user_a not in connections:
        raise ValueError(f"User {user_a} not found in connections")
    if user_b not in connections:
        raise ValueError(f"User {user_b} not found in connections")
    
    return connections[user_a] & connections[user_b]


def find_exclusive_connections(user_a, user_b, connections):
    """
    Find connections exclusive to each user (not shared).
    
    Args:
        user_a (str): First user
        user_b (str): Second user
        connections (dict): Dictionary of user connections
    
    Returns:
        set: Set of exclusive connections
    """
    if connections is None:
        raise ValueError("Connections cannot be None")
        
    if user_a not in connections:
        raise ValueError(f"User {user_a} not found in connections")
    if user_b not in connections:
        raise ValueError(f"User {user_b} not found in connections")
    
    return connections[user_a] ^ connections[user_b]

def find_common_group_members(group_a, group_b):
    """
    Find users that are members of both groups.
    
    Args:
        group_a (set): First group of users
        group_b (set): Second group of users
    
    Returns:
        set: Set of users in both groups
    """
    if group_a is None or group_b is None:
        raise ValueError("Group sets cannot be None")
    
    return group_a & group_b

def find_users_in_any_group(group_a, group_b):
    """
    Find users that are members of either group.
    
    Args:
        group_a (set): First group of users
        group_b (set): Second group of users
    
    Returns:
        set: Set of users in either group
    """
    if group_a is None or group_b is None:
        raise ValueError("Group sets cannot be None")
    
    return group_a | group_b

def find_all_connections(user, connections, depth=1):
    """
    Find all connections up to a certain depth.
    
    Args:
        user (str): The user to find connections for
        connections (dict): Dictionary of user connections
        depth (int): Connection depth (1 = direct, 2 = friend of friend)
    
    Returns:
        set: Set of all connections up to specified depth
    """
    if connections is None:
        raise ValueError("Connections cannot be None")
        
    if user not in connections:
        raise ValueError(f"User {user} not found in connections")
    if depth < 1:
        raise ValueError("Depth must be at least 1")
    
    all_connections = set()
    
    # Add direct connections (depth 1)
    direct_connections = connections[user]
    all_connections.update(direct_connections)
    
    # Add deeper connections if depth > 1
    current_depth = 1
    frontier = direct_connections
    
    while current_depth < depth and frontier:
        new_frontier = set()
        for connection in frontier:
            if connection in connections:  # Ensure the connection exists in our data
                new_connections = connections[connection] - all_connections - {user}
                new_frontier.update(new_connections)
        
        all_connections.update(new_frontier)
        frontier = new_frontier
        current_depth += 1
    
    return all_connections

def is_direct_connection(user_a, user_b, connections):
    """
    Check if two users are directly connected.
    
    Args:
        user_a (str): First user
        user_b (str): Second user
        connections (dict): Dictionary of user connections
    
    Returns:
        bool: True if directly connected, False otherwise
    """
    if connections is None:
        raise ValueError("Connections cannot be None")
        
    if user_a not in connections:
        raise ValueError(f"User {user_a} not found in connections")
    
    return user_b in connections[user_a]

def is_second_degree_connection(user_a, user_b, connections):
    """
    Check if two users are connected through a mutual friend.
    
    Args:
        user_a (str): First user
        user_b (str): Second user
        connections (dict): Dictionary of user connections
    
    Returns:
        bool: True if second-degree connected, False otherwise
    """
    if connections is None:
        raise ValueError("Connections cannot be None")
        
    if user_a not in connections:
        raise ValueError(f"User {user_a} not found in connections")
    if user_b not in connections:
        raise ValueError(f"User {user_b} not found in connections")
    
    # If they're directly connected, they're not second-degree
    if is_direct_connection(user_a, user_b, connections):
        return False
    
    # Check if any of user_a's friends is also a friend of user_b
    for friend in connections[user_a]:
        if friend in connections and user_b in connections[friend]:
            return True
    
    return False

def identify_bridge_users(communities):
    """
    Identify users that connect multiple communities.
    
    Args:
        communities (dict): Dictionary of community sets
    
    Returns:
        dict: Dictionary with users as keys and set of communities as values
    """
    if communities is None:
        raise ValueError("Communities data cannot be None")
    
    # Create a dictionary to track which communities each user belongs to
    user_communities = {}
    
    # Go through each community and add users to the tracking dictionary
    for community_name, members in communities.items():
        for user in members:
            if user not in user_communities:
                user_communities[user] = set()
            user_communities[user].add(community_name)
    
    # Filter to only users that are in more than one community
    bridge_users = {user: comms for user, comms in user_communities.items() if len(comms) > 1}
    
    return bridge_users

def calculate_network_density(users, connections):
    """
    Calculate network density (ratio of actual to possible connections).
    
    Args:
        users (set): Set of users
        connections (dict): Dictionary of user connections
    
    Returns:
        float: Network density (0-1)
    """
    if users is None:
        raise ValueError("Users set cannot be None")
    if connections is None:
        raise ValueError("Connections cannot be None")
    if not users:
        raise ValueError("User set cannot be empty")
    
    # Calculate the number of possible connections
    # In an undirected graph, max connections = n(n-1)/2 where n is number of users
    num_users = len(users)
    max_possible_connections = (num_users * (num_users - 1)) / 2
    
    if max_possible_connections == 0:  # Handle case with only 1 user
        return 0.0
    
    # Count actual connections (avoid counting twice in undirected graph)
    actual_connections = 0
    counted_pairs = set()
    
    for user in users:
        if user in connections:
            for connection in connections[user]:
                if connection in users:
                    # Create a pair identifier that is order-independent
                    pair = tuple(sorted([user, connection]))
                    if pair not in counted_pairs:
                        actual_connections += 1
                        counted_pairs.add(pair)
    
    return actual_connections / max_possible_connections

def find_isolated_users(users, connections):
    """
    Find users with no connections.
    
    Args:
        users (set): Set of all users
        connections (dict): Dictionary of user connections
    
    Returns:
        set: Set of isolated users
    """
    if users is None:
        raise ValueError("Users set cannot be None")
    if connections is None:
        raise ValueError("Connections cannot be None")
    
    isolated = set()
    
    for user in users:
        if user not in connections or not connections[user]:
            isolated.add(user)
        # Also check if anyone connects to this user
        elif all(user not in connections.get(other_user, set()) for other_user in users if other_user != user):
            isolated.add(user)
    
    return isolated

def recommend_connections(user, connections, depth=2):
    """
    Recommend new connections based on friends of friends.
    
    Args:
        user (str): User to make recommendations for
        connections (dict): Dictionary of user connections
        depth (int): Connection depth for recommendations
    
    Returns:
        set: Set of recommended connections
    """
    if connections is None:
        raise ValueError("Connections cannot be None")
        
    if user not in connections:
        raise ValueError(f"User {user} not found in connections")
    
    # Get all connections up to the depth
    all_connections = find_all_connections(user, connections, depth)
    
    # Direct connections
    direct_connections = connections[user]
    
    # Recommendations are connections of depth > 1 that aren't direct connections
    recommendations = all_connections - direct_connections - {user}
    
    return recommendations

def format_users_for_display(group_name, users):
   """
   Format a user set for display.
   
   Args:
       group_name (str): Name of the user group
       users (set): Set of users
   
   Returns:
       str: Formatted user string
   """
   if users is None:
       raise ValueError("User set cannot be None")
   
   formatted_users = ", ".join(sorted(users))
   return f"{group_name}: {{{formatted_users}}}"

def display_analysis_result(operation, set_a, set_b, result):
   """
   Display set operation result.
   
   Args:
       operation (str): Operation description
       set_a (set): First set
       set_b (set): Second set
       result (set): Result set
   """
   print(f"\nAnalysis Result: {operation}")
   print(f"Set A: {set_a}")
   print(f"Set B: {set_b}")
   print(f"Result: {result}")

def display_data(data, data_type):
   """
   Display formatted data based on data type.
   
   Args:
       data: Data to display (set, dict, etc.)
       data_type (str): Type of data being displayed
   """
   if data is None:
       print("No data to display.")
       return
   
   if data_type == "networks":
       print("\nCurrent Network Data:")
       
       if not data:
           print("No networks to display.")
           return
       
       for network_name, users in data.items():
           print(format_users_for_display(network_name, users))
   
   elif data_type == "connections":
       print("\nUser Connections:")
       
       if not data:
           print("No connections to display.")
           return
       
       for user, connections in sorted(data.items()):
           print(f"{user} → {', '.join(sorted(connections))}")
   
   elif data_type == "mutual_connections":
       print("\nMutual Connections:")
       user_a, user_b, mutual = data
       print(f"Between {user_a} and {user_b}: {', '.join(sorted(mutual))}")
   
   elif data_type == "bridge_users":
       print("\nBridge Users (connecting multiple communities):")
       
       if not data:
           print("No bridge users found.")
           return
       
       for user, communities in data.items():
           print(f"{user}: connects {', '.join(sorted(communities))}")
   
   elif data_type == "recommendations":
       print("\nConnection Recommendations:")
       user, recommendations = data
       if recommendations:
           print(f"For {user}: {', '.join(sorted(recommendations))}")
       else:
           print(f"No recommendations for {user}")
   
   else:
       print(f"\n{data_type}:")
       print(data)

def main():
   """Main program function."""
   network_a, network_b, tech_group, gaming_group, arts_group, connections, new_users, influencers = initialize_data()
   
   # Store network groups for easy access
   networks = {
       "Network A": network_a,
       "Network B": network_b,
       "Tech Group": tech_group,
       "Gaming Group": gaming_group,
       "Arts Group": arts_group
   }
   
   while True:
       # Calculate basic statistics
       all_users = set()
       for network in networks.values():
           all_users.update(network)
       
       print(f"\n===== SOCIAL NETWORK GRAPH ANALYSIS =====")
       print(f"Total Users: {len(all_users)}")
       print(f"Available Networks: {', '.join(networks.keys())}")
       
       print("\nMain Menu:")
       print("1. View Network Data")
       print("2. Analyze Connections")
       print("3. Find Community Patterns")
       print("4. Calculate Network Metrics")
       print("5. Generate Recommendations")
       print("0. Exit")
       
       choice = input("Enter your choice (0-5): ")
       
       if choice == "0":
           print("Thank you for using the Social Network Graph Analysis System!")
           break
       
       elif choice == "1":
           print("\nView Options:")
           print("1. All Networks")
           print("2. User Connections")
           view_choice = input("Select view option (1-2): ")
           
           if view_choice == "1":
               display_data(networks, "networks")
           
           elif view_choice == "2":
               display_data(connections, "connections")
           
           else:
               print("Invalid choice.")
       
       elif choice == "2":
           print("\nConnection Analysis Options:")
           print("1. Find Mutual Connections")
           print("2. Find Exclusive Connections")
           print("3. Check Direct Connection")
           print("4. Check Second-Degree Connection")
           connection_choice = input("Select analysis option (1-4): ")
           
           if connection_choice == "1":
               try:
                   user_a = input("Enter first user ID: ")
                   user_b = input("Enter second user ID: ")
                   mutual = find_mutual_connections(user_a, user_b, connections)
                   display_data((user_a, user_b, mutual), "mutual_connections")
               except ValueError as e:
                   print(f"Error: {e}")
           
           elif connection_choice == "2":
               try:
                   user_a = input("Enter first user ID: ")
                   user_b = input("Enter second user ID: ")
                   exclusive = find_exclusive_connections(user_a, user_b, connections)
                   display_analysis_result("Exclusive Connections", 
                                         connections[user_a], connections[user_b], exclusive)
               except ValueError as e:
                   print(f"Error: {e}")
           
           elif connection_choice == "3":
               try:
                   user_a = input("Enter first user ID: ")
                   user_b = input("Enter second user ID: ")
                   if is_direct_connection(user_a, user_b, connections):
                       print(f"{user_a} and {user_b} are directly connected.")
                   else:
                       print(f"{user_a} and {user_b} are NOT directly connected.")
               except ValueError as e:
                   print(f"Error: {e}")
           
           elif connection_choice == "4":
               try:
                   user_a = input("Enter first user ID: ")
                   user_b = input("Enter second user ID: ")
                   if is_second_degree_connection(user_a, user_b, connections):
                       print(f"{user_a} and {user_b} are second-degree connections.")
                   else:
                       print(f"{user_a} and {user_b} are NOT second-degree connections.")
               except ValueError as e:
                   print(f"Error: {e}")
           
           else:
               print("Invalid choice.")
       
       elif choice == "3":
           print("\nCommunity Analysis Options:")
           print("1. Find Common Group Members")
           print("2. Find Users in Either Group")
           print("3. Identify Bridge Users")
           community_choice = input("Select analysis option (1-3): ")
           
           if community_choice == "1":
               try:
                   print("\nAvailable groups:", ", ".join(networks.keys()))
                   group_a_name = input("Enter first group name: ")
                   group_b_name = input("Enter second group name: ")
                   
                   if group_a_name not in networks or group_b_name not in networks:
                       print("Group not found!")
                       continue
                   
                   common = find_common_group_members(networks[group_a_name], networks[group_b_name])
                   display_analysis_result("Common Group Members", 
                                         networks[group_a_name], networks[group_b_name], common)
               except ValueError as e:
                   print(f"Error: {e}")
           
           elif community_choice == "2":
               try:
                   print("\nAvailable groups:", ", ".join(networks.keys()))
                   group_a_name = input("Enter first group name: ")
                   group_b_name = input("Enter second group name: ")
                   
                   if group_a_name not in networks or group_b_name not in networks:
                       print("Group not found!")
                       continue
                   
                   in_either = find_users_in_any_group(networks[group_a_name], networks[group_b_name])
                   display_analysis_result("Users in Either Group", 
                                         networks[group_a_name], networks[group_b_name], in_either)
               except ValueError as e:
                   print(f"Error: {e}")
           
           elif community_choice == "3":
               bridge_users = identify_bridge_users(networks)
               display_data(bridge_users, "bridge_users")
           
           else:
               print("Invalid choice.")
       
       elif choice == "4":
           print("\nNetwork Metrics Options:")
           print("1. Calculate Network Density")
           print("2. Find Isolated Users")
           metrics_choice = input("Select metrics option (1-2): ")
           
           if metrics_choice == "1":
               try:
                   density = calculate_network_density(all_users, connections)
                   print(f"\nNetwork Density: {density:.4f}")
                   print(f"This network is {density*100:.1f}% connected out of all possible connections.")
               except ValueError as e:
                   print(f"Error: {e}")
           
           elif metrics_choice == "2":
               isolated = find_isolated_users(all_users, connections)
               if isolated:
                   print("\nIsolated Users (no connections):")
                   print(", ".join(sorted(isolated)))
               else:
                   print("\nNo isolated users found.")
           
           else:
               print("Invalid choice.")
       
       elif choice == "5":
           try:
               user = input("Enter user ID for recommendations: ")
               recommendations = recommend_connections(user, connections)
               display_data((user, recommendations), "recommendations")
           except ValueError as e:
               print(f"Error: {e}")
       
       else:
           print("Invalid choice. Please try again.")

if __name__ == "__main__":
   main()