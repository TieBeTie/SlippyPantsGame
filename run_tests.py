import unittest
import player
import pygame
import monsters
import game_model





class TestPlayerInit(unittest.TestCase):
    def test_init(self):
        self.player = player.Player(0, 0)
        self.assertEqual(self.player.start_x, 0)
        self.assertEqual(self.player.start_y, 0)
        self.assertEqual(self.player.rect, pygame.Rect(0, 0, 22, 32))
        self.assertEqual(self.player.x_speed, 0)
        self.assertEqual(self.player.y_speed, 0)
        self.assertTrue(self.player.on_ground, True)


class TestPlayerUpdate(unittest.TestCase):
    def test_update(self):
        self.player = player.Player(0, 0)
        self.player.update(False, True, True, [])
        self.assertEqual(self.player.x_speed, 7)
        self.assertEqual(self.player.y_speed, -11)
        self.assertFalse(self.player.on_ground)
        self.assertEqual(self.player.rect.x, 7)
        self.assertEqual(self.player.rect.y, -11)


class TestPlayerDie(unittest.TestCase):
    def test_die(self):
        self.player = player.Player(0, 0)
        self.player.teleporting(200, 430)
        self.assertEqual(self.player.rect.x, 200)
        self.assertEqual(self.player.rect.y, 430)


class TestGameModel(unittest.TestCase):
    def test_create_monster(self):
        model = game_model.GameModel("levels/graphic_test.json")
        gm_monster = model.createMonster(0, 100, 300, 1, 1000)
        monster = monsters.Monster(100, 300, 1, 1000)
        self.assertEqual(gm_monster.start_x, monster.start_x)
        self.assertEqual(gm_monster.start_y, monster.start_y)
        self.assertEqual(gm_monster.walking_length, monster.walking_length)
        self.assertEqual(gm_monster.x_speed, monster.x_speed)


if __name__ == '__main__':
    unittest.main()
