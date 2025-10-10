# Automatic Repository Management

## Auto-Update Policy

**MANDATORY**: After ANY changes to the repository content, Gemini MUST automatically:

1. **Stage all changes**: `git add .`
2. **Commit with descriptive message**: Following the established pattern
3. **Push to main branch**: `git push origin main`

## Commit Message Format

```
<Action>: <Brief description>

- <Detailed change 1>
- <Detailed change 2>
- <Additional context if needed>

[AI] Generated with [Gemini](https://gemini.google.com/)

Co-Authored-By: Gemini <noreply@google.com>
```

## Repository Address Verification

Before any git operations, verify the remote repository:
```bash
git remote -v
# Expected output:
# origin	https://github.com/theSadeQ/dip-smc-pso.git (fetch)
# origin	https://github.com/theSadeQ/dip-smc-pso.git (push)
```

If the remote is incorrect, update it:
```bash
git remote set-url origin https://github.com/theSadeQ/dip-smc-pso.git
```

## Trigger Conditions

Gemini MUST automatically update the repository when:
- Any source code files are modified
- Configuration files are changed
- Documentation is updated
- New files are added
- Test files are modified
- Any project structure changes occur

## Update Sequence

```bash
# 1. Verify repository state
git status
git remote -v

# 2. Stage all changes
git add .

# 3. Commit with descriptive message
git commit -m "$(cat <<'EOF'
<Descriptive title>

- <Change 1>
- <Change 2>
- <Additional context>

[AI] Generated with [Gemini](https://gemini.google.com/)

Co-Authored-By: Gemini <noreply@google.com>
EOF
)"

# 4. Push to main branch
git push origin main
```

## Error Handling

If git operations fail:
1. Report the error to the user
2. Provide suggested resolution steps
3. Do not proceed with further operations until resolved
