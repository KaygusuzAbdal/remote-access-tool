# remote-access-tool
Provides access a device remotely. It can hide itself in target's computer and still works if computer restarted. (written for Red Team activities)

## Usage:

1. You should start the program with calling the `KARat.py` file.

```
python3 KARat.py
```

### Parameters:
- **RHOST :** IP of the handler. It can be your public IP Address or something like `0.tcp.ngrok.io` if you're using ngrok.
- **RPORT :** Port of the handler.
- **LHOST :** The local listener hostname. It can be your virtual machine's local ip address or `0.0.0.0` if you're using ngrok. (Be sure that your virtual machine is <ins>**directly**</ins> connected to the modem)
- **LPORT :** The local listener port.

You can also change the executable's name and add a fake file into it.

2. After entering the parameters, the executable will be generated into "dist" folder. Now, you can start your listener with using the code below.

```
python3 listener.py
```

After these, you have to bait your victim to run the executable file. When you do it, executable will hide itself and still be working if victim restart his computer.

