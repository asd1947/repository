"""The template of the main script of the machine learning process
"""
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
#f = open(r"C:\Users\7741_team\Downloads\Day02教材\Day02教材\04-磚塊怎麼打\MLGame-master\MLGame-master\test.pickle","rb")
#print(pickle.load(f))
import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def check(current,last):
    direction_x = current[0] - last[0]
    direction_y = current[1] - last[1]
    predict_ball_position = 0
    if direction_y > 0:
        m=direction_y/direction_x
        k=current[1]-m*current[0]
        predict_ball_position = (400-k)/m
    else:
        predict_ball_position = 100
    while predict_ball_position <0 or predict_ball_position >200:
        if predict_ball_position < 0:
            predict_ball_position = -predict_ball_position
        elif predict_ball_position > 200:
            predict_ball_position = 400-predict_ball_position
    #print(predict_ball_position)
    return predict_ball_position

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    last_ball_position = [101,101]
    # 3. Start an endless loop.
    
    while True:
        scene_info = comm.get_scene_info()              
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
            
        platform_x = scene_info.platform[0]
        # 3.1. Receive the scene information sent from the game process.
        current_ball_position = scene_info.ball
        end_ball_x = check(current_ball_position,last_ball_position)
        last_ball_position = scene_info.ball
        move = end_ball_x - (scene_info.platform[0]+20)
        
        

        if move > 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif move <0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        # 3.3. Put the code here to handle the scene information
        
        # 3.4. Send the instruction for this frame to the game process
        
