const CLAUSE_KEYWORDS = [
  "WITH",
  "SELECT",
  "FROM",
  "INNER JOIN",
  "LEFT JOIN",
  "RIGHT JOIN",
  "FULL JOIN",
  "CROSS JOIN",
  "WHERE",
  "GROUP BY",
  "HAVING",
  "ORDER BY",
  "LIMIT",
];

export function formatSqlForDisplay(query = "") {
  if (!query) {
    return "";
  }

  let formatted = query.trim().replace(/\s+/g, " ");

  CLAUSE_KEYWORDS.forEach((keyword) => {
    const pattern = new RegExp(`\\s+${keyword.replace(" ", "\\s+")}\\b`, "gi");
    formatted = formatted.replace(pattern, `\n${keyword}`);
  });

  formatted = formatted
    .replace(/\s+CASE\b/gi, "\nCASE")
    .replace(/\s+WHEN\b/gi, "\n  WHEN")
    .replace(/\s+ELSE\b/gi, "\n  ELSE")
    .replace(/\s+END\b/gi, "\nEND")
    .replace(/,\s*/g, ",\n  ")
    .replace(/\(\s*SELECT\b/gi, "(\nSELECT")
    .replace(/\)\s*,\s*/g, "\n),\n")
    .replace(/;\s*$/, ";");

  return formatted
    .split("\n")
    .map((line) => line.trimEnd())
    .join("\n")
    .trim();
}
