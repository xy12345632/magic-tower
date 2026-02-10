import pygame
from constants import *

class Map:
    def __init__(self):
        # 地图数据
        self.current_floor = 1
        self.max_floors = 100  # 将关卡数量增加到100个
        self.map_data = []
        self.monsters = []
        self.items = []
        
        # 初始化地图
        self.load_map()
    
    def load_map(self):
        """加载当前楼层的地图"""
        # 清空当前数据
        self.map_data = []
        self.monsters = []
        self.items = []
        
        # 生成随机地图或加载预定义地图
        self.generate_random_map()
    
    def generate_random_map(self):
        """生成随机地图"""
        import random
        
        # 创建空地图
        self.map_data = [[MAP_ELEMENTS['wall'] for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # 生成地板区域，确保有连通的路径
        
        # 1. 创建大量初始地板
        # 先填充大部分区域为地板
        for y in range(1, MAP_HEIGHT - 1):
            for x in range(1, MAP_WIDTH - 1):
                # 确保80%的概率是地板，20%是墙壁
                if random.random() < 0.8:
                    self.map_data[y][x] = MAP_ELEMENTS['floor']
                else:
                    self.map_data[y][x] = MAP_ELEMENTS['wall']
        
        # 2. 创建额外的连通通道
        # 增加多条横向和纵向通道，确保连通性
        for i in range(3):  # 3条横向通道
            y = 2 + i * (MAP_HEIGHT - 4) // 2
            for x in range(1, MAP_WIDTH - 1):
                self.map_data[y][x] = MAP_ELEMENTS['floor']
        
        for i in range(3):  # 3条纵向通道
            x = 2 + i * (MAP_WIDTH - 4) // 2
            for y in range(1, MAP_HEIGHT - 1):
                self.map_data[y][x] = MAP_ELEMENTS['floor']
        
        # 3. 确保关键位置是地板
        # 确保外围有通道
        for y in range(1, MAP_HEIGHT - 1):
            self.map_data[y][1] = MAP_ELEMENTS['floor']
            self.map_data[y][MAP_WIDTH - 2] = MAP_ELEMENTS['floor']
        for x in range(1, MAP_WIDTH - 1):
            self.map_data[1][x] = MAP_ELEMENTS['floor']
            self.map_data[MAP_HEIGHT - 2][x] = MAP_ELEMENTS['floor']
        
        # 确保楼梯位置是地板
        self.map_data[MAP_HEIGHT - 2][MAP_WIDTH - 2] = MAP_ELEMENTS['floor']  # 上楼楼梯位置
        if self.current_floor > 1:
            self.map_data[1][1] = MAP_ELEMENTS['floor']  # 下楼楼梯位置
        
        # 确保玩家初始位置是地板
        self.map_data[1][1] = MAP_ELEMENTS['floor']
        
        # 4. 最终检查，确保地板比例足够
        # 统计地板数量
        floor_count = 0
        total_tiles = (MAP_WIDTH - 2) * (MAP_HEIGHT - 2)
        for y in range(1, MAP_HEIGHT - 1):
            for x in range(1, MAP_WIDTH - 1):
                if self.map_data[y][x] == MAP_ELEMENTS['floor']:
                    floor_count += 1
        
        # 如果地板比例低于60%，增加更多地板
        target_floor_ratio = 0.6
        while floor_count < total_tiles * target_floor_ratio:
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            if self.map_data[y][x] == MAP_ELEMENTS['wall']:
                self.map_data[y][x] = MAP_ELEMENTS['floor']
                floor_count += 1
        
        # 放置楼梯
        self.map_data[MAP_HEIGHT - 2][MAP_WIDTH - 2] = MAP_ELEMENTS['stairs_up']
        if self.current_floor > 1:
            self.map_data[1][1] = MAP_ELEMENTS['stairs_down']
        
        # 放置商店NPC（每5层出现一次）
        if self.current_floor % 5 == 0:
            # 找一个合适的位置放置商店NPC
            shop_x, shop_y = None, None
            import random
            attempts = 0
            max_attempts = 50
            
            while shop_x is None and attempts < max_attempts:
                x = random.randint(2, MAP_WIDTH - 3)
                y = random.randint(2, MAP_HEIGHT - 3)
                
                # 确保周围有足够的空间
                has_space = True
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if self.map_data[ny][nx] != MAP_ELEMENTS['floor']:
                            has_space = False
                            break
                    if not has_space:
                        break
                
                if has_space:
                    shop_x, shop_y = x, y
                attempts += 1
            
            if shop_x is not None and shop_y is not None:
                self.map_data[shop_y][shop_x] = MAP_ELEMENTS['npc']
        
        # 放置怪物
        # 根据当前楼层确定可用的怪物类型
        monster_types = ['slime', 'goblin', 'skeleton', 'orc', 'dragon']
        
        # 确保每个楼层有不同的怪物组合和强度
        # 根据楼层确定主要怪物类型和强度系数
        floor_level = self.current_floor
        strength_factor = 1 + (floor_level - 1) * 0.1  # 每层增加10%的强度
        
        # 确定当前楼层的主要怪物类型
        # 随着楼层增加，逐渐引入更强的怪物类型
        primary_monster_type = None
        if floor_level <= 3:
            primary_monster_type = 'slime'  # 1-3层：史莱姆为主
        elif floor_level <= 6:
            primary_monster_type = 'goblin'  # 4-6层：哥布林为主
        elif floor_level <= 9:
            primary_monster_type = 'skeleton'  # 7-9层：骷髅为主
        elif floor_level <= 15:
            primary_monster_type = 'orc'  # 10-15层：兽人为主
        else:
            primary_monster_type = 'dragon'  # 16+层：龙为主
        
        # 确定可用的怪物类型：当前主要类型 + 可能的更强类型
        available_monsters = [primary_monster_type]
        
        # 根据楼层解锁更强的怪物类型
        if floor_level > 3:
            available_monsters.append('goblin')
        if floor_level > 6:
            available_monsters.append('skeleton')
        if floor_level > 10:
            available_monsters.append('orc')
        if floor_level > 15:
            available_monsters.append('dragon')
        
        # 确保列表不重复
        available_monsters = list(set(available_monsters))
        
        monster_count = min(5 + floor_level, 15)  # 每层怪物数量逐渐增加，但有上限
        
        placed_monsters = 0
        attempts = 0
        max_attempts = monster_count * 20
        
        while placed_monsters < monster_count and attempts < max_attempts:
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            attempts += 1
            
            # 确保位置是地板，且不是楼梯
            if self.map_data[y][x] == MAP_ELEMENTS['floor']:
                # 确保怪物周围至少有一个相邻的地板格子，方便玩家接近
                has_adjacent_floor = False
                adj_floors = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                        if self.map_data[ny][nx] == MAP_ELEMENTS['floor']:
                            has_adjacent_floor = True
                            adj_floors.append((dx, dy))
                
                if has_adjacent_floor:
                    # 随机选择可用的怪物类型
                    monster_type = random.choice(available_monsters)
                    # 创建怪物时传入强度系数
                    self.monsters.append(Monster(monster_type, x, y, strength_factor))
                    placed_monsters += 1
        
        # 确保地图上有至少一个怪物
        if not self.monsters:
            # 在玩家附近生成一个怪物
            x = self.player.x + random.choice([-2, -1, 1, 2])
            y = self.player.y + random.choice([-2, -1, 1, 2])
            x = max(1, min(MAP_WIDTH - 2, x))
            y = max(1, min(MAP_HEIGHT - 2, y))
            self.map_data[y][x] = MAP_ELEMENTS['floor']  # 确保是地板
            monster_type = random.choice(available_monsters)
            self.monsters.append(Monster(monster_type, x, y))
        
        # 放置道具
        for _ in range(3 + self.current_floor):
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            
            if self.map_data[y][x] == MAP_ELEMENTS['floor']:
                self.items.append({'type': 'potion', 'x': x, 'y': y})
        
        # 放置钥匙
        key_types = ['key_yellow', 'key_yellow', 'key_red', 'key_blue']
        for i in range(min(self.current_floor, len(key_types))):
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            
            if self.map_data[y][x] == MAP_ELEMENTS['floor']:
                self.items.append({'type': key_types[i], 'x': x, 'y': y})
    
    def get_monster_at(self, x, y):
        """获取指定位置的怪物"""
        for monster in self.monsters:
            if monster.x == x and monster.y == y and monster.alive:
                return monster
        return None
    
    def get_item_at(self, x, y):
        """获取指定位置的物品"""
        for item in self.items:
            if item['x'] == x and item['y'] == y:
                return item
        return None
    
    def remove_item(self, item):
        """移除物品"""
        if item in self.items:
            self.items.remove(item)
    
    def next_floor(self):
        """前往上一层"""
        if self.current_floor < self.max_floors:
            self.current_floor += 1
            self.load_map()
            return True
        return False
    
    def prev_floor(self):
        """前往下一层"""
        if self.current_floor > 1:
            self.current_floor -= 1
            self.load_map()
            return True
        return False
    
    def draw(self, screen, player):
        """绘制地图"""
        # 绘制地图背景
        screen.fill(COLORS['black'])
        
        # 绘制地图元素
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                element = self.map_data[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                # 绘制不同的地图元素
                if element == MAP_ELEMENTS['wall']:
                    # 墙壁带有边框效果
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect)
                    pygame.draw.rect(screen, COLORS['wall'], rect.inflate(-4, -4))
                elif element == MAP_ELEMENTS['floor']:
                    # 地板带有纹理效果
                    pygame.draw.rect(screen, COLORS['floor'], rect)
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
                elif element == MAP_ELEMENTS['stairs_up']:
                    # 上楼楼梯
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect)
                    pygame.draw.rect(screen, COLORS['stairs_up'], rect.inflate(-4, -4))
                    # 添加箭头指示
                    pygame.draw.polygon(screen, COLORS['dark_gray'], [
                        (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 4),
                        (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + 3 * TILE_SIZE // 4),
                        (x * TILE_SIZE + 3 * TILE_SIZE // 4, y * TILE_SIZE + 3 * TILE_SIZE // 4)
                    ])
                elif element == MAP_ELEMENTS['stairs_down']:
                    # 下楼楼梯
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect)
                    pygame.draw.rect(screen, COLORS['stairs_down'], rect.inflate(-4, -4))
                    # 添加箭头指示
                    pygame.draw.polygon(screen, COLORS['dark_gray'], [
                        (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + 3 * TILE_SIZE // 4),
                        (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4),
                        (x * TILE_SIZE + 3 * TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4)
                    ])
                elif element == MAP_ELEMENTS['door_red']:
                    # 红色门
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect)
                    pygame.draw.rect(screen, COLORS['door_red'], rect.inflate(-4, -4))
                    # 添加门把效果
                    pygame.draw.circle(screen, COLORS['dark_gray'], 
                                      (x * TILE_SIZE + TILE_SIZE * 0.75, y * TILE_SIZE + TILE_SIZE // 2), 
                                      TILE_SIZE // 8)
                elif element == MAP_ELEMENTS['door_yellow']:
                    # 黄色门
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect)
                    pygame.draw.rect(screen, COLORS['door_yellow'], rect.inflate(-4, -4))
                    # 添加门把效果
                    pygame.draw.circle(screen, COLORS['dark_gray'], 
                                      (x * TILE_SIZE + TILE_SIZE * 0.75, y * TILE_SIZE + TILE_SIZE // 2), 
                                      TILE_SIZE // 8)
                elif element == MAP_ELEMENTS['door_blue']:
                    # 蓝色门
                    pygame.draw.rect(screen, COLORS['dark_gray'], rect)
                    pygame.draw.rect(screen, COLORS['door_blue'], rect.inflate(-4, -4))
                    # 添加门把效果
                    pygame.draw.circle(screen, COLORS['dark_gray'], 
                                      (x * TILE_SIZE + TILE_SIZE * 0.75, y * TILE_SIZE + TILE_SIZE // 2), 
                                      TILE_SIZE // 8)
        
        # 绘制物品
        for item in self.items:
            rect = pygame.Rect(item['x'] * TILE_SIZE, item['y'] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            if item['type'] == 'potion':
                # 红药水，带有玻璃瓶效果
                pygame.draw.rect(screen, COLORS['floor'], rect)
                pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
                # 药水瓶身
                bottle_rect = rect.inflate(-8, -8)
                pygame.draw.ellipse(screen, COLORS['light_gray'], bottle_rect)
                # 药水液体
                liquid_rect = bottle_rect.copy()
                liquid_rect.height = liquid_rect.height * 0.7
                liquid_rect.top = bottle_rect.bottom - liquid_rect.height
                pygame.draw.ellipse(screen, COLORS['hp'], liquid_rect)
                # 瓶盖
                cap_rect = pygame.Rect(
                    bottle_rect.centerx - bottle_rect.width * 0.3,
                    bottle_rect.top - bottle_rect.height * 0.1,
                    bottle_rect.width * 0.6,
                    bottle_rect.height * 0.2
                )
                pygame.draw.rect(screen, COLORS['dark_gray'], cap_rect)
            elif item['type'] == 'key_red':
                # 红色钥匙
                pygame.draw.rect(screen, COLORS['floor'], rect)
                pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
                # 钥匙形状
                key_points = [
                    (rect.centerx, rect.top + rect.height * 0.3),
                    (rect.centerx + rect.width * 0.3, rect.top + rect.height * 0.5),
                    (rect.centerx, rect.top + rect.height * 0.7),
                    (rect.centerx - rect.width * 0.3, rect.top + rect.height * 0.5)
                ]
                pygame.draw.polygon(screen, COLORS['key_red'], key_points)
                pygame.draw.circle(screen, COLORS['key_red'], 
                                  (rect.centerx, rect.top + rect.height * 0.3), 
                                  rect.width * 0.15)
            elif item['type'] == 'key_yellow':
                # 黄色钥匙
                pygame.draw.rect(screen, COLORS['floor'], rect)
                pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
                # 钥匙形状
                key_points = [
                    (rect.centerx, rect.top + rect.height * 0.3),
                    (rect.centerx + rect.width * 0.3, rect.top + rect.height * 0.5),
                    (rect.centerx, rect.top + rect.height * 0.7),
                    (rect.centerx - rect.width * 0.3, rect.top + rect.height * 0.5)
                ]
                pygame.draw.polygon(screen, COLORS['key_yellow'], key_points)
                pygame.draw.circle(screen, COLORS['key_yellow'], 
                                  (rect.centerx, rect.top + rect.height * 0.3), 
                                  rect.width * 0.15)
            elif item['type'] == 'key_blue':
                # 蓝色钥匙
                pygame.draw.rect(screen, COLORS['floor'], rect)
                pygame.draw.rect(screen, COLORS['dark_gray'], rect, 1)
                # 钥匙形状
                key_points = [
                    (rect.centerx, rect.top + rect.height * 0.3),
                    (rect.centerx + rect.width * 0.3, rect.top + rect.height * 0.5),
                    (rect.centerx, rect.top + rect.height * 0.7),
                    (rect.centerx - rect.width * 0.3, rect.top + rect.height * 0.5)
                ]
                pygame.draw.polygon(screen, COLORS['key_blue'], key_points)
                pygame.draw.circle(screen, COLORS['key_blue'], 
                                  (rect.centerx, rect.top + rect.height * 0.3), 
                                  rect.width * 0.15)
        
        # 绘制怪物
        for monster in self.monsters:
            monster.draw(screen)
        
        # 绘制玩家
        player.draw(screen)
    
    def check_collision(self, x, y):
        """检查碰撞"""
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return True
        
        element = self.map_data[y][x]
        if element == MAP_ELEMENTS['wall']:
            return True
        
        return False

# 导入怪物类以避免循环依赖
from monster import Monster