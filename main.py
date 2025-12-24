import pygame

from Classes.game_class import Game
from Classes.nodes import Node, CorporationNetwork
from Classes.player import Player
from Classes.ui_classes import ConfirmPopup, Tooltip

pygame.init()

# -------------------------
# Window
# -------------------------
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Network Prototype (Branching Test)")

clock = pygame.time.Clock()

# -------------------------
# Player
# -------------------------
player = Player(
    click_power=1,
    click_per_second=0,
    currency={"credits": 150}
)

# -------------------------
# Branching test network
# -------------------------
nodes = [
    # =========================================================
    # ENTRY RING
    # =========================================================
    Node(
        1, "edge_terminal", (250, 350), 14, [2, 3, 4],
        base_unlock_cost=5,
        udf_per_click=1,
        influence_emit=1,
        is_entry_point=True
    ),
    Node(
        2, "edge_terminal", (250, 550), 14, [1, 3, 4],
        base_unlock_cost=5,
        udf_per_click=1,
        influence_emit=1,
        is_entry_point=True
    ),
    Node(
        3, "kiosk_net", (400, 300), 16, [1, 2, 5, 7],
        base_unlock_cost=10,
        udf_per_click=1,
        udf_per_second=1,
        influence_emit=1
    ),
    Node(
        4, "kiosk_net", (400, 600), 16, [1, 2, 6, 8],
        base_unlock_cost=10,
        udf_per_click=1,
        udf_per_second=1,
        influence_emit=1
    ),

    # =========================================================
    # EARLY MID
    # =========================================================
    Node(
        5, "datavault", (550, 220), 18, [3, 7, 9],
        base_unlock_cost=20,
        udf_per_click=2,
        udf_per_second=2,
        influence_emit=2
    ),
    Node(
        6, "datavault", (550, 680), 18, [4, 8, 10],
        base_unlock_cost=20,
        udf_per_click=2,
        udf_per_second=2,
        influence_emit=2
    ),
    Node(
        7, "credit_forge", (550, 380), 18, [3, 5, 9, 11],
        base_unlock_cost=25,
        udf_per_click=1,
        udf_per_second=2,
        credits_per_second=2,
        influence_emit=2
    ),
    Node(
        8, "credit_forge", (550, 520), 18, [4, 6, 10, 12],
        base_unlock_cost=25,
        udf_per_click=1,
        udf_per_second=2,
        credits_per_second=2,
        influence_emit=2
    ),

    # =========================================================
    # LATERAL / UTILITY SPINE
    # =========================================================
    Node(
        9, "proxy_cache", (700, 300), 16, [5, 7, 11, 13],
        base_unlock_cost=30,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=3
    ),
    Node(
        10, "proxy_cache", (700, 600), 16, [6, 8, 12, 14],
        base_unlock_cost=30,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=3
    ),
    Node(
        11, "market_ai", (850, 240), 18, [7, 9, 13, 15],
        base_unlock_cost=35,
        udf_per_click=2,
        udf_per_second=2,
        credits_per_second=3,
        influence_emit=3
    ),
    Node(
        12, "market_ai", (850, 660), 18, [8, 10, 14, 16],
        base_unlock_cost=35,
        udf_per_click=2,
        udf_per_second=2,
        credits_per_second=3,
        influence_emit=3
    ),

    # =========================================================
    # HIGH-TIER CHOKE CLUSTERS
    # =========================================================
    Node(
        13, "cloud_spire", (1000, 180), 20, [9, 11, 15, 17],
        base_unlock_cost=45,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=4
    ),
    Node(
        14, "neurogrid", (1000, 720), 20, [10, 12, 16, 17],
        base_unlock_cost=45,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=4
    ),
    Node(
        15, "cloud_spire", (1000, 380), 20, [11, 13, 17],
        base_unlock_cost=45,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=4
    ),
    Node(
        16, "neurogrid", (1000, 520), 20, [12, 14, 17],
        base_unlock_cost=45,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=4
    ),

    # =========================================================
    # DEEP CORE APPROACH
    # =========================================================
    Node(
        17, "identity_forge", (1150, 450), 18,
        [13, 14, 15, 16, 18],
        base_unlock_cost=55,
        udf_per_click=3,
        udf_per_second=3,
        influence_emit=4
    ),
    Node(
        18, "black_db", (1300, 450), 20,
        [17, 19],
        base_unlock_cost=65,
        udf_per_click=4,
        udf_per_second=4,
        influence_emit=5
    ),

    # =========================================================
    # CORE
    # =========================================================
    Node(
        19, "corp_core", (1450, 450), 28,
        [18],
        base_unlock_cost=90,
        udf_per_click=7,
        udf_per_second=10,
        credits_per_second=8,
        influence_emit=6,
        is_core=True
    ),
]

corp = CorporationNetwork(
    corp_id="MegaCorp",
    nodes=nodes,
    difficulty=3,
    total_udf_gathered=0,
    total_heat=0
)



game = Game(player, [corp])

# -------------------------
# Debug helpers
# -------------------------
DEBUG = True

def dbg(*args):
    if DEBUG:
        print("[DBG]", *args)

def node_summary(n):
    if n is None:
        return "None"
    return (
        f"id={n.id} type={n.node_type} state={n.state} "
        f"entry={getattr(n,'is_entry_point',False)} core={n.is_core}"
    )

# -------------------------
# UI
# -------------------------
tooltip = Tooltip()

def debug_confirm_wrapper():
    dbg("CONFIRM CLICKED (YES)")
    dbg("Before:", player.currency, "UDF:", corp.total_udf_gathered)

    ok = game.confirm_purchase()

    dbg("confirm_purchase ->", ok)
    dbg("After:", player.currency, "UDF:", corp.total_udf_gathered)

    popup.close()

def debug_cancel_wrapper():
    dbg("CANCEL CLICKED (NO)")
    popup.close()

popup = ConfirmPopup(
    rect=(550, 320, 300, 160),
    on_confirm=debug_confirm_wrapper,
    on_cancel=debug_cancel_wrapper
)

# -------------------------
# Render helpers
# -------------------------
NODE_COLORS = {
    "locked": (60, 60, 60),
    "unlocked": (80, 140, 220),
    "compromised": (0, 220, 140),
}

font = pygame.font.SysFont("arial", 18)

def draw_network(screen, corp):
    for node in corp.nodes:
        for other in corp.nodes:
            if other.id in node.neighbors:
                pygame.draw.line(screen, (50, 50, 50), node.pos, other.pos, 2)

    for node in corp.nodes:
        pygame.draw.circle(
            screen,
            NODE_COLORS[node.state],
            node.pos,
            node.radius_size
        )

def draw_hover_outline(screen, node):
    if node:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            node.pos,
            node.radius_size + 3,
            2
        )

def tooltip_lines(node):
    if not node:
        return []

    cost = max(0, node.base_unlock_cost - node.influence_build_up)

    return [
        node.node_type,
        f"State: {node.state}",
        f"Cost: {cost}",
        f"UDF/sec: {node.udf_per_second}",
        f"UDF/click: {node.udf_per_click}",
        f"Credits/sec: {node.credits_per_second}",
        f"Influence: {node.influence_build_up}/{node.base_unlock_cost}"

    ]

# -------------------------
# Main loop
# -------------------------
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()

            if not popup.visible:
                game.handle_mouse_click(mx, my)

                if (
                    game.last_action
                    and game.last_action.get("action") == "confirm_purchase"
                ):
                    popup.open()

        popup.handle_event(event)

    mx, my = pygame.mouse.get_pos()
    game.update_hover(mx, my)
    game.update(dt)

    # -------------------------
    # Draw
    # -------------------------
    screen.fill((10, 10, 10))

    draw_network(screen, corp)
    draw_hover_outline(screen, game.hovered_node)

    tooltip.draw(screen, mx, my, tooltip_lines(game.hovered_node))

    popup.draw(
        screen,
        (
            ["Compromise node?"]
            + (
                [f"Cost: {game.last_action['cost']}"]
                if game.last_action
                and game.last_action.get("action") == "confirm_purchase"
                else []
            )
        )
    )

    screen.blit(
        font.render(f"Credits: {player.currency['credits']}", True, (220, 220, 220)),
        (20, 20)
    )
    screen.blit(
        font.render(f"UDF: {corp.total_udf_gathered}", True, (220, 220, 220)),
        (20, 45)
    )

    pygame.display.flip()

pygame.quit()
