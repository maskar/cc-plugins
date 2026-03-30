# Node/TypeScript Project Layout

## Standard Layout

```text
project-name/
├── .claude/
│   └── CLAUDE.md
├── src/
│   ├── index.ts
│   ├── config.ts
│   └── modules/
│       └── feature/
│           ├── feature.ts
│           └── feature.test.ts
├── dist/                   # build output, gitignored
├── docs/
├── scripts/
├── tmp/                    # gitignored
├── .gitignore
├── justfile
├── package.json
├── tsconfig.json
└── README.md
```

## Package Management

Use `npm` or `pnpm`:

```bash
npm init                   # Initialize
npm install <package>      # Add dependency
npm install -D <package>   # Add dev dependency
npm run <script>           # Run script
```

## package.json

```json
{
  "name": "project-name",
  "version": "0.1.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts",
    "test": "vitest",
    "lint": "eslint src/"
  }
}
```

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "tmp"]
}
```

## ESM Conventions

- Always use `"type": "module"` in package.json
- Use `.js` extensions in import paths (even for TypeScript)
- Prefer named exports over default exports
- Use `tsx` for development, `tsc` for production builds

## Testing

Use `vitest` for unit tests:

```typescript
import { describe, it, expect } from 'vitest';
import { myFunction } from './module.js';

describe('myFunction', () => {
  it('should return expected result', () => {
    expect(myFunction('input')).toBe('output');
  });
});
```

## Conventions

- ESM (not CommonJS)
- TypeScript by default
- Use `vitest` for testing
- Use `eslint` for linting
- Use `prettier` for formatting
- Colocate tests with source (`feature.test.ts` next to `feature.ts`)
