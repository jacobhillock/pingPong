import json

class Configurator:
    def __init__(self, file):
        config = json.load(file)
        self.FPS = config.get("FPS", 15)
        self.delta = int(1000/self.FPS)
        self.height = config.get("height", 720)
        self.width = config.get("width", 1280)
        self.hWidth = int(self.width/2)
        self.size = self.width, self.height
        self.MAX_SCORE = config.get("win_score", 11)
        self.baseX = 10
        self.baseY = 10
        self.scale = 5
        self.font_size = config.get("font_size", 64)
        self.p1 = config.get('p1','Player 1')
        self.p2 = config.get('p2','Player 2')
        self.do_player_switching = config.get("do_player_switching", True)
        self.do_server_tracking = config.get("do_server_tracking", True)


