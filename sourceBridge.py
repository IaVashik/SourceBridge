import telnetlib
import subprocess
import psutil

SOURCE_ENGINE_GAMES = ["hl2.exe", "csgo.exe", "portal2.exe", "portal2_linux"] # todo

class SourceBridge:
    def __init__(self):
        self.tn = None
        self.is_connected = False
        self.connect()


    def connect(self):
        if not self.connect_netcon():
            self.connect_hijack()


    def connect_netcon(self) -> bool:
        try:
            self.tn = telnetlib.Telnet("127.0.0.1", 2121)
            self.is_connected = True
            print("Connected via NetCon")
            return True
        except Exception:
            return False


    def connect_hijack(self) -> bool:
        game = self.__find_game_process()
        if game:
            print(f"Connected to {game.name} via hijack")
            self.is_connected = True
            return True
        return False

    
    def __find_game_process(self):
        if self.game_process:
            return self.game_process
        
        for game_process in psutil.process_iter():
            if game_process.name() in SOURCE_ENGINE_GAMES:
                self.game_process = game_process
                return game_process
        return None
    

    def send_netcon_command(self, command):
        if self.tn:
            self.tn.write(f"{command}\n".encode("utf-8"))


    def send_hijack_command(self, command):
        if self.IsValid():
            game = self.__find_game_process()
            params = [game.exe(), "-hijack", "+", command]
            subprocess.Popen(params, creationflags=subprocess.DETACHED_PROCESS) 


    def run(self, command):
        if self.IsValid() is False:
            print("Source game offline now, try reconnect...")
            self.connect()
            
        if self.tn:
            self.send_netcon_command(command)
        else:
            self.send_hijack_command(command)   # todo
       
            
    def is_valid(self):
        if not self.is_connected:
            return False
        
        if self.game_process and self.game_process.is_running():
            return True
        try:
            if self.tn:
                self.tn.read_very_eager() # hack :<
                return True
        except:
            return False
        
        return False
        