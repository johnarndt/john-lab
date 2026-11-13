---
name: reaction-hook-videos
description: Research recent short-form hooks for a business, write original variants, generate swappable AI character reactions with fal, Replicate, Sunra, or Grok Imagine, and cut each reaction onto one real product demo. Use to deliver polished, post-ready TikTok and Instagram Reels videos.
---

# Reaction Hook Videos

Deliver finished vertical MP4s, with a short caption and suggested cover frame for each. The reusable timeline is a reaction and a hook line, followed by one real recording that delivers on the hook. Research-only and scripting requests can stop at the requested stage.

## 1. Find the business's proof

Read the supplied website, product page, and recording. Identify the intended viewer, their specific problem, one verifiable benefit, the exact demo moment that proves it, and the desired next action. Record the proof timestamp. Use supplied brand cues or derive the tone and colors from the business. If no usable recording exists, capture a permitted demo in a clean account with sample data, or request the footage needed for an accurate final edit. For a physical product or service, use an equivalent owned product demonstration. Keep the original source file.

## 2. Research the first few seconds

- Search recent native TikToks and Reels for the buyer's problem, comparable products, and adjacent niches. Start with the last 30 days and widen the window when the niche is sparse. Use [TikTok Creative Center Top Ads](https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en) for paid examples and the owner's analytics for their own posts when available. Sample across several creators and include ordinary comparables where possible.
- For each useful clip, record the original URL, date, platform, paid or organic context, what happens in the opening seconds, how it hands off to proof, and the metric you actually observed with its capture date. Use early retention when available. Compare like metrics within comparable groups and check creator baselines when visible. Treat public counts as signals. When a clip or metric is unavailable, mark it unavailable. Rank the evidence by relevance and quality and identify which mechanics look promising for this business.
- Write original hooks that fit the visible payoff. Test different ideas such as a recognizable mistake, a visual reveal, a specific question, or a before-and-after. Score audience fit, clarity on mute, and match to the proof frame. Keep a short caption, a distinct reaction beat, and a demo start time for each candidate. Use the owner's exact wording when supplied. Draw inspiration from the opening structure and write fresh copy, visuals, and audio.

## 3. Generate the reactions

Default to three distinct edits unless the user gives a count. Use one fictional adult character and a consistent camera look for the first comparison. Put the expression in motion at frame one, time its peak to the hard cut, and keep the shot usable at about 1–3 seconds. When the provider has a longer minimum duration, request one continuous shot and trim the strongest moment. Place the face away from planned text, use natural motion and phone-camera framing, and keep generated captions and logos out of the clip. Keep references and look consistent across batches. Use likeness or voice references with permission, and write the character as a presenter without a fabricated customer story.

Use the connected provider the user names. Otherwise choose an available route with suitable reference control, vertical output, and cost. Check its current model schema, output limits, and price. Apply the user's authorized spend and any provider confirmation requirements. For a large batch, prove the first edit before committing the remaining budget. Keep the selected payer, count retries against the budget, and recover submitted job IDs after timeouts.

- **fal** — Find a suitable [image-to-video model](https://fal.ai/explore/image-to-video-apis). Use its model-specific input schema with the fal client. For queued jobs, save the request ID, check status, retrieve the result, and download the clip.
- **Replicate** — Pick a model from the [image-to-video collection](https://replicate.com/collections/image-to-video). Use the model's documented prediction input and endpoint, record the prediction ID, poll to completion, and save the video locally.
- **Sunra** — Run `sunra tools`, follow payer and credit guidance, and inspect `list_models` and `get_model_schema`. Use `create_video`, confirm the quoted run as required, and recover the file through `get_job`.
- **Grok Imagine** — Use [xAI's current video API](https://docs.x.ai/developers/model-capabilities/video/overview) or an existing connected Grok Imagine route. Choose image-to-video for a reference portrait or text-to-video for a fresh character. Save the request ID, poll for completion, and download the temporary output promptly.

Reuse approved reactions from the same project when they suit the hook. Keep a record of each prompt, reference, model, request ID, local clip, and generation cost. Give the provider only the inputs it needs. Assemble the real demo locally. If generation is unavailable, use suitable authorized footage or state what is needed to complete the edit.

## 4. Edit, watch, and deliver

- Open immediately on the reaction and a short, legible hook. Cut directly into the product action at the payoff. Keep the most important UI readable at phone size. Reframe a wide recording around the relevant UI when needed. Use a restrained brand type treatment, high contrast, deliberate caption placement clear of faces and feed controls, and a single relevant next action. Time captions to speech if used. Keep voice clear and use music or sound effects only where they support the edit and are cleared for use.
- Render a 1080 × 1920 H.264/AAC MP4 for each variant. The bundled local renderer gives repeatable cuts, optional timed text, a soft demo background for mismatched aspect ratios, and audio leveling. Use your editor for custom motion, reframing, or more complex audio. For a clean comparison, keep the proof segment and CTA fixed while changing the hook or reaction, one at a time where feasible.
- Watch each export at phone size, with sound and muted. Inspect the first frame, both sides of the cut, proof, and ending. Fix awkward expressions, clipped captions, covered UI, audio jumps, dead frames, and watermarks. Check TikTok/Reels preview safe areas and current AI labeling rules for the intended placement. Include any applicable disclosure in the handoff. See [TikTok guidance](https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content) and [Meta guidance](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/).
- Hand over the final MP4s, one caption and cover frame time per variant, and a compact source and variant log. If the owner later supplies post metrics, compare early retention, completion, and the campaign's conversion or click metric for comparable audiences. Use the results to choose the next batch. Publish only when the user authorizes posting.

## Local renderer

Requires Python 3 and FFmpeg with ffprobe, libx264, and libass. Place files next to a JSON manifest or use absolute paths. Times are seconds. Use `demo_crop: [x, y, width, height]` in displayed source pixels to frame a wide demo around the action. A variant can override the shared `demo_start`, `demo_duration`, or `demo_crop`. Set `hook` to a string or to an object with `text` and `position`. Optional `captions` on a variant are timed from the start of the final video and can style text as `top`, `lower`, or `center`. Supply short lines and check placement in the render. Use `reaction_audio: false` to mute the reaction, or use an audio track in an editor before the final export.

```json
{
  "demo": "product-demo.mp4",
  "demo_start": 4,
  "demo_duration": 9,
  "font": "Arial",
  "variants": [
    {
      "id": "reveal",
      "reaction": "reactions/reveal.mp4",
      "reaction_start": 0.3,
      "reaction_duration": 2.1,
      "reaction_audio": false,
      "hook": "Where did that renewal go?",
      "captions": [
        {"start": 8, "end": 11, "text": "See every upcoming renewal", "position": "lower"}
      ]
    }
  ]
}
```

Run `python3 <skill-folder>/scripts/render.py batch.json --out exports`. Use `--only reveal` to render one variant. Output files are named by variant ID. Move a previous export or use a fresh output directory for revisions.
