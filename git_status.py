import subprocess
from time import sleep

for i in range(1, 30):
        
    # Executa o comando de commit
    subprocess.run('git add .', shell=True)
    sleep(10)
    
    # Executa o comando de commit
    subprocess.run(f'git commit -m " commit n°0{i}"', shell=True)
    sleep(10)
    
    # Executa o comando de commit
    subprocess.run('git push origin main', shell=True)
    sleep(25)