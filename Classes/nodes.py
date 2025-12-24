NODE_TYPE_DEFS = {
    # -------------------------
    # Low-tier / entry nodes
    # -------------------------
    "edge_terminal": {
        "description": "Disposable street terminals and personal cyberdecks.",
        "base_unlock_cost": 4,
        "udf_per_click": 1,
        "udf_per_second": 0,
        "credits_per_click": 0,
        "credits_per_second": 0,
        "influence_emit": 1,
        "radius_size": 12,
    },

    "kiosk_net": {
        "description": "Public kiosks, vending AIs, ad-panels skimming microtransactions.",
        "base_unlock_cost": 10,
        "udf_per_click": 1,
        "udf_per_second": 1,
        "credits_per_click": 1,
        "credits_per_second": 1,
        "influence_emit": 1,
        "radius_size": 13,
    },

    # -------------------------
    # Data-focused nodes
    # -------------------------
    "datavault": {
        "description": "Encrypted corporate storage stacks.",
        "base_unlock_cost": 22,
        "udf_per_click": 2,
        "udf_per_second": 1,
        "credits_per_click": 0,
        "credits_per_second": 1,
        "influence_emit": 2,
        "radius_size": 14,
    },

    "black_db": {
        "description": "Shadow databases with illegal or proprietary intel.",
        "base_unlock_cost": 48,
        "udf_per_click": 4,
        "udf_per_second": 3,
        "credits_per_click": 1,
        "credits_per_second": 2,
        "influence_emit": 4,
        "radius_size": 16,
    },

    # -------------------------
    # Financial nodes
    # -------------------------
    "credit_forge": {
        "description": "Automated laundering engines and shell-account routers.",
        "base_unlock_cost": 55,
        "udf_per_click": 1,
        "udf_per_second": 1,
        "credits_per_click": 4,
        "credits_per_second": 5,
        "influence_emit": 3,
        "radius_size": 16,
    },

    "market_ai": {
        "description": "High-frequency trading AIs and synthetic markets.",
        "base_unlock_cost": 70,
        "udf_per_click": 2,
        "udf_per_second": 2,
        "credits_per_click": 6,
        "credits_per_second": 6,
        "influence_emit": 4,
        "radius_size": 17,
    },

    # -------------------------
    # Control & access nodes
    # -------------------------
    "cloud_spire": {
        "description": "Corporate cloud spires routing global traffic.",
        "base_unlock_cost": 65,
        "udf_per_click": 3,
        "udf_per_second": 4,
        "credits_per_click": 1,
        "credits_per_second": 2,
        "influence_emit": 7,
        "radius_size": 17,
    },

    "identity_forge": {
        "description": "Biometric identity engines and credential authorities.",
        "base_unlock_cost": 42,
        "udf_per_click": 2,
        "udf_per_second": 2,
        "credits_per_click": 0,
        "credits_per_second": 1,
        "influence_emit": 9,
        "radius_size": 15,
    },

    # -------------------------
    # Industrial / high-risk
    # -------------------------
    "neurogrid": {
        "description": "Neural-linked industrial control grids and automation cores.",
        "base_unlock_cost": 85,
        "udf_per_click": 5,
        "udf_per_second": 6,
        "credits_per_click": 2,
        "credits_per_second": 4,
        "influence_emit": 11,
        "radius_size": 18,
    },

    "drone_fabricator": {
        "description": "Autonomous manufacturing lines and drone foundries.",
        "base_unlock_cost": 95,
        "udf_per_click": 3,
        "udf_per_second": 4,
        "credits_per_click": 3,
        "credits_per_second": 6,
        "influence_emit": 8,
        "radius_size": 18,
    },

    # -------------------------
    # Defensive / hostile nodes
    # -------------------------
    "black_ice": {
        "description": "Adaptive ICE and hostile counter-intrusion systems.",
        "base_unlock_cost": 75,
        "udf_per_click": 1,
        "udf_per_second": 1,
        "credits_per_click": 0,
        "credits_per_second": 0,
        "influence_emit": -7,  # suppresses influence buildup
        "radius_size": 16,
    },

    "trace_hub": {
        "description": "Surveillance and trace-analysis hubs monitoring intrusions.",
        "base_unlock_cost": 60,
        "udf_per_click": 1,
        "udf_per_second": 0,
        "credits_per_click": 0,
        "credits_per_second": 0,
        "influence_emit": -4,
        "radius_size": 15,
    },

    # -------------------------
    # Endgame
    # -------------------------
    "corp_core": {
        "description": "Corporate nexus: boardroom logic, financial AIs, root keys.",
        "base_unlock_cost": 130,
        "udf_per_click": 9,
        "udf_per_second": 11,
        "credits_per_click": 6,
        "credits_per_second": 10,
        "influence_emit": 18,
        "radius_size": 20,
    },
}


class Node:
    """
    A network node belonging to a single corporation.
    UDF -- Unauthorized Data Flow
    States:
        - "locked"        : not accessible, costs UDF to unlock
        - "unlocked"      : accessible but inert
        - "compromised"   : generates UDF + Credits and emits influence
    """

    def __init__(
            self,
            node_id,
            node_type,
            pos,
            radius_size,
            neighbors,
            *,
            state="locked",
            base_unlock_cost=0,
            influence_emit=0,
            influence_build_up=0,
            udf_per_click=0,
            udf_per_second=0,
            credits_per_second=0,
            credits_per_click=0,
            is_entry_point=False,
            is_core=False
    ):

        self.id = node_id
        self.node_type = node_type
        self.pos = pos
        self.radius_size = radius_size
        self.neighbors = neighbors            # list of neighbor node IDs
        self.state = state                    # locked | unlocked | compromised

        self.blue_pressure = 0
        self.blue_threshold = 0

        self.is_anchored = False
        self.cooldown_timer = 0
        self.base_unlock_cost = base_unlock_cost
        self.influence_emit = influence_emit
        self.influence_build_up = influence_build_up

        self.udf_per_click = udf_per_click
        self.udf_per_second = udf_per_second
        self.credits_per_second = credits_per_second
        self.credits_per_click = credits_per_click

        self.is_entry_point = is_entry_point
        self.is_core = is_core


    def __repr__(self):
        return f"<Node id={self.id} state={self.state}>"

    # -------------------------
    # State queries
    # -------------------------

    @property
    def is_locked(self):
        return self.state == "locked"

    @property
    def is_unlocked(self):
        return self.state == "unlocked"

    @property
    def is_compromised(self):
        return self.state == "compromised"

    @property
    def get_influence_buildup(self):
        return self.influence_build_up
    # -------------------------
    # Economic output
    # -------------------------

    def emits_influence(self):
        """Only compromised nodes emit influence."""
        return self.is_compromised and self.influence_emit > 0

    def generates_udf(self):
        """Only compromised nodes generate UDF."""
        return self.is_compromised

    # -------------------------
    # State transitions
    # -------------------------

    def unlock(self):
        """Called by the network once cost is paid."""
        if self.state != "locked":
            return False
        self.state = "unlocked"
        return True

    def compromise(self):
        if self.state not in ("unlocked", "locked"):
            return False
        self.state = "compromised"
        return True


class CorporationNetwork:
    def __init__(self, corp_id, nodes, difficulty, total_udf_gathered, total_heat):
        self.corp_id = corp_id
        self.nodes = nodes
        self.difficulty = difficulty

        # local, per-corp resources
        self.total_udf_gathered = total_udf_gathered
        self.total_heat = total_heat

        self.is_active = False
        self.is_complete = False
        self.is_network_entered = False


    # -------------------------
    # Spatial query
    # -------------------------

    def get_clicked_node(self, mx, my):
        for node in self.nodes:
            cx, cy = node.pos
            if ((mx - cx) ** 2 + (my - cy) ** 2) <= node.radius_size ** 2:
                return node
        return None

    def get_hovered_node(self, mx, my):
        return self.get_clicked_node(mx, my)

    # -------------------------
    # UDF generation
    # -------------------------

    def get_udf_per_click(self, mx, my):
        node = self.get_clicked_node(mx, my)
        if node is None or not node.is_compromised:
            return 0
        return node.udf_per_click


    def get_udf_per_second(self):
        udf_ps = 0
        for node in self.nodes:
            if node.is_compromised:
                udf_ps += node.udf_per_second
        return udf_ps

    def get_credits_per_second(self):
        cps = 0
        for node in self.nodes:
            if node.is_compromised:
                cps += node.credits_per_second
        return cps
    # -------------------------
    # Network tick
    # -------------------------

    def advance_network_state(self):
        # passive UDF gain
        total_credits_per_second = 0
        self.total_udf_gathered += self.get_udf_per_second()
        # passive credit gain
        total_credits_per_second += self.get_credits_per_second()

        # influence buildup (non-destructive)
        for node in self.nodes:
            if not node.is_compromised:
                continue

            for neighbor in self.nodes:
                if neighbor.id in node.neighbors and not neighbor.is_compromised:
                    neighbor.influence_build_up += node.influence_emit
                    if neighbor.influence_build_up > neighbor.base_unlock_cost:
                        neighbor.influence_build_up = neighbor.base_unlock_cost
        return total_credits_per_second


    # -------------------------
    # Economic actions
    # -------------------------
    def confirm_node_purchase(self, node, player):
        return self.compromise_node(node, player)

    def compromise_node(self, node, player):
        # eligibility:
        # - entry points can be bought anytime
        # - normal nodes must be unlocked via adjacency
        if not node.is_entry_point and not node.is_unlocked:
            return False

        # calculate effective cost
        effective_cost = node.base_unlock_cost - node.influence_build_up
        if effective_cost < 0:
            effective_cost = 0

        # first entry uses credits
        if node.is_entry_point and not self.is_network_entered:
            if player.currency["credits"] < effective_cost:
                return False

            player.currency["credits"] -= effective_cost
            self.is_network_entered = True

        # all other cases use UDF
        else:
            if self.total_udf_gathered < effective_cost:
                return False

            self.total_udf_gathered -= effective_cost

        # commit compromise
        if not node.compromise():
            return False

        # unlock neighbors
        for neighbor in self.nodes:
            if neighbor.id in node.neighbors and neighbor.is_locked:
                neighbor.unlock()

        # completion check
        if node.is_core:
            self.is_active = False
            self.is_complete = True

        return True

    def handle_click(self, mx, my, player):
        """
        Resolves a mouse click into a gameplay action.
        Returns an action dict for the UI layer.
        """

        node = self.get_clicked_node(mx, my)
        if node is None:
            return {"action": "none"}

        # -------------------------
        # Case 1: Compromised node
        # -------------------------
        if node.is_compromised:
            udf_gain = node.udf_per_click
            credit_gain = node.credits_per_click

            # UDF stays inside the corp network
            self.total_udf_gathered += udf_gain

            # credits go to player
            if credit_gain > 0:
                player.currency["credits"] += credit_gain

            return {
                "action": "harvest",
                "node": node,
                "udf_gained": udf_gain,
                "credits_gained": credit_gain,
            }

        # -------------------------
        # Case 2: Unlocked but not owned
        # -------------------------
        if node.is_unlocked or node.is_entry_point:
            effective_cost = node.base_unlock_cost - node.influence_build_up
            if effective_cost < 0:
                effective_cost = 0

            return {
                "action": "confirm_purchase",
                "node": node,
                "cost": effective_cost,
                "uses_credits": node.is_entry_point and not self.is_network_entered,

            }

        # -------------------------
        # Case 3: Locked node
        # -------------------------
        return {"action": "locked"}

