# LizeLive's Rust Style Guide




## architecture
- use sub crates to help improve build speed + scache
- use `_` for crate names eg `physics_types`
- subcrates go into `crates/` directory
- every subcrate has `README.md`
- minimize symbols exposed by crates
- lib.rs only declares modules and exposes
- crates depend directly on what they need (avoid workspace deps)
- avoid unsafe code. when not avoidable, create dedicated crate to help.
- for ffi have `$name_sys` libary that is the raw FFI and `$name` that is nice wraper.

## linter
see `clippy.toml` and `

## ecosystem
- wgpu for graphics
- serde for serlization
- 

## git 
