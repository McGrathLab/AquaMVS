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

Tested with torch 2.5.1 (the version behind the published validation results) and
torch 2.14; both reproduce the ground-truth accuracy metrics to reported precision.

> **Use the pytorch.org index URL for your CUDA version.** A bare `pip install torch`
> gets PyPI's default build, which is currently a CUDA 13 build requiring NVIDIA
> driver 580 or newer. On an older driver it installs without error, but
> `torch.cuda.is_available()` returns `False` and everything runs on the CPU.
> Check with:
> ```bash
> python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
> ```

## 2. Install Git-Based Prerequisites

LightGlue and RoMa v2 are not available on PyPI and must be installed directly from git repositories.

**Quick install (recommended):**
```bash
pip install -r requirements-prereqs.txt
pip install --no-deps -r requirements-romav2.txt
```

**Manual install:**
```bash
pip install git+https://github.com/cvg/LightGlue.git@edb2b83 einops rich
pip install --no-deps git+https://github.com/tlancaster6/RoMaV2.git@29ee4277d075e2ba7b309615343c709b314867bb
```

Notes:
- **Install RoMa v2 with `--no-deps`.** It declares `torchvision>=0.23.0` and
  `fused-local-corr`. Resolving those makes pip replace the torch you installed in
  step 1 with PyPI's default build (see the driver warning above), and installs a
  `fused-local-corr` whose CUDA kernel only loads under the single torch version it
  was built for. AquaMVS uses RoMa's native-torch correlation. RoMa's remaining
  runtime dependencies (`einops`, optionally `rich`) are listed in
  `requirements-prereqs.txt`.
- pip may then print `ERROR: pip's dependency resolver does not currently take into
  account all the packages that are installed`, naming `romav2`'s `torchvision` and
  `fused-local-corr` requirements. This is expected after a `--no-deps` install and
  does not mean the installation failed.
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

**`torch.cuda.is_available()` is `False` after installing the prerequisites**
- pip probably replaced your torch while resolving RoMa v2's dependencies. Reinstall
  torch from the pytorch.org index (step 1), then reinstall RoMa v2 with `--no-deps`.
