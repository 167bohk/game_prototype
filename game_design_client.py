import random
from random import randint

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from card import Card
from player import Player

FILENAME = "cards.txt"


class GameDesignClient(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cards = []
        self.normal_card_pile = []
        self.normal_discard_pile = []
        self.premium_card_pile = []
        self.premium_discard_pile = []
        self.premium_cards = []
        self.total_premium_card_number = 0
        self.normal_cards = []
        self.total_normal_card_number = 0

        self.player1 = Player(name="player1")
        self.player2 = Player(name="player2")
        self.player3 = Player(name="player3")
        self.player4 = Player(name="player4")
        self.players = [self.player1, self.player2, self.player3, self.player4]

        with open(FILENAME, "r", encoding="utf-8", newline='') as in_file:
            in_file.readline()  # ignore headers
            lines = in_file.readlines()
            for line in lines:
                parts = line.strip().split("/")
                if parts != [""]:
                    print(parts)
                    parts[1] = parts[1].replace("\\n", "\n")
                    parts[2] = True if parts[2] == "p" else False
                    parts[3] = int(parts[3])
                    card = Card(parts[0], parts[1], parts[2], parts[3])
                    self.cards.append(card)
        for card in self.cards:
            if card.is_premium:
                self.premium_cards.append(card)
            else:
                self.normal_cards.append(card)
        for normal_card in self.normal_cards:
            self.total_normal_card_number += normal_card.number
            for i in range(1, normal_card.number + 1):
                self.normal_card_pile.append(Card(name=f"{normal_card.name}({i})", description=normal_card.description,
                                                  is_premium=normal_card.is_premium, number=1))
        for premium_card in self.premium_cards:
            self.total_premium_card_number += premium_card.number
            for i in range(1, premium_card.number + 1):
                self.premium_card_pile.append(
                    Card(name=(premium_card.name + str(i)), description=premium_card.description,
                         is_premium=premium_card.is_premium, number=1))
        self.display_card_pile()

    def display_card_pile(self, instance=None):
        print("Normal Cards: ")
        for normal_card in self.normal_cards:
            print(normal_card)
        print()
        print("Normal card pile: ")
        print([card.name for card in self.normal_card_pile])
        print("<---------------------------------------------------------->")
        print("Premium Cards: ")
        for premium_card in self.premium_cards:
            print(premium_card)
        print()
        print("Premium card pile: ")
        print([card.name for card in self.premium_card_pile])

    def build(self):
        self.title = "Game Prototype"
        self.root = Builder.load_file("game_design_client.kv")
        return self.root

    def draw_card(self, card_type):
        additional_prompt = ""
        color = (1, 1, 1, 1)
        if self.normal_card_pile == []:
            self.normal_card_pile[:], self.normal_discard_pile[:] = self.normal_discard_pile[:], self.normal_card_pile[
                                                                                                 :]
            additional_prompt = "Normal card pile has been reset!\n"
            color = (1, 0, 0, 1)

        if self.premium_card_pile == []:
            self.premium_card_pile[:], self.premium_discard_pile[:] = self.premium_discard_pile[
                                                                      :], self.premium_card_pile[:]
            additional_prompt = "Premium card pile has been reset!\n"
            color = (1, 0, 0, 1)

        try:
            selected_player = [player for player in self.players if player.selected][0]
            if card_type == "normal":
                random_index = random.randint(0, len(self.normal_card_pile) - 1)
                new_card = self.normal_card_pile.pop(random_index)
                selected_player.cards.append(new_card)
            else:
                # print(len(self.premium_card_pile) - 1)
                random_index = random.randint(0, len(self.premium_card_pile) - 1)
                new_card = self.premium_card_pile.pop(random_index)
                selected_player.cards.append(new_card)
            self.switch_player(selected_player.name)
            self.change_prompt(f"{additional_prompt}New card: {new_card.description}", color)

        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")
        except ValueError:
            self.change_prompt("No cards left to draw!")

    def switch_player(self, player_name="MENU"):
        self.change_prompt("")
        self.root.ids.cards.clear_widgets()
        self.root.ids.equipments.clear_widgets()
        self.root.ids.up_down.clear_widgets()
        for i, player in enumerate(self.players):
            player.selected = False
            self.players[i] = player
        for player in self.players:
            self.root.ids[player.name].clear_widgets()
            for card in player.equipments:
                if card.number == 114514:
                    button_text = card.name
                else:
                    button_text = ""
                temp_button = Button(font_name="fonts/msyh.ttc", text=button_text, color=(0.5, 1, 0, 1), font_size=20)
                self.root.ids[player.name].add_widget(temp_button)
        if player_name == "MENU":
            self.root.ids.statistics.text = f"Normal card pile: ({len(self.normal_card_pile)}/{self.total_normal_card_number})\nPremium card pile: ({len(self.premium_card_pile)}/{self.total_premium_card_number})"
            self.root.ids.statistics.color = (1, 1, 1, 1)
            temp_button = Button(font_name="fonts/msyh.ttc",
                                 text="Display Current Card Piles\n             (for DM only)", color=(1, 0, 0, 1),
                                 font_size=30)
            temp_button.bind(on_press=self.display_card_pile)
            self.root.ids.equipments.add_widget(temp_button)
            self.change_prompt("Switch to next player.")

        else:
            selected_player = [player for player in self.players if player.name == player_name][0]
            selected_player.selected = True
            self.root.ids.statistics.text = f"Name: {selected_player.name}\nMax HP:      {selected_player.max_hp}{selected_player.max_hp * "[]"}\nCurrent HP: {selected_player.current_hp}{selected_player.current_hp * "[]"}\nAttack Range: {selected_player.attack_range}\nMax Energy: {selected_player.max_energy}\nCurrent Energy: {selected_player.current_energy}"
            self.root.ids.statistics.color = tuple(self.root.ids[selected_player.name + "_button"].color)
            for card in selected_player.cards:
                if card.is_premium:
                    color = (0.9, 0, 0.9, 1)
                else:
                    color = (0, 1, 1, 1)
                temp_button = Button(font_name="fonts/msyh.ttc", text=f"{card.name}", font_size=30, color=color)
                temp_button.card = card
                temp_button.bind(on_press=self.discard_a_card)
                temp_button.player = selected_player
                self.root.ids.cards.add_widget(temp_button)

            for equipment in selected_player.equipments:
                temp_button = Button(font_name="fonts/msyh.ttc", text=equipment.name, color=(0.5, 1, 0, 1),
                                     font_size=30)
                temp_button.card = equipment
                temp_button.bind(on_press=self.discard_an_equipment)
                temp_button.player = selected_player
                self.root.ids.equipments.add_widget(temp_button)

            temp_up_button = Button(font_name="fonts/msyh.ttc", text="up", font_size=30)
            temp_down_button = Button(font_name="fonts/msyh.ttc", text="down", font_size=30)
            self.root.ids.up_down.add_widget(temp_up_button)
            self.root.ids.up_down.add_widget(temp_down_button)

    def change_prompt(self, prompt, color=(1, 1, 1, 1)):
        self.root.ids.output_prompt.color = color
        self.root.ids.output_prompt.text = prompt

    def discard_a_card(self, instance):
        selected_player = instance.player
        player_name = selected_player.name
        card_to_discard = instance.card
        card_to_discard.number = 1
        selected_player.cards.remove(card_to_discard)
        if card_to_discard.is_premium:
            self.premium_discard_pile.append(card_to_discard)
        else:
            self.normal_discard_pile.append(card_to_discard)
        self.switch_player(player_name)

    def activate_modify_model(self, name):
        try:
            selected_player = [player for player in self.players if player.selected][0]
            self.root.ids.up_down.clear_widgets()
            temp_up_button = Button(font_name="fonts/msyh.ttc", text=name, color=(0.5, 1, 0, 1), font_size=30)
            temp_up_button.bind(on_press=self.modify_statistic)

            temp_down_button = Button(font_name="fonts/msyh.ttc", text=name, color=(1, 0, 0, 1), font_size=30)
            temp_down_button.bind(on_press=self.modify_statistic)

            self.root.ids.up_down.add_widget(temp_up_button)
            self.root.ids.up_down.add_widget(temp_down_button)
            self.change_prompt(f"Modifying {name}, press green button to +1, press red button to -1.")
        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")

    def activate_steal(self):
        try:
            selected_player = [player for player in self.players if player.selected][0]
            self.root.ids.cards.clear_widgets()
            for player in self.players:
                if player.name != selected_player.name:
                    temp_button_hand = Button(font_name="fonts/msyh.ttc",
                                              text=f"{player.name}\n(hand){len(player.cards)}", font_size=30,
                                              color=tuple(self.root.ids[player.name + "_button"].color))
                    temp_button_hand.bind(on_press=self.steal_a_card)
                    temp_button_hand.selected_player = selected_player
                    temp_button_hand.victim_player = player
                    self.root.ids.cards.add_widget(temp_button_hand)
                    self.root.ids[player.name].clear_widgets()
                    for card in player.equipments:
                        if card.number == 114514:
                            button_text = card.name
                        else:
                            button_text = ""
                        temp_button = Button(font_name="fonts/msyh.ttc", text=button_text, color=(1, 0, 0, 1))
                        temp_button.card = card
                        temp_button.bind(on_press=self.steal_an_equipment)
                        self.root.ids[player.name].add_widget(temp_button)


        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")

    def steal_a_card(self, instance):
        selected_player = instance.selected_player
        victim_player = instance.victim_player
        if victim_player.cards == []:
            self.change_prompt("There's no card to steal!")
        else:
            random_card_index = randint(0, len(victim_player.cards) - 1)
            selected_player.cards.append(victim_player.cards.pop(random_card_index))
            self.switch_player(selected_player.name)

    def steal_an_equipment(self, instance):
        selected_player = [player for player in self.players if player.selected][0]
        equipment = instance.card
        victim_player = [player for player in self.players if equipment in player.equipments][0]
        equipment.number = 1
        victim_player.equipments.remove(equipment)
        selected_player.cards.append(equipment)
        self.switch_player(selected_player.name)

    def modify_statistic(self, instance):
        try:
            selected_player = [player for player in self.players if player.selected][0]
            if instance.text == "Reset Energy":
                selected_player.current_energy = selected_player.max_energy
            else:
                statistic_type = instance.text
                # print(instance.color)
                modify = 1 if instance.color == [0.5, 1, 0, 1] else -1
                setattr(selected_player, statistic_type, getattr(selected_player,
                                                                 statistic_type) + modify)  # can't use selected_player.statistic_type to get value
            self.switch_player(selected_player.name)
        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")

    def equip_item(self):
        self.change_prompt("")
        self.root.ids.cards.clear_widgets()
        try:
            selected_player = [player for player in self.players if player.selected][0]
            if selected_player.cards == []:
                self.change_prompt("You don't have any card :(")
            else:
                for card in selected_player.cards:
                    temp_button = Button(font_name="fonts/msyh.ttc", text=card.name, color=(1, 0, 0, 1), font_size=30)
                    temp_button.bind(on_press=self.move_card_to_equipment)
                    self.root.ids.cards.add_widget(temp_button)
                self.change_prompt("Equipment select model.")
        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")

    def move_card_to_equipment(self, instance):
        selected_player = [player for player in self.players if player.selected][0]
        equipment_card = [card for card in selected_player.cards if card.name == instance.text][0]
        selected_player.equipments.append(equipment_card)
        selected_player.cards.remove(equipment_card)
        self.switch_player(selected_player.name)

    def discard_an_equipment(self, instance):
        selected_player = instance.player
        equipment_card_to_discard = instance.card
        equipment_card_to_discard.number = 1
        selected_player.equipments.remove(equipment_card_to_discard)
        if equipment_card_to_discard.is_premium:
            self.premium_discard_pile.append(equipment_card_to_discard)
        else:
            self.normal_discard_pile.append(equipment_card_to_discard)
        self.switch_player(selected_player.name)

    def create_show_equipment_buttons(self):
        try:
            selected_player = [player for player in self.players if player.selected][0]
            self.root.ids.equipments.clear_widgets()
            equipments = selected_player.equipments
            if equipments == []:
                self.change_prompt("You don't have any equipment!")
            else:
                for equipment in equipments:
                    temp_button = Button(font_name="fonts/msyh.ttc", text=equipment.name, color=(1, 0, 0, 1),
                                         font_size=30)
                    temp_button.bind(on_press=self.show_equipment)
                    self.root.ids.equipments.add_widget(temp_button)
                self.change_prompt("Select equipment to show.")

        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")

    def show_equipment(self, instance):
        selected_player = [player for player in self.players if player.selected][0]
        equipment_to_show = [equipment for equipment in selected_player.equipments if equipment.name == instance.text][
            0]
        equipment_to_show.number = 114514
        self.switch_player(selected_player.name)

    def activate_check_card(self):
        try:
            selected_player = [player for player in self.players if player.selected][0]
            self.root.ids.cards.clear_widgets()
            self.root.ids.equipments.clear_widgets()
            for equipment in selected_player.equipments:
                temp_button = Button(font_name="fonts/msyh.ttc", text=equipment.name, color=(1, 0, 0, 1), font_size=30)
                temp_button.card = equipment
                temp_button.player = selected_player
                temp_button.bind(on_press=self.display_card)
                self.root.ids.equipments.add_widget(temp_button)
            for card in selected_player.cards:
                temp_button = Button(font_name="fonts/msyh.ttc", text=card.name, color=(1, 0, 0, 1), font_size=30)
                temp_button.bind(on_press=self.display_card)
                temp_button.card = card
                temp_button.player = selected_player
                self.root.ids.cards.add_widget(temp_button)
            for player in self.players:
                self.root.ids[player.name].clear_widgets()
                for card in player.equipments:
                    if card.number == 114514:
                        button_text = card.name
                    else:
                        button_text = ""
                    temp_button = Button(font_name="fonts/msyh.ttc", text=button_text, color=(1, 0, 0, 1), font_size=20)
                    temp_button.bind(on_press=self.display_card)
                    temp_button.card = card
                    temp_button.player = selected_player
                    self.root.ids[player.name].add_widget(temp_button)

        except IndexError:
            self.change_prompt("You haven't select a player yet!")
        except UnboundLocalError:
            self.change_prompt("You haven't select a player yet!")

    def display_card(self, instance):
        if instance.card not in instance.player.cards + instance.player.equipments and instance.card.number != 114514:
            self.change_prompt("Can't check unrevealed card!")
        else:
            self.change_prompt(f"{instance.card.name[:instance.card.name.find("(")]}: {instance.card.description}")


GameDesignClient().run()
