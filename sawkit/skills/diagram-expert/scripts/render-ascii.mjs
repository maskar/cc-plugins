#!/usr/bin/env node
/**
 * Render mermaid diagrams as ASCII art using beautiful-mermaid.
 *
 * Usage:
 *   echo '```mermaid\ngraph TD\n  A-->B\n```' | node render-ascii.mjs
 *   node render-ascii.mjs input.md
 *   node render-ascii.mjs --raw 'graph TD; A-->B'
 *
 * Supports: flowcharts, sequence, state, ER, class, XY charts.
 */

import { readFileSync } from 'fs';
import { createRequire } from 'module';

// beautiful-mermaid is installed globally; resolve via createRequire fallback
let renderMermaidASCII;
try {
  const mod = await import('beautiful-mermaid');
  renderMermaidASCII = mod.renderMermaidASCII;
} catch {
  try {
    const require = createRequire(import.meta.url);
    // Try global node_modules paths
    const globalPaths = [
      '/usr/local/lib/node_modules/beautiful-mermaid',
      '/usr/lib/node_modules/beautiful-mermaid',
      '/opt/homebrew/lib/node_modules/beautiful-mermaid',
      `${process.env.HOME}/.local/lib/node_modules/beautiful-mermaid`,
      `${process.env.HOME}/.npm-global/lib/node_modules/beautiful-mermaid`,
    ];
    let loaded = false;
    for (const p of globalPaths) {
      try {
        const mod = require(p);
        renderMermaidASCII = mod.renderMermaidASCII;
        loaded = true;
        break;
      } catch {
        // try next
      }
    }
    if (!loaded) {
      // Try NODE_PATH resolution
      const mod = require('beautiful-mermaid');
      renderMermaidASCII = mod.renderMermaidASCII;
    }
  } catch (err) {
    console.error('Error: beautiful-mermaid not found.');
    console.error('Install globally: npm install -g beautiful-mermaid');
    console.error(err.message);
    process.exit(1);
  }
}

function extractMermaidBlocks(text) {
  const blocks = [];
  const regex = /```mermaid\n([\s\S]*?)```/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    blocks.push(match[1].trim());
  }
  return blocks;
}

function renderBlock(code) {
  try {
    return renderMermaidASCII(code);
  } catch (err) {
    return `Error rendering diagram: ${err.message}`;
  }
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf8');
}

async function main() {
  const args = process.argv.slice(2);
  let input;

  if (args[0] === '--raw') {
    // Direct mermaid code as argument
    const code = args.slice(1).join(' ');
    console.log(renderBlock(code));
    return;
  }

  if (args.length > 0 && args[0] !== '-') {
    // Read from file
    input = readFileSync(args[0], 'utf8');
  } else {
    // Read from stdin
    input = await readStdin();
  }

  // Check if input contains fenced mermaid blocks
  const blocks = extractMermaidBlocks(input);

  if (blocks.length > 0) {
    blocks.forEach((block, i) => {
      if (blocks.length > 1) {
        console.log(`\n--- Diagram ${i + 1} ---\n`);
      }
      console.log(renderBlock(block));
    });
  } else {
    // Treat entire input as mermaid code
    console.log(renderBlock(input.trim()));
  }
}

main().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
