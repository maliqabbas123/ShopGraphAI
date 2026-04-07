# Migration Guide: Old Structure → New Unified Structure

This guide helps you migrate from the old separated structure to the new unified structure where everything runs from the root.

---

## What Changed?

### Old Structure ❌
```
ShopGraphAI/
├── backend/
│   ├── .env                    # Backend config
│   ├── venv/                   # Backend venv
│   ├── requirements.txt
│   └── app/
│       └── main.py            # Backend entry point
│
└── frontend/                   # Separate frontend
    ├── .env                    # Frontend config
    └── (runs on :5173)
```

### New Structure ✅
```
ShopGraphAI/
├── main.py                     # 🚀 Single entry point
├── frontend_routes.py          # Frontend serving
├── .env                        # Unified config
├── venv/                       # Root venv
├── requirements.txt            # Root requirements
│
├── backend/app/               # Backend code
│
└── frontend/                   # Frontend code
    └── dist/                   # Built frontend
```

---

## Benefits of New Structure

✅ **Single Server** - One process serves both frontend and API
✅ **Simpler Deployment** - One build, one deploy
✅ **Unified Config** - One `.env` file
✅ **Better Integration** - No CORS issues in production
✅ **Professional Pattern** - Matches industry standards

---

## Step-by-Step Migration

### Step 1: Backup Your Current Setup

```bash
# In case something goes wrong
cp backend/.env backend/.env.backup
cp frontend/.env frontend/.env.backup
```

### Step 2: Move Configuration to Root

```bash
# Copy backend .env to root
cp backend/.env .env

# Edit .env if needed
# Make sure CORS_ORIGINS includes http://localhost:8000
```

### Step 3: Create New Virtual Environment in Root

```bash
# Deactivate old venv if active
deactivate

# Create new venv in root
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Update Frontend Config

Edit `frontend/.env`:
```env
# Change API base URL to point to same server
VITE_API_BASE_URL=http://localhost:8000
```

### Step 5: Build Frontend

```bash
cd frontend

# Install dependencies (if not already done)
npm install

# Build for production
npm run build

# Verify dist/ folder was created
ls dist/  # Should show index.html, assets/, etc.

cd ..
```

### Step 6: Test the New Setup

```bash
# Make sure MongoDB is running
mongosh  # Should connect

# Seed database (if not already done)
python seed_database.py

# Run the unified server
python main.py
```

You should see:
```
ShopGraph AI Backend Starting...
Serving frontend from: /path/to/ShopGraphAI/frontend/dist
Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7: Test in Browser

Open http://localhost:8000

You should see the React frontend loaded.

Try these:
- ✅ Chat interface works
- ✅ Search for products
- ✅ API calls work (check browser console)
- ✅ No CORS errors

### Step 8: Clean Up Old Files (Optional)

Once everything works:

```bash
# Remove old backend venv (if you want)
rm -rf backend/venv

# Remove old .env files
rm backend/.env
rm frontend/.env

# Keep the backups just in case
```

---

## Development Workflow

### For Backend Changes

```bash
# Just run from root with auto-reload
source venv/bin/activate
python main.py

# Edit files in backend/app/
# Server auto-reloads on changes
```

### For Frontend Changes

**During Development:**
```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend dev server
cd frontend
npm run dev  # Hot reload on :5173
```

**For Production Testing:**
```bash
# Rebuild and test
cd frontend
npm run build
cd ..
python main.py  # Serves from :8000
```

---

## Troubleshooting Migration

### Error: "No module named 'backend'"

**Problem**: Python can't find the backend module.

**Solution**: Make sure you're running from the root directory.

```bash
pwd  # Should show /path/to/ShopGraphAI (root)
ls    # Should show main.py, backend/, frontend/

# If not in root, navigate there
cd /path/to/ShopGraphAI

# Then run
python main.py
```

### Error: "Frontend not built"

**Problem**: Frontend build doesn't exist.

**Solution**: Build the frontend.

```bash
cd frontend
npm run build
cd ..
```

### Error: Import errors in backend code

**Problem**: Imports still use old paths.

**Solution**: Imports should use `from backend.app.` prefix:

```python
# Correct ✅
from backend.app.core.config import settings
from backend.app.db import get_db

# Wrong ❌ (old backend/app structure)
from app.core.config import settings
```

The main.py and all backend code use `backend.app.` imports now.

### Frontend shows blank page

**Problem**: Build might be outdated or not served correctly.

**Solution**:
1. Rebuild frontend: `cd frontend && npm run build && cd ..`
2. Check `frontend/dist/` exists with files
3. Restart server: `python main.py`
4. Check browser console for errors
5. Verify VITE_API_BASE_URL in frontend/.env

### Port conflicts

**Problem**: Port 8000 already in use.

**Solution**: Either change port or kill existing process.

```bash
# Option 1: Change port in .env
PORT=8001

# Option 2: Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

---

## Verification Checklist

After migration, verify:

- [ ] `python main.py` runs without errors
- [ ] http://localhost:8000 shows the React app
- [ ] http://localhost:8000/docs shows API docs
- [ ] Chat interface works
- [ ] Search returns products
- [ ] No console errors in browser
- [ ] Backend logs show no errors
- [ ] MongoDB connection works
- [ ] Gemini API calls work

---

## Rolling Back (If Needed)

If something goes wrong:

```bash
# 1. Restore old .env files
cp backend/.env.backup backend/.env
cp frontend/.env.backup frontend/.env

# 2. Use old venv
cd backend
source venv/bin/activate

# 3. Run old way
python -m app.main

# In another terminal:
cd frontend
npm run dev
```

---

## File Mapping Reference

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `backend/app/main.py` | `main.py` (root) | Moved to root |
| `backend/.env` | `.env` (root) | Unified config |
| `backend/venv/` | `venv/` (root) | One venv |
| `backend/requirements.txt` | `requirements.txt` (root) | One file |
| `backend/scripts/seed_database.py` | `seed_database.py` (root) | Moved to root |
| `backend/app/*` | `backend/app/*` | Stays same |
| `frontend/src/*` | `frontend/src/*` | Stays same |
| N/A | `frontend_routes.py` (root) | New file |

---

## Next Steps After Migration

1. ✅ **Test thoroughly** - Try all features
2. ✅ **Update documentation** - If you made changes
3. ✅ **Commit changes** - Git commit the new structure
4. ✅ **Update CI/CD** - If you have deployment pipelines
5. ✅ **Share with team** - If working with others

---

## Need Help?

- **Setup Issues**: See [SETUP.md](./SETUP.md)
- **Architecture Questions**: See [CLAUDE.md](./CLAUDE.md)
- **Development Workflow**: See [SETUP.md](./SETUP.md#development-workflow)

---

**Migration complete!** 🎉

Run `python main.py` and enjoy the unified structure!
