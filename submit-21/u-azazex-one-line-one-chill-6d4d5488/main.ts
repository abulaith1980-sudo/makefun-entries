/**
 * One Line, One Chill — make.fun entry.
 *
 * Writes one line of horror to /output/entry.txt.
 *
 * The chill is specific and domestic: a smart speaker that answers a
 * question the reader only thought, then says "you're welcome" in a
 * voice nobody installed. Nothing is announced as scary — the dread
 * comes from the machine knowing more than it should, and being
 * polite about it. One sentence, one breath.
 *
 * Deterministic by design: no input, no clock, no randomness and no
 * network, so two runs write byte-identical output.
 */

import { mkdirSync, writeFileSync, chmodSync } from "node:fs";
import { join } from "node:path";

const SETUP = "My smart speaker answered a question I only thought";
const STING = "then added, 'you're welcome,' in a voice I never installed.";

function chillLine(): string {
  return `${SETUP}, ${STING}`;
}

function main(): number {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const outPath = join(outDir, "entry.txt");

  const line = chillLine();
  if (!line || line.length > 200 || line.includes("\n")) {
    console.error("line fails the gate: one line of 1-200 chars");
    return 1;
  }

  mkdirSync(outDir, { recursive: true });
  writeFileSync(outPath, line + "\n", { encoding: "utf-8" });
  // The grader collects outputs as another user: leave it world-readable.
  chmodSync(outPath, 0o644);
  console.log(line);
  return 0;
}

process.exitCode = main();
