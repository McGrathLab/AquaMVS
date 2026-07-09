# Installation Instructions

AquaMVS requires several prerequisites to be installed before the main package. Follow these steps in order.

## 1. Install PyTorch

AquaMVS requires PyTorch with CUDA support (recommended) or CPU-only. Install from [pytorch.org](https://pytorch.org/get-started/locally/) choosing the appropriate CUDA version for your system.

**Example (CUDA 12.1):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Example (CPU only):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 2. Install Git-Based Prerequisites

LightGlue and RoMa v2 are not available on PyPI and must be installed directly from git repositories.

**Quick install (recommended):**
```bash
pip install -r requirements-prereqs.txt
```

**Manual install:**
```bash
pip install git+https://github.com/cvg/LightGlue.git@edb2b83
pip install git+https://github.com/Parskatt/RoMaV2.git@95c9968145c8906b7b59383258e9f73b02853d89
```

Notes:
- LightGlue is pinned to commit `edb2b83` (v0.2 release)
- RoMa v2 is pinned to an upstream commit (`95c9968`) that includes the
  dataclasses metadata fix; the earlier fork is no longer needed

## 3. Install AquaMVS

After prerequisites are installed, install AquaMVS (AquaCal will be installed automatically as a dependency):

**From PyPI:**
```bash
pip install aquamvs
```

**Development install (current):**
```bash
git clone https://github.com/McGrathLab/AquaMVS.git
cd AquaMVS
pip install -e ".[dev]"
```

## Verification

Verify the installation:
```bash
python -c "import aquamvs; print(aquamvs.__version__)"
aquamvs --help
```

## Common Issues

**ImportError: PyTorch is required but not installed**
- Follow Step 1 to install PyTorch before AquaMVS

**ModuleNotFoundError: No module named 'lightglue'**
- Follow Step 2 to install git-based prerequisites

**ModuleNotFoundError: No module named 'romav2'**
- Follow Step 2 to install git-based prerequisites
