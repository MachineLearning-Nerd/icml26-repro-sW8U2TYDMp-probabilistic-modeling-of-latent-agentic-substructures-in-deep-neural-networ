import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Claim-level reproduction: latent agentic substructures

    **Evidence first.** The current package obtains five `VERIFIED`
    statuses and one assumption-satisfying `FALSIFIED` status. These are
    evidence assessments; the live judge score remains **7/12** until the
    published revision is evaluated.

    ![Headline claim results](https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/main/reports/claim-reproduction/images/headline.svg)
    """)
    return


@app.cell
def _():
    results = {
        "Claim 1 · log score": {
            "status": "VERIFIED",
            "paper": "U(o)=log P(o), and expected utility is −H(P).",
            "observed": "Maximum pointwise and entropy-identity errors: 0.0.",
            "control": "Replacing log P(o) by P(o) is detected.",
        },
        "Claim 2 · linear pooling": {
            "status": "VERIFIED",
            "paper": "Strict unanimity is impossible for any finite outcome space.",
            "observed": "Symmetric-KL certificate; independent residual 1E−70.",
            "control": "Dropping reverse KL breaks the identity; clones remove strictness.",
        },
        "Claim 3 · logarithmic pooling": {
            "status": "VERIFIED",
            "paper": "Strict unanimity exists with at least three outcomes.",
            "observed": "Predeclared ε=10⁻⁵ witness; minimum gap 1.11675e−4.",
            "control": "Linear pooling flips the signs; binary grid has zero strict cases.",
        },
        "Claim 4 · Waluigi wording": {
            "status": "FALSIFIED",
            "paper": "Broad paraphrase: manifesting Luigi necessarily strengthens Waluigi.",
            "observed": "Aligned-duplicate transfer gives ΔW=0 and pool shift 0.",
            "control": "Removing the aligned-downweight term yields a false inequality.",
        },
        "Claim 5 · shattering": {
            "status": "VERIFIED",
            "paper": "A novel event-correlated direction gives stricter suppression.",
            "observed": "First-order gain 0.03660254; finite tilts converge.",
            "control": "Inside-span and event-orthogonal directions remove strictness.",
        },
        "Claim 6 · recursive split": {
            "status": "VERIFIED",
            "paper": "A parent's benefit need not propagate to every child.",
            "observed": "Parent +0.128975; compatible child −2.620105 at λ=8.",
            "control": "Clone stays positive; incompatible tilt breaks both invariants.",
        },
    }
    return (results,)


@app.cell
def _(mo, results):
    claim = mo.ui.dropdown(
        options=list(results),
        value="Claim 2 · linear pooling",
        label="Inspect one exact claim contract",
    )
    claim
    return (claim,)


@app.cell
def _(claim, mo, results):
    selected = results[claim.value]
    mo.md(
        f"""
        ## {claim.value}

        **Evidence status:** `{selected["status"]}`

        **Paper statement tested.** {selected["paper"]}

        **Observed evidence.** {selected["observed"]}

        **Negative control.** {selected["control"]}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why Claim 2 needs a certificate

    A random search can fail to find strict unanimity without proving
    impossibility. For a linear pool \(P=\sum_i\beta_iP_i\), define

    \[
    \Delta_i
      = \mathbb E_P[\log P_i]-\mathbb E_{P_i}[\log P_i].
    \]

    Direct expansion gives

    \[
    \sum_i\beta_i\Delta_i
      =-\sum_i\beta_i\left[
        D_{\mathrm{KL}}(P_i\Vert P)+D_{\mathrm{KL}}(P\Vert P_i)
      \right].
    \]

    Gibbs' inequality makes the right side strictly negative unless every
    belief is identical; identical beliefs give all gaps exactly zero.
    Thus strict unanimity is impossible over the complete stated domain.
    The executable fixtures audit this derivation but do not replace it.
    """)
    return


@app.cell
def _(mo):
    epsilon = mo.ui.slider(
        start=0.01,
        stop=0.25,
        step=0.01,
        value=0.20,
        label="First-order intervention budget ε",
    )
    epsilon
    return (epsilon,)


@app.cell
def _(epsilon, mo):
    pure = epsilon.value * 0.25
    shatter = epsilon.value * 0.4330127018922193
    gain = shatter - pure
    mo.md(
        f"""
        ## Bounded interaction: Claim 5's first-order geometry

        The fixture's projection norms are fixed by the published evidence.
        At budget **{epsilon.value:.2f}**:

        | Available span | Maximum first-order event reduction |
        |---|---:|
        | pure benevolence | `{pure:.8f}` |
        | benevolence + novel Waluigi direction | `{shatter:.8f}` |
        | strict gain | **`{gain:.8f}`** |

        The formal verifier independently reconstructs the weighted Gram
        projection and checks the Pythagorean identity. This slider only
        illustrates its linear budget scaling; it is not formal evidence.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Reproduction boundary

    The formal command is fixed across all experiment nodes:

    ```bash
    uv sync --locked --no-dev && .venv/bin/python -m reproduction.run_all
    ```

    It uses one CPU thread and completed in 0.295 verifier seconds. The
    notebook embeds the already-produced results, so opening it does not
    rerun formal experiments. Full contracts, code, raw JSON, independent
    checker outputs, and controls are linked from the
    [illustrated report](https://github.com/MachineLearning-Nerd/icml26-repro-sW8U2TYDMp-probabilistic-modeling-of-latent-agentic-substructures-in-deep-neural-networ/blob/main/reports/claim-reproduction/report.md).

    Remaining interpretation risk is concentrated in the breadth of the
    Claim 4 paraphrase and Claim 5's first-order scope. Nothing here claims
    to identify a latent agent in a trained neural network.
    """)
    return


if __name__ == "__main__":
    app.run()
