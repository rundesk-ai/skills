# What these rules rest on

Use this file to audit a rule, not as more workflow. Each entry says what it establishes and what it
does not.

## Practice recorded from production work

The build order, the part tests, the parts catalog, the pivot and manifest contracts and the exact
arithmetic at mating vertices are **recorded practice** from production kits. They are not measurements, and no controlled
comparison establishes that a kit built this way is better than one built another way.

Where a rule states a mechanism rather than a preference, the mechanism is checkable and worth
checking yourself:

- **Hairline light leaks and z-fighting** follow from floating-point representation, not from
  judgment. Accumulated addition carries rounding error forward; integers and exact halves are
  representable in binary floating point and most decimal fractions are not.
- **A divisor in an assembler** scales every instance by the ratio between the authored dimension and
  the one the code expects. This is arithmetic, and it is silent.
- **Auto-centering a pivot on visible bounds** moves the origin whenever the visible bounds change,
  which is every time the part is revised.

## Generated imagery

The source-candidate rule, the refusal list and the consistency requirements are **inferences drawn
from recorded intake work**, not vendor guarantees and not measured results.

What is established: generated output that must decompose into registered parts frequently cannot,
and a reused seed does not hold a family together on its own. What is not established: that an
automatic detector exists for each refusal in the list, or that a generated image can never be used
directly. Decomposability and intended use decide that, case by case.

## What is not settled here

- **Polygon budgets, LOD strategy and baking.** These follow from the consumer and the camera, and
  nothing here sets a number.
- **Whether a material channel may be inferred from a color image.** Assign broad color to albedo,
  relief to normal or height, reflectance variation to roughness and deliberate wear to masks — but
  treat a plausible color image as evidence for none of the other channels.
- **Rights.** A tool's label is not a license, and "free" is not a license. Record provenance and
  treat acceptance as a separate gate.

## Re-check when

- The consumer changes how it places or scales pieces: the pivot and mating dimensions follow from
  the assembler, and a new assembler can invalidate both.
- An image model changes behavior: the refusal list is about failure modes, and those move.
