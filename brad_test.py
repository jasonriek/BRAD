from controls import Controls

def run():
    controls = Controls()
    for i in range(3):
        data = ['CMD_MOVE', '1', '0', '35', '10', '0']
        controls.run(data)
    #controls.relax(True)

run()
print("moved!")