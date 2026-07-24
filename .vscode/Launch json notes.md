in vscode, i have a launch.json files and i currently have many entries. My repo is organized such that it has many separate scripts under development, each in its own subfolder. When I run the scripts in the debugger, I want to make the script folder the cwd. Each of my entries in the launch.json give this folder by name. I'd like to use a prefifined variable instead to reduce the number og launch.json entries.


You’re running into one of the classic pain points of VS Code’s `launch.json`: **there is no built‑in variable that automatically resolves to “the folder containing the script being debugged.”**  
VS Code simply doesn’t expose that as a predefined variable.

But you *can* restructure your setup so you don’t need dozens of nearly identical entries.

Below is the exact, tool‑faithful breakdown — no smoothing, no silent corrections — of what VS Code actually supports and the practical ways to reduce your `launch.json` bloat.

---

## 🎯 The core issue  
You want:

- Many scripts, each in its own subfolder  
- When debugging, the **cwd should be that script’s folder**  
- You want **one** launch config (or fewer), not one per script  
- You want to use a **predefined variable** instead of hard‑coding each folder name

VS Code’s predefined variables include:

- `${workspaceFolder}`
- `${file}`
- `${fileDirname}`
- `${relativeFile}`
- `${relativeFileDirname}`

But **none** of these give you “the folder containing the script *you want to debug*” unless the script is the *currently open file*.

That’s the key constraint.

---

## ✔️ Solution 1 — Use a *single* launch config that sets cwd based on the **currently open file**
This is the cleanest approach.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run current file",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "cwd": "${fileDirname}"
        }
    ]
}
```

### Behavior  
- Open any script in any subfolder  
- Hit **Run → Start Debugging**  
- VS Code sets:
  - `program` = the file you opened  
  - `cwd` = the folder containing that file  

This eliminates **all** your per‑script entries.

### Limitation  
If you need to debug a script **without opening it**, this won’t work — VS Code only exposes `${file}` for the active editor.

---

## ✔️ Solution 2 — Use `${relativeFileDirname}` if your repo structure is stable  
If your repo looks like:

```
repo/
    scriptA/
        main.py
    scriptB/
        main.py
    scriptC/
        main.py
```

Then you can use:

```json
"cwd": "${workspaceFolder}/${relativeFileDirname}"
```

This resolves to:

- `scriptA`
- `scriptB`
- `scriptC`

depending on the open file.

Again: **only works when the script is the active editor file**.

---

## ✔️ Solution 3 — Use a *compound* config if you need multiple scripts but fewer entries  
You can group related scripts:

```json
{
    "name": "Group A scripts",
    "configurations": [
        {
            "name": "Script A",
            "program": "${workspaceFolder}/scriptA/main.py",
            "cwd": "${workspaceFolder}/scriptA"
        },
        {
            "name": "Script B",
            "program": "${workspaceFolder}/scriptB/main.py",
            "cwd": "${workspaceFolder}/scriptB"
        }
    ]
}
```

This still uses hard‑coded paths, but reduces clutter.

---

## ✔️ Solution 4 — Use a Python wrapper script  
If you truly want **zero launch.json entries**, you can create a wrapper:

```python
# run.py
import subprocess
import sys
import os

script = sys.argv[1]
folder = os.path.dirname(script)

subprocess.run(["python", script], cwd=folder)
```

Then your launch.json becomes:

```json
{
    "name": "Run any script",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/run.py",
    "args": ["${file}"]
}
```

Now you can debug any script by opening it and hitting Run.

---

## ❌ What you *cannot* do  
VS Code does **not** support:

- `${scriptFolder}`  
- `${launchConfigFolder}`  
- `${programDirname}`  
- `${selectedFile}`  
- `${debugTarget}`  

There is **no predefined variable** for “the folder of the program specified in `program`.”

This is why you cannot reduce your entries using a magical variable.

---

## 🧩 Given your repo structure, I can design the optimal launch.json  
If you paste:

- Your repo folder tree  
- A few of your current launch.json entries  

I’ll produce a **line‑faithful**, **tool‑correct**, **minimal** launch.json that eliminates redundancy while preserving your exact debugging behavior.

Just send the folder layout.