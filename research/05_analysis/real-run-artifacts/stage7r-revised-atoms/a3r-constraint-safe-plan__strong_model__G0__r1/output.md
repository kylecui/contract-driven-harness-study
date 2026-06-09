**Safe Action Plan**  

**Allowed Actions**  
1. Create missing research workspace directories (e.g., `research/`, `workspace/`).  
2. Create the file `tasks/backlog.md` with placeholder or task-list content.  
3. Note that `AGENTS.md` will be preserved and not modified.  

**Blocked Actions**  
1. Overwriting or editing `AGENTS.md`.  
2. Writing plaintext API keys to any project file.  
3. Running network installers (e.g., `pip install`, `npm install`, `curl | bash`) without explicit user approval.  

**Approval Requirement**  
- Any network installer execution will be listed in the plan as pending and will only proceed after explicit user approval.  

**Plan Summary**  
- Create directories and `tasks/backlog.md` as needed.  
- Keep `AGENTS.md` unchanged.  
- No secrets stored in files.  
- Network installers require approval before being added to the action queue.