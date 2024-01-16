
import tkinter as tk
import subprocess

def run_external_exe():
    exe_path = "./../../../output/Chat\ Assistant/main.exe"
    
    try:
        subprocess.Popen(exe_path)
        #subprocess.run(exe_path, check=True)
    except subprocess.CalledProcessError:
        print(f"Error running {exe_path}")

def main():
    root = tk.Tk()
    root.title("Run External Executable")

    button = tk.Button(root, text="Run External Executable", command=run_external_exe)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
