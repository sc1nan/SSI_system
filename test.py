import subprocess 
Data = subprocess.check_output(['wmic', 'product', 'get', 'name']) 
a = str(Data) 
try: 
    for i in range(len(a)): 
        app = a.split("\\r\\r\\n")[6:][i]
        if 'MariaDB' in app:
            if float(app.split(' ')[1]) < 11:
                print('Unable to proceed')
            else:
                break
except IndexError as e: 
    print("All Done")