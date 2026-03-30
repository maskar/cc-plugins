# Go Project Layout

## Standard Layout

```text
project-name/
├── .claude/
│   └── CLAUDE.md
├── cmd/
│   └── project-name/
│       └── main.go
├── internal/
│   ├── config/
│   │   └── config.go
│   └── feature/
│       ├── feature.go
│       └── feature_test.go
├── pkg/                    # only if exporting libraries
│   └── shared/
│       └── shared.go
├── docs/
├── scripts/
├── tmp/                    # gitignored
├── .gitignore
├── go.mod
├── go.sum
├── justfile
└── README.md
```

## Module Initialization

```bash
go mod init github.com/org/project-name
```

## Key Directories

| Directory    | Purpose                                     | Importable?          |
|-------------|---------------------------------------------|----------------------|
| `cmd/`      | Entry points (one per binary)               | No                   |
| `internal/` | Private application code                    | No (enforced by Go)  |
| `pkg/`      | Public library code (use sparingly)         | Yes                  |

## Conventions

- `internal/` for all application logic (Go enforces import restriction)
- `cmd/<name>/main.go` for each binary
- `pkg/` only when building a library others will import
- Tests colocated: `feature.go` + `feature_test.go` in same directory
- Use `go test ./...` to run all tests
- No `src/` directory — Go convention uses `cmd/` + `internal/`

## justfile

```just
# Build
build:
    go build -o bin/project-name ./cmd/project-name

# Run
run *ARGS:
    go run ./cmd/project-name {{ARGS}}

# Test
test:
    go test ./...

# Lint
lint:
    golangci-lint run
```

## Testing

```go
package feature_test

import (
    "testing"
    "github.com/org/project-name/internal/feature"
)

func TestFeature(t *testing.T) {
    result := feature.Process("input")
    if result != "expected" {
        t.Errorf("got %s, want expected", result)
    }
}
```
