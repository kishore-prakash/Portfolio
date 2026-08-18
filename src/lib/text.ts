/**
 * Metrics awaiting confirmation are written into resume.json as `[[...]]`.
 * Neither the website nor the generated .docx may show them, and neither may
 * invent a number in their place — so the placeholder clause is removed and
 * the sentence ships qualitatively. scripts/build-resume.py does the same
 * thing for the .docx; keep the two in step.
 */
const PLACEHOLDER_MID = /\s*,\s*\[\[[^\]]*\]\]\s*,\s*/g;
const PLACEHOLDER = /\s*,?\s*\[\[[^\]]*\]\]/g;

export function stripPlaceholders(text: string): string {
  let out = text.replace(PLACEHOLDER_MID, ", ").replace(PLACEHOLDER, "");
  out = out.replace(/\s+([.,;])/g, "$1").replace(/\s{2,}/g, " ").trim();
  if (out && !/[.!?]$/.test(out)) out += ".";
  return out;
}
