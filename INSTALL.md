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
pip install git+https://github.com/tlancaster6/RoMaV2.git@29ee4277d075e2ba7b309615343c709b314867bb
```

Notes:
- LightGlue is pinned to commit `edb2b83` (v0.2 release)
- RoMa v2 is pinned to our fork at `29ee427`: upstream v2.0.1 (which carries
  the dataclasses metadata fix) plus a one-line GPU-memory fix. Upstream
  loads the ~1 GB checkpoint with `map_location=device`, leaving two copies
  of the model in VRAM at init (2211 MiB peak vs 1162 MiB with the fix) and
  OOMing ROMA full mode on 12 GB cards. The loaded weights are bit-identical.
  Revert to `Parskatt/RoMaV2` once the upstream PR lands.

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
