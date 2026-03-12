import tensorflow as tf


def assemble_pressure_eigenvalues(Px, Py, Pz, Txy, Txz, Tyz):
    matrix = tf.stack(
        [
            tf.stack([Px, Txy, Txz], axis=-1),
            tf.stack([Txy, Py, Tyz], axis=-1),
            tf.stack([Txz, Tyz, Pz], axis=-1),
        ],
        axis=-2,
    )
    eigenvalues = tf.linalg.eigvalsh(matrix)
    return eigenvalues[:, 0], eigenvalues[:, 1], eigenvalues[:, 2]


def principal_stress_margins(rho, Px, Py, Pz, Txy, Txz, Tyz):
    lam1, lam2, lam3 = assemble_pressure_eigenvalues(Px, Py, Pz, Txy, Txz, Tyz)
    lam_min = tf.minimum(lam1, tf.minimum(lam2, lam3))
    zero = tf.zeros_like(lam_min)
    nec_margin = rho + lam_min
    wec_margin = rho + tf.minimum(lam_min, zero)
    dec_margin = rho - tf.maximum(tf.abs(lam1), tf.maximum(tf.abs(lam2), tf.abs(lam3)))
    sec_margin = rho + lam1 + lam2 + lam3
    return nec_margin, wec_margin, dec_margin, sec_margin
