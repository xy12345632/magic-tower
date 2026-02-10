# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40

# 地图设置
MAP_WIDTH = 20
MAP_HEIGHT = 15

# 颜色定义
COLORS = {
    # 基础颜色
    'white': (255, 255, 255),
    'black': (30, 30, 30),
    'gray': (100, 100, 100),
    'light_gray': (180, 180, 180),
    'dark_gray': (50, 50, 50),
    
    # 主题颜色
    'primary': (65, 105, 225),  # 皇家蓝
    'secondary': (255, 140, 0),  # 暗橙
    'accent': (138, 43, 226),    # 蓝紫色
    
    # 元素颜色
    'wall': (139, 69, 19),       # 棕色
    'floor': (222, 184, 135),    # 小麦色
    'player': (30, 144, 255),    #  dodger蓝
    'monster': (220, 20, 60),    # 猩红
    'stairs_up': (255, 215, 0),  # 金
    'stairs_down': (255, 165, 0), # 橙
    
    # 门和钥匙颜色
    'door_red': (220, 20, 60),   # 猩红
    'door_yellow': (255, 215, 0),# 金
    'door_blue': (30, 144, 255), # dodger蓝
    'key_red': (255, 99, 71),    # 番茄红
    'key_yellow': (255, 223, 0), # 浅黄
    'key_blue': (0, 191, 255),   # 深天蓝
    
    # 状态颜色
    'hp': (220, 20, 60),         # 猩红
    'mp': (30, 144, 255),        # dodger蓝
    'exp': (144, 238, 144),      # 浅绿
    'gold': (255, 215, 0),       # 金
    
    # UI颜色
    'ui_bg': (50, 50, 50),       # 深灰
    'ui_text': (240, 240, 240),  # 亮灰
    'ui_border': (100, 100, 100),# 中灰
    'ui_highlight': (173, 216, 230) # 浅蓝
}

# 地图元素ID
MAP_ELEMENTS = {
    'empty': 0,
    'wall': 1,
    'floor': 2,
    'stairs_up': 3,
    'stairs_down': 4,
    'player': 5,
    'monster': 6,
    'item': 7,
    'door_red': 8,
    'door_yellow': 9,
    'door_blue': 10,
    'key_red': 11,
    'key_yellow': 12,
    'key_blue': 13,
    'npc': 14
}

# 游戏状态
GAME_STATES = {
    'menu': 0,  # 主菜单
    'playing': 1,
    'battle': 2,
    'inventory': 3,
    'level_up': 4,
    'game_over': 5,
    'victory': 6,
    'shop': 7,
    'about': 8  # 关于游戏
}

# AI模式
AI_MODE = False
AI_UPDATE_INTERVAL = 100  # AI更新间隔（毫秒） - 提高移动速度

# 商店系统
SHOP_ITEMS = {
    'potion': {
        'name': '红药水',
        'price': 50,
        'description': '恢复50点生命值'
    },
    'key_red': {
        'name': '红钥匙',
        'price': 100,
        'description': '用于打开红色门'
    },
    'key_yellow': {
        'name': '黄钥匙',
        'price': 50,
        'description': '用于打开黄色门'
    },
    'key_blue': {
        'name': '蓝钥匙',
        'price': 150,
        'description': '用于打开蓝色门'
    },
    'attack_boost': {
        'name': '攻击药水',
        'price': 200,
        'description': '永久增加5点攻击'
    },
    'defense_boost': {
        'name': '防御药水',
        'price': 200,
        'description': '永久增加5点防御'
    },
    'hp_boost': {
        'name': '生命药水',
        'price': 250,
        'description': '永久增加20点生命值上限'
    }
}

# 游戏状态添加商店
GAME_STATES['shop'] = 6

# 玩家初始属性
PLAYER_INITIAL = {
    'level': 1,
    'attack': 10,
    'defense': 10,
    'max_hp': 100,
    'hp': 100,
    'gold': 0,
    'experience': 0,
    'experience_to_next': 100
}

# 升级属性点
LEVEL_UP_POINTS = 3

# 经验值成长系数
EXPERIENCE_GROWTH = 1.5