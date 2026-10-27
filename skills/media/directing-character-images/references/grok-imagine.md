# Grok Imagine

Read this when making character images with xAI's image models, through their API or an agent's
built-in image tools. Checked on 2026-10-27 against xAI's documentation and Grok Build 1.0.70's
bundled guidance; confirm names and limits in the current reference before relying on them.

- **Edit, do not generate, the recurring person.** The built-in tools are `image_gen` (new image
  from text) and `image_edit` (an existing image plus a prompt). Use `image_gen` only for the very
  first anchor of an invented person; every later image is `image_edit` from an accepted image.
- **Keep the face large in the reference.** References are downscaled before they reach the model,
  to roughly 768 pixels on the long side, so a face that is small in a wide shot carries little
  identity. Edit from a close or medium image of the person, or use a tight crop of the face as a
  second reference with the job "the face only".
- **Aspect ratio.** A single-image edit keeps the input's aspect ratio; `image_gen` offers 1:1,
  16:9, 9:16, 3:2 and 2:3. Make the anchor at the ratio the work needs, video keyframes included,
  rather than cropping later.
- **One clean reference beats several.** The edit tool accepts more than one image, but one strong
  reference of the person is more reliable; add a second only with a single named job.
- **Variations are separate calls.** There is no count parameter; each candidate is its own edit,
  logged as its own take.
- **Through the API**, the image model (`grok-imagine-image-2.0` at the time of checking) handles
  both generation and editing; the same rules apply.
