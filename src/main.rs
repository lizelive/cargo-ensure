// #region clippy
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
)]
// #endregion
#![doc = include_str!("../README.md")]
fn main() {
    #![expect(clippy::print_stdout, reason = "uwu")]
    println!("Hello, world!");
}
