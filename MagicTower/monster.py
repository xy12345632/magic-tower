import pygame
from constants import *

class Monster:
    def __init__(self, monster_type, x, y, strength_factor=1.0):
        # 怪物类型定义
        self.monster_data = {
            'slime': {
                'name': '史莱姆',
                'attack': 5,
                'defense': 2,
                'hp': 20,
                'experience': 10,
                'gold': 5,
                'color': (0, 255, 0)  # 绿色
            },
            'goblin': {
                'name': '哥布林',
                'attack': 8,
                'defense': 4,
                'hp': 35,
                'experience': 20,
                'gold': 10,
                'color': (0, 128, 0)  # 深绿色
            },
            'skeleton': {
                'name': '骷髅',
                'attack': 12,
                'defense': 6,
                'hp': 50,
                'experience': 35,
                'gold': 15,
                'color': COLORS['light_gray']
            },
            'orc': {
                'name': '兽人',
                'attack': 18,
                'defense': 10,
                'hp': 80,
                'experience': 60,
                'gold': 25,
                'color': COLORS['monster']
            },
            'dragon': {
                'name': '龙',
                'attack': 30,
                'defense': 20,
                'hp': 200,
                'experience': 200,
                'gold': 100,
                'color': COLORS['accent']
            }
        }
        
        # 获取怪物属性
        monster_attrs = self.monster_data[monster_type]
        
        # 初始化怪物属性，应用强度系数
        self.type = monster_type
        self.name = monster_attrs['name']
        self.attack = int(monster_attrs['attack'] * strength_factor)
        self.defense = int(monster_attrs['defense'] * strength_factor)
        self.max_hp = int(monster_attrs['hp'] * strength_factor)
        self.hp = self.max_hp
        self.experience = int(monster_attrs['experience'] * strength_factor)
        self.gold = int(monster_attrs['gold'] * strength_factor)
        self.color = monster_attrs['color']
        
        # 初始化位置
        self.x = x
        self.y = y
        self.alive = True
    
    def calculate_damage_to_player(self, player_defense):
        """计算对玩家造成的伤害"""
        damage = max(self.attack - player_defense, 1)
        return damage
    
    def take_damage(self, player_attack):
        """受到玩家伤害"""
        damage = max(player_attack - self.defense, 1)
        self.hp = max(0, self.hp - damage)
        if self.hp <= 0:
            self.alive = False
        return damage
    
    def get_rewards(self):
        """获取击败怪物的奖励"""
        return {
            'experience': self.experience,
            'gold': self.gold
        }
    
    def draw(self, screen):
        """绘制怪物"""
        if not self.alive:
            return
        
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
        # 绘制怪物脚下的地板
        pygame.draw.rect(screen, COLORS['floor'], rect)
        pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
        
        # 根据怪物类型绘制不同的外观
        monster_rect = rect.inflate(-8, -8)
        
        if self.type == 'slime':
            # 史莱姆 - 果冻状
            pygame.draw.ellipse(screen, self.color, monster_rect)
            pygame.draw.ellipse(screen, COLORS['dark_gray'], monster_rect, 2)
            
            # 眼睛
            eye_offset = monster_rect.width * 0.2
            pygame.draw.circle(screen, COLORS['black'], 
                              (monster_rect.centerx - eye_offset, monster_rect.centery - 5), 
                              monster_rect.width * 0.1)
            pygame.draw.circle(screen, COLORS['black'], 
                              (monster_rect.centerx + eye_offset, monster_rect.centery - 5), 
                              monster_rect.width * 0.1)
            
            # 嘴巴
            mouth_rect = pygame.Rect(
                monster_rect.centerx - monster_rect.width * 0.2,
                monster_rect.centery + monster_rect.height * 0.1,
                monster_rect.width * 0.4,
                monster_rect.height * 0.2
            )
            pygame.draw.arc(screen, COLORS['black'], mouth_rect, 0, 3.14, 2)
            
        elif self.type == 'goblin':
            # 哥布林 - 绿色小人
            # 身体
            pygame.draw.rect(screen, self.color, monster_rect)
            pygame.draw.rect(screen, COLORS['dark_gray'], monster_rect, 2)
            
            # 头部
            head_rect = pygame.Rect(
                monster_rect.centerx - monster_rect.width * 0.4,
                monster_rect.top - monster_rect.height * 0.2,
                monster_rect.width * 0.8,
                monster_rect.height * 0.5
            )
            pygame.draw.circle(screen, self.color, head_rect.center, head_rect.width * 0.5)
            pygame.draw.circle(screen, COLORS['dark_gray'], head_rect.center, head_rect.width * 0.5, 2)
            
            # 眼睛
            eye_offset = head_rect.width * 0.25
            pygame.draw.circle(screen, COLORS['white'], 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.08)
            pygame.draw.circle(screen, COLORS['white'], 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.08)
            
            # 耳朵
            pygame.draw.polygon(screen, self.color, [
                (head_rect.left, head_rect.centery),
                (head_rect.left - head_rect.width * 0.3, head_rect.centery - head_rect.height * 0.3),
                (head_rect.left - head_rect.width * 0.1, head_rect.centery)
            ])
            pygame.draw.polygon(screen, self.color, [
                (head_rect.right, head_rect.centery),
                (head_rect.right + head_rect.width * 0.3, head_rect.centery - head_rect.height * 0.3),
                (head_rect.right + head_rect.width * 0.1, head_rect.centery)
            ])
            
        elif self.type == 'skeleton':
            # 骷髅 - 骨架
            # 身体
            spine_rect = pygame.Rect(
                monster_rect.centerx - monster_rect.width * 0.1,
                monster_rect.top + monster_rect.height * 0.2,
                monster_rect.width * 0.2,
                monster_rect.height * 0.6
            )
            pygame.draw.rect(screen, COLORS['white'], spine_rect)
            pygame.draw.rect(screen, COLORS['dark_gray'], spine_rect, 2)
            
            # 头部
            head_rect = pygame.Rect(
                monster_rect.centerx - monster_rect.width * 0.3,
                monster_rect.top - monster_rect.height * 0.2,
                monster_rect.width * 0.6,
                monster_rect.height * 0.4
            )
            pygame.draw.circle(screen, COLORS['white'], head_rect.center, head_rect.width * 0.5)
            pygame.draw.circle(screen, COLORS['dark_gray'], head_rect.center, head_rect.width * 0.5, 2)
            
            # 眼窝
            eye_offset = head_rect.width * 0.2
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            
            # 肋骨
            for i in range(3):
                rib_y = spine_rect.top + spine_rect.height * (i + 1) * 0.25
                pygame.draw.line(screen, COLORS['white'], 
                               (spine_rect.left, rib_y), 
                               (spine_rect.left - spine_rect.width * 2, rib_y), 
                               2)
                pygame.draw.line(screen, COLORS['white'], 
                               (spine_rect.right, rib_y), 
                               (spine_rect.right + spine_rect.width * 2, rib_y), 
                               2)
            
        elif self.type == 'orc':
            # 兽人 - 肌肉发达
            # 身体
            pygame.draw.rect(screen, self.color, monster_rect)
            pygame.draw.rect(screen, COLORS['dark_gray'], monster_rect, 2)
            
            # 头部
            head_rect = pygame.Rect(
                monster_rect.centerx - monster_rect.width * 0.35,
                monster_rect.top - monster_rect.height * 0.2,
                monster_rect.width * 0.7,
                monster_rect.height * 0.4
            )
            pygame.draw.rect(screen, self.color, head_rect)
            pygame.draw.rect(screen, COLORS['dark_gray'], head_rect, 2)
            
            # 眼睛
            eye_offset = head_rect.width * 0.25
            pygame.draw.circle(screen, (255, 255, 0), 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.08)
            pygame.draw.circle(screen, (255, 255, 0), 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.08)
            
            # 獠牙
            pygame.draw.polygon(screen, COLORS['white'], [
                (head_rect.left + head_rect.width * 0.3, head_rect.bottom),
                (head_rect.left + head_rect.width * 0.25, head_rect.bottom + head_rect.height * 0.2),
                (head_rect.left + head_rect.width * 0.35, head_rect.bottom)
            ])
            pygame.draw.polygon(screen, COLORS['white'], [
                (head_rect.right - head_rect.width * 0.3, head_rect.bottom),
                (head_rect.right - head_rect.width * 0.25, head_rect.bottom + head_rect.height * 0.2),
                (head_rect.right - head_rect.width * 0.35, head_rect.bottom)
            ])
            
        elif self.type == 'dragon':
            # 龙 - 强大的生物
            # 身体
            pygame.draw.ellipse(screen, self.color, monster_rect)
            pygame.draw.ellipse(screen, COLORS['dark_gray'], monster_rect, 3)
            
            # 头部
            head_rect = pygame.Rect(
                monster_rect.centerx - monster_rect.width * 0.3,
                monster_rect.top - monster_rect.height * 0.2,
                monster_rect.width * 0.6,
                monster_rect.height * 0.4
            )
            pygame.draw.circle(screen, self.color, head_rect.center, head_rect.width * 0.5)
            pygame.draw.circle(screen, COLORS['dark_gray'], head_rect.center, head_rect.width * 0.5, 3)
            
            # 眼睛
            eye_offset = head_rect.width * 0.2
            pygame.draw.circle(screen, (255, 255, 0), 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx - eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.08)
            pygame.draw.circle(screen, (255, 255, 0), 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.15)
            pygame.draw.circle(screen, COLORS['black'], 
                              (head_rect.centerx + eye_offset, head_rect.centery - 5), 
                              head_rect.width * 0.08)
            
            #  horns
            horn_points = [
                (head_rect.centerx - head_rect.width * 0.3, head_rect.top - head_rect.height * 0.1),
                (head_rect.centerx - head_rect.width * 0.4, head_rect.top - head_rect.height * 0.4),
                (head_rect.centerx - head_rect.width * 0.2, head_rect.top - head_rect.height * 0.2)
            ]
            pygame.draw.polygon(screen, COLORS['gold'], horn_points)
            pygame.draw.polygon(screen, COLORS['dark_gray'], horn_points, 2)
            
            horn_points = [
                (head_rect.centerx + head_rect.width * 0.3, head_rect.top - head_rect.height * 0.1),
                (head_rect.centerx + head_rect.width * 0.4, head_rect.top - head_rect.height * 0.4),
                (head_rect.centerx + head_rect.width * 0.2, head_rect.top - head_rect.height * 0.2)
            ]
            pygame.draw.polygon(screen, COLORS['gold'], horn_points)
            pygame.draw.polygon(screen, COLORS['dark_gray'], horn_points, 2)
        
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
    
    def get_status(self):
        """获取怪物状态信息"""
        return {
            'name': self.name,
            'attack': self.attack,
            'defense': self.defense,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'experience': self.experience,
            'gold': self.gold
        }