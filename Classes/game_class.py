class Game:
    def __init__(self, player, active_corps):
        self.player = player
        self.active_corps = active_corps

        self.last_action = None
        self.hovered_node = None

        self.time_accumulator = 0.0

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

        success = corp.confirm_node_purchase(node, self.player)

        # clear action after resolution
        self.last_action = None
        return success

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
        """
        dt_seconds: elapsed time since last frame (float)
        """
        self.time_accumulator += dt_seconds

        # allow for catch-up if frame stutters
        while self.time_accumulator >= 1.0:
            self.advance_active_corps_networks()
            self.time_accumulator -= 1.0
