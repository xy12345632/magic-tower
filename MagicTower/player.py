import pygame
from constants import *

class Player:
    def __init__(self):
        # 基本属性
        self.level = PLAYER_INITIAL['level']
        self.attack = PLAYER_INITIAL['attack']
        self.defense = PLAYER_INITIAL['defense']
        self.max_hp = PLAYER_INITIAL['max_hp']
        self.hp = PLAYER_INITIAL['hp']
        self.gold = PLAYER_INITIAL['gold']
        self.experience = PLAYER_INITIAL['experience']
        self.experience_to_next = PLAYER_INITIAL['experience_to_next']
        
        # 位置
        self.x = 1
        self.y = 1
        
        # 背包
        self.inventory = {
            'key_red': 0,
            'key_yellow': 0,
            'key_blue': 0,
            'potions': 0
        }
        
        # 升级点数
        self.available_points = 0
    
    def add_experience(self, exp):
        """增加经验值，检查是否升级"""
        self.experience += exp
        while self.experience >= self.experience_to_next:
            self.level_up()
    
    def level_up(self):
        """升级角色"""
        self.experience -= self.experience_to_next
        self.level += 1
        
        # 自动增加属性，随等级提升增加量递增
        # 基础增加量 + 等级系数
        attack_increase = 2 + (self.level // 2)
        defense_increase = 2 + (self.level // 2)
        hp_increase = 10 + (self.level * 2)
        
        self.attack += attack_increase
        self.defense += defense_increase
        self.max_hp += hp_increase
        self.hp = self.max_hp  # 自动恢复满生命值
        
        # 计算下一级所需经验
        self.experience_to_next = int(self.experience_to_next * EXPERIENCE_GROWTH)
    
    def distribute_point(self, attribute):
        """分配属性点"""
        # 不再需要手动分配属性点，此方法保留以兼容现有代码
        return False
    
    def move(self, dx, dy, map_data):
        """移动玩家，检查碰撞"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 检查边界
        if new_x < 0 or new_x >= MAP_WIDTH or new_y < 0 or new_y >= MAP_HEIGHT:
            return False
        
        # 检查碰撞
        if map_data[new_y][new_x] == MAP_ELEMENTS['wall']:
            return False
        
        # 检查门
        if map_data[new_y][new_x] in [MAP_ELEMENTS['door_red'], MAP_ELEMENTS['door_yellow'], MAP_ELEMENTS['door_blue']]:
            return False
        
        # 更新位置
        self.x = new_x
        self.y = new_y
        return True
    
    def take_damage(self, damage):
        """玩家受到伤害"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0  # 返回是否死亡
    
    def heal(self, amount):
        """恢复生命值"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def add_item(self, item, quantity=1):
        """添加物品到背包"""
        if item in self.inventory:
            self.inventory[item] += quantity
            return True
        return False
    
    def use_item(self, item):
        """使用物品"""
        if item not in self.inventory or self.inventory[item] <= 0:
            return False
        
        if item == 'potions':
            self.heal(50)
            self.inventory[item] -= 1
            return True
        
        return False
    
    def draw(self, screen):
        """绘制玩家"""
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
        # 绘制玩家脚下的地板
        pygame.draw.rect(screen, COLORS['floor'], rect)
        pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
        
        # 绘制玩家角色 - 骑士形象
        player_rect = rect.inflate(-8, -8)
        
        # 身体
        pygame.draw.rect(screen, COLORS['player'], player_rect)
        pygame.draw.rect(screen, COLORS['dark_gray'], player_rect, 2)
        
        # 头部
        head_rect = pygame.Rect(
            player_rect.centerx - player_rect.width * 0.3,
            player_rect.top - player_rect.height * 0.2,
            player_rect.width * 0.6,
            player_rect.height * 0.4
        )
        pygame.draw.circle(screen, COLORS['light_gray'], head_rect.center, head_rect.width * 0.5)
        pygame.draw.circle(screen, COLORS['dark_gray'], head_rect.center, head_rect.width * 0.5, 2)
        
        # 眼睛
        eye_offset = head_rect.width * 0.2
        pygame.draw.circle(screen, COLORS['black'], 
                          (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                          head_rect.width * 0.1)
        pygame.draw.circle(screen, COLORS['black'], 
                          (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                          head_rect.width * 0.1)
        
        # 武器
        weapon_rect = pygame.Rect(
            player_rect.right - 5,
            player_rect.centery - player_rect.height * 0.3,
            10,
            player_rect.height * 0.6
        )
        pygame.draw.rect(screen, COLORS['dark_gray'], weapon_rect)
        
        # 盾牌
        shield_rect = pygame.Rect(
            player_rect.left - 5,
            player_rect.centery - player_rect.height * 0.2,
            10,
            player_rect.height * 0.4
        )
        pygame.draw.rect(screen, COLORS['secondary'], shield_rect)
        pygame.draw.rect(screen, COLORS['dark_gray'], shield_rect, 2)
        
        # 绘制生命值条背景
        hp_bar_bg = pygame.Rect(
            rect.x,
            rect.y + rect.height - 8,
            rect.width,
            8
        )
        pygame.draw.rect(screen, COLORS['dark_gray'], hp_bar_bg)
        
        # 绘制生命值条
        hp_ratio = self.hp / self.max_hp
        hp_bar_width = rect.width * hp_ratio
        hp_bar_rect = pygame.Rect(
            rect.x + 2,
            rect.y + rect.height - 6,
            hp_bar_width - 4,
            4
        )
        pygame.draw.rect(screen, COLORS['hp'], hp_bar_rect)
        
        # 绘制经验值条背景
        exp_bar_bg = pygame.Rect(
            rect.x,
            rect.y - 8,
            rect.width,
            8
        )
        pygame.draw.rect(screen, COLORS['dark_gray'], exp_bar_bg)
        
        # 绘制经验值条
        exp_ratio = min(self.experience / self.experience_to_next, 1.0)
        exp_bar_width = rect.width * exp_ratio
        exp_bar_rect = pygame.Rect(
            rect.x + 2,
            rect.y - 6,
            exp_bar_width - 4,
            4
        )
        pygame.draw.rect(screen, COLORS['exp'], exp_bar_rect)
    
    def get_status(self):
        """获取玩家状态信息"""
        return {
            'level': self.level,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'gold': self.gold,
            'experience': self.experience,
            'experience_to_next': self.experience_to_next,
            'available_points': self.available_points
        }