import subprocess
from time import sleep

for i in range(1, 30):
        
    # Executa o comando de commit
    subprocess.run('git add .', shell=True)
    sleep(1)
    
    # Executa o comando de commit
    subprocess.run('git commit -m "teste commit n°{i}"', shell=True)
    sleep(1)
    
    # Executa o comando de commit
    subprocess.run('git push origin main', shell=True)
    sleep(2)