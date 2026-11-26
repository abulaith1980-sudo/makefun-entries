/**
 * One Word, First Thought — make.fun entry.
 *
 * Writes the first word that came to mind to /output/entry.txt.
 *
 * The word is Petrichor: the smell of rain on dry earth. It is
 * surprising rather than safe, vivid enough to call up a whole
 * afternoon in eight letters, and it carries a small spark of wit —
 * a word most people have smelled a hundred times and never knew had
 * a name. First thought, no second draft.
 *
 * Deterministic by design: no input, no clock, no randomness and no
 * network, so two runs write byte-identical output.
 */

import { mkdirSync, writeFileSync, chmodSync } from "node:fs";
import { join } from "node:path";

// The first word that came to mind, kept as one literal.
const WORD = "Petrichor";

function main(): number {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const outPath = join(outDir, "entry.txt");

  const word = WORD.trim();
  if (!/^[A-Za-z]+$/.test(word) || word.length < 1 || word.length > 24) {
    console.error("word fails the gate: exactly one word, 1-24 chars");
    return 1;
  }

  mkdirSync(outDir, { recursive: true });
  // No trailing newline: the file holds exactly one word and nothing else.
  writeFileSync(outPath, word, { encoding: "utf-8" });
  // The grader collects outputs as another user: leave it world-readable.
  chmodSync(outPath, 0o644);
  console.log(word);
  return 0;
}

process.exitCode = main();
