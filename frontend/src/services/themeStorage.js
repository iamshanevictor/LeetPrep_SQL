const THEME_KEY = "leetprep-sql-theme";
const DARK_QUERY = "(prefers-color-scheme: dark)";

export function getStoredTheme() {
  if (!canUseStorage()) {
    return getSystemTheme();
  }

  const storedTheme = window.localStorage.getItem(THEME_KEY);
  return storedTheme === "dark" || storedTheme === "light"
    ? storedTheme
    : getSystemTheme();
}

export function applyTheme(theme) {
  if (typeof document === "undefined") {
    return;
  }

  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
}

export function saveTheme(theme) {
  if (canUseStorage()) {
    window.localStorage.setItem(THEME_KEY, theme);
  }

  applyTheme(theme);
}

export function getSystemTheme() {
  if (typeof window === "undefined") {
    return "light";
  }

  return window.matchMedia(DARK_QUERY).matches ? "dark" : "light";
}

function canUseStorage() {
  try {
    return typeof window !== "undefined" && Boolean(window.localStorage);
  } catch {
    return false;
  }
}
