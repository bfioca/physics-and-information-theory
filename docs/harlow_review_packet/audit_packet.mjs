import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = dirname(fileURLToPath(import.meta.url));
const htmlPath = join(dir, "packet.html");
const pdfPath = join(dir, "finite_directional_observer_review_packet.pdf");
const emailPath = join(dir, "drafts", "outreach_email.md");
const diagramPath = join(dir, "dependency_diagram.svg");
const bibliographyPath = join(dir, "bibliography.md");
const manifestPath = join(dir, "artifact_manifest.json");

const html = readFileSync(htmlPath, "utf8");
const pdf = readFileSync(pdfPath);
const email = readFileSync(emailPath, "utf8");
const diagram = readFileSync(diagramPath, "utf8");
const bibliography = readFileSync(bibliographyPath, "utf8");
const failures = [];

function check(condition, message) {
  if (!condition) failures.push(message);
}

function segment(id) {
  const pattern = new RegExp(`<section[^>]+id="${id}"[\\s\\S]*?<\\/section>`, "m");
  const match = html.match(pattern);
  check(Boolean(match), `missing section #${id}`);
  return match?.[0] ?? "";
}

function textOnly(value) {
  return value
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&(?:nbsp|amp|lt|gt|mdash|ndash|alpha);/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function words(value) {
  return textOnly(value).split(/\s+/).filter(Boolean);
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

const sheets = html.match(/<section class="sheet/g) ?? [];
const note = segment("conceptual-note");
const questions = segment("review-questions");
const appendix = segment("technical-appendix-start") + html.split('id="technical-appendix-start"')[1];
const emailWords = email
  .replace(/^#.*$/gm, "")
  .replace(/^\*\*Subject:\*\*.*$/gm, "")
  .trim()
  .split(/\s+/)
  .filter(Boolean);
const fullEmailWords = email
  .replace(/^#.*$/gm, "")
  .replace(/[*_`#]/g, "")
  .trim()
  .split(/\s+/)
  .filter(Boolean);
const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
const internalTargets = [...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
const missingInternalTargets = internalTargets.filter((target) => !ids.has(target));
const pdfLatin1 = pdf.toString("latin1");
const pdfLinkCount = (pdfLatin1.match(/\/Subtype\s*\/Link\b/g) ?? []).length;

check(sheets.length === 9, `expected 9 explicit sheets, found ${sheets.length}`);
check((note.match(/class="equation"/g) ?? []).length === 3,
  "conceptual note must contain exactly 3 displayed equations");
check(words(note).length <= 1200,
  `conceptual note exceeds 1200 words (${words(note).length})`);
check(!/\b0\.\d{2,}\b/.test(textOnly(note)),
  "conceptual note contains an implementation-level numerical constant");
check((questions.match(/class="review-question"/g) ?? []).length === 3,
  "review page must contain exactly 3 review questions");
check((textOnly(questions).match(/\?/g) ?? []).length === 3,
  "review page must contain exactly 3 question marks");
check(emailWords.length <= 200, `email exceeds 200 words (${emailWords.length})`);
check(fullEmailWords.length <= 200,
  `email including subject exceeds 200 words (${fullEmailWords.length})`);
check(!/approve publication|approval for publication|endorse (?:the|this) paper/i.test(email),
  "email appears to request approval or endorsement");
check(/S_dir[^<]{0,80}(?:not|!=)[^<]{0,80}S_Ob|S_dir\s*!=\s*S_Ob/.test(html),
  "packet does not state that S_dir is distinct from S_Ob");
check(/(?:does not (?:yet )?exclude zero|no rigorous.{0,120}interval.{0,120}excludes? zero)/i.test(textOnly(html)),
  "packet does not state the current Weyl zero-exclusion boundary");
check(/common-action.{0,120}(?:open|missing)/i.test(textOnly(html)),
  "packet does not identify the common-action channel as open");
check(/fixed-background/i.test(html) && /not (?:a |the )?capacity bound/i.test(html),
  "packet does not distinguish the fixed-background witness from a capacity bound");
check(/\[PROVED\]/.test(appendix) && /\[CONDITIONAL\]/.test(appendix) && /\[OPEN\]/.test(appendix),
  "technical appendix is missing one or more status labels");
check((bibliography.match(/https:\/\/arxiv\.org\/abs\//g) ?? []).length === 12,
  "short bibliography must contain 12 primary arXiv links");
check(missingInternalTargets.length === 0,
  `HTML contains broken internal links: ${missingInternalTargets.join(", ")}`);
check(internalTargets.length >= 7,
  `expected at least 7 internal citations, found ${internalTargets.length}`);
check(/\[PROVED\]/.test(diagram) && /\[CONDITIONAL\]/.test(diagram) && /\[OPEN\]/.test(diagram),
  "dependency diagram is missing one or more status labels");
check(/S_dir != S_Ob/.test(diagram),
  "dependency diagram does not mark the S_dir/S_Ob dictionary as open");
check(pdf.subarray(0, 5).toString("ascii") === "%PDF-", "compiled output is not a PDF");
check(pdf.length > 100_000, `compiled PDF is unexpectedly small (${pdf.length} bytes)`);
const pageCount = (pdfLatin1.match(/\/Type\s*\/Page\b/g) ?? []).length;
check(pageCount === 9, `expected 9 PDF pages, found ${pageCount}`);
check(pdfLinkCount >= 19, `expected at least 19 PDF link annotations, found ${pdfLinkCount}`);
check(/\/Title \(Finite Directional Records as a Concrete Observer Model\)/.test(pdfLatin1),
  "compiled PDF is missing the expected title metadata");

const sourceFiles = [
  "packet.html",
  "README.md",
  "build_packet.sh",
  "audit_packet.mjs",
  "dependency_diagram.svg",
  "bibliography.md",
  "drafts/conceptual_note.md",
  "drafts/three_questions.md",
  "drafts/technical_appendix.md",
  "drafts/outreach_email.md",
  "claim_evidence_ledger.md",
  "literature_matrix.md",
  "source_verification_log.md",
  "adversarial_audit.md",
  "requirement_audit.md",
];

const manifest = {
  generated_at_utc: new Date().toISOString(),
  packet_pages: pageCount,
  conceptual_note_words: words(note).length,
  conceptual_note_equations: (note.match(/class="equation"/g) ?? []).length,
  review_questions: (questions.match(/class="review-question"/g) ?? []).length,
  email_words_excluding_heading_and_subject: emailWords.length,
  email_words_including_subject: fullEmailWords.length,
  internal_html_links: internalTargets.length,
  pdf_link_annotations: pdfLinkCount,
  files: {},
};

for (const relative of sourceFiles) {
  const data = readFileSync(join(dir, relative));
  manifest.files[relative] = { bytes: data.length, sha256: sha256(data) };
}
manifest.files["finite_directional_observer_review_packet.pdf"] = {
  bytes: pdf.length,
  sha256: sha256(pdf),
};

if (failures.length) {
  console.error("Packet audit failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`Packet audit passed: ${pageCount} pages, ${words(note).length} opening words, ` +
  `${emailWords.length} email words.`);
