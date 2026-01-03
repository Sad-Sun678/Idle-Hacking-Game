import pygame

from Classes.game_class import Game
from Classes.nodes import Node, CorporationNetwork
from Classes.player import Player
from Classes.ui_classes import ConfirmPopup, Tooltip
from Classes.camera import Camera
pygame.init()

# -------------------------
# Window
# -------------------------
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Network Prototype (Branching Test)")

clock = pygame.time.Clock()
camera = Camera()
# -------------------------
# Player
# -------------------------
player = Player(
    click_power=1,
    click_per_second=0,
    currency={"credits": 150}
)

# -------------------------
# Branching test network (with suspicion tuning)
# -------------------------

nodes = [
    Node(
        1, "corp_core", (700, 400), 28, [2,5,3,4],
        network_suspicion_base_value=30,
        base_unlock_cost=120,
        udf_per_click=8,
        udf_per_second=12,
        credits_per_second=10,
        influence_emit=0,
        is_core=True
    ),

    Node(
        2, "access_router", (600, 400), 14, [1,5,4,7,9],
        network_suspicion_base_value=6,
        base_unlock_cost=18,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=.02
    ),
    Node(
        3, "access_router", (800, 400), 14, [1,5,4,6,8],
        network_suspicion_base_value=6,
        base_unlock_cost=18,
        udf_per_click=2,
        udf_per_second=1,
        influence_emit=.02
    ),
    Node(
        4, "relay_switch", (700, 500), 14, [1,2,3,8,9],
        network_suspicion_base_value=7,
        base_unlock_cost=22,
        udf_per_click=2,
        udf_per_second=2,
        influence_emit=.02
    ),
    Node(
        5, "relay_switch", (700, 300), 14, [3,2,1,7,6],
        network_suspicion_base_value=7,
        base_unlock_cost=22,
        udf_per_click=2,
        udf_per_second=2,
        influence_emit=.02
    ),

    Node(
        6, "data_cache", (900, 200), 14, [10,13,3,8],
        network_suspicion_base_value=9,
        base_unlock_cost=30,
        udf_per_click=3,
        udf_per_second=2,
        credits_per_second=1,
        influence_emit=.03
    ),
    Node(
        7, "data_cache", (500, 200), 14, [5,2,11,12,9],
        network_suspicion_base_value=9,
        base_unlock_cost=30,
        udf_per_click=3,
        udf_per_second=2,
        credits_per_second=1,
        influence_emit=.03
    ),

    Node(
        8, "market_node", (900, 600), 14, [10,4,3,6,14],
        network_suspicion_base_value=11,
        base_unlock_cost=40,
        udf_per_click=2,
        udf_per_second=3,
        credits_per_second=3,
        influence_emit=.03
    ),
    Node(
        9, "market_node", (500, 600), 14, [2,4,14,7,11],
        network_suspicion_base_value=11,
        base_unlock_cost=40,
        udf_per_click=2,
        udf_per_second=3,
        credits_per_second=3,
        influence_emit=.03
    ),

    Node(
        10, "security_hub", (1100, 400), 14, [6,8],
        network_suspicion_base_value=14,
        base_unlock_cost=55,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=.04
    ),
    Node(
        11, "security_hub", (300, 400), 14, [7,9],
        network_suspicion_base_value=14,
        base_unlock_cost=55,
        udf_per_click=3,
        udf_per_second=4,
        influence_emit=.04
    ),


    Node(
        12, "external_gateway", (100, 200), 14, [7],
        network_suspicion_base_value=4,
        base_unlock_cost=8,
        udf_per_click=1,
        influence_emit=.01,
        is_entry_point=True
    ),
    Node(
        13, "external_gateway", (1300, 200), 14, [6],
        network_suspicion_base_value=4,
        base_unlock_cost=8,
        udf_per_click=1,
        influence_emit=.01,
        is_entry_point=True
    ),

    Node(
        14, "logistics_node", (700, 800), 14, [9,8],
        network_suspicion_base_value=10,
        base_unlock_cost=35,
        udf_per_click=2,
        udf_per_second=2,
        credits_per_second=2,
        influence_emit=.03
    ),
]





corp = CorporationNetwork(
    corp_id="MegaCorp",
    nodes=nodes,
    difficulty=3,
    total_udf_gathered=1000,
    total_heat=0
)

blue_alert_popup = ConfirmPopup(
    rect=(400, 200, 300, 140),
    on_confirm=lambda: blue_alert_popup.close(),
    on_cancel=lambda: blue_alert_popup.close()
)


game = Game(player, [corp])
game.blue_alert_popup = blue_alert_popup

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
    "blue_team": (220, 60, 60),
}

BLUE_ALERT_TEXT = [
    "⚠ BLUE TEAM DEPLOYED ⚠",
    "",
    "Network defenses are responding.",
    "Expect node reclamation."
]

font = pygame.font.SysFont("arial", 18)

def lerp(a, b, t):
    return a + (b - a) * t

def draw_network(screen, corp, camera, active_signals):
    # -------- DRAW EDGES --------
    for node in corp.nodes:
        for neighbor_id in node.neighbors:
            other = corp.get_node_by_id(neighbor_id)
            color = (100, 50, 50) if node.is_compromised else (50, 50, 50)

            pygame.draw.line(
                screen,
                color,
                camera.apply(node.pos),
                camera.apply(other.pos),
                2
            )

    # -------- DRAW NODES --------
    for node in corp.nodes:
        color = NODE_COLORS[node.state]

        if corp.blue_team.active and corp.blue_team.occupies(node.id):
            color = NODE_COLORS["blue_team"]

        pygame.draw.circle(
            screen,
            color,
            camera.apply(node.pos),
            node.radius_size
        )

        # Debug telegraph
        if corp.blue_team.active and corp.blue_team.next_target == node.id:
            pygame.draw.circle(
                screen,
                (240, 200, 40),
                camera.apply(node.pos),
                node.radius_size + 6,
                2
            )

    # -------- DRAW SIGNALS (LAST so they show up) --------
    for s in active_signals:
        sx, sy = s["start"]
        ex, ey = s["end"]

        x = sx + (ex - sx) * s["t"]
        y = sy + (ey - sy) * s["t"]

        pygame.draw.circle(
            screen,
            (255, 240, 180),
            camera.apply((x, y)),
            4
        )



        # Debug telegraph
        if corp.blue_team.active and corp.blue_team.next_target == node.id:
            pygame.draw.circle(
                screen,
                (240, 200, 40),
                camera.apply(node.pos),
                node.radius_size + 6,
                2
            )

def update_signals(active_signals, dt):
    for s in active_signals[:]:
        s["t"] += s["speed"] * dt
        if s["t"] >= 1.0:
            active_signals.remove(s)


def draw_hover_outline(screen, node, camera):
    if not node:
        return

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        camera.apply(node.pos),
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
        f"Influence: {node.influence_build_up}/{node.base_unlock_cost}",
        f"ID: {node.id}",
        f"Neighbors {node.neighbors}"


    ]

# -------------------------
# Main loop
# -------------------------
running = True

while running:
    dt = clock.tick(60) / 1000.0

    # update camera first
    camera.update(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            world_mx, world_my = camera.to_world((mx, my))
            print(f"mx, my:{mx,my}, world my,my {world_mx,world_my}")

            if not popup.visible:
                game.handle_mouse_click(world_mx, world_my)

                if (
                    game.last_action
                    and game.last_action.get("action") == "confirm_purchase"
                ):
                    popup.open()

        popup.handle_event(event)
        blue_alert_popup.handle_event(event)

    # hover detection uses world coordinates
    mx, my = pygame.mouse.get_pos()
    world_mx, world_my = camera.to_world((mx, my))
    game.update_hover(world_mx, world_my)

    # advance simulation
    game.update(dt)
    # advance signal pulses
    update_signals(game.active_signals, dt)

    # -------------------------
    # Draw
    # -------------------------
    screen.fill((10, 10, 10))

    draw_network(screen, corp, camera,game.active_signals)
    draw_hover_outline(screen, game.hovered_node, camera)

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

    blue_alert_popup.draw(screen, BLUE_ALERT_TEXT)

    # UI text (screen space, no camera)
    screen.blit(
        font.render(f"Credits: {player.currency['credits']}", True, (220, 220, 220)),
        (20, 20)
    )
    screen.blit(
        font.render(f"UDF: {corp.total_udf_gathered}", True, (220, 220, 220)),
        (20, 45)
    )
    screen.blit(
        font.render(
            f"Network suspicion: {corp.network_suspicion}",
            True,
            (220, 220, 220)
        ),
        (20, 65)
    )

    pygame.display.flip()

pygame.quit()

