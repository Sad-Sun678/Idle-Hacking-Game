class Game:
    def __init__(self, player, active_corps):
        self.player = player
        self.active_corps = active_corps

        self.last_action = None
        self.hovered_node = None

        self.time_accumulator = 0.0
        self.active_signals = []
        # NEW
        self.prev_blue_active = False

    # -------------------------
    # Network ticking
    # -------------------------

    def advance_active_corps_networks(self):
        for corp in self.active_corps:
            credits_gained = corp.advance_network_state()
            if credits_gained:
                self.player.currency["credits"] += credits_gained

    # -------------------------
    # Input routing
    # -------------------------

    def handle_mouse_click(self, mx, my):
        if not self.active_corps:
            return

        corp = self.active_corps[0]  # single active corp for now
        self.last_action = corp.handle_click(mx, my, self.player)

    def confirm_purchase(self):
        if not self.last_action:
            return False

        if self.last_action.get("action") != "confirm_purchase":
            return False

        corp = self.active_corps[0]
        node = self.last_action["node"]

        compromised = corp.confirm_node_purchase(node, self.player)

        # Spawn pulses only if the purchase actually compromised the node
        if compromised:
            # "compromised" should be the node object if you changed corp.compromise_node to `return node`
            source = compromised if compromised is not True else node

            for neighbor_id in source.neighbors:
                other = corp.get_node_by_id(neighbor_id)

                self.active_signals.append({
                    "origin_id": source.id,
                    "target_id": other.id,
                    "start": source.pos,
                    "end": other.pos,
                    "t": 0.0,
                    "speed": .7
                })

        # clear action after resolution
        self.last_action = None
        return bool(compromised)

    # -------------------------
    # Hover / tooltip support
    # -------------------------

    def update_hover(self, mx, my):
        if not self.active_corps:
            self.hovered_node = None
            return

        corp = self.active_corps[0]
        self.hovered_node = corp.get_hovered_node(mx, my)

    # -------------------------
    # Main update hook
    # -------------------------

    def update(self, dt_seconds):
        self.time_accumulator += dt_seconds

        while self.time_accumulator >= 1.0:
            self.advance_active_corps_networks()

            # single active corp for now
            corp = self.active_corps[0]

            # detect inactive -> active transition
            if corp.blue_team.active and not self.prev_blue_active:
                # trigger popup here
                self.on_blue_team_activated()

            self.prev_blue_active = corp.blue_team.active
            self.time_accumulator -= 1.0

    def on_blue_team_activated(self):
        self.blue_alert_popup.open()
