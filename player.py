class Player:
    def __init__(self, name="player", max_hp=5, current_hp=5, attack_range=2, max_energy=4, current_energy = 4, selected=False, cards=None,
                 equipments=None):
        if equipments is None:
            equipments = []
        if cards is None:
            cards = []
        self.name = name
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.attack_range = attack_range
        self.max_energy = max_energy
        self.cards = cards
        self.equipments = equipments
        self.selected = selected
        self.current_energy = current_energy