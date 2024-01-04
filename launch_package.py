import os
from pick import pick

project_dir = os.listdir("adb_connector_python/dist")

credentials_path="~/.credentials/classic_token_github"

clear = [el for el in project_dir]
clear.append("auto")

scelta = pick(options=clear,title="scegli una versione",indicator=">")[0]

CMD = "twine upload adb_connector_python/dist/{0} -u {1} -p {2}"

with open(credenziali_path,"r") as credenziali:
    user, token = credenziali.readlines()
    if scelta == "auto":
        os.system(CMD.format("*",user.strip(),token.strip()))        
    else:
        os.system(CMD.format(scelta.strip(),user.strip(),token.strip()))
