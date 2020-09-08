import json

class Configurator:
    def __init__(self, file):
        config = json.load(file)
        self.delta = 66 # 66 ms, is ~15 FPS
        self.font_size = 64
        self.update(config)
        self.size = [
            1280,
            720
        ]
        self.hWidth = int(self.size[0]/2)
        self.padding = 10
        self.scale = 5
        
    
    def update(self, config):
        self.MAX_SCORE = config.get("win_score", 11)
        self.p = [
            config.get('p1','Player 1'),
            config.get('p2','Player 2')
        ]
        self.do_player_switching = config.get("do_player_switching", True)




