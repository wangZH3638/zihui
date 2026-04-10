# exec-structured Skill

Wrap exec tool results with structured error information to help the model distinguish success from failure.

## When to Use

When the user asks to run a command, use `exec` as normal but format the result description to include:
- Whether the command succeeded or failed
- The return/exit code
- Any error indicators

## How It Works

This is a documentation skill - the actual exec tool already returns structured data including `code`, `signal`, `killed`, `termination`. The issue is that when results are rendered for the model, they often become plain text.

**Current exec result structure (from `runCommandWithTimeout`):**
```javascript
{
  pid,        // process ID
  stdout,     // standard output
  stderr,     // standard error  
  code,       // exit code (0 = success, non-zero = error)
  signal,     // signal that terminated process (if any)
  killed,     // boolean - was process killed
  termination,// "exit" | "timeout" | "signal" | "no-output-timeout"
  noOutputTimedOut
}
```

## Best Practice for Model Interpretation

When you receive an exec result, check:
1. **`code !== 0`** → Command failed, include `stderr` in response
2. **`killed === true`** → Command was terminated (timeout or signal)
3. **`termination === "timeout"`** → Command exceeded time limit
4. **`stderr && stderr.length > 0`** → There were error messages (even if exit code is 0)

## Structured Result Format for User

When reporting exec results to user, use this format:

```
✅ Command succeeded (exit code: 0)
[Output]
---
❌ Command failed (exit code: N)
[Error output]
---
⚠️ Command terminated (killed, timeout after Xs)
```

## Relationship to Claw Code

Claw Code's exec tool returns `is_error` as an explicit boolean. OpenClaw's exec doesn't have this field explicitly, but `code !== 0` serves the same purpose.

The exec tool in OpenClaw is already well-structured - this skill documents how to best interpret and communicate its results.
