<table>
  <tr>
    <td><img src="docs/_static/tank_image.jpg" alt="Experimental setup" width="480"></td>
    <td><img src="docs/_static/orbit.gif" alt="3D surface reconstruction" width="480"></td>
  </tr>
</table>

[![PyPI](https://img.shields.io/pypi/v/aquamvs)](https://pypi.org/project/aquamvs/)
[![Python](https://img.shields.io/pypi/pyversions/aquamvs)](https://pypi.org/project/aquamvs/)
[![CI](https://github.com/McGrathLab/AquaMVS/actions/workflows/test.yml/badge.svg)](https://github.com/McGrathLab/AquaMVS/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Dataset DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18702024.svg)](https://doi.org/10.5281/zenodo.18702024)

# AquaMVS

Multi-view-stereo (MVS) reconstruction of underwater surfaces viewed through a flat water surface, with Snell's law refraction modeling.

## Status
AquaMVS is available on [PyPI](https://pypi.org/project/aquamvs/). The API is considered stable; breaking changes will follow semantic versioning.

## What it does

AquaMVS is a companion library to [AquaCal](https://github.com/tlancaster6/AquaCal). It consumes calibration output and synchronized video from above-water cameras to produce time-series 3D surface reconstructions. The pipeline handles the unique challenge of cameras positioned in air observing underwater geometry, accounting for refraction at the air-water interface using Snell's law.

## Key Features

- **Refractive ray casting** through air-water interface (Snell's law)
- **Dual matching pathways**: LightGlue (sparse) and RoMa v2 (dense) for different accuracy/speed tradeoffs
- **Multi-view depth fusion** with geometric consistency filtering
- **Surface reconstruction** (Poisson, heightfield, Ball Pivoting Algorithm)
- **Mesh export** (PLY, OBJ, STL, GLTF) with simplification
- **Full CLI and Python API** for pipeline users and custom workflow developers

## Quick Start

```python
from aquamvs import Pipeline

pipeline = Pipeline("config.yaml")
pipeline.run()
```

See the [full documentation](https://aquamvs.readthedocs.io/) for configuration details, API reference, and examples.

## Installation

AquaMVS requires several prerequisites (PyTorch, LightGlue, RoMa v2) to be installed first. AquaCal is installed automatically as a dependency.

**See [INSTALL.md](INSTALL.md) for complete installation instructions.**

Quick summary:
```bash
# 1. Install PyTorch from pytorch.org
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 2. Install git-based prerequisites (LightGlue, RoMa v2).
#    RoMa v2 must be installed --no-deps, or pip replaces your torch (see INSTALL.md)
pip install -r requirements-prereqs.txt
pip install --no-deps -r requirements-romav2.txt

# 3. Install AquaMVS (pulls AquaCal automatically)
pip install aquamvs
```

## Documentation

Full documentation is available at [https://aquamvs.readthedocs.io/](https://aquamvs.readthedocs.io/)

Topics include:
- Installation guide
- Configuration reference
- API documentation
- Usage examples
- Extension points for custom workflows

## Validation

AquaMVS's geometric accuracy has been validated against independent ChArUco
calibration-board ground truth, recovered from the boards without using the MVS
reconstruction it assesses. On the ground-truth set (13 cameras, 10 board poses,
AquaMVS 1.7.2 with RoMa v2 and an AquaCal 2.1.0 calibration), the reconstruction gives:

| Metric | Value |
|---|---|
| Board flatness (RMS) | 1.11 mm |
| Rigid-fit corner error (inlier RMSE) | 1.08 mm |
| Lateral / range error (RMS) | 0.53 / 1.78 mm |
| Absolute scale error | +0.064 % |

- Analysis code, reproducing every figure and number in the paper:
  [McGrathLab/AquaMVS_gtanalysis](https://github.com/McGrathLab/AquaMVS_gtanalysis)
- Ground-truth dataset: [10.5281/zenodo.21134748](https://doi.org/10.5281/zenodo.21134748)

AquaMVS 1.7.3 reproduces the 1.7.2 reconstruction bit for bit (checked on the
ground-truth set's first frame); its changes are to installation, headless rendering and
CPU device handling.

## Citation

If you use AquaMVS in your research, please cite the software (machine-readable
metadata in [CITATION.cff](CITATION.cff); GitHub's "Cite this repository" button uses it):

```
Lancaster, T. (2026). AquaMVS: Multi-view stereo reconstruction of underwater surfaces
with refractive modeling [Computer software]. https://github.com/McGrathLab/AquaMVS
Example dataset: https://doi.org/10.5281/zenodo.18702024
```

A paper describing AquaMVS is under review; this section will cite it once published.

## License

AquaMVS is released under the MIT License. See [LICENSE](LICENSE) for details.

### Third-party components and commercial use

AquaMVS vendors no third-party source code or model weights; all optional
components are installed separately at the user's request. The out-of-the-box
configuration is fully MIT/permissive: the default matcher is **RoMa v2** (MIT)
and the default feature extractor is **ALIKED** (BSD-3-Clause).

The optional **SuperPoint** extractor (reachable via LightGlue by setting
`extractor_type: superpoint`) is provided under Magic Leap's non-commercial
academic-research-only license. It is *not* a default. **Commercial users
should select ALIKED (BSD-3) or DISK (Apache-2.0) instead of SuperPoint.**

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for the full breakdown.
