
import subprocess

def start_gunicorn():
    # تحديد مسار مشروع Django، واسم المشروع (على سبيل المثال myproject)
    project_path = '/path/to/your/django/project'
    wsgi_module = 'myproject.wsgi:application'
    
    # تحديد عدد العمال والمنفذ الذي سيستمع عليه Gunicorn
    command = [
        'gunicorn',
        '--workers', '3',
        '--bind', '0.0.0.0:8000',
        wsgi_module
    ]

    # تشغيل Gunicorn
    process = subprocess.Popen(command, cwd=project_path)
    
    return process

if __name__ == "__main__":
    # بدء Gunicorn
    process = start_gunicorn()
    print(f'Gunicorn started with PID: {process.pid}')
