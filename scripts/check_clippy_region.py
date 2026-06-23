"""
Scan a Cargo project for `main.rs` and `lib.rs` files and enforce a
standardized Clippy lint region.

This script searches recursively for Rust entrypoint files matching
`{main,lib}.rs`. For each file, it looks for a region delimited by:

    // #region clippy
    ... lint attributes ...
    // #endregion

If the region exists but its contents differ from the canonical lint
block defined in this script, the file is updated in-place unless
`--check` is used.

Behavior:
    • Without flags:
        - Automatically rewrites mismatched regions to the canonical lint block.
        - Exits with status 0.

    • With `--check`:
        - Performs the same scan but does NOT modify any files.
        - Exits with status 1 if any file differs from the expected region.
        - Exits with status 0 if all files are compliant.

Workspace detection:
    If no explicit path is provided, the script walks upward from the
    current working directory to locate the nearest Cargo project or
    workspace root (equivalent to `cargo locate-project --workspace`).

Intended use:
    - Enforce strict lint hygiene across a workspace.
    - Integrate into CI to ensure no file drifts from the required lint set.
"""

import glob
from pathlib import Path
import tomllib


REGION_START = "// #region clippy"
REGION_BODY = """\
#![forbid(unsafe_code)]
#![warn(clippy::todo)]
#![deny(
    // Panic hygiene
    clippy::panic,
    clippy::panic_in_result_fn,
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::unimplemented,

    // API hygiene
    missing_docs,
    clippy::missing_errors_doc,
    clippy::missing_panics_doc,
    clippy::missing_safety_doc,
    clippy::undocumented_unsafe_blocks,

    // Slop prevention
    clippy::dbg_macro,
    clippy::print_stdout,
    clippy::print_stderr,
    clippy::allow_attributes_without_reason,
    clippy::unnecessary_safety_comment,
    clippy::unreachable,
    clippy::empty_loop,
    clippy::needless_borrow,
    clippy::needless_pass_by_value,

    // Future-proofing
    clippy::large_enum_variant,
    clippy::large_stack_arrays,
    clippy::alloc_instead_of_core,
    clippy::std_instead_of_core,
    clippy::std_instead_of_alloc,

    // Performance hygiene
    clippy::inefficient_to_string,
    clippy::map_clone,
    clippy::map_collect_result_unit,
    clippy::slow_vector_initialization,
    clippy::redundant_clone,

    // Correctness
    clippy::match_wildcard_for_single_variants,
    clippy::indexing_slicing,
    clippy::match_same_arms,
    clippy::bool_comparison,
    clippy::let_unit_value,
)]\
""".splitlines()
REGION_END = "// #endregion"

def _do_check(directory: Path, check : bool = False) -> bool:
    any_body_diffrent = False
    # search for 
    files = glob.iglob(str(directory.joinpath("**","{main,lib}.rs")))

    for path in files:
        with open(path, "rt") as file:
            lines = file.readlines()
        region_start = lines.index(REGION_START) or 0
        region_end = lines.index(REGION_END, region_start) or 0
        body_diffrent = lines[region_start:region_end] != REGION_BODY
        any_body_diffrent |= body_diffrent 
        if not check and body_diffrent:
            new_lines = (
                *lines[:region_start],
                REGION_START,
                *REGION_BODY,
                REGION_END,
                *lines[region_end:]
            )
            with open(path, "wt") as file:
                file.writelines(new_lines)    
    return any_body_diffrent




def _find_cargo_project_dir() -> Path:
    """
    Pure-Python equivalent of:
        cargo locate-project --workspace --message-format=plain

    Starting from cwd, walk upward looking for Cargo.toml.
    If a Cargo.toml contains a [workspace] table, that directory
    is the workspace root. Otherwise, return the nearest Cargo.toml.
    """
    cwd = Path.cwd()
    nearest_project = None

    for directory in [cwd, *cwd.parents]:
        cargo_toml = directory / "Cargo.toml"
        if not cargo_toml.is_file():
            continue

        # Record the nearest Cargo.toml in case no workspace root is found
        if nearest_project is None:
            nearest_project = directory

        # Check if this Cargo.toml defines a workspace
        try:
            with cargo_toml.open("rb") as f:
                data = tomllib.load(f)
        except Exception:
            # If unreadable, skip it but keep searching upward
            continue

        if "workspace" in data:
            return directory

    if nearest_project is not None:
        return nearest_project

    raise RuntimeError("No Cargo.toml found in this directory or its parents")

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="Path to process")
    parser.add_argument("--check", action="store_true", help="Run in check mode")
    return parser.parse_args()

import sys
import argparse
def main():
    args = _parse_args()

    check = args.check
    workspace = args.path or _find_cargo_project_dir()
    any_body_diffrent = _do_check(workspace)

    if any_body_diffrent and check:
        sys.exit(1)
