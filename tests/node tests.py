nodes = [
    # =========================================================
    # ENTRY CLUSTER
    # =========================================================
    Node(
        1, "edge_terminal", (200, 350), 14, [2, 3],
        network_suspicion_base_value=3,
        base_unlock_cost=5,
        udf_per_click=1,
        influence_emit=1,
        is_entry_point=True
    ),
    Node(
        2, "edge_terminal", (200, 500), 14, [1, 4],
        network_suspicion_base_value=3,
        base_unlock_cost=5,
        udf_per_click=1,
        influence_emit=1,
        is_entry_point=True
    ),
    Node(
        3, "kiosk_net", (350, 300), 16, [1, 4, 5],
        network_suspicion_base_value=4,
        base_unlock_cost=10,
        udf_per_click=1,
        udf_per_second=1,
        influence_emit=1
    ),
    Node(
        4, "kiosk_net", (350, 500), 16, [2, 3, 6],
        network_suspicion_base_value=4,
        base_unlock_cost=10,
        udf_per_click=1,
        udf_per_second=1,
        influence_emit=1
    ),

    # =========================================================
    # EARLY MID WEB
    # =========================================================
    Node(
        5, "datavault", (550, 260), 18, [3, 7],
        network_suspicion_base_value=6,
        base_unlock_cost=20,
        udf_per_click=2,
        udf_per_second=2,
        influence_emit=2
    ),
    Node(
        6, "datavault", (550, 540), 18, [4, 8],
        network_suspicion_base_value=6,
        base_unlock_cost=20,
        udf_per_click=2,
        udf_per_second=2,
        influence_emit=2
    ),
    Node(
        7, "credit_forge", (700, 350), 18, [5, 9, 10],
        network_suspicion_base_value=7,
        base_unlock_cost=25,
        udf_per_click=1,
        udf_per_second=2,
        credits_per_second=2,
        influence_emit=2
    ),
    Node(
        8, "credit_forge", (700, 450), 18, [6, 9],
        network_suspicion_base_value=7,
        base_unlock_cost=25,
        udf_per_click=1,
        udf_per_second=2,
        credits_per_second=2,
        influence_emit=2
    ),

    # =========================================================
    # MID SPINE + LOOPS
    # =========================================================
    Node(
        9, "proxy_cache", (900, 300), 16, [7, 8, 11],
        network_suspicion_base_value=9,
        base_unlock_cost=30,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=3
    ),
    Node(
        10, "proxy_cache", (900, 500), 16, [7, 12],
        network_suspicion_base_value=9,
        base_unlock_cost=30,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=3
    ),
    Node(
        11, "market_ai", (1050, 260), 18, [9, 13],
        network_suspicion_base_value=11,
        base_unlock_cost=35,
        udf_per_click=2,
        udf_per_second=2,
        credits_per_second=3,
        influence_emit=3
    ),
    Node(
        12, "market_ai", (1050, 540), 18, [10, 13],
        network_suspicion_base_value=11,
        base_unlock_cost=35,
        udf_per_click=2,
        udf_per_second=2,
        credits_per_second=3,
        influence_emit=3
    ),

    # =========================================================
    # HIGH-TIER CONVERGENCE
    # =========================================================
    Node(
        13, "cloud_spire", (1200, 350), 20, [11, 12, 14],
        network_suspicion_base_value=14,
        base_unlock_cost=45,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=4
    ),
    Node(
        14, "identity_forge", (1350, 350), 18, [13, 15],
        network_suspicion_base_value=18,
        base_unlock_cost=55,
        udf_per_click=3,
        udf_per_second=3,
        influence_emit=4
    ),

    # =========================================================
    # CORE APPROACH
    # =========================================================
    Node(
        15, "black_db", (1500, 350), 20, [14, 16],
        network_suspicion_base_value=22,
        base_unlock_cost=65,
        udf_per_click=4,
        udf_per_second=4,
        influence_emit=5
    ),

    # =========================================================
    # CORE
    # =========================================================
    Node(
        16, "corp_core", (1700, 350), 28, [15],
        network_suspicion_base_value=30,
        base_unlock_cost=90,
        udf_per_click=7,
        udf_per_second=10,
        credits_per_second=8,
        influence_emit=6,
        is_core=True
    ),
    # =========================================================
    # DEEP MID — SIDE LOOPS & ALTERNATE ROUTES
    # =========================================================
    Node(
        17, "signal_relay", (950, 150), 16, [9, 11, 18],
        network_suspicion_base_value=10,
        base_unlock_cost=28,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=3
    ),
    Node(
        18, "signal_relay", (1100, 150), 16, [17, 13, 19],
        network_suspicion_base_value=12,
        base_unlock_cost=32,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=3
    ),

    # =========================================================
    # HIGH-TIER SIDE WEB
    # =========================================================
    Node(
        19, "audit_node", (1250, 200), 18, [18, 14, 20],
        network_suspicion_base_value=15,
        base_unlock_cost=48,
        udf_per_click=3,
        udf_per_second=2,
        influence_emit=4
    ),
    Node(
        20, "audit_node", (1250, 500), 18, [12, 14, 21],
        network_suspicion_base_value=15,
        base_unlock_cost=48,
        udf_per_click=3,
        udf_per_second=2,
        influence_emit=4
    ),

    # =========================================================
    # CORE PERIMETER RING
    # =========================================================
    Node(
        21, "firewall_mesh", (1450, 200), 20, [19, 22],
        network_suspicion_base_value=20,
        base_unlock_cost=60,
        udf_per_click=4,
        udf_per_second=3,
        influence_emit=5
    ),
    Node(
        22, "firewall_mesh", (1550, 200), 20, [21, 15],
        network_suspicion_base_value=20,
        base_unlock_cost=60,
        udf_per_click=4,
        udf_per_second=3,
        influence_emit=5
    ),
    Node(
        23, "firewall_mesh", (1450, 500), 20, [20, 24],
        network_suspicion_base_value=20,
        base_unlock_cost=60,
        udf_per_click=4,
        udf_per_second=3,
        influence_emit=5
    ),
    Node(
        24, "firewall_mesh", (1550, 500), 20, [23, 15],
        network_suspicion_base_value=20,
        base_unlock_cost=60,
        udf_per_click=4,
        udf_per_second=3,
        influence_emit=5
    ),

    # =========================================================
    # CORE ADJACENT SUPPORT
    # =========================================================
    Node(
        25, "sentinel_ai", (1650, 250), 18, [22, 16],
        network_suspicion_base_value=26,
        base_unlock_cost=75,
        udf_per_click=5,
        udf_per_second=5,
        influence_emit=6
    ),
    Node(
        26, "sentinel_ai", (1650, 450), 18, [24, 16],
        network_suspicion_base_value=26,
        base_unlock_cost=75,
        udf_per_click=5,
        udf_per_second=5,
        influence_emit=6
    ),

]
