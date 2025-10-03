from scenes import SCENE_MAP, SCENES

class Player:
    def __init__(self):
        self.current_scene = "forest"
        self.game_over = False

        # Item flags
        self.has_key = False
        self.has_boots = False
        self.has_scroll = False
        self.has_seal = False

        # Usage flags
        self.boots_used = False
        self.chest_unlocked = False
        self.scroll_used = False
        self.seal_used = False

        # Dialogue flags
        self.talked_to_ruins = False
        self.talked_to_lake = False

        # Inventory selection
        self.inventory_index = 0

    def to_dict(self, message="", msg_type="neutral"):
        items = self.get_inventory()
        scene_data = SCENES[self.current_scene]

        # --- Description variants ---
        description = scene_data.get("description")
        if self.current_scene == "forest" and self.has_key:
            description = scene_data.get("description_key", description)
        if self.current_scene == "cave" and self.scroll_used:
            description = scene_data.get("description_scroll", description)
        if self.current_scene == "city" and self.seal_used:
            description = scene_data.get("description_seal", description)

        # --- Image variants ---
        image = scene_data.get("image")
        if self.current_scene == "forest":
            image = "/static/assets/forest.png" if self.has_key else "/static/assets/forest_with_key.png"
        elif self.current_scene == "mountain":
            image = "/static/assets/mountain.png" if self.has_boots else "/static/assets/mountain_with_boots.png"
        elif self.current_scene == "cave":
            image = "/static/assets/cave_unlocked.png" if self.scroll_used else "/static/assets/cave_locked.png"
        elif self.current_scene == "city":
            image = "/static/assets/city_open.png" if self.seal_used else "/static/assets/city_closed.png"

        return {
            "message": message,
            "type": msg_type,
            "scene": self.current_scene,
            "description": description,
            "inventory": items,
            "selected": items[self.inventory_index] if items else None,
            "game_over": self.game_over,
            "seal_used": self.seal_used,
            "image": image
        }


    # --- Actions ---
    def move(self, direction):
        if self.seal_used and self.current_scene == "city":
            return self.to_dict("The seal has awakened. Your journey ends...", "end")

        next_scene = SCENE_MAP.get((self.current_scene, direction))
        if next_scene == "city" and not self.boots_used:
            return self.to_dict("You need to use boots before climbing to the city.", "feedback")
        if next_scene:
            self.current_scene = next_scene
            return self.to_dict(f"You moved {direction} to {next_scene}.", "neutral")
        return self.to_dict("Can't go that way.", "feedback")

    def grab(self):
        if self.current_scene == "forest" and not self.has_key:
            self.has_key = True
            return self.to_dict("You picked up a shiny key.", "feedback")
        elif self.current_scene == "mountain" and not self.has_boots:
            self.has_boots = True
            return self.to_dict("You found sturdy boots buried in the snow.", "feedback")
        elif self.current_scene == "swamp" and not self.has_scroll:
            if not self.boots_used:
                return self.to_dict("You see something in the mud but can't reach it.", "feedback")
            elif self.boots_used and not self.talked_to_ruins:
                return self.to_dict("You need some magic... But where?", "feedback")
            elif self.boots_used and self.talked_to_ruins:
                self.has_scroll = True
                return self.to_dict("You found a damp scroll hidden beneath the roots.", "feedback")
        return self.to_dict("Nothing to grab here.", "neutral")

    def use(self):
        items = self.get_inventory()
        if not items:
            return self.to_dict("Inventory is empty.", "feedback")
        selected = items[self.inventory_index]

        if selected == "Boots" and not self.boots_used:
            self.boots_used = True
            return self.to_dict("You put on the boots. Ready to climb!", "feedback")
        elif selected == "Key" and self.current_scene == "cave" and not self.chest_unlocked:
            self.chest_unlocked = True
            self.has_seal = True
            return self.to_dict("Altar unlocked. You acquired the seal!", "feedback")
        elif selected == "Scroll" and self.current_scene == "cave" and self.has_seal and not self.scroll_used:
            self.scroll_used = True
            return self.to_dict("You read the scroll aloud. The seal pulses with power!", "feedback")
        elif selected == "Seal" and self.current_scene == "city":
            if self.talked_to_ruins and self.talked_to_lake and self.scroll_used:
                self.seal_used = True
                self.game_over = True
                return self.to_dict("Seal used. Light floods the streets. You win!", "end")
            else:
                return self.to_dict("The seal remains dormant. Something is missing...", "feedback")
        return self.to_dict(f"You can't use {selected} here.", "feedback")

    def talk(self):
        if self.current_scene == "lake":
            self.talked_to_lake = True
            return self.to_dict("Fisherman: The seal lies below.", "feedback")
        elif self.current_scene == "ruins":
            self.talked_to_ruins = True
            return self.to_dict("Echoes whisper: 'Seek the altar.'", "feedback")
        elif self.current_scene == "cave":
            return self.to_dict("You hear faint chants in stone.", "neutral")
        elif self.current_scene == "city" and not self.seal_used:
            return self.to_dict("Guard: Show the royal seal!", "feedback")
        elif self.current_scene == "city" and self.seal_used:
            return self.to_dict("Citizens cheer! Welcome hero!", "feedback")
        return self.to_dict("There's no one to talk to.", "neutral")

    def get_inventory(self):
        items = []
        if self.has_key: items.append("Key")
        if self.has_boots: items.append("Boots")
        if self.has_scroll: items.append("Scroll")
        if self.has_seal: items.append("Seal")
        return items

    def cycle_inventory(self, direction):
        items = self.get_inventory()
        if not items:
            return self.to_dict("Inventory is empty.", "feedback")
        if direction == "next":
            self.inventory_index = (self.inventory_index + 1) % len(items)
        elif direction == "prev":
            self.inventory_index = (self.inventory_index - 1 + len(items)) % len(items)
        return self.to_dict(f"Selected: {items[self.inventory_index]}", "feedback")
