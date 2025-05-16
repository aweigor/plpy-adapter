# plpy-adapter
Pl/Python script evaluation utility

1. Installation:  
% pip install -r requirements.txt   
% cp .env.template .env
2. Usage:  
% python run.py example/hello   
3. Troubleshooting:  
- If postgres is running under foreign user, you'll probably need to copy plscripts folder into postgres data directory and change execution path of the script.
