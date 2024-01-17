from sourceBridge import SourceBridge

game = SourceBridge()
if game.is_valid():
    game.run(["echo 1", "echo 2", "echo 3", "echo 4", "echo 554"])
