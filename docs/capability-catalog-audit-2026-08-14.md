# Life-science capability catalog audit — 2026-08-14

Source: Feishu document `K45edIKv5oyIlgxm2GQcNJJTntc`, revision 717, heading `生命科学能力包（222 项）`.

## Verified facts

- The life-science table contains exactly 222 rows.
- Type/source/status distribution from the document body:
  - 21 internal MCP/SCP rows: platform-provided, but endpoint connectivity/authentication/permission still require verification.
  - 15 Claude Science skills: conditionally connectable; implementation, dependencies and external-service terms require verification.
  - 55 Claude Science MCP/SCP rows: conditionally connectable; authorization, interface, authentication and service terms require verification.
  - 131 internal skills: internally provided, but authentication, dependencies and integration still require verification.
- Therefore “present in the 222 catalog” and “available in the target client for this run” are separate gates.
- The document defines these entries as candidate capabilities, not as 222 guaranteed working packages.

## Repository discrepancy

`docs/capability-whitelist-v1.tsv` contains 22 experimental rows, not the full 222-row catalog. It must not be described as the catalog authority or used to exclude other catalog-listed entries in T1/T2. It may only serve as a previously smoke-tested subset after each exact package is confirmed in the target client.

## Catalog data-quality findings

- The source table contains duplicate display names, including `Epigenetics & Drug Response`, `Multi-Species Gene Analysis`, and `Protein Similarity Search`. Display name alone is therefore not a unique installation key; the client package/version identifier must be captured in the run trace.
- At least one source display name is visibly malformed/truncated (`earch biomedical literature...`), and one long `Given a gene symbol...` row is not safe to parse as a stable package key from Markdown alone.
- The embedded capability Base view (`tblLc90nbxF8J6Lr` / `vewThfnob4`) returned Feishu error 131006 to both current user and bot identities. The document body was readable, but the Base cannot currently be used to resolve canonical package IDs.

## Formal T1/T2 gate

Before the first with-capabilities run, export from the actual Duanyan client:

1. all discoverable life-science packages with canonical package ID, display name, type and version;
2. catalog-match result against Feishu revision 717;
3. installation/enable and invocation event schema;
4. uninstall/disable and normalized post-reset inventory.

If the client exposes only display names, duplicated or malformed rows require an evaluator-owned disambiguation table before formal scoring. A capability that is catalog-listed but fails discovery, installation, authentication or invocation is recorded as an availability/reliability observation; it is not silently replaced by an out-of-catalog tool.
