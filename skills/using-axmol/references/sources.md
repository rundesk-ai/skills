# Axmol source basis

Use these sources to audit or update a rule, not as more procedure. v2 implementation claims were
checked against tag `v2.11.4`.

## Version and scope

- [GitHub releases API](https://api.github.com/repos/axmolengine/axmol/releases) and the
  [v2.11.4 release](https://github.com/axmolengine/axmol/releases/tag/v2.11.4) establish that
  v2.11.4 as an LTS release. They do not establish that no later v2 minor can ship.
- [About the upcoming Axmol v3](https://github.com/axmolengine/axmol/wiki/About-RHI-in-Axmol-v3)
  states that v3 remains in active development and recommends v2 when a stable release is required.
- [Axmol v2.11.4 README](https://github.com/axmolengine/axmol/blob/v2.11.4/README.md) and
  [Axmol versus Cocos2d-x](https://github.com/axmolengine/axmol/wiki/Axmol-vs-Cocos2d%E2%80%90x)
  establish the fork, C++20 line, platforms, and backends. The skill does not repeat that feature
  inventory because it does not change execution.

## Memory

- [Memory Management](https://github.com/axmolengine/axmol/wiki/Memory-Management) establishes the
  initial reference count, balanced `retain()`/`release()`, autorelease timing, `create()` convention,
  parent ownership, `RefPtr`, and engine containers. Its `AX_REF_LEAK_DETECTION` name is stale for
  the pinned release; v2.11.4 source uses `AX_OBJECT_LEAK_DETECTION`, so the skill follows the tagged
  implementation. The worked leak and dangling examples are the basis for [memory.md](memory.md).
- Tagged source confirms the contract in
  [`Object.cpp`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/base/Object.cpp),
  [`RefPtr.h`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/base/RefPtr.h), and
  [`Vector.h`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/base/Vector.h).

## Graphics

- [Shaders in Axmol 2.x](https://github.com/axmolengine/axmol/wiki/Shaders-in-Axmol-2.x)
  establishes accepted shader languages, generated variants, the one non-sampler uniform block per
  stage rule, `#include`, custom-shader batching behavior, and `updateBatchId()` conditions.
  [Shaders in Axmol 3](https://github.com/axmolengine/axmol/wiki/Shaders-in-Axmol3) establishes that
  v3 uses a different authoring and binding model.
- [The GLSL 4.50 specification](https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.50.pdf),
  section 3.3, requires `#version` before anything except whitespace or comments. The rule keeps
  the conservative line-one form; a leading comment is permitted by the specification.
- [Sprite Sheets: Tools and Formats](https://github.com/axmolengine/axmol/wiki/Sprite-Sheets-Tools-and-Formats)
  establishes the global frame-name collision and prefix/subdirectory replacements.
- Tagged [`Texture2D.cpp`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/renderer/Texture2D.cpp#L610-L640)
  establishes that `setAliasTexParameters()` selects nearest sampling and
  `setAntiAliasTexParameters()` selects linear sampling. NASA Earth Observatory's practitioner note
  [Design basics: anti-aliasing](https://earthobservatory.nasa.gov/blogs/elegantfigures/2010/09/24/163/)
  explains why blended resampling, unlike nearest-neighbor, preserves antialiased detail when an
  image is reduced. An anonymized first-hand Axmol v2.11.3 record reproduced the scaled-UI symptom;
  the tagged source and practitioner guidance establish the scoped replacement.
- [SDF text rendering](https://github.com/axmolengine/axmol/wiki/SDF-text-rendering) establishes the
  outline ranges and the coupled spread/shader scale.

## Scene, input, and physics

- Tagged [`RenderView.cpp`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/platform/RenderView.cpp)
  establishes the exact v2.11.4 resolution-policy behavior of frame, design, visible size, and
  visible origin.
- Tagged [`StencilStateManager.cpp`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/base/StencilStateManager.cpp)
  implements nested stencil layers, and the engine ships a
  [`NestedTest`](https://github.com/axmolengine/axmol/blob/v2.11.4/tests/cpp-tests/Source/ClippingNodeTest/ClippingNodeTest.cpp).
  Together they show nested `ClippingNode` is supported, so a failure needs a reduced
  backend-specific reproduction. Tagged
  [`ClippingRectangleNode.cpp`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/2d/ClippingRectangleNode.cpp)
  establishes the scissor-based rectangular replacement.
- Tagged [`EventListenerMouse.h`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/base/EventListenerMouse.h)
  establishes the `bool` callbacks for v2.11.4. The
  [PR 3173 migration guide](https://github.com/axmolengine/axmol/wiki/Migration-Guide-for-PR-3173)
  establishes the v3 pointer/input replacements.
- Tagged [`EventListener.h`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/base/EventListener.h)
  establishes that node-associated listeners follow node enter/exit state while fixed-priority
  listeners do not; this is the basis for preferring node-bound listeners or explicit teardown.
- Tagged [`RenderViewImpl.cpp` dispatch](https://github.com/axmolengine/axmol/blob/v2.11.4/core/platform/RenderViewImpl.cpp#L1246-L1268)
  establishes the v2 desktop keyboard-before-IME order and unconsumed control-key fallback; its
  [`key map`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/platform/RenderViewImpl.cpp#L338-L342)
  maps GLFW Super to `KEY_HYPER`. Tagged
  [`TextFieldTTF.cpp`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/2d/TextFieldTTF.cpp#L254-L312) and
  [`TextFieldTTF.h`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/2d/TextFieldTTF.h#L225-L258)
  establish newline detachment and the absence of a cursor-position getter. Tagged
  [`Label.cpp` TTF configuration](https://github.com/axmolengine/axmol/blob/v2.11.4/core/2d/Label.cpp#L827-L830)
  and [`system-font sizing`](https://github.com/axmolengine/axmol/blob/v2.11.4/core/2d/Label.cpp#L2326-L2334)
  establish that `setSystemFontSize()` selects `STRING_TEXTURE` while `setTTFConfig()` preserves the
  TTF path. An
  anonymized first-hand Axmol v2.11.3 desktop record supplies the four symptoms and adopted
  replacements; v2.11.4 tagged source supplies their exact causes and confirms the paths remain.
- [FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) documents Android interception of three-or-more
  point gestures and the resulting missing terminal touch event.
- [2D Physics Engines](https://github.com/axmolengine/axmol/wiki/2D-Physics-Engines-Information)
  establishes that content size cannot change after a body is attached and that animation frames
  must therefore share a size.

## Setup, build, and extensions

- Tagged [DevSetup](https://github.com/axmolengine/axmol/blob/v2.11.4/docs/DevSetup.md) and the
  [FAQ](https://github.com/axmolengine/axmol/wiki/FAQ) establish `setup.ps1`, platform setup options,
  PowerShell policy handling, source-glob regeneration, and the branch/axslcc mismatch diagnosis.
- [Introduction to Game Development using Axmol](https://github.com/axmolengine/axmol/wiki/Introduction-to-Game-Dev-using-Axmol)
  tells users to modify their generated project rather than the engine or template tree; this is the
  source for keeping project changes outside the pinned submodule.
- [Extensions](https://github.com/axmolengine/axmol/wiki/Extensions) and the tagged
  [`AXGameEngineOptions.cmake`](https://github.com/axmolengine/axmol/blob/v2.11.4/templates/common/cmake/modules/AXGameEngineOptions.cmake)
  establish extension flags and defaults; inspect the pinned file when an extension task needs them.
- Community discussion
  [Axmol build time improvement #1814](https://github.com/axmolengine/axmol/discussions/1814)
  records a 7–15 minute Xcode rebuild, an optional ccache mitigation, a maintainer's failure to
  reproduce it, and advice to keep project inputs out of generated build directories. It does not
  support calling ccache the fix or prescribing another generator universally.

## Migration

- [Cocos2d-x migration guide](https://github.com/axmolengine/axmol/wiki/Cocos2d%E2%80%90x-migration-guide)
  establishes the compatibility header, modernized names/types, and `axmol-migrate`'s v4.0 scope and
  warning for older projects.
- In community discussion
  [Using Axmol as a replacement engine #1129](https://github.com/axmolengine/axmol/discussions/1129),
  maintainer rh101 recommends generating a new Axmol project and moving code/resources because the
  CMake and Android files differ materially. This is the preferred port replacement in
  [migration.md](migration.md).
- [PR 3173 migration guide](https://github.com/axmolengine/axmol/wiki/Migration-Guide-for-PR-3173)
  establishes the v3 input, text, keyboard, and label replacements. Later
  [PR 3228 guidance](https://github.com/axmolengine/axmol/wiki/Migration-Guide-for-PR-3228) shows that
  pointer APIs continued changing, which is why the skill requires the pinned headers.
- [Axmol v3 roadmap #2650](https://github.com/axmolengine/axmol/discussions/2650) records planned and
  in-progress removals, C++23, RHIs, physics, and platform work. It is a roadmap discussion, not a
  release contract.

## Architecture and practitioner evidence

- [Game Programming Patterns: Decoupling Patterns](https://gameprogrammingpatterns.com/decoupling-patterns.html)
  explains why reducing coupling makes a codebase easier to change and understand. Combined with
  Axmol's documented ownership/runtime model, it supports keeping engine types at the presentation
  seam.

## License

Copyright (c) 2026 Rundesk AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
