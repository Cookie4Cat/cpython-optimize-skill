# pyperformance Environment Auditor

## Focus

Audit benchmark commands, interpreter paths, environment variables, and dependency versions before trusting results.

## Use When

- Before a formal `pyperformance run`.
- When worker behavior differs from direct execution.
- When results shift after changing Docker, SSH, tmux, shell, or install steps.

## Output

Return:

- Python executable and version
- pyperformance path and version
- CinderX path and initialization status
- key environment variables
- command parity between baseline and candidate
- risks that can invalidate the run
- concrete fix or rerun command

Treat `LD_LIBRARY_PATH`, `PYTHONPATH`, JIT flags, and worker environment inheritance as first-class evidence.
