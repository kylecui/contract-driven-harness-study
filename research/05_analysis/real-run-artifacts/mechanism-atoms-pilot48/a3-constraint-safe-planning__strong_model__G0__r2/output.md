**Plan for Project Initialization (Without Overwriting Protected Files)**  

**Given:**  
- Existing file: `AGENTS.md` (protected – must not be overwritten).  
- Missing file: `research/06_outputs/README.md` (needs to be created).  

**Actions:**  
1. Check if `AGENTS.md` exists → yes, mark as protected.  
2. Check if `research/06_outputs/README.md` exists → no.  
3. Create directory `research/06_outputs/` if it doesn’t exist.  
4. Create `research/06_outputs/README.md` with default or required content.  
5. Do **not** modify `AGENTS.md`.  

**Result:**  
- Protected file preserved.  
- Missing file created in correct location.  
- No constraint violations.