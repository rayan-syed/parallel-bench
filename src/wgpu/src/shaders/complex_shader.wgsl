@group(0) @binding(0) var<storage, read> A: array<f32>;
@group(0) @binding(1) var<storage, read> B: array<f32>;
@group(0) @binding(2) var<storage, read_write> out: array<f32>;

@compute @workgroup_size({{WORKGROUP_SIZE}})
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let i: u32 = id.x;
    if (i >= arrayLength(&out)) { return; }

    let ai: f32 = A[i];
    let bi: f32 = B[i];
    let prod: f32 = ai * bi;

    // heavy math
    var v: f32 = prod + f32(i) * 1e-4 + 1.0;
    for (var outer: u32 = 0u; outer < 128u; outer = outer + 1u) {
        for (var inner: u32 = 0u; inner < 16u; inner = inner + 1u) {
            v = sin(v) + cos(v) * sqrt(abs(v) + 1.0);
        }
    }

    // force branch
    if (v > 0.0) {
        out[i] = prod;
    } else {
        out[i] = prod;
    }
}
