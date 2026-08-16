# Pinned Opentrons simulator contract

This evaluator environment supports LS09-1. Protocol API 2.16 was introduced in Robot Software 7.1.0, so the Python package is pinned to `opentrons==7.1.0`.

## Reference environment

- CPython 3.10.x
- Linux x86_64, manylinux2014-compatible
- exact dependency versions and wheel hashes in `requirements-linux-x86_64-py310.lock`
- lock-file SHA-256: `3af81dcdb8953713e370ae8d69896ec45d075a9a1c76adf6b191b942c41902dd`
- simulator invocation: `python -m opentrons.simulate output/protocol.py`

Provision this environment before the timed run. Install with `pip --require-hashes` from an evaluator-cached wheelhouse, then record Python version, platform, `pip freeze`, lock-file SHA-256, and a smoke-test result. Do not relax hashes or download packages during a timed task.

This lock defines the environment but does not itself prove cross-harness availability. LS09-1 remains blocked until Codex C0 and every scheduled Duanyan arm use the same environment contract and a real simulator reference passes 3/3 while wrong and empty controls fail.

Opentrons is Apache-2.0. Official simulator usage is documented by Opentrons at <https://github.com/Opentrons/opentrons/blob/edge/api/README.rst>.
