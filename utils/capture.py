import subprocess


def capture(args=""):
    execute_file_path = "utils/TBotCaptureTool/TBotCaptureTool.exe"
    if args:
        result = subprocess.run([execute_file_path, args], capture_output=True, text=True)
    else:
        result = subprocess.run([execute_file_path], capture_output=True, text=True)
    return result.returncode, result.stdout
