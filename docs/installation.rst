Installation
============

This guide covers installing AquaMVS on Windows, Linux, and macOS.

Prerequisites
-------------

- **Python**: 3.10 or later
- **pip**: Latest version (upgrade with ``pip install --upgrade pip``)
- **git**: For installing git-based prerequisites

Install PyTorch
---------------

AquaMVS requires PyTorch. Visit the `PyTorch installation page <https://pytorch.org/get-started/locally/>`_
and use their configuration selector to get the correct install command for your system.

**GPU (CUDA 12.1) examples:**

.. code-block:: bash

   # Windows or Linux with NVIDIA GPU
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

**CPU-only examples:**

.. code-block:: bash

   # Windows, Linux, or macOS (CPU only)
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

Choose the command matching your OS and GPU from pytorch.org. For other CUDA versions
or ROCm (AMD GPU), consult the PyTorch website.

AquaMVS is tested with torch 2.5.1 (the version behind the published validation
results) and torch 2.14; both reproduce the ground-truth accuracy metrics to reported
precision.

.. warning::

   Use the pytorch.org index URL for your CUDA version. A bare ``pip install torch``
   gets PyPI's default build, currently a CUDA 13 build that needs NVIDIA driver 580
   or newer. On an older driver it installs without error, but
   ``torch.cuda.is_available()`` returns ``False`` and everything runs on the CPU.

Install Git Prerequisites
--------------------------

AquaMVS depends on two libraries that are not available on PyPI and must be installed from git:

**Quick method** (recommended):

.. code-block:: bash

   pip install -r requirements-prereqs.txt
   pip install --no-deps -r requirements-romav2.txt

**Manual method:**

.. code-block:: bash

   pip install git+https://github.com/cvg/LightGlue.git@edb2b83 einops rich
   pip install --no-deps git+https://github.com/tlancaster6/RoMaV2.git@29ee4277d075e2ba7b309615343c709b314867bb

.. important::

   Install RoMa v2 with ``--no-deps``. It declares ``torchvision>=0.23.0`` and
   ``fused-local-corr``; resolving those makes pip replace the torch you installed
   above with PyPI's default build (see the warning above), and installs a
   ``fused-local-corr`` whose CUDA kernel only loads under the single torch version
   it was built for. AquaMVS uses RoMa's native-torch correlation. RoMa's remaining
   runtime dependencies (``einops``, optionally ``rich``) are listed in
   ``requirements-prereqs.txt``.

   Later pip commands may print ``ERROR: pip's dependency resolver does not
   currently take into account all the packages that are installed``, naming
   RoMa v2's ``torchvision`` and ``fused-local-corr`` requirements. This is expected
   after a ``--no-deps`` install and does not mean the installation failed.

**Why git dependencies?**

- **LightGlue**: Not yet published to PyPI by upstream maintainers
- **RoMa v2**: Not yet published to PyPI; pinned to our fork at ``29ee427``, which is
  upstream v2.0.1 plus a one-line GPU-memory fix (the checkpoint is no longer
  materialized in VRAM alongside the model, which OOMed ROMA full mode on 12 GB cards).
  The loaded weights are bit-identical. Upstream PR:
  https://github.com/Parskatt/RoMaV2/pull/50

Install AquaMVS
---------------

**From PyPI** (recommended for users):

.. code-block:: bash

   pip install aquamvs

**From source** (for development):

.. code-block:: bash

   git clone https://github.com/McGrathLab/AquaMVS.git
   cd AquaMVS
   pip install -e ".[dev]"

Platform-Specific Notes
------------------------

Windows
^^^^^^^

If you encounter build errors during Open3D installation, you may need to install
`Visual C++ Build Tools <https://visualstudio.microsoft.com/visual-cpp-build-tools/>`_.
Select "Desktop development with C++" during installation.

Linux
^^^^^

Open3D requires OpenGL libraries for visualization. On Ubuntu/Debian:

.. code-block:: bash

   sudo apt install libgl1-mesa-glx

On headless servers without a display, AquaMVS uses Open3D's EGL headless renderer
when the GPU driver supports it (it probes this in a subprocess, so a failed probe
cannot crash the pipeline). Where no rendering backend is available, it degrades
gracefully, skipping only the 3D render images.

macOS
^^^^^

On Apple Silicon (M1/M2/M3), PyTorch supports the MPS (Metal Performance Shaders) backend
for GPU acceleration. Use the standard CPU/MPS install command from pytorch.org:

.. code-block:: bash

   pip install torch torchvision

Verify Installation
--------------------

Check that AquaMVS installed correctly:

.. code-block:: bash

   python -c "import aquamvs; print(aquamvs.__version__)"
   aquamvs --help

You should see version information and the CLI help text.

Troubleshooting
---------------

**"No module named 'torch'"**
   PyTorch must be installed before AquaMVS. See `Install PyTorch`_ above.

**"No module named 'lightglue'" or "No module named 'romav2'"**
   Git prerequisites must be installed before AquaMVS. See `Install Git Prerequisites`_ above.

**GPU not detected after installing the prerequisites**
   If ``torch.cuda.is_available()`` became ``False``, pip probably replaced your torch
   while resolving RoMa v2's dependencies. Reinstall torch from the pytorch.org index,
   then reinstall RoMa v2 with ``--no-deps``.

**CUDA version mismatch**
   Your installed PyTorch CUDA version must match your NVIDIA driver. Check compatibility
   at https://pytorch.org/get-started/locally/. To check your installed PyTorch:

   .. code-block:: bash

      python -c "import torch; print(torch.__version__)"

   The output shows the CUDA version (e.g., ``2.1.0+cu121`` = CUDA 12.1).

**Open3D visualization errors on headless Linux**
   Expected where neither a display nor EGL headless rendering is available. AquaMVS
   then skips the 3D render images; reconstruction and all other outputs still work.

**ImportError on Windows (DLL load failed)**
   This usually indicates missing Visual C++ runtime libraries. Install the
   `Visual C++ Redistributable <https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist>`_.
