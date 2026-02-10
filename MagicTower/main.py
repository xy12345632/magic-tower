import pygame
import sys
from constants import *
from player import Player
from monster import Monster
from map import Map

class Game:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('魔塔传说')
        
        # 创建时钟
        self.clock = pygame.time.Clock()
        
        # 初始化游戏对象
        self.player = Player()
        self.map = Map()
        
        # 游戏状态
        self.game_state = GAME_STATES['menu']  # 初始状态为主菜单
        
        # 战斗相关
        self.current_battle = None
        
        # 初始化字体
        pygame.font.init()
        self.font = pygame.font.SysFont('SimHei', 24)
        self.small_font = pygame.font.SysFont('SimHei', 18)
        
        # 存档系统
        self.save_data = {
            'player': None,
            'floor': 1
        }
        self.save_game()
        
        # AI系统
        self.ai_mode = AI_MODE
        self.ai_last_update = pygame.time.get_ticks()
        self.ai_battle_last_update = pygame.time.get_ticks()
        self.ai_target = None  # AI当前目标（怪物或楼梯）
        self.AI_BATTLE_INTERVAL = 500  # 战斗回合间隔（毫秒） - 更快一点
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 处理键盘事件
            if event.type == pygame.KEYDOWN:
                # 切换AI模式（按F键），任何状态下都可以切换
                if event.key == pygame.K_f:
                    self.ai_mode = not self.ai_mode
                else:
                    self.handle_keydown(event.key)
    
    def handle_keydown(self, key):
        """处理键盘按下事件"""
        # 主菜单状态下的操作
        if self.game_state == GAME_STATES['menu']:
            if key == pygame.K_1:
                # 开始游戏
                self.reset_game()
                self.game_state = GAME_STATES['playing']
            elif key == pygame.K_3:
                # 退出游戏
                pygame.quit()
                sys.exit()
            elif key == pygame.K_2:
                # 关于游戏 - 显示简单的关于信息
                self.game_state = GAME_STATES['about']
            return
        
        # 关于游戏状态下的操作
        if self.game_state == GAME_STATES['about']:
            # 按任意键返回主菜单
            self.game_state = GAME_STATES['menu']
            return
        
        # 只有在游戏结束状态下，按R键才会从存档点重新开始
        if self.game_state == GAME_STATES['game_over']:
            if key == pygame.K_r:
                self.load_game()
                self.game_state = GAME_STATES['playing']
            return
        
        if self.game_state == GAME_STATES['playing']:
            # 移动玩家
            dx, dy = 0, 0
            if key == pygame.K_UP or key == pygame.K_w:
                dy = -1
            elif key == pygame.K_DOWN or key == pygame.K_s:
                dy = 1
            elif key == pygame.K_LEFT or key == pygame.K_a:
                dx = -1
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                dx = 1
            
            if dx != 0 or dy != 0:
                self.move_player(dx, dy)
            
            # 打开背包
            if key == pygame.K_i:
                self.game_state = GAME_STATES['inventory']
            
        elif self.game_state == GAME_STATES['battle']:
            # 战斗状态下的操作
            if key == pygame.K_SPACE:
                self.next_battle_turn()
        
        elif self.game_state == GAME_STATES['inventory']:
            # 背包状态下的操作
            if key == pygame.K_i:
                self.game_state = GAME_STATES['playing']
            elif key == pygame.K_1:
                self.player.use_item('potions')
        
        elif self.game_state == GAME_STATES['shop']:
            # 商店状态下的操作
            if key == pygame.K_ESCAPE:
                # 离开商店
                self.game_state = GAME_STATES['playing']
            elif pygame.K_1 <= key <= pygame.K_7:
                # 购买对应商品
                item_id = key - pygame.K_1
                self.buy_item(item_id)
        
        # 删除了升级状态下的操作，因为现在升级自动增加属性
    
    def move_player(self, dx, dy):
        """移动玩家"""
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # 检查碰撞
        if not self.map.check_collision(new_x, new_y):
            # 检查是否有怪物
            monster = self.map.get_monster_at(new_x, new_y)
            if monster:
                # 进入战斗
                self.start_battle(monster)
            else:
                # 检查是否有物品
                item = self.map.get_item_at(new_x, new_y)
                if item:
                    self.collect_item(item)
                
                # 检查是否是楼梯
                if self.map.map_data[new_y][new_x] == MAP_ELEMENTS['stairs_up']:
                    # 检查当前楼层是否还有存活的怪物
                    has_alive_monsters = any(monster.alive for monster in self.map.monsters)
                    if not has_alive_monsters:
                        if self.map.next_floor():
                            self.player.x, self.player.y = 1, 1  # 重置玩家位置
                            self.save_game()  # 上楼梯时保存游戏
                        else:
                            # 到达最高楼层，触发胜利
                            self.game_state = GAME_STATES['victory']
                    # 如果还有怪物，不允许上楼
                elif self.map.map_data[new_y][new_x] == MAP_ELEMENTS['stairs_down']:
                    if self.map.prev_floor():
                        self.player.x, self.player.y = MAP_WIDTH - 2, MAP_HEIGHT - 2  # 重置玩家位置
                        self.save_game()  # 下楼梯时保存游戏
                elif self.map.map_data[new_y][new_x] == MAP_ELEMENTS['npc']:
                    # 与NPC交互，进入商店
                    self.game_state = GAME_STATES['shop']
                else:
                    # 更新玩家位置
                    self.player.x = new_x
                    self.player.y = new_y
    
    def start_battle(self, monster):
        """开始战斗"""
        self.current_battle = {
            'monster': monster,
            'turn': 'player'
        }
        self.game_state = GAME_STATES['battle']
    
    def next_battle_turn(self):
        """战斗下一回合"""
        if not self.current_battle:
            return
        
        monster = self.current_battle['monster']
        
        if self.current_battle['turn'] == 'player':
            # 玩家攻击
            damage = monster.take_damage(self.player.attack)
            if not monster.alive:
                # 怪物被击败
                rewards = monster.get_rewards()
                self.player.add_experience(rewards['experience'])
                self.player.gold += rewards['gold']
                
                # 升级后自动增加属性，无需手动分配
                # 检查是否升级的逻辑已在player.level_up()中处理
                self.game_state = GAME_STATES['playing']
                self.current_battle = None
            else:
                # 切换到怪物回合
                self.current_battle['turn'] = 'monster'
                
                # 怪物攻击
                damage = monster.calculate_damage_to_player(self.player.defense)
                is_dead = self.player.take_damage(damage)
                if is_dead:
                    # 玩家死亡
                    self.game_state = GAME_STATES['game_over']
                    self.current_battle = None
                else:
                    # 切换回玩家回合
                    self.current_battle['turn'] = 'player'
    
    def collect_item(self, item):
        """收集物品"""
        if item['type'] == 'potion':
            # 自动使用红药水
            self.player.heal(50)
        elif item['type'] in ['key_red', 'key_yellow', 'key_blue']:
            self.player.add_item(item['type'])
        
        # 从地图上移除物品
        self.map.remove_item(item)
    
    def save_game(self):
        """保存游戏状态"""
        # 保存玩家状态
        self.save_data['player'] = {
            'level': self.player.level,
            'attack': self.player.attack,
            'defense': self.player.defense,
            'max_hp': self.player.max_hp,
            'hp': self.player.max_hp,  # 存档时恢复满生命值
            'gold': self.player.gold,
            'experience': self.player.experience,
            'experience_to_next': self.player.experience_to_next,
            'inventory': self.player.inventory.copy()
        }
        
        # 保存当前楼层
        self.save_data['floor'] = self.map.current_floor
    
    def load_game(self):
        """从存档加载游戏状态"""
        if self.save_data['player'] is None:
            return
        
        # 恢复玩家状态
        player_data = self.save_data['player']
        self.player.level = player_data['level']
        self.player.attack = player_data['attack']
        self.player.defense = player_data['defense']
        self.player.max_hp = player_data['max_hp']
        self.player.hp = player_data['hp']
        self.player.gold = player_data['gold']
        self.player.experience = player_data['experience']
        self.player.experience_to_next = player_data['experience_to_next']
        self.player.inventory = player_data['inventory'].copy()
        
        # 恢复当前楼层
        self.map.current_floor = self.save_data['floor']
        self.map.load_map()
        
        # 设置玩家初始位置
        if self.map.current_floor == 1:
            self.player.x, self.player.y = 1, 1
        else:
            self.player.x, self.player.y = 1, 1
    
    def draw(self):
        """绘制游戏界面"""
        # 清空屏幕
        self.screen.fill(COLORS['black'])
        
        if self.game_state == GAME_STATES['playing'] or self.game_state == GAME_STATES['inventory']:
            # 绘制地图
            self.map.draw(self.screen, self.player)
            
            # 绘制玩家状态
            self.draw_player_status()
            
            if self.game_state == GAME_STATES['inventory']:
                self.draw_inventory()
        
        elif self.game_state == GAME_STATES['battle']:
            self.draw_battle()
        
        # 删除了level_up状态的绘制，因为现在升级自动增加属性
        
        elif self.game_state == GAME_STATES['game_over']:
            self.draw_game_over()
        
        elif self.game_state == GAME_STATES['victory']:
            self.draw_victory()
        
        elif self.game_state == GAME_STATES['shop']:
            self.draw_shop()
        
        elif self.game_state == GAME_STATES['menu']:
            self.draw_menu()
        
        elif self.game_state == GAME_STATES['about']:
            self.draw_about()
        
        # 更新屏幕
        pygame.display.flip()
    
    def draw_player_status(self):
        """绘制玩家状态"""
        status = self.player.get_status()
        
        # 绘制状态文本
        status_texts = [
            f'等级: {status["level"]}',
            f'攻击: {status["attack"]}',
            f'防御: {status["defense"]}',
            f'生命: {status["hp"]}/{status["max_hp"]}',
            f'金币: {status["gold"]}',
            f'经验: {status["experience"]}/{status["experience_to_next"]}',
            f'当前楼层: {self.map.current_floor}',
            f'AI模式: {"开启" if self.ai_mode else "关闭"} (按F键切换)'
        ]
        
        for i, text in enumerate(status_texts):
            text_surface = self.small_font.render(text, True, COLORS['white'])
            self.screen.blit(text_surface, (10, SCREEN_HEIGHT - 225 + i * 25))
        
        # 绘制背包提示
        inventory_text = '按I键打开背包'
        text_surface = self.small_font.render(inventory_text, True, COLORS['white'])
        self.screen.blit(text_surface, (10, SCREEN_HEIGHT - 30))
    
    def draw_inventory(self):
        """绘制背包界面"""
        # 绘制背包背景
        inventory_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, COLORS['gray'], inventory_rect)
        pygame.draw.rect(self.screen, COLORS['white'], inventory_rect, 2)
        
        # 绘制背包标题
        title_surface = self.font.render('背包', True, COLORS['white'])
        self.screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        
        # 绘制物品列表
        inventory_texts = [
            f'红药水: {self.player.inventory["potions"]} (按1使用)',
            f'红钥匙: {self.player.inventory["key_red"]}',
            f'黄钥匙: {self.player.inventory["key_yellow"]}',
            f'蓝钥匙: {self.player.inventory["key_blue"]}'
        ]
        
        for i, text in enumerate(inventory_texts):
            text_surface = self.small_font.render(text, True, COLORS['white'])
            self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 40 + i * 30))
        
        # 绘制关闭提示
        close_text = '按I键关闭背包'
        text_surface = self.small_font.render(close_text, True, COLORS['white'])
        self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    
    def draw_battle(self):
        """绘制战斗界面"""
        if not self.current_battle:
            return
        
        monster = self.current_battle['monster']
        
        # 绘制战斗背景
        battle_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 300)
        pygame.draw.rect(self.screen, COLORS['gray'], battle_rect)
        pygame.draw.rect(self.screen, COLORS['white'], battle_rect, 2)
        
        # 绘制怪物信息
        monster_name = self.small_font.render(f'怪物: {monster.name}', True, COLORS['white'])
        monster_hp = self.small_font.render(f'生命值: {monster.hp}/{monster.max_hp}', True, COLORS['white'])
        self.screen.blit(monster_name, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(monster_hp, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 90))
        
        # 绘制玩家信息
        player_hp = self.small_font.render(f'你的生命值: {self.player.hp}/{self.player.max_hp}', True, COLORS['white'])
        self.screen.blit(player_hp, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 30))
        
        # 绘制战斗提示
        turn_text = self.small_font.render('按空格键继续战斗', True, COLORS['white'])
        self.screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    

    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 绘制游戏结束文本
        game_over_surface = self.font.render('游戏结束', True, COLORS['hp'])
        restart_surface = self.small_font.render('按R键重新开始', True, COLORS['white'])
        
        self.screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    
    def draw_victory(self):
        """绘制胜利界面"""
        # 绘制胜利文本
        victory_surface = self.font.render('恭喜通关!', True, COLORS['stairs_up'])
        self.screen.blit(victory_surface, (SCREEN_WIDTH // 2 - victory_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    
    def draw_shop(self):
        """绘制商店界面"""
        # 绘制商店背景
        shop_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200, 600, 400)
        pygame.draw.rect(self.screen, COLORS['gray'], shop_rect)
        pygame.draw.rect(self.screen, COLORS['white'], shop_rect, 3)
        
        # 绘制商店标题
        title_surface = self.font.render('商店', True, COLORS['accent'])
        self.screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 180))
        
        # 绘制玩家金币
        gold_surface = self.small_font.render(f'金币: {self.player.gold}', True, COLORS['gold'])
        self.screen.blit(gold_surface, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 150))
        
        # 绘制商品列表
        shop_item_list = list(SHOP_ITEMS.items())
        for i, (item_id, item) in enumerate(shop_item_list):
            # 绘制商品背景
            item_rect = pygame.Rect(SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 120 + i * 50, 560, 45)
            pygame.draw.rect(self.screen, COLORS['dark_gray'], item_rect)
            
            # 绘制商品信息
            item_text = f'{i+1}. {item["name"]} - {item["price"]}金币'
            desc_text = item["description"]
            
            item_surface = self.small_font.render(item_text, True, COLORS['white'])
            desc_surface = self.small_font.render(desc_text, True, COLORS['light_gray'])
            
            self.screen.blit(item_surface, (SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 110 + i * 50))
            self.screen.blit(desc_surface, (SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 90 + i * 50))
        
        # 绘制操作提示
        hint_text = '按1-7购买对应商品，按ESC键离开商店'
        hint_surface = self.small_font.render(hint_text, True, COLORS['white'])
        self.screen.blit(hint_surface, (SCREEN_WIDTH // 2 - hint_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 160))
    
    def draw_menu(self):
        """绘制主菜单界面"""
        # 绘制背景
        self.screen.fill(COLORS['black'])
        
        # 绘制游戏标题
        title_surface = pygame.font.SysFont('SimHei', 48).render('魔塔传说', True, COLORS['accent'])
        self.screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        # 绘制菜单选项
        menu_items = [
            '1. 开始游戏',
            '2. 关于游戏',
            '3. 退出游戏'
        ]
        
        for i, item in enumerate(menu_items):
            item_surface = self.font.render(item, True, COLORS['white'])
            self.screen.blit(item_surface, (SCREEN_WIDTH // 2 - item_surface.get_width() // 2, SCREEN_HEIGHT // 2 + i * 40))
        
        # 绘制版本信息
        version_surface = self.small_font.render('版本 1.0', True, COLORS['light_gray'])
        self.screen.blit(version_surface, (SCREEN_WIDTH // 2 - version_surface.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def draw_about(self):
        """绘制关于游戏界面"""
        # 绘制背景
        self.screen.fill(COLORS['black'])
        
        # 绘制游戏标题
        title_surface = pygame.font.SysFont('SimHei', 36).render('魔塔传说', True, COLORS['accent'])
        self.screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        
        # 绘制版本信息
        version_surface = self.font.render('版本 1.0', True, COLORS['white'])
        self.screen.blit(version_surface, (SCREEN_WIDTH // 2 - version_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        # 绘制游戏介绍
        intro_texts = [
            '一款经典的魔塔类游戏复刻作品',
            '玩家需要探索100层魔塔，击败怪物，',
            '收集道具，提升自己的实力，',
            '最终到达塔顶，完成挑战。',
            '',
            '游戏特色：',
            '- 100层精心设计的关卡',
            '- 自动属性成长系统',
            '- AI自动战斗模式',
            '- 丰富的商店系统',
            '- 精美的视觉效果'
        ]
        
        for i, text in enumerate(intro_texts):
            text_surface = self.small_font.render(text, True, COLORS['light_gray'])
            self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 50 + i * 30))
        
        # 绘制操作提示
        hint_text = '按任意键返回主菜单'
        hint_surface = self.small_font.render(hint_text, True, COLORS['white'])
        self.screen.blit(hint_surface, (SCREEN_WIDTH // 2 - hint_surface.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def buy_item(self, item_id):
        """购买物品"""
        shop_item_list = list(SHOP_ITEMS.items())
        if item_id < 0 or item_id >= len(shop_item_list):
            return False
        
        item_key, item = shop_item_list[item_id]
        
        # 检查金币是否足够
        if self.player.gold < item['price']:
            return False
        
        # 扣除金币
        self.player.gold -= item['price']
        
        # 处理物品效果
        if item_key == 'potion':
            # 恢复生命值
            self.player.heal(50)
        elif item_key in ['key_red', 'key_yellow', 'key_blue']:
            # 添加钥匙
            self.player.add_item(item_key)
        elif item_key == 'attack_boost':
            # 永久增加攻击
            self.player.attack += 5
        elif item_key == 'defense_boost':
            # 永久增加防御
            self.player.defense += 5
        elif item_key == 'hp_boost':
            # 永久增加生命值上限
            self.player.max_hp += 20
            self.player.hp += 20
        
        return True
    
    def find_path(self, start, end):
        """使用BFS寻找从start到end的路径"""
        from collections import deque
        
        # 定义四个方向
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # 初始化队列和访问记录
        queue = deque()
        queue.append(start)
        visited = set()
        visited.add(start)
        parent = {}
        
        # BFS搜索
        while queue:
            current = queue.popleft()
            
            if current == end:
                # 找到了路径，回溯构建路径
                path = []
                while current in parent:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path
            
            # 尝试四个方向
            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                
                # 检查边界
                if nx < 0 or nx >= MAP_WIDTH or ny < 0 or ny >= MAP_HEIGHT:
                    continue
                
                # 检查是否是墙壁
                if self.map.map_data[ny][nx] == MAP_ELEMENTS['wall']:
                    continue
                
                # 检查是否已经访问过
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
                    queue.append((nx, ny))
        
        return None  # 没有找到路径
    
    def update_ai(self):
        """AI控制逻辑"""
        if self.game_state == GAME_STATES['battle']:
            # 战斗状态下自动进行回合，但使用较慢的间隔
            current_time = pygame.time.get_ticks()
            if current_time - self.ai_battle_last_update >= self.AI_BATTLE_INTERVAL:
                self.next_battle_turn()
                self.ai_battle_last_update = current_time
            return
        
        if self.game_state != GAME_STATES['playing']:
            return
        
        # 1. 检查生命值，如果低则优先寻找红药水
        low_hp_threshold = self.player.max_hp * 0.3  # 生命值低于30%时寻找药水
        nearest_potion = None
        potion_distance = float('inf')
        
        if self.player.hp < low_hp_threshold:
            # 寻找最近的红药水
            for item in self.map.items:
                if item['type'] == 'potion':
                    distance = abs(item['x'] - self.player.x) + abs(item['y'] - self.player.y)
                    if distance < potion_distance:
                        nearest_potion = item
                        potion_distance = distance
        
        # 2. 如果需要药水且找到了药水，优先前往药水位置
        if nearest_potion:
            self.ai_target = nearest_potion
            target_pos = (nearest_potion['x'], nearest_potion['y'])
        else:
            # 3. 否则寻找最近的怪物
            nearest_monster = None
            nearest_distance = float('inf')
            
            for monster in self.map.monsters:
                if monster.alive:
                    distance = abs(monster.x - self.player.x) + abs(monster.y - self.player.y)
                    if distance < nearest_distance:
                        nearest_monster = monster
                        nearest_distance = distance
            
            target_pos = None
            
            # 如果有怪物，设置目标为怪物位置
            if nearest_monster:
                self.ai_target = nearest_monster
                target_pos = (nearest_monster.x, nearest_monster.y)
            else:
                # 没有怪物，寻找楼梯上楼
                self.ai_target = None
                
                # 寻找上楼楼梯
                stairs_x, stairs_y = None, None
                for y in range(MAP_HEIGHT):
                    for x in range(MAP_WIDTH):
                        if self.map.map_data[y][x] == MAP_ELEMENTS['stairs_up']:
                            stairs_x, stairs_y = x, y
                            break
                    if stairs_x is not None:
                        break
                
                if stairs_x is not None and stairs_y is not None:
                    target_pos = (stairs_x, stairs_y)
        
        if target_pos:
            # 寻找路径
            current_pos = (self.player.x, self.player.y)
            path = self.find_path(current_pos, target_pos)
            
            if path and len(path) > 0:
                # 移动到路径的第一个点
                next_pos = path[0]
                dx = next_pos[0] - self.player.x
                dy = next_pos[1] - self.player.y
                
                # 执行移动
                self.move_player(dx, dy)
            else:
                # 没有找到路径，尝试随机移动
                import random
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                self.move_player(dx, dy)
        else:
            # 没有目标，随机移动
            import random
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            self.move_player(dx, dy)
    
    def reset_game(self):
        """从存档点重置游戏"""
        self.load_game()
        self.game_state = GAME_STATES['playing']
        self.current_battle = None
    
    def run(self):
        """游戏主循环"""
        while True:
            # 处理事件
            self.handle_events()
            
            # AI控制
            if self.ai_mode:
                current_time = pygame.time.get_ticks()
                if current_time - self.ai_last_update >= AI_UPDATE_INTERVAL:
                    self.update_ai()
                    self.ai_last_update = current_time
            
            # 绘制游戏
            self.draw()
            
            # 控制帧率
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()