
# Windows Filesystem Security Design

## Status

Proposed design — not yet implemented or security-validated.

## Objective

Allow AgentLock to read and write files inside a designated workspace while preventing access outside that workspace through unsafe filesystem paths.

## Security requirements

1. The workspace must be opened and validated before file operations begin.
2. Paths must be traversed one component at a time relative to validated directory handles.
3. Reparse points must be rejected at every relevant path component.
4. File operations must use the validated file handle rather than reopening a path.
5. Directory and file handles must remain valid for the duration of the operation.
6. All handles must be closed reliably, including when errors occur.
7. Operations must fail closed when a security guarantee cannot be established.

## Proposed architecture

1. Open the designated workspace directory.
2. Retain its directory handle.
3. Traverse requested child directories relative to their parent handles.
4. Inspect each opened component for reparse-point attributes.
5. Reject components that violate workspace restrictions.
6. Open the requested file relative to the validated parent directory.
7. Perform the read or write through the resulting file handle.
8. Release all handles safely.

## Threats to investigate

- Symbolic links and junctions.
- Other Windows reparse-point types.
- Path traversal using `..`.
- Directory renames and path substitution.
- Time-of-check-to-time-of-use (TOCTOU) races.
- Hard links.
- Concurrent modification by another process.
- Unexpected filesystem errors and permission failures.

## Implementation constraints

- Do not rely on Path.resolve() as the security boundary.
- Do not validate a path and then reopen it using Path.read_text() or Path.write_text().
- Do not assume FILE_FLAG_OPEN_REPARSE_POINT protects every intermediate path component.
- Do not claim complete sandbox isolation based only on filesystem checks.
- Prefer supported Windows APIs where they can provide the required guarantees.
- Document any limitations of native APIs and filesystem behavior.

## Validation requirements

- Test normal file and directory operations.
- Test attempts to escape the workspace.
- Test junctions and symbolic links where supported.
- Test reparse-point handling.
- Test concurrent path changes.
- Test cleanup after failed operations.
- Verify that rejected operations do not modify files outside the workspace.

## Outstanding questions

- Can NtCreateFile with RootDirectory provide the required component-by-component traversal?
- What sharing modes and access flags are necessary?
- How should NTSTATUS errors be translated?
- How will handle identity and concurrent renames be handled?
- What guarantees can be made across supported Windows filesystems?

## Completion criteria

The implementation must satisfy the security requirements, pass automated tests, and undergo security review before being described as a hardened filesystem boundary.
