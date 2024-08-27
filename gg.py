import subprocess

def start_gunicorn():
    command = [
        'gunicorn',
        '--workers', '3',
        '--bind', '0.0.0.0:8000',
        'myproject.wsgi:application'
    ]
    process = subprocess.Popen(command)
    return process

if __name__ == "__main__":
    process = start_gunicorn()
    print(f'Gunicorn started with PID: {process.pid}')
