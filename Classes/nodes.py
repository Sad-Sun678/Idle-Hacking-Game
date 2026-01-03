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
            network_suspicion_decay_rate=.2,
            network_suspicion_base_value=5,
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
        self.network_suspicion_decay_rate = network_suspicion_decay_rate
        self.network_suspicion_base_value = network_suspicion_base_value
        self.active_network_suspicion = 0
        self.cooldown_timer = 60
        self.is_anchored = False
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
        """Sets state to compromised and sets active blue pressure to the base val"""
        if self.state not in ("unlocked", "locked"):
            return False
        self.state = "compromised"
        self.active_network_suspicion = self.network_suspicion_base_value
        return True

    def decay_heat(self):
        if self.state == "compromised":
            self.active_network_suspicion = max(
                0,
                self.active_network_suspicion - self.network_suspicion_decay_rate
            )


class CorporationNetwork:
    def __init__(self, corp_id, nodes, difficulty, total_udf_gathered, total_heat):
        self.corp_id = corp_id
        self.nodes = nodes
        self.difficulty = difficulty
        self.network_suspicion = 0
        self.blue_threshold = 200

        # local, per-corp resources
        self.total_udf_gathered = total_udf_gathered
        self.total_heat = total_heat

        self.is_active = False
        self.is_complete = False
        self.is_network_entered = False

        self.blue_team = BlueTeam(self)
        self.blue_active = False

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

    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_neighbors(self, node):
        return [
            other
            for other in self.nodes
            if other.id in node.neighbors
        ]

    def distance_to_nearest_compromised(self, start_node):
        visited = set()
        queue = [(start_node, 0)]

        while queue:
            node, dist = queue.pop(0)
            if node.id in visited:
                continue

            visited.add(node.id)

            if node.is_compromised:
                return dist

            for neighbor in self.get_neighbors(node):
                if neighbor.id not in visited:
                    queue.append((neighbor, dist + 1))

        return None  # no compromised nodes reachable

    def distance_to_core(self, start_node):
        visited = set()
        queue = [(start_node, 0)]

        while queue:
            node, dist = queue.pop(0)
            if node.id in visited:
                continue

            visited.add(node.id)

            if node.is_core:
                return dist

            for neighbor in self.get_neighbors(node):
                if neighbor.id not in visited:
                    queue.append((neighbor, dist + 1))

        return None

    def distance_between(self, start_node, target_node):
        """
        BFS distance from start_node to target_node.
        """
        visited = set()
        queue = [(start_node, 0)]

        while queue:
            node, dist = queue.pop(0)

            if node.id == target_node.id:
                return dist

            if node.id in visited:
                continue

            visited.add(node.id)

            for neighbor in self.get_neighbors(node):
                if neighbor.id not in visited:
                    queue.append((neighbor, dist + 1))

        return None

    # -------------------------
    # Network tick
    # -------------------------

    def advance_network_state(self):
        # passive UDF gain
        total_credits_per_second = 0
        self.total_udf_gathered += self.get_udf_per_second()

        # passive credit gain
        total_credits_per_second += self.get_credits_per_second()

        # network suspicion accumulation + decay
        for node in self.nodes:
            if node.is_compromised:
                self.network_suspicion += node.active_network_suspicion
                self.network_suspicion -= node.network_suspicion_decay_rate
                self.network_suspicion = max(0, self.network_suspicion)
                node.decay_heat()

        # influence buildup (non-destructive)
        for node in self.nodes:
            if not node.is_compromised:
                continue

            for neighbor in self.nodes:
                if neighbor.id in node.neighbors and not neighbor.is_compromised:
                    neighbor.influence_build_up += node.influence_emit
                    if neighbor.influence_build_up > neighbor.base_unlock_cost:
                        neighbor.influence_build_up = neighbor.base_unlock_cost

        # blue team activation & behavior
        if self.network_suspicion >= self.blue_threshold:
            self.blue_team.activate()
        else:
            self.blue_team.deactivate()

        self.blue_team.tick()

        return total_credits_per_second

    # -------------------------
    # Economic actions
    # -------------------------
    def confirm_node_purchase(self, node, player):
        return self.compromise_node(node, player)

    def compromise_node(self, node, player):
        # eligibility
        if not node.is_entry_point and not node.is_unlocked:
            return False

        effective_cost = max(0, node.base_unlock_cost - node.influence_build_up)

        if node.is_entry_point and not self.is_network_entered:
            if player.currency["credits"] < effective_cost:
                return False
            player.currency["credits"] -= effective_cost
            self.is_network_entered = True
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

        return node

    def relock_neighbors_if_needed(self, reclaimed_node):
        for neighbor in self.nodes:
            if neighbor.id not in reclaimed_node.neighbors:
                continue

            # never relock entry points
            if neighbor.is_entry_point:
                continue

            # never relock compromised nodes
            if neighbor.is_compromised:
                continue

            # check if ANY compromised neighbor still unlocks it
            still_supported = False
            for other in self.nodes:
                if (
                        other.is_compromised
                        and neighbor.id in other.neighbors
                ):
                    still_supported = True
                    break

            if still_supported:
                neighbor.state = "unlocked"
            else:
                neighbor.state = "locked"

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

class BlueTeam:
    def __init__(self, network):
        self.network = network

        # activation
        self.active = False

        # spatial state (SINGLE position model)
        self.frontier = set()          # always 0 or 1 node id
        self.moving_to = None          # (node_id, ticks_remaining) or None
        self.reclaiming = None         # (node_id, ticks_remaining) or None
        self.next_target = None        # node_id or None (debug / telegraph)

        # timing
        self.tick_timer = 0
        self.tick_interval = 1
        self.move_time = 2
        self.reclaim_time = 4

    # -------------------------
    # Activation control
    # -------------------------

    def activate(self):
        if self.active:
            return
        self.active = True
        self.spawn_at_core()

    def deactivate(self):
        self.active = False
        self.frontier.clear()
        self.moving_to = None
        self.reclaiming = None
        self.next_target = None

    def spawn_at_core(self):
        for node in self.network.nodes:
            if node.is_core:
                self.frontier = {node.id}
                break

    # -------------------------
    # Tick entry point
    # -------------------------

    def tick(self):
        if not self.active:
            return

        # safety: if we ever got activated but have no position, respawn
        if not self.frontier:
            self.spawn_at_core()

        # run logic once per tick
        self.tick_timer += 1
        if self.tick_timer < self.tick_interval:
            return
        self.tick_timer = 0

        core_threat = self._core_under_threat()

        # core under threat → faster response (but DO NOT cancel active actions)
        if core_threat:
            self.move_time = 1
            self.reclaim_time = 2
        else:
            self.move_time = 2
            self.reclaim_time = 4

        # --- HARD STATE GATING ---
        # if we're reclaiming, keep reclaiming until done
        if self.reclaiming:
            self._advance_reclaim()
            return

        # if we're moving, keep moving until we arrive
        if self.moving_to:
            self._advance_movement()
            return

        # idle → decide next move
        self._choose_next_move()

    # -------------------------
    # State queries
    # -------------------------

    def occupies(self, node_id):
        return node_id in self.frontier

    # -------------------------
    # Movement logic
    # -------------------------
    def _score_compromised_node(self, node):
        """
        Higher score = higher priority to reclaim
        """
        score = 0

        dist_to_core = self.network.distance_to_core(node)
        if dist_to_core is not None:
            # closer to core = more dangerous
            score += max(0, 10 - dist_to_core) * 10

        # nodes that generate more suspicion matter more
        score += node.network_suspicion_base_value

        return score

    def _closest_compromised_neighbor(self, current_node):
        best = None
        best_dist = None

        for neighbor in self.network.get_neighbors(current_node):
            if neighbor.is_compromised:
                return neighbor  # immediate reclaim opportunity

            dist = self.network.distance_to_nearest_compromised(neighbor)
            if dist is None:
                continue

            if best_dist is None or dist < best_dist:
                best_dist = dist
                best = neighbor

        return best

    def _choose_next_move(self):
        current_id = next(iter(self.frontier))
        current_node = self.network.get_node_by_id(current_id)

        # --- find highest-value compromised node ---
        compromised = [
            n for n in self.network.nodes
            if n.is_compromised
        ]

        if not compromised:
            return

        target = max(compromised, key=self._score_compromised_node)

        # --- move one step toward *that specific target* ---
        best_neighbor = None
        best_distance = None
        fallback_neighbor = None

        current_dist = self.network.distance_between(current_node, target)

        for neighbor in self.network.get_neighbors(current_node):
            dist = self.network.distance_between(neighbor, target)

            # unreachable via this neighbor
            if dist is None:
                continue

            # remember *any* legal move as a deadlock escape
            if fallback_neighbor is None:
                fallback_neighbor = neighbor

            # when core is threatened, avoid moves that get strictly worse
            if (
                    self._core_under_threat()
                    and current_dist is not None
                    and dist > current_dist
            ):
                continue

            if best_distance is None or dist < best_distance:
                best_distance = dist
                best_neighbor = neighbor

        # preferred move
        if best_neighbor:
            self.next_target = best_neighbor.id
            self.moving_to = (best_neighbor.id, self.move_time)
            return

        # --- DEADLOCK ESCAPE ---
        # If optimal progress is impossible, move anyway to restore connectivity
        if fallback_neighbor:
            self.next_target = fallback_neighbor.id
            self.moving_to = (fallback_neighbor.id, self.move_time)

    def _core_under_threat(self):
        for node in self.network.nodes:
            if node.is_compromised:
                dist = self.network.distance_to_core(node)
                if dist is not None and dist <= 1:
                    return True
        return False

    def _advance_movement(self):
        target_id, ticks_left = self.moving_to
        ticks_left -= 1

        if ticks_left > 0:
            self.moving_to = (target_id, ticks_left)
            return

        # arrive
        self.moving_to = None
        self.frontier = {target_id}
        self.next_target = None

        node = self.network.get_node_by_id(target_id)
        if node.is_compromised:
            self.reclaiming = (target_id, self.reclaim_time)

    # -------------------------
    # Reclaim logic
    # -------------------------

    def _advance_reclaim(self):
        node_id, ticks_left = self.reclaiming
        ticks_left -= 1

        if ticks_left > 0:
            self.reclaiming = (node_id, ticks_left)
            return

        node = self.network.get_node_by_id(node_id)
        self._finish_reclaim(node)
        self.reclaiming = None

    def _finish_reclaim(self, node):
        if node.is_anchored:
            node.state = "unlocked"
            node.cooldown_timer = 60
        else:
            node.state = "locked"

        node.active_network_suspicion = 0
        self.network.relock_neighbors_if_needed(node)
